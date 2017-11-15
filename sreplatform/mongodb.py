# -*- coding: UTF-8 -*-
import pymongo
import aliyunslb_api
import mns_api
from pymongo import MongoClient
from pymongo import 


class mongodb_opertion(aliyunslb_api.aliyun_slb_api,mns_api.aliyun_mns_api):

    def __init__(self):
        """客户端初始化"""
        self.client = MongoClient('localhost',27017)

    def create_slb_db(self,dbname,collection_name):
        """获取slb所有数据与ecs对应关系并写入mongodb"""
        create_db = self.client[dbname]
        create_collection = create_db[collection_name]
        slb_api = aliyunslb_api.aliyun_slb_api()
        slb_list = slb_api.selectloadbalancer()
        slb_new_name = []
        for slb_instance in slb_list:
            for slb_name,slb_ip in slb_instance.items():
                s = str(slb_name).split('-')
                s.pop(-1)
                s_new = '-'.join(s)
                slb_new_name.append(s_new)
        slb_new_name = list(set(slb_new_name))
        #print slb_new_name
        while '' in slb_new_name:
            slb_new_name.remove('')
        slb_ecs_new_list = []
        for s_name in slb_new_name:
            slb_ecslist = slb_api.createslbjson(s_name)
            slb_ecs_new_list.append(slb_ecslist)
        #print slb_ecs_new_list
        result = create_collection.insert_many(slb_ecs_new_list)
        #print result

    def create_mns_db(self,dbname,collection_name):
        """获取mns列表并写入mongo"""
        create_db = self.client[dbname]
        create_collection = create_db[collection_name]
        alimns_api = mns_api.aliyun_mns_api()
        mnslist = alimns_api.getlistqueuenames()
        for name in mnslist:
            mnsjson = {}
            mnsjson['name'] = name
            create_collection.insert_one(mnsjson)


    def drop_project_collection(self,dbname,collection_name):
        """清空旧collection数据"""
        drop_db = self.client[dbname]
        drop_db.drop_collection(collection_name)
    
    def update_slb_collection(self,dbname,collection_name):
        """更新slb的collection 数据"""
        self.drop_project_collection(dbname,collection_name)
        self.create_slb_db(dbname,collection_name)

    def update_mns_collection(self,dbname,collection_name):
        """更新mns的collection数据"""
        self.drop_project_collection(dbname,collection_name)
        self.create_mns_db(dbname.collection_name)



    def select_project_info(self,dbname,collection_name,project_name):
        """查询服务对应的slb和ecs关系"""
        select_info = self.client[dbname]
        #info = select_info.get_collection(collection_name).find_one(project_name)
        info = select_info.get_collection(collection_name).find()

        for i in info:
            if project_name in i:
                reasult = select_info.get_collection(collection_name).find_one()
        print reasult

        #print info

    def get_database_names(self):
        """获取数据库名字列表"""
        conn = self.client
        names = conn.database_names()
        print names

    def get_collection_names(self,dbname):
        """获取当前数据库下的collection的列表"""
        conn = self.client[dbname]
        names = conn.collection_names()
        print names



if __name__ == '__main__':
    x = mongodb_opertion()
    #x.create_slb_db('iwjw_project_name','slb_ecs_list')
    #x.drop_project_collection('iwjw_project_name','slb_ecs_list')
    #x.select_project_info('iwjw_project_name','slb_ecs_list','iw-pos-appserver')
    # x.get_database_names()
    # x.get_collection_names('iwjw_project_name')
    #x.create_mns_db('iwjw_mns_name','mns_names')
    x.update_slb_collection('iwjw_project_name','slb_ecs_list')





