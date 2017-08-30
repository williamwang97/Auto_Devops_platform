# -*- coding=utf-8 -*-
from fabric.api import *
from fabric.colors import *
from pymongo import MongoClient
import subprocess
import hashlib
import os,sys
from datetime import *

now_time = datetime.now()
fomat_time = str(now_time.date()) + '_' + \
			 str(now_time.time()).split(':')[0] + '_' + \
			 str(now_time.time()).split(':')[1] + '_' + \
			 str(now_time.time()).split(':')[2] 

#env.hosts = ['45.32.23.144','45.32.60.134']
#env.key_filename = "/home/william/my_server-Identity"
env.project_dir = '/path/to/project'
env.roledefs = {
	'userbase':['45.32.23.144','45.32.60.134'],
	'fundbase':['45.32.23.144','45.32.60.134']
}
@runs_once()
def local_op():
	local('ls -l /tmp')


@roles('userbase')
def user_update():
	run('ls -l /tmp')


@roles('fundbase')
def fund_update():
	run('ls -l /home')

def update():
	local_op()
	execute(user_update)
	execute(fund_update)

class DataBase_select(object):
	def __init__(self,server_name):
		self.ip = ips
		client= MongoClient("127.0.0.1",27017)
		db = client.server_info
		ips = db.server_ips.find_one({'server_names':server_name})
		return ips	


class deploy_server(object):

	l_dir = '/local_path/to/files'
	r_tmp_dir = '/remote_path/to/files'
	r_project_dir = '/remote_path/to/project'
	r_server_dir = '/remote_path/to/server'
	backup_dir = '/backup_path/to/files'

	def create_update_package(self,server_name):
    	with lcd(l_dir):  
        	local("tar -cjf %s.tar.bz %s" % (server_name,server_name))

	def rsync_files(self,server_name,hosts): 
	    with settings(hide('running','stdout'), warn_only=True): 
	        with lcd(l_dir):
	           result = local('rsync -qPavz %s %s:%s' % (server_name,hosts,r_tmp_dir)) 
	           
	def check_md5_files(self,server_name):
		with run('cd %s' % r_tmp_dir)
		    with settings(warn_only=True):  
		        lmd5=local("md5sum %s.tar.gz" % server_name,capture=True).split(' ')[0]  
		        rmd5=run("md5sum %s.tar.gz" % server_name).split(' ')[0]  
		    if lmd5==rmd5:  
		        print "OK"  
		    else:  
		        print "ERROR"

	def deploy_files(self,server_name):
		with run('cd %s' % r_tmp_dir)
			with run('tar -zxvf %s.tar.gz && rsync -qavz %s %s' % (server_name,server_name,r_project_dir)) 



	def backup_files(self,server_name):
		with cd(r_project_dir):
			with run('tar cjf %s+%s.tar.bz %s' % (server_name,format_time,server_name)):
				with run('mv %s+%s.tar.bz backup_dir' % (server_name,format_time))  

	def roll_back_version(self,server_name):
		with cd(backup_dir):
			roll_back_filename = run("ls -l *.tar.bz | tail -n 1 | awk '{print $9}'")
			with run('tar jxf %s -C %s' % (roll_back_filename,r_project_dir))

	def restart_server(self,hosts):
		with cd(r_server_dir):
			with run('bash shutdown.sh && bash startup.sh'):






env.roledefs = DataBase_select().ip(server_name)
@task
@roles(server_name)
@parallel(pool_size=16)
def execute_rsync():
    execute(deploy_server().rsync_files, env.host) ### 读取 @roles('test.com') 里面的主机，并把 host 传递给 rsync_deploy 函数，并且 @parallel(pool_size=16) 来并发 









		
		