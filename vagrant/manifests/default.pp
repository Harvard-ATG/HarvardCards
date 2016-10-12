# Make sure the correct directories are in the path:
Exec {
	path => [
	'/usr/local/sbin',
	'/usr/local/bin',
	'/usr/sbin',
	'/usr/bin',
	'/sbin',
	'/bin',
	],
	logoutput => true,
}

class init {
	exec {'apt-get-update': command => 'apt-get update'}
	$packages = [
		"build-essential",
		"redis-server",
		"libxml2-dev",
		"libxslt1-dev",
		"curl",
		"git",
		
		# For Postgres Database
		"postgresql",
		"postgresql-contrib",
		"libpq-dev",

		# For Pillow library
		'libtiff4-dev',
		'libjpeg8-dev',
		'zlib1g-dev',
		'libfreetype6-dev',
		'liblcms2-dev',
		'tcl8.5-dev',
		'tk8.5-dev',

		# For Matplotlib (python 2d plotting module)
		"libpng-dev",
		"g++",

		'python-tk',
		"python", 
		"python-dev", 
		"python-setuptools"
	]
	package {
		$packages:
		ensure => installed,
		require => Exec['apt-get-update']
	}
}

class database {
	require init

	exec {'drop-project-db':
		require => Package['postgresql'],
		command => '/usr/bin/psql -d postgres -c "DROP DATABASE IF EXISTS flash"',
		user => 'postgres',
		group => 'postgres',
		logoutput => true,
	}

	exec {'drop-existing-project-user':
		require => Exec['drop-project-db'],
		command => '/usr/bin/psql -d postgres -c "DROP USER IF EXISTS flash"',
		user => 'postgres',
		group => 'postgres',
		logoutput => true,
	}

	exec {'create-project-user':
		require => Exec['drop-existing-project-user'],
		command => '/usr/bin/psql -d postgres -c "CREATE USER flash WITH PASSWORD \'flash\'"',
		user => 'postgres',
		group => 'postgres',
		logoutput => true,
	}

	exec {'create-project-db':
		require => Exec['create-project-user'],
		command => '/usr/bin/psql -d postgres -c "CREATE DATABASE flash WITH OWNER flash"',
		user => 'postgres',
		group => 'postgres',
		logoutput => true,
	}
}

class application {
	require init

	#exec {'pip-install':
	#	command => 'sudo pip install /vagrant/harvardcards/requirements/local.txt',
	#	require => [ File['/vagrant/harvardcards/requirements/local.txt'], ],
	#}

	# set the DJANGO_SETTINGS_MODULE environment variable
	#file_line {'set env DJANGO_SETTINGS_MODULE':
	#    ensure => present,
	#    line => 'export DJANGO_SETTINGS_MODULE=harvardcards.settings.local',
	#    path => '/home/vagrant/.bashrc',
	#    require => Exec['apt-get-update'],
	#}
}

class environment {
	require init

	# Ensure github.com ssh public key is in the .ssh/known_hosts file so
	# pip won't try to prompt on the terminal to accept it
	file {'/home/vagrant/.ssh':
		ensure => directory,
		mode => 0700,
	}
	exec {'known_hosts':
		provider => 'shell',
		user => 'vagrant',
		group => 'vagrant',
		command => 'ssh-keyscan github.com >> /home/vagrant/.ssh/known_hosts',
		unless => 'grep -sq github.com /home/vagrant/.ssh/known_hosts',
		require => [ File['/home/vagrant/.ssh'], ],
	}
	file {'/home/vagrant/.ssh/known_hosts':
		ensure => file,
		mode => 0744,
		require => [ Exec['known_hosts'], ],
	}
	file {'/home/vagrant/HarvardCards':
		ensure => link,
		target => '/vagrant',
	}
}

require database
require application
require environment

