import os
import base64
import uuid

from datetime import datetime

from django.template.defaultfilters import slugify as _slugify

from fabric.api import local, sudo, run, env, cd, get
from fabric.operations import prompt
from fabric.colors import red
from fabric.contrib.console import confirm


def _get_branch_name(on_local=True):
    cmd = "git branch --no-color 2> /dev/null | sed -e '/^[^*]/d'"
    if on_local:
        name = local(cmd, capture=True).replace("* ", "")
    else:
        name = run(cmd)
    return name.replace("* ", "").strip()


def switch(stage):
    """
        Switch to given stage (dev/qa/production) + pull
    """
    stage = stage.lower()
    local("git pull")
    if stage in ['dev', 'devel', 'develop']:
        branch_name = 'develop'
    elif stage in ['qa', 'release']:
        branches = local('git branch -r', capture=True)
        possible_branches = []
        for b in branches.split("\n"):
            b_parts = b.split('/')
            if b_parts[1] == 'release':
                possible_branches.append(b_parts[2])
        if len(possible_branches) == 0:
            raise Exception('No release branches found. Please create a new release first.')
        possible_branches = sorted(possible_branches, reverse=True)
        branch_name = 'release/%s' % possible_branches[0]
    elif stage in ['production', 'master']:
        branch_name = 'master'
    else:
        raise NotImplemented
    local("git checkout %s" % branch_name)
    local("git pull")


def release_qa():
    """
        Release code to QA server
    """
    name = prompt(red('Sprint name?'), default='Sprint 1').lower().replace(' ', "_")
    release_date = prompt(red('Sprint start date (Y-m-d)?'), default='2013-01-20').replace('-', '')
    release_name = '%s_%s' % (release_date, name)
    local('git flow release start %s' % release_name)
    local('git flow release publish %s' % release_name)
    print red('PLEASE DEPLOY CODE: fab deploy:all')


def update_qa():
    """
        Merge code from develop to qa
    """
    switch('dev')
    switch('qa')
    local('git merge --no-edit develop')
    local('git push')
    print red('PLEASE DEPLOY CODE: fab deploy:all')


def _check_branch(environment, user):
    if environment == 'qa':
        local_branch = _get_branch_name()
        remote_branch = _get_branch_name(False)
        if local_branch != remote_branch:
            change = confirm(red('Branch on server is different, do you want to checkout %s ?' % local_branch),
                             default=True)
            if change:
                sudo('git checkout %s' % local_branch, user=user)


def _sql_paths(*args):
    args = [str(arg) for arg in args]
    args.append(_get_branch_name())
    return _slugify('-'.join(args)) + '.sql.gz'


def backup_db():
    """
        Backup local database
    """
    if not os.path.exists('backups'):
        os.makedirs('backups')
    local('python manage.py dump_database | gzip > backups/' + _sql_paths('local', datetime.now()))


def _get_db():
    """
        Get database from server
    """
    with cd(env.remote_path):
        file_path = '/tmp/' + _sql_paths('remote', base64.urlsafe_b64encode(uuid.uuid4().bytes).replace('=', ''))
        run(env.python + ' manage.py dump_database | gzip > ' + file_path)
    local_file_path = './backups/' + _sql_paths('remote_', datetime.now())
    get(file_path, local_file_path)
    run('rm ' + file_path)
    return local_file_path


def restore_db(path):
    """
        Restore database with given file path (support compressed and not compressed files)
        Usage:
            fab restore_db:~/dump.sql
            fab restore_db:~/dump.sql.gz
    """
    if path.endswith('.gz'):
        local('gzip -dc %s | python manage.py dbshell' % path)
    else:
        local('python manage.py dbshell < %s ' % path)


def pull_db():
    """
        Replace local database with database from server (server based on branch)
    """
    backup_db()
    local_file_path = _get_db()
    local('gzip -dc %s | python manage.py dbshell' % local_file_path)


def command(command):
    """
        Run custom Django management command
    """
    with cd(env.remote_path):
        sudo(env.python + ' manage.py %s' % command, user=env.remote_user)


def update_cron():
    """
        Update cron
    """
    sudo('crontab  %sconfig/crontab' % env.remote_path, user=env.remote_user)


def setup_server(clear_old=False):
    """
        Setup server
    """
    pwd = os.path.dirname(os.path.realpath(__file__))
    project = pwd.split('/')[-1]

    if clear_old:
        sudo('userdel -r %s' % env.remote_user)

    sudo('useradd --create-home %s' % env.remote_user, user='root')
    sudo('ssh-keygen -t rsa -P "" -f /home/%s/.ssh/id_rsa' % env.remote_user)
    sudo('cp -f /home/%s/.ssh/id_rsa.pub ~/key.tmp' % env.remote_user, user='root')
    key = sudo('cat ~/key.tmp', user='root')
    #TODO: try github API (Hint: Basic is not working because of 2FA)
    sudo('rm ~/key.tmp', user='root')
    print red('Please put following deploy key in GitHub - https://github.com/ArabellaTech/%s/settings/keys' % project)
    print key
    prompt(red('Press any key to continue'))
    sudo('export WORKON_HOME=/home/%s/Envs &&\
         source /usr/local/bin/virtualenvwrapper_lazy.sh &&\
         mkvirtualenv %s --no-site-packages' % (env.remote_user, project),
         warn_only=True)
    sudo('cd /home/%s/ && git clone git@github.com:ArabellaTech/%s.git www' % (env.remote_user, project))
    with cd(env.remote_path):
        sudo('git checkout %s' % env.branch)
        sudo('cd %s && ln -sf ../config/%s/yd_local_settings.py local_settings.py' % (project, env.environment))
        sudo(env.pip + ' install -r requirements.txt')
        sudo(env.python + ' manage.py syncdb --migrate', user=env.remote_user)
        sudo(env.python + ' manage.py collectstatic -v0 --noinput', user=env.remote_user)
        sudo(env.python + ' manage.py compress -f', user=env.remote_user)

        params = (env.remote_user, env.environment, env.remote_user)
        sudo('cd /etc/nginx/sites-enabled && ln -sf /home/%s/www/config/%s/nginx.conf %s.conf' % params, user='root')
        sudo('cd /etc/supervisor/conf.d/ && ln -sf /home/%s/www/config/%s/supervisord.conf %s.conf' % params,
             user='root')
        sudo('/etc/init.d/nginx reload', user='root')
        sudo('supervisorctl reread && supervisorctl update', user='root')

    update_cron()
