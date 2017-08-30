from fabric.api import *
from datetime import *


env.project_dir = '/path/to/project'
env.roledefs = {
	'userbase':['45.32.23.144','45.32.60.134'],
	'fundbase':['45.32.23.144','45.32.60.134']
}

x = now.st
file_name = 'yum.log'


def local_op():
	local('ls -l /tmp')


@roles('userbase')
def user_update():
	with cd('/var/log'):
		run('tar -zcvf %s.tar.gz %s' % (file_name,file_name))


@roles('fundbase')
def fund_update():
	run('ls -l /home')

def update():
	execute(user_update)




