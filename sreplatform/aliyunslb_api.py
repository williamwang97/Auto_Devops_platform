# -*- coding: UTF-8 -*-
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest,AddBackendServersRequest,RemoveBackendServersRequest,SetBackendServersRequest,DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json
import ConfigParser




class aliyun_slb_api(object):
    
    def __init__(self):
        """客户端初始化"""
        cf = ConfigParser.ConfigParser()
        cf.read("aliyun.conf")
        accesskey = cf.get('AccessKey_slb',"AccessKey_ID")
        accesssecret = cf.get('AccessKey_slb',"AccessSecret")
        regionid = cf.get('AccessKey_slb',"RegionId")
        self.cli = client.AcsClient(accesskey,accesssecret,regionid)

    def request_aliyun_api(self, request, *values):
        """请求接口"""
        if values:
            for value in values:
                for k, v in value.iteritems():
                    #print k,v

                    request.add_query_param(k, v)
        request.set_accept_format('json')
        result = self.cli.do_action_with_exception(request)
        return json.loads(result)

    def describeloadbalancer(self, loadbalancername):
        """查询slb实例id"""
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()

        values = {"RegionId":"cn-hangzhou","LoadBalancerName":str(loadbalancername)}
        info = self.request_aliyun_api(request,values)['LoadBalancers']['LoadBalancer']
        if info:
            return [loadbalancer_info['LoadBalancerId'] for loadbalancer_info in info]
    
    def selcetmasterzoneid(self,loadbalancername):
        """查询slb主可用区id"""
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        values = {"RegionId":"cn-hangzhou","LoadBalancerName":str(loadbalancername)}
        info = self.request_aliyun_api(request,values)['LoadBalancers']['LoadBalancer']
        if info:
            return [masterzone_info['MasterZoneId'] for masterzone_info in info]

    def describelbackenserverid(self,loadbalancername):
        """通过slb 查询后端ecs id"""
        loadbalancerid = self.describeloadbalancer(loadbalancername)[0]
        masterzoneid = self.selcetmasterzoneid(loadbalancername)[0]
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        values = {"RegionId":"cn-hangzhou","MasterZoneId":str(masterzoneid),"LoadBalancerId":str(loadbalancerid)}
        info = self.request_aliyun_api(request,values)['BackendServers']['BackendServer']      
        ecsidlist = [ecsid['ServerId'] for ecsid in info]
        return ecsidlist
        

    def selectlecslist(self,loadbalancername):
        """查询slb与ecs对应关系"""
        ecsids = self.describelbackenserverid(loadbalancername)
        ecsidlist = []
        for ecsid in ecsids:
            ecsidlist.append(str(ecsid))

        request = DescribeInstancesRequest.DescribeInstancesRequest()
        values = {'RegionId':"cn-hangzhou","InstanceIds":str(ecsidlist)}
        info = self.request_aliyun_api(request,values)['Instances']['Instance']
        ecsitems = {}
        ecsipjson = {}
        if info:
            for i in info:
                ecsitems[str(i['InstanceName'])] = str(i['InnerIpAddress']['IpAddress'][0])
                
        #ecsiplist.append(ecsitems)
         
        ecsipjson[loadbalancername] = ecsitems
        return ecsipjson
        #print ecsipjson

    def selectloadbalancer(self):
        """查询slb列表"""
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        values = {'RegionId':"cn-hangzhou"}
        info = self.request_aliyun_api(request,values)
        slb_list = []
        for i in info["LoadBalancers"]["LoadBalancer"]:

            slb_list.append({i["LoadBalancerName"]:i["Address"]})
        return slb_list
        #print slb_list

    def searchloadbalancer(self,loadbalancername):
        """搜索slb的wan和lan的id"""
        slb_list = self.selectloadbalancer()
        slb_wan_lan_list = []
        for slb_name in slb_list:
            if str(slb_name).find(loadbalancername) >= 0 :
                slb_wan_lan_list.append(slb_name)

        return slb_wan_lan_list

    def createslbjson(self,loadbalancername):
        """创建slb的json信息"""
        slb_list = self.selectloadbalancer()
        slb_wan_lan_list = self.searchloadbalancer(loadbalancername)
        projectname = {}
        projectslblist = []
        for name in slb_wan_lan_list:
            for key,values in name.items():
                slb_backservers = self.selectlecslist(str(key))
                slb_backservers[key]['ip'] = str(values)
                projectslblist.append(slb_backservers)
                projectname["name"] = loadbalancername 
        projectname["info"] = projectslblist
                
        return projectname
        #print projectname


    def selectecsinfo(self,ecsip):
        """查询ecs实例Id"""
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        values = {'RegionId':"cn-hangzhou","InnerIpAddresses":[str(ecsip)]}
        info = self.request_aliyun_api(request,values)
        for i in info["Instances"]["Instance"]:
            return i["InstanceId"]


    def addbackendecs(self,loadbalancername,ecsip):
        """添加后端ecs服务器"""
        loadbalancerid = self.describeloadbalancer(loadbalancername)[0]
        serverid = self.selectecsinfo(ecsip)[0]
        if not loadbalancerid or not serverid:
            print "slb or server is not found!"
        else:
            request = AddBackendServersRequest.AddBackendServersRequest()
            values = {"BackendServers":[{'ServerId':str(serverid),"Weight":"100"}],"LoadBalancerId":str(loadbalancerid)}
            backendinfo = self.request_api(request, values)['BackendServers']
            print backendinfo

    def removebackendecs(self,loadbalancername,ecsip):
        """移除后端ecs服务器"""
        loadbalancerid = self.describeloadbalancer(loadbalancername)[0]
        serverid = self.selectecsinfo(ecsip)[0]
        if not loadbalancerid or not serverid:
            print "slb or server is not found!"
        else:
            request = RemoveBackendServersRequest.RemoveBackendServersRequest()
            values = {"BackendServers":[{'ServerId':str(serverid)}],"LoadBalancerId":str(loadbalancerid)}
            backendinfo = self.request_api(request, values)['BackendServers']
            print backendinfo

    def increasebackendecs_weight(self,loadbalancername,ecsip):
        """set后端ecs服务器权重100"""
        loadbalancerid = self.describeloadbalancer(loadbalancername)[0]
        serverid = self.selectecsinfo(ecsip)[0]
        if not loadbalancerid or not serverid:
            print "slb or server is not found!"
        else:
            request = SetBackendServersRequest.SetBackendServersRequest()
            values = {"RegionId":"cn-hangzhou","LoadBalancerId":str(loadbalancerid),"BackendServers":[{'ServerId':str(serverid),"Weight":"100"}]}
            backendinfo = self.request_api(request, values)['BackendServers']
            print backendinfo

    def decreasebackendecs_weight(self,loadbalancername,ecsip):
        """set后端ecs服务器权重0"""
        loadbalancerid = self.describeloadbalancer(loadbalancername)[0]
        serverid = self.selectecsinfo(ecsip)[0]
        if not loadbalancerid or not serverid:
            print "slb or server is not found!"
        else:
            request = SetBackendServersRequest.SetBackendServersRequest()
            values = {"RegionId":"cn-hangzhou","LoadBalancerId":str(loadbalancerid),"BackendServers":[{'ServerId':str(serverid),"Weight":"0"}]}
            backendinfo = self.request_api(request, values)['BackendServers']
            print backendinfo


if __name__ == '__main__':
    x = aliyun_slb_api()
    #x.selectloadbalancer()
    #x.describelbackenserverid("iwjw-poros-lan")
    #x.selcetmasterzoneid('iwjw-poros-lan')
    #x.describeloadbalancer("iwjw-poros-lan")
    #x.selectecsinfo("ip")
    x.createslbjson('iw-demeter')
    #x.selectlecslist('iwjw-poros-wan')
    #x.searchloadbalancer('iwjw-poros')













echo $PASSWORD | hal config ci jenkins master add my-jenkins-master \
    --address 192.168.1.238:8080 \
    --username admin \
    --password





	


