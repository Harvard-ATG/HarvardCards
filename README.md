[![Build Status](https://travis-ci.org/Harvard-ATG/HarvardCards.png?branch=dev)](https://travis-ci.org/Harvard-ATG/HarvardCards)

# Overview

HarvardCards is a web-based flashcard application for students who want to memorize words, media, or concepts and instructors who want to assess student progress. It is open source and released under the [BSD License](https://github.com/Harvard-ATG/HarvardCards/blob/master/LICENSE).

# Quickstart

- Requires [Python 2.7.x](http://python.org/download/releases/) and [Pip](http://www.pip-installer.org/) to install. 
- To install Pip, see [their instructions](http://www.pip-installer.org/en/latest/installing.html).

```sh
pip install -r requirements.txt
```

```sh
$ git clone git@github.com:Harvard-ATG/HarvardCards.git HarvardCards
$ cd HarvardCards
$ ./manage.py syncdb
$ ./manage.py runserver
```
You should now be able to run the application on your localhost at ```http://127.0.0.1:8000```. 
