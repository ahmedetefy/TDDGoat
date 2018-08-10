# TDDGoat

Following Example Project in Obeying the Testing Goat Book

## Staging Site

book-example.staging.taibahegypt.com

Provisioning a new site
=======================

## Required Packages

* ngnix
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu 16.04:

```sh
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt install nginx git python36 python3.6-venv
```

## Nginx Virtual Host Config

```sh
$ cd /etc/nginx/sites-available/
$ sudo vim DOMAIN
```
Then you should add nginx.template.conf, proceeding that follow the following steps.
```sh
$ export SITENAME=DOMAIN
$ cd /etc/nginx/sites-enabled
$ sudo ln -s /etc/nginx/sites-available/$SITENAME $SITENAME
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo systemctl reload nginx
```

## Create Environment Variables 

* In root directory of project, create .env file
* Insert all environment variables
* Make sure this file is in .gitignore

## Create a Systemd Service

```sh
$ cd /etc/systemd/system/
$ sudo vim DOMAIN.service
```
* Then you should add gunicorn-systemd.template.service, proceeding that follow the following steps.
```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable DOMAIN
$ sudo systemctl start DOMAIN
```

## Folder Structure

Assume we have a user account at /home/username

/home/username  
```
└── sites        
    ├── DOMAIN1    
    │    ├── .env  
    │    ├── db.sqlite3  
    │    ├── manage.py etc  
    │    ├── static  
    │    └── virtualenv  
    └── DOMAIN2    
         ├── .env  
         ├── db.sqlite3  
         ├── etc  
```

