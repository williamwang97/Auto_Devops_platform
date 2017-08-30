from datetime import *
from random import randint

class test():
	l_dir = '/local_path/to/files'
	r_dir = '/remote_path/to/files'


	def rsync_deploy(self,server_name,hosts): 
	    with settings(hide('running','stdout'), warn_only=True): 
	        with lcd(l_dir):
	           result = local('rsync -qPavz %s %s:%s' % (server_name,hosts,r_dir)) 

x = test()






now_time = datetime.now()
fomat_time = str(now_time.date()) + '_' + \
			 str(now_time.time()).split(':')[0] + '_' + \
			 str(now_time.time()).split(':')[1] + '_' + \
			 str(now_time.time()).split(':')[2] 


print fomat_time

class Vehicle:
    speed = 60.0

    def drive(self, distance):
        time = distance / self.speed
        print time

class Bike(Vehicle):
    speed = 25.0

class Train(Vehicle):
    speed = 200.0
    fuel = 500.0

bike = Bike()
bike.drive(1000.0)

train = Train()
train.drive(1000.0)
print train.fuel
