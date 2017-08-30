# -*- coding: UTF-8 -*-
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515 import *
from aliyunsdkecs.request.v20140526 import *
import json
import ConfigParser


class aliyun_slb_api(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.cli = client.AcsClient(AccessKey,AccessSecret,RegionId)

	def request_api(self, request, *values):
        if values:
            for value in values:
                for k, v in value.iteritems():
                    request.add_query_param(k, v)
        request.set_accept_format('xml')
        result = self.cli.do_action_with_exception(request)
        return json.loads(result)

    def describeloadbalancer(self,loadbalancername):
    	'''查询slb信息'''
    	request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    	values = {"RegionId":"cn-hangzhou","LoadBalancerId":str(loadbalancername)}
    	info = self.request_api(request,values)['LoadBalancers']['LoadBalancer']
    	if info:
            return [loadbalancer_info['LoadBalancerId']
                    for loadbalancer_info in info]





