# -*- coding: UTF-8 -*-
from mns import mns_client
from mns.account import Account
from mns.queue import *
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class aliyun_mns_api(object):
    
    def __init__(self):
        """客户端初始化"""
        cf = ConfigParser.ConfigParser()
        cf.read("aliyun.conf")
        host = cf.get('AccessKey_mns',"Host")
        accessid = cf.get('AccessKey_mns',"Access_ID")
        accesskey = cf.get('AccessKey_mns',"Access_Key")
        self.cli = Account(host,accessid,accesskey)
        
    def sendmessagerequest(self,queue_name):
        """向指定mns发送message"""
        with open('SendMessage.txt','r') as f:
            for line in f:
                message = Message(line)
                re_msg = self.cli.get_queue(queue_name).send_message(message)
                print "Send Message Succeed! MessageBody:%s MessageID:%s" % (line,re_msg.message_id)
        
    def getlistqueuenames(self):
        """查询消息列队名字"""
        result = self.cli.list_queue()
        name_list = []
        for name in result[0]:
            real_name = str(name).split('/')[-1]
            name_list.append(real_name)
        #print name_list    
        return name_list

if __name__ == '__main__':
    x = aliyun_mns_api()
    #x.sendmessagerequest()
    #x.getlistqueuenames()
    x.sendmessagerequest('a')
