Provisioning a new site
=======================

## Required Packages

* ngnix
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu 16.04:

	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install nginx git python36 python3.6-venv

## Nginx Virtual Host Config

* cd /etc/nginx/sites-available/
* sudo vim <DOMAIN>
* Add nginx.template.conf and rename file to <DOMAIN>
* export SITENAME=<DOMAIN>
* cd /etc/nginx/sites-enabled
* sudo ln -s /etc/nginx/sites-available/$SITENAME $SITENAME
* sudo rm /etc/nginx/sites-enabled/default
* sudo systemctl reload nginx

## Create Environment Variables 

* In root directory of project, create .env file
* Insert all environment variables
* Make sure this file is in .gitignore

## Create a Systemd Service

* cd /etc/systemd/system/
* sudo vim _<DOMAIN>.service
* Check gunicorn-systemd.template.service
* sudo systemctl daemon-reload
* sudo systemctl enable <DOMAIN>
* sudo systemctl start <DOMAIN>

## Folder Structure

Assume we have a user account at /home/username

/home/username
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
