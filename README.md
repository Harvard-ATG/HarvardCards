[![Build Status](https://travis-ci.org/Harvard-ATG/HarvardCards.png?branch=dev)](https://travis-ci.org/Harvard-ATG/HarvardCards)

# Overview

HarvardCards is a web-based flashcard application for students who want to memorize words, media, or concepts and instructors who want to assess student progress. It is open source and released under the [BSD License](https://github.com/Harvard-ATG/HarvardCards/blob/master/LICENSE).

# Quickstart

To  install the application locally you can:
- Manually install the application and and run the django server.
- Use our [Vagrant](http://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) configuration to setup a VM that will host and run the application, so you don't have to worry about installing dependencies.

### Manual Quickstart

Requires [python 2.7.x](http://python.org/download/releases/) and [pip](http://www.pip-installer.org/) to install.

```sh
$ git clone git@github.com:Harvard-ATG/HarvardCards.git harvardcards
$ cd harvardcards
$ pip install -r harvardcards/requirements/local.txt
$ ./manage.py syncdb
$ ./manage.py migrate
$ ./manage.py runserver
```

You should now be able to access the application at: ```http://localhost:8000```

Tip: If you're familiar with python's [virtualenv](https://pypi.python.org/pypi/virtualenv), it's recommended to setup a virtualenv for the application first. See the [documentation](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation) for how to install and activate it.

Notes:

* Requires postgres to be installed on your system. See ```harvardcards/settings/local.py``` for the configuration settings.
* Requires external image manipulation libraries to be installed on your system. See [Pillow](https://pypi.python.org/pypi/Pillow/) documentation.

### Vagrant Quickstart

Make sure you have [Vagrant](http://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) installed on your computer. Note that this has only been tested on unix-based machines.

```sh
$ git clone git@github.com:Harvard-ATG/HarvardCards.git && cd HarvardCards
$ vagrant box add precise32 http://files.vagrantup.com/precise32.box
$ vagrant up
```

You should now be able to access the application at: ```http://localhost:8080```

You should be able to login as "admin" (which is also the password) at: ```http://localhost:8080/admin```
