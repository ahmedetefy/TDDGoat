import random

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/ahmedetefy/TDDGoat.git'


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    # -p tag serves two functions. First it ensures that even
    # if the parent dir is not there, it is created. Second,
    # if requested dir already exists, it just ignores it
    run(f"mkdir -p {site_folder}")
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
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('env/bin/pip'):
        run(f'python3.6 -m venv env')
    run('./env/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    # Adds a line if that line is not already there
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    # We cannot rely on the append's conditional logic here
    # because our new key and any potential existing one won't be same
    if 'SECRET_KEY' not in current_contents:
        new_secret = ''.join(
            random.SystemRandom().choices(
                3
                'abcdefghijklmnopqrstuvwxyz0123456789',
                k=50
            ))
        append('.env', f'SECRET_KEY={new_secret}')


def _update_static_files():
    run('./env/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./env/bin/python manage.py migrate --noinput')


