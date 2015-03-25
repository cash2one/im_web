# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import time

# 部署服务器ssh地址
env.hosts = [
    'root@106.186.29.217:22',
]
env.passwords = {
    'root@106.186.29.217:22': 'we654321',
}

# 部署服务器角色定义，使用项目configs/目录中post-receive_{role}
env.roledefs = {
    'production': ['root@106.186.29.217:22'],
}

domain_configs = {
    'default': {
        'domain': 'gobelieve.io',
        'prefix': '',
        'port': 80
    },
}


def _get_domain():
    role = _get_current_role()
    if role in domain_configs.keys():
        return domain_configs[role]
    return domain_configs['default']


data_root = '/data'
git_root = '/data/gitroot'
www_root = '/data/wwwroot'
app_root = '/data/approot'

# 部署项目
projects = {
    'gobelieve.io': {
        "local_path": "/Users/lost/PycharmProjects/im-web",
        "alive": '-H "Host: {prefix}www.{domain}" {host}:{port}/login',
        'roles': ['production'],  # 部署角色
    },
}

# ============ 以下不需要修改 ====================================

pull_template = '''#!/bin/sh
app_dir={app_dir}
cd $app_dir || exit
unset GIT_DIR
git pull origin master
'''


@task
@parallel
def prepare():
    """
    开发环境准备： fab prepare:roles=development
    生成环境准备： fab prepare:roles=production
    """
    check_user()
    check_git()
    # check_docker()
    check_data_dir()
    check_app_git()
    add_local_git()
    push()
    check_app_dir()
    check_alive()


@task
def prepare_no_git():
    with settings(warn_only=True):
        # install docker
        run("whoami")
        result = run("which docker")
        if result.failed:
            print("docker not installed, try to install docker")
            install_docker()

        result = run("docker version")
        if result.failed:
            who = run("whoami")
            # add user to docker group
            print("docker get version fail, add {who} user to docker group".format(who=who))
            with settings(sudo_user="root"):
                # not permission
                sudo("gpasswd -a {who} docker".format(who=who))
                # docker daemon down
                sudo("service docker restart")

        with cd(www_root):
            for p, items in projects.iteritems():
                app_dir = get_app_dir(p, items)
                role = _get_current_role()
                if app_dir and role:
                    if run("test -f {app_dir}/configs/post-receive_{env}".format(app_dir=app_dir,
                                                                                 env=role)).succeeded:
                        post_receive = "{app_dir}/configs/post-receive_{env}".format(app_dir=app_dir,
                                                                                     env=role)
                        run("chmod +x {post_receive}".format(post_receive=post_receive))
                        run(post_receive)


@task
@parallel
def deploy(project=None, role=None, is_check_service=True):
    # test(project)
    push(project, role)
    if is_check_service:
        check_alive()


@task
@parallel
@roles('development')
def d(project=None, is_reload=False):
    deploy_and_check(project=project, role=env.effective_roles[0], is_reload=is_reload)


@task
@parallel
@roles('production')
def p(project=None, is_reload=False):
    deploy_and_check(project=project, role=env.effective_roles[0], is_reload=is_reload)


def deploy_and_check(project=None, is_reload=False, role=None):
    deploy(project=project, role=role if role else env.effective_roles[0],
           is_check_service=False if is_reload else True)
    if is_reload:
        reload_service(project)
        time.sleep(3)
        check_alive()


def install_docker():
    with settings(sudo_user="root"):
        # centos 6

        # install epel
        result = sudo('rpm -q "epel-release-6-8.noarch"')
        if result.failed:
            sudo("rpm -ivh http://mirrors.yun-idc.com/epel/6/i386/epel-release-6-8.noarch.rpm")

        # install docker
        sudo("yum update -y && yum install -y docker-io")

        # add unshare to docker, direct run in shell
        sudo(r'sed -i "s/^        \$exec -d \$other_args \$DOCKER_STORAGE_OPTIONS \&>> \$logfile \&$/'
             '        unshare -m -- \$exec -d \$other_args \$DOCKER_STORAGE_OPTIONS \&>> \$logfile \&/"'
             ' /etc/init.d/docker',
             shell=False)
        # add register
        sudo(r'''sed -i 's/^other_args=$/other_args="--insecure-registry 58.22.120.52:5000"/' /etc/sysconfig/docker''')
        # start service
        sudo("service docker start")
        sudo("chkconfig docker on")


def check_docker():
    check_user()
    # check is docker is installed
    with settings(sudo_user="git", warn_only=True):
        sudo("whoami")
        result = sudo("which docker")
        if result.failed:
            print("docker not installed, try to install docker")
            install_docker()

        result = sudo("docker version")
        if result.failed:
            who = sudo("whoami")
            # add user to docker group
            print("docker get version fail, add {who} user to docker group".format(who=who))
            with settings(sudo_user="root"):
                # not permission
                sudo("gpasswd -a {who} docker".format(who=who))
                # docker daemon down
                sudo("service docker restart")


def check_git():
    result = sudo("which git")
    if result.failed:
        print("git not installed, try to install git")
        sudo("yum update -y && yum install -y git")


def check_user():
    with settings(warn_only=True):
        # check git user is exist
        result = run("id -u git")
        if result.failed:
            # useradd git
            sudo("adduser git")
            # sudo("adduser git && gpasswd -a git docker")

        # check key is authorized
        key = local("cat ~/.ssh/id_rsa.pub", capture=True)
        if key.failed:
            local('ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ""')
            key = local("cat ~/.ssh/id_rsa.pub", capture=True)
        # print key.stdout
        res = sudo('grep "{key}" /home/git/.ssh/authorized_keys'.format(key=key))
        if res.failed:
            sudo("mkdir -p /home/git/.ssh && chmod 700 /home/git/.ssh")
            sudo("touch /home/git/.ssh/authorized_keys && chmod 600 /home/git/.ssh/authorized_keys")
            sudo('echo "{key}" >> /home/git/.ssh/authorized_keys'.format(key=key))
            sudo("chown -R git:git /home/git/.ssh")


def check_data_dir():
    with settings(warn_only=True):
        for d in [data_root, git_root, www_root]:
            if sudo("test -d {dir}".format(dir=d)).failed:
                sudo("mkdir -p {dir}".format(dir=d))
                sudo("chown -R git:git {dir}".format(dir=d))


def check_app_git():
    with settings(sudo_user="git", warn_only=True):
        for project, items in projects.iteritems():
            if _get_current_role() in items.get('roles', env.roledefs.keys()):
                app_git = project + ".git"
                app_git_dir = "{git_root}/{app_git}".format(git_root=git_root, app_git=app_git)
                if sudo("test -d {app_git_dir}".format(app_git_dir=app_git_dir)).failed:
                    with cd(git_root):
                        sudo("git init --bare {app_git}".format(app_git=app_git))


def add_local_git():
    with settings(warn_only=True):
        for project, items in projects.iteritems():
            local_path = items.get('local_path')
            if local_path:
                with lcd(local_path):
                    role = _get_current_role()
                    remote_url = get_remote_url(env.host, project)
                    if role and role in items.get('roles', env.roledefs.keys()):
                        if local('git remote -v | grep "{name}\t{remote_url}"'.format(name=role, remote_url=remote_url),
                                 capture=True).failed:
                            if local('git remote -v | grep "{name}\t"'.format(name=role), capture=True).failed:
                                local("git remote add {name} {remote_url}".format(name=role, remote_url=remote_url))
                            else:
                                local("git remote set-url --add {name} {remote_url}".format(name=role,
                                                                                            remote_url=remote_url))


def _get_current_role():
    for role in env.roledefs.keys():
        if env.host_string in env.roledefs[role]:
            return role
    return None


@task
def push(project=None, role=None):
    if not role:
        role = _get_current_role()
    with settings(warn_only=True):
        for p, items in projects.iteritems():
            if project is None or p == project:
                local_path = items.get('local_path')
                if local_path and role in items.get('roles', env.roledefs.keys()):
                    with lcd(local_path):
                        print "push {project} {name} to {host}".format(host=env.host, project=p, name=role)
                        local("git push {name} master".format(name=role))


def check_app_dir():
    with settings(sudo_user="git", warn_only=True):
        with cd(www_root):
            for project, items in projects.iteritems():
                if _get_current_role() in items.get('roles', env.roledefs.keys()):
                    app_dir = get_app_dir(project, items)
                    git_dir = '{git_root}/{project}.git'.format(git_root=git_root, project=project)
                    if app_dir and sudo("test -d %s" % app_dir).failed:
                        sudo("git clone {git_dir} {app_dir}".format(git_dir=git_dir, app_dir=app_dir))

    update_post_receive()


def get_app_dir(project, items):
    if items.get('is_app') is True:
        app_dir = '{app_root}/{project}'.format(app_root=app_root, project=project)
    elif _get_current_role() in items.get('roles', env.roledefs.keys()):
        app_dir = '{www_root}/{project}'.format(www_root=www_root, project=project)
    else:
        app_dir = ''
    return app_dir


@task
def update_post_receive(project=None):
    with settings(sudo_user="git", warn_only=True):
        with cd(www_root):
            for p, items in projects.iteritems():
                if _get_current_role() in items.get('roles', env.roledefs.keys()):
                    if project is None or project == p:
                        app_dir = get_app_dir(p, items)
                        if app_dir:
                            sudo(" cd {app_dir} && git pull origin master".format(app_dir=app_dir))
                            git_dir = '{git_root}/{project}.git'.format(git_root=git_root, project=p)

                            role = _get_current_role()
                            post_receive = "{git_dir}/hooks/post-receive".format(git_dir=git_dir)
                            if role:
                                if sudo("test -f {app_dir}/configs/post-receive_{env}".format(app_dir=app_dir,
                                                                                              env=role)).succeeded:
                                    sudo(
                                        "cp {app_dir}/configs/post-receive_{env} {post_receive}".format(
                                            app_dir=app_dir, env=role, post_receive=post_receive))

                                elif sudo(
                                        "test -f {app_dir}/post-receive_{env}".format(app_dir=app_dir,
                                                                                      env=role)).succeeded:
                                    sudo(
                                        "cp {app_dir}/post-receive_{env} {post_receive}".format(
                                            app_dir=app_dir, env=role, post_receive=post_receive))
                                else:
                                    sudo("echo '{pull_template}' > {post_receive}".format(
                                        pull_template=pull_template.format(app_dir=app_dir),
                                        post_receive=post_receive))
                            else:
                                sudo("echo '{pull_template}'ll > {post_receive}".format(
                                    pull_template=pull_template.format(app_dir=app_dir),
                                    post_receive=post_receive))
                            sudo("chmod +x {post_receive}".format(post_receive=post_receive))
                            sudo(post_receive)


def get_remote_url(host, project):
    return 'git@{host}:{git_root}/{project}.git'.format(host=host, git_root=git_root, project=project)


def test(project):
    with settings(warn_only=True):
        for p, items in projects.iteritems():
            if project is None or p == project:
                local_path = items.get('local_path')
                unittest = items.get('unittest')
                if unittest and local("test -d {local_path}/tests".format(local_path=local_path),
                                      capture=True).succeeded:
                    result = local(
                        'python -m unittest discover {local_path}/tests'.format(local_path=local_path),
                        capture=True)
                    if result.failed and not confirm("Tests failed. Continue anyway?"):
                        abort("Aborting at user request.")


def commit():
    local("git add -p && git commit")


@task
def reload_service(project=None):
    with settings(warn_only=True):
        if project is None:
            container = "$(docker ps -a -q)"
        else:
            container = project
        run("docker stop {container}".format(container=container))
        run("docker rm {container}".format(container=container))
        update_post_receive(project)


def start(project=""):
    git_dir = '{git_root}/{project}.git'.format(git_root=git_root, project=project)
    post_receive = "{git_dir}/hooks/post-receive".format(git_dir=git_dir)
    run(post_receive)


@task
def check_alive():
    with settings(warn_only=True):
        time.sleep(1)
        for project, items in projects.iteritems():
            if items.get('is_app') is not True:
                domain_config = _get_domain()
                alive = items.get('alive')
                role = _get_current_role()
                if role in items.get('roles', env.roledefs.keys()):
                    if isinstance(alive, dict):
                        for url, status_code in alive.iteritems():
                            check_url = url.format(prefix=domain_config['prefix'], domain=domain_config['domain'],
                                                   port=domain_config['port'], host=env.host)
                            c = local(
                                'curl -sL -w "%{http_code}"' + ' {check_url} -o /dev/null'.format(check_url=check_url),
                                capture=True)
                            if int(c.stdout) != status_code:
                                print "curl {project} failed： status={status} ".format(project=project,
                                                                                       status=str(c.stdout))
                    else:
                        check_url = items.get('alive').format(prefix=domain_config['prefix'],
                                                              domain=domain_config['domain'],
                                                              port=domain_config['port'], host=env.host)
                        c = local(
                            'curl -sL -f -w "%{http_code}"' + ' {check_url} -o /dev/null'.format(check_url=check_url),
                            capture=True)
                        if c.failed:
                            print "curl {project} failed： status={status} ".format(project=project,
                                                                                   status=str(c.stdout))

