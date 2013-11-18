from fabric.api import local, sudo, run
from fabric.operations import prompt
from fabric.colors import red
from fabric.contrib.console import confirm


def get_branch_name(on_local=True):
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
    date = prompt(red('Sprint start date (Y-m-d)?'), default='2013-01-20').replace('-', '')
    release_name = '%s_%s' % (date, name)
    local('git flow release start %s' % release_name)
    local('git flow release publish %s' % release_name)
    print red('PLEASE DEPLOY CODE: fab deploy:all')


def update_qa():
    """
        Merge code from develop to qa
    """
    switch('dev')
    switch('qa')
    local('git merge develop')
    local('git push')
    print red('PLEASE DEPLOY CODE: fab deploy:all')


def check_branch(environment, user):
    if environment == 'qa':
        local_branch = get_branch_name()
        remote_branch = get_branch_name(False)
        if local_branch != remote_branch:
            change = confirm(red('Branch on server is different, do you want to change to your?'), default=True)
            if change:
                sudo('git checkout %s' % local_branch, user=user)
