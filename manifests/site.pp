Exec {
	path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

include init

class init {
	group { "puppet":
		ensure => "present",
	}
	
	exec { "update-apt":
		command => "sudo apt-get update",
	}
	
	package { 'git':
		ensure => latest,
		require => Exec['update-apt'],
	}

	# install some system dependencies
	package {
		["python", "python-dev", "python-pip", "python-setuptools", "python-mysqldb", "mysql-server", "mysql-client"]:
		ensure => installed,
		require => Exec['update-apt']
	}
}

class djangoapp {
	$PROJ_DIR = "/vagrant"
	$DB_NAME = "flashdb"
	$DB_USER = "flashuser"
	$DB_HOST = "localhost"
	$DB_PASS = "flashpass"

	# install dependencies needed for Pillow (python imaging module)
	# https://pypi.python.org/pypi/Pillow/
	# http://pillow.readthedocs.org/
	package { 
		['libtiff4-dev', 'libjpeg8-dev', 'zlib1g-dev',  'libfreetype6-dev', 'liblcms2-dev', 'tcl8.5-dev', 'tk8.5-dev', 'python-tk']:
		ensure => installed,
		require => Exec['update-apt']
	}

	# install project dependencies
	exec { "pip-install-requirements":
		command => "sudo /usr/bin/pip install -r $PROJ_DIR/requirements.txt",
		tries => 2,
		timeout => 600,
		require => Package['python-pip', 'python-dev'],
		logoutput => true,
	}

	# setup mysql database
	exec { "mysql-setup-db":
		command => "mysql -u root -e \"CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8 COLLATE utf8_general_ci; GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS'; FLUSH PRIVILEGES;\"",
		cwd => "$PROJ_DIR",
		logoutput => true,
	}

	# django sync database
	exec { "django-syncdb":
		environment => ["DJANGO_SETTINGS_MODULE=harvardcards.settings.dev-mysql"],
		command => "python manage.py syncdb --noinput",
		cwd => "$PROJ_DIR",
		require => [Exec['mysql-setup-db'],Exec['pip-install-requirements']],
		logoutput => true,
	}

	# setup super user
	exec { "django-setup-superuser":
		environment => ["DJANGO_SETTINGS_MODULE=harvardcards.settings.dev-mysql"],
		command => 'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin\')" | ./manage.py shell',
		cwd => "$PROJ_DIR",
		require => Exec['django-syncdb']
	}

	# start server?
	exec { "django-runserver":
		environment => ["DJANGO_SETTINGS_MODULE=harvardcards.settings.dev-mysql"],
		command => "python manage.py runserver 0.0.0.0:8000 >django-server.log 2>&1 &",
		cwd => "$PROJ_DIR",
		require => Exec['django-syncdb'],
		logoutput => true,	
	}
}

include djangoapp
