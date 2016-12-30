from __future__ import print_function

import base64
import django
import os
import uuid

from datetime import datetime

from django.template.defaultfilters import slugify as _slugify

from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import sudo
from fabric.colors import red
from fabric.contrib.console import confirm
from fabric.operations import prompt


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


def release_qa(quietly=False):
    """
        Release code to QA server
    """
    name = prompt(red('Sprint name?'), default='Sprint 1').lower().replace(' ', "_")
    release_date = prompt(red('Sprint start date (Y-m-d)?'), default='2013-01-20').replace('-', '')
    release_name = '%s_%s' % (release_date, name)
    local('git flow release start %s' % release_name)
    local('git flow release publish %s' % release_name)
    if not quietly:
        print(red('PLEASE DEPLOY CODE: fab deploy:all'))


def update_qa(quietly=False):
    """
        Merge code from develop to qa
    """
    switch('dev')
    switch('qa')
    local('git merge --no-edit develop')
    local('git push')
    if not quietly:
        print(red('PLEASE DEPLOY CODE: fab deploy:all'))


def _check_branch(environment, user, change=False):
    if environment == 'qa':
        local_branch = _get_branch_name()
        remote_branch = _get_branch_name(False)
        if local_branch != remote_branch:
            if not change:
                change = confirm(red('Branch on server is different, do you want to checkout %s ?' % local_branch),
                                 default=True)
            if change:
                sudo('git checkout %s' % local_branch, user=user)


def _check_feature_branch(full, environment, user):
    local_branch = _get_branch_name()
    remote_branch = _get_branch_name(False)
    if local_branch != remote_branch:
        if full:
            red('Current branch is %s. Your branch is %s. Switching.'
                % (remote_branch, local_branch))
            change = True
        else:
            change = confirm(red('Current branch is %s. Your branch is %s, do you want to change?'
                                 % (remote_branch, local_branch)),
                             default=True)
        if change:
            sudo('git checkout %s' % local_branch, user=user)
            sudo('git pull', user=env.remote_user)


def _sql_paths(*args):
    args = [str(arg) for arg in args]
    args.append(_slugify(_get_branch_name(False)))
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
        local_file_path = './backups/' + _sql_paths('remote', datetime.now())
    get(file_path, local_file_path)
    run('rm ' + file_path)
    return local_file_path


def clear_db():
    local('python manage.py clear_database')


def restore_db(path):
    """
        Restore database with given file path (support compressed and not compressed files)
        Usage:
            fab restore_db:~/dump.sql
            fab restore_db:~/dump.sql.gz
    """
    clear_db()
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
    clear_db()
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


def setup_server(clear_old=False, repo="github"):
    """
        Setup server
    """

    if repo == 'github':
        url_keys = 'https://github.com/ArabellaTech/%s/settings/keys' % env.repo_name
        url_clone = 'git@github.com:ArabellaTech/%s.git' % env.repo_name
    elif repo == 'bitbucket':
        url_keys = 'https://bitbucket.org/arabellatech/%s/admin/deploy-keys/' % env.repo_name
        url_clone = 'git@bitbucket.org:arabellatech/%s.git' % env.repo_name
    else:
        raise NotImplementedError('Unknown repo type')

    if clear_old:
        sudo('userdel -r %s' % env.remote_user)

    sudo('useradd --shell /bin/bash --create-home %s' % env.remote_user, user='root')
    sudo('ssh-keygen -t rsa -P "" -f /home/%s/.ssh/id_rsa' % env.remote_user, user=env.remote_user)
    sudo('cp -f /home/%s/.ssh/id_rsa.pub ~/key.tmp' % env.remote_user, user='root')
    key = sudo('cat ~/key.tmp', user='root')
    sudo('rm ~/key.tmp', user='root')
    print(red('Please put following deploy key in %s' % url_keys))
    print (key)
    prompt(red('Press any key to continue'))
    sudo('export WORKON_HOME=/home/%s/Envs &&\
         source /usr/local/bin/virtualenvwrapper_lazy.sh &&\
         mkvirtualenv %s --no-site-packages' % (env.remote_user, env.app_dir),
         warn_only=True, user=env.remote_user)
    sudo('cd /home/%s/ && git clone %s www' % (env.remote_user, url_clone), user=env.remote_user)
    with cd(env.remote_path):
        sudo('git checkout %s' % env.branch, user=env.remote_user)
        sudo('git pull', user=env.remote_user)
        sudo('cd %s && ln -sf ../config/%s/yd_local_settings.py local_settings.py' % (env.app_dir, env.environment),
             user=env.remote_user)
        sudo(env.pip + ' install -r requirements.txt --no-cache-dir', user=env.remote_user)
        if django.VERSION >= (1, 8):
            sudo(env.python + ' manage.py migrate', user=env.remote_user)
        else:
            sudo(env.python + ' manage.py syncdb --migrate', user=env.remote_user)

        sudo('cd config && ln -sf %s/logrotate.conf logrotate.conf' % (env.environment))

        # try installing npm
        # install npm modules
        # sudo('/bin/bash ./scripts/fab_build_bower_npm.sh ' + env.remote_user, user=env.remote_user, warn_only=True)
        # fix angular for webkit

        # sudo('/home/' + env.remote_user + '/www/node_modules/.bin/webkit-assign /home/' + env.remote_user +
        #      '/www/nutrimom/static/libs/bower_components/angular/angular.js', user=env.remote_user, warn_only=True)

        # build js
        # sudo('grunt build-js', warn_only=True)

        sudo(env.python + ' manage.py collectstatic -v0 --noinput', user=env.remote_user)
        sudo(env.python + ' manage.py compress -f', user=env.remote_user)

        params = (env.remote_user, env.environment, env.remote_user)
        sudo('cd /etc/nginx/sites-enabled && ln -sf /home/%s/www/config/%s/nginx.conf %s.conf' % params, user='root')
        sudo('cd /etc/supervisor/conf.d/ && ln -sf /home/%s/www/config/%s/supervisord.conf %s.conf' % params,
             user='root')
        sudo('/etc/init.d/nginx reload', user='root')
        sudo('supervisorctl reread && supervisorctl update', user='root')

    update_cron()


def copy_db(source_env, destination_env):
    """
        Copies Db betweem servers, ie develop to qa.
        Should be called by function from function defined in project fabfile.
        Example usage:

        def copy_db_between_servers(source_server, destination_server):

            source_env = {}
            destination_env = {}

            def populate_env_dict(server, local_env):
                app_dir = 'nutrimom'
                if server == 'nm-dev':
                    user = 'nutrimom-dev'
                    prefix = "dev"
                    environment = 'devel'
                    host_string = 'dev.arabel.la'
                elif server == 'nm-qa':
                    user = 'nutrimom-qa'
                    prefix = "qa"
                    environment = 'qa'
                    host_string = 'qa.arabel.la'
                elif server.startswith('nm-f'):
                    if server in ['nm-f1', 'nm-f2', 'nm-f3', 'nm-f4', 'nm-f5']:
                        user = 'nutrimom-' + server.split('-')[1]
                        prefix = user.split('-')[1]
                        environment = prefix
                        host_string = 'dev.arabel.la'
                else:
                    print ("supported params: nm-dev, nm-qa, nm-fx")
                    sys.exit()

                local_env['app_dir'] = app_dir
                local_env['remote_user'] = user
                local_env['remote_path'] = '/home/%s/www/' % (user)
                local_env['dir'] = '/home/%s/Envs/%s' % (user, app_dir)
                local_env['python'] = '/home/%s/Envs/%s/bin/python' % (user, app_dir)
                local_env['pip'] = '/home/%s/Envs/%s/bin/pip' % (user, app_dir)
                local_env['prefix'] = prefix
                local_env['environment'] = environment
                local_env['host_string'] = host_string
                local_env['is_feature'] = False
                return local_env

            source_env = populate_env_dict(source_server, source_env)
            destination_env = populate_env_dict(destination_server, destination_env)

            copy_db(source_env, destination_env)
    """
    env.update(source_env)
    local_file_path = _get_db()

    # put the file on external file system
    # clean external db
    # load database into external file system
    env.update(destination_env)

    with cd(env.remote_path):
        sudo('mkdir -p backups', user=env.remote_user)
        sudo(env.python + ' manage.py dump_database | gzip > backups/' + _sql_paths('local', datetime.now()))
        put(local_file_path, 'backups', use_sudo=True)
        sudo(env.python + ' manage.py clear_database', user=env.remote_user)
        if local_file_path.endswith('.gz'):  # the path is the same here and there
            sudo('gzip -dc %s | %s manage.py dbshell' % (local_file_path, env.python), user=env.remote_user)
        else:
            sudo('%s manage.py dbshell < %s ' % (env.python, local_file_path), user=env.remote_user)


def copy_s3_bucket(src_bucket_name, src_bucket_secret_key, src_bucket_access_key,
                   dst_bucket_name, dst_bucket_secret_key, dst_bucket_access_key):
    """ Copy S3 bucket directory with CMS data between environments. Operations are done on server. """
    with cd(env.remote_path):
        tmp_dir = "s3_tmp"
        sudo('rm -rf %s' % tmp_dir, warn_only=True, user=env.remote_user)
        sudo('mkdir %s' % tmp_dir, user=env.remote_user)
        sudo('s3cmd --recursive get s3://%s/upload/ %s --secret_key=%s --access_key=%s' % (
            src_bucket_name, tmp_dir, src_bucket_secret_key, src_bucket_access_key),
            user=env.remote_user)
        sudo('s3cmd --recursive put %s/ s3://%s/upload/ --secret_key=%s --access_key=%s' % (
            tmp_dir, dst_bucket_name, dst_bucket_secret_key, dst_bucket_access_key),
            user=env.remote_user)

        sudo('s3cmd setacl s3://%s/upload --acl-public --recursive --secret_key=%s --access_key=%s' % (
             dst_bucket_name, dst_bucket_secret_key, dst_bucket_access_key),
             user=env.remote_user)
        # cleanup
        sudo('rm -rf %s' % tmp_dir, warn_only=True, user=env.remote_user)
