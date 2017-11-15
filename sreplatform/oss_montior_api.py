# -*- coding: UTF-8 -*-
import oss2
import ConfigParser
import sys






class aliyun_oss_api(object):
    
    def __init__(self):
        """客户端初始化"""
        cf = ConfigParser.ConfigParser()
        cf.read("aliyun.conf")
        endpoint = cf.get('AccessKey_oss',"Endpoint")
        accessid = cf.get('AccessKey_oss',"AccessKey_ID")
        accesskey = cf.get('AccessKey_oss',"AccessSecret")
        auth = oss2.Auth(accessid,accesskey)
        self.service = oss2.Service(auth,endpoint)

    def selectbucketlist(self):
        """查询bucket列表"""
        buckets_list = []
        for i in oss2.BucketIterator(self.service):
            buckets_list.append(i.name)
        #return buckets_list
        print buckets_list
            
        


if __name__ == '__main__':
    x = aliyun_oss_api()
    x.selectbucketlist()





        