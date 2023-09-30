#!/usr/bin/python3
"""Deploy API to remote server"""
from fabric.api import local, run, sudo, env, put, cd
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()
PSN = getenv('PROJECT_SHORT_NAME', 'python') + '_api'  # from environment
ARCHIVE_DIR = 'versions/'
FILES = [
    'api', 'models', '.env',
    'requirements.txt', 'setup_db.sql',
    'flush_db'
]  # update this list according to your purposes


def create_archive():
    """Archive the entire project"""
    current_time = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    local("mkdir -p {}".format(ARCHIVE_DIR))
    archive_path = '{}/{}_{}.tar.gz'.format(ARCHIVE_DIR, PSN, current_time)
    local("tar -czvf {} {}".format(archive_path, ' '.join(FILES)))
    return archive_path


def copy_and_unpack_archive(archive_path):
    """Move arcive to remote"""
    archive_name = archive_path.split('/')[-1]
    run("mkdir -p {}".format(PSN))
    put(archive_path, PSN)
    run("tar -xzvf {}/{} -C {}".format(PSN, archive_name, PSN))
    run("rm {}/{}".format(PSN, archive_name))


def install_dependencies():
    """Install remote dependencies"""
    put('requirements.txt', '{}'.format(PSN))
    run('pip install -r {}/requirements.txt'.format(PSN))
    sudo('pip install gunicorn')


def start_api_service():
    """Starts remote API service"""
    sudo('systemctl start {}.service'.format(PSN))


def stop_api_service():
    """Stops remote API service"""
    sudo('systemctl stop {}.service'.format(PSN))


def remove_existing():
    """Removes all existing project files in remote server"""
    sudo('rm -rf {}'.format(PSN))


def flush_db():
    """Setup remote database"""
    stop_api_service()
    sudo('mysql < {}'.format(PSN + '/setup_db.sql'))
    start_api_service()


def upload_service_script():
    """Uploads, Enables and Start service script"""
    put(
        '{}.service'.format(PSN),
        '/etc/systemd/system/{}.service'.format(PSN),
        use_sudo=True
    )
    sudo('systemctl enable {}.service'.format(PSN))
    start_api_service()


def restart_api_service():
    """Restarts remote API service"""
    sudo('systemctl restart {}.service'.format(PSN))


def deploy():
    """Deploys API to remote"""
    archive_path = create_archive()
    remove_existing()
    copy_and_unpack_archive(archive_path=archive_path)
    install_dependencies()


def update():
    """Updates remote API"""
    deploy()
    restart_api_service()

# TODO
# write a funxtion to install the following list of apt packages
# pkg-config libmysqlclient-dev
