import random

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/ahmedetefy/TDDGoat.git'


# Run from local machine with the following command:
# fab provision -i '/home/etefy/Downloads/tutorial.pem'\
# -H ubuntu@book-example.staging.taibahegypt.com
# Running it again will abort so its fine
def provision():
    site_folder = "/home/" + env.user + "/sites/" + env.host
    with cd(site_folder):
        _nginx_config()
        _gunicorn_config()
        _start_gunicorn_and_nginx()


def _nginx_config():
    run('cat ./deploy_tools/nginx.template.conf ' +
        '| sed "s/DOMAIN/' + env.host + '/g" ' +
        '| sudo tee /etc/nginx/sites-available/' + env.host)
    run('sudo ln -s /etc/nginx/sites-available/' + env.host +
        ' /etc/nginx/sites-enabled/' + env.host)


def _gunicorn_config():
    run('cat ./deploy_tools/gunicorn-systemd.template.service ' +
        '| sed "s/DOMAIN/' + env.host + '/g" ' +
        '| sudo tee /etc/systemd/system/gunicorn-' + env.host + '.service')


def _start_gunicorn_and_nginx():
    run('sudo systemctl daemon-reload')
    run('sudo systemctl reload nginx')
    run('sudo systemctl enable gunicorn-' + env.host)
    run('sudo systemctl start gunicorn-' + env.host)


# Run from local machine with the following command:
# fab deploy -i '/home/etefy/Downloads/tutorial.pem'\
# -H ubuntu@book-example.staging.taibahegypt.com
# ** Should be called before provision() **
def deploy():
    site_folder = "/home/" + env.user + "/sites/" + env.host
    # -p tag serves two functions. First it ensures that even
    # if the parent dir is not there, it is created. Second,
    # if requested dir already exists, it just ignores it
    run("mkdir -p " + site_folder)
    # cd command means that all commands in subsequent function
    # calls will be executed in site_folder dir
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run("git fetch")
    else:
        run('git clone ' + REPO_URL + ' .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('git reset --hard ' + current_commit)


def _update_virtualenv():
    if not exists('env/bin/pip'):
        run('python3.6 -m venv env')
    run('./env/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    # Adds a line if that line is not already there
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', 'SITENAME=' + env.host)
    current_contents = run('cat .env')
    # We cannot rely on the append's conditional logic here
    # because our new key and any potential existing one won't be same
    if 'SECRET_KEY' not in current_contents:
        # new_secret = (
        #     ''.join(
        #         random.SystemRandom(
        #         ).choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)))
        # append('.env', 'SECRET_KEY=' + new_secret)
        run('echo SECRET_KEY=$(python3.6 -c"import random; print(\'\'.join(' +
            'random.SystemRandom().choices(\'abcdefghijklmnopqrstuvwxyz' +
            '0123456789\', k=50)))") >> .env')


def _update_static_files():
    run('./env/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./env/bin/python manage.py migrate --noinput')
