#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis
@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: lg_job.py
@time: 17/8/3 13:53
@desc:
'''

import urllib
import json
from datetime import datetime
from lxml import etree

import jsonpath
import requests
from frame.http.request import Request
from item.item import Item

from settings import CITY, KEYWORDS


class Spider(object):
    '''
    params = {
        "px": "new",
        "city": "北京",
        "needAddtionalResult": "false",
    }
    data = {
        "first": "true",
        "pn": '1',
        "kd": "Python",
    }
    '''

    name = 'lg_job'
    # 拉勾城市
    lg_job_city_code = {
        u"北京": u"北京",
        u"上海": u"上海",
        u"广州": u"广州",
        u"深圳": u"深圳",
        u"武汉": u"武汉",
        u"成都": u"成都",
        u"重庆": u"重庆",
        u"郑州": u"郑州",
        u"杭州": u"杭州",
        u"济南": u"济南",
        u"南京": u"南京",
        u"西安": u"西安",
        u"长沙": u"长沙",
        u"哈尔滨": u"哈尔滨",
        u"石家庄": u"石家庄",
        u"合肥": u"合肥",
        u"太原": u"太原",
    }
    city_code = lg_job_city_code

    def __init__(self, db):
        self.headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Content-Length":"26",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            #"Cookie":"user_trace_token=20170714210131-8eb9df85-6894-11e7-a8f8-5254005c3644; LGUID=20170714210131-8eb9e64d-6894-11e7-a8f8-5254005c3644; ab_test_random_num=0; fromsite=cn.bing.com; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215d736a6b3e0-0cff62ef498db4-3065780b-2073600-15d736a6b3f8e5%22%7D; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B75368; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%8C%97%E4%BA%AC; _putrc=E04A5FDFC900D0CD; JSESSIONID=ABAAABAAAFCAAEG6F97C70B5898C8598F9E7FD79F2223F3; LGSID=20170726225636-9f787d14-7212-11e7-8808-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Dnew%26city%3D%25E5%258C%2597%25E4%25BA%25AC; LGRID=20170726225636-9f787e92-7212-11e7-8808-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500864188,1500879867,1500879879,1501037368; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501080997; _ga=GA1.2.1767314830.1500037290; _gid=GA1.2.1576305902.1501037368; TG-TRACK-CODE=search_code; SEARCH_ID=71c416b89d7c4d31a8498e8cbebd5617",
            "Host":"www.lagou.com",
            "Origin":"https://www.lagou.com",
            "Pragma":"no-cache",
            "Referer":"https://www.lagou.com/jobs/list_Python?px=new&city=%E5%8C%97%E4%BA%AC",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Anit-Forge-Code":"0",
            "X-Anit-Forge-Token":"None",
            "X-Requested-With":"XMLHttpRequest",
        }
        self.db = db
        # Ajax的url
        self.baseurl = "https://www.lagou.com/jobs/positionAjax.json"


    def get_list_response(self, city, keywords, page):
        '''
        method: POST
        :param params:
        :return:
        '''
        params_ = {
            "px": "new",
            "city": "北京",
            "needAddtionalResult": "false",
        }
        data_ = {
            "first": "true",
            "pn": '99',
            "kd": "java",
        }
        params_["city"] = city
        data_["pn"] = str(page)
        data_["kd"] = keywords
        url = "https://www.lagou.com/jobs/positionAjax.json"
        response = requests.post(url, params=params_, data=data_, headers=self.headers)
        return response

    def parse_list(self, resposne):
        # 提取职位信息
        positionResult = jsonpath.jsonpath(json.loads(response.content), "$..result")
        if positionResult:
            return positionResult[0]

    def run(self, cities, keywords):
        for city in cities:
            for kw in keywords:
                response = self.get_list_response(city, kw)
                result = self.parse_list(response)
                data = {
                    "sipder": self.name,
                    "city": city,
                    "keyword": kw,
                    "result": result
                }
                self.db.insert_one(self.name, data)

    @staticmethod
    def judgeDays(response, days=7):
        # 判断是否是七天以内
        ret = jsonpath.jsonpath(json.loads(response.content), "$..createTime")
        if not ret:
            return 'again',
        for t in ret:
            if  (datetime.now() - datetime.strptime(t, "%Y-%m-%d %H:%M:%S")).days > days:
                return False, ret.index(t)
            if len(ret) != 15:
                return False, len(ret)
        return True,

    #add
    def start_requests(self):
        # 请求参数
        lg_params = {
            "px": "new",
            "city": "北京",
            "needAddtionalResult": "false",
        }
        lg_data = {
            "first": "false",
            "pn": "1",
            "kd": "python",
        }

        for city in CITY:
            for keyword in KEYWORDS:
                lg_params['city'] = self.city_code[city]
                lg_data['kd'] = urllib.quote(keyword.encode("utf-8"))

                yield Request(self.baseurl, meta={"next":int(lg_data["pn"])+1}, method="POST", data=lg_data, params=lg_params, headers=self.headers, parse="parse_list")


     # 解析当前页中列表页链接a[href]
    def parse_list(self, response):
        lg_data = {
            "first": "false",
            "pn": "1",
            "kd": "python",
        }
        # 将json格式的数据转化为python字符串
        res = json.loads(response.content)
        # 提取详情页链接中的positionId
        positionIdlist = jsonpath.jsonpath(res, "$..positionId")
        # 详情页url模板
        origin_url = "https://www.lagou.com/jobs/{positionId}.html"
        # 组装url
        index = 15
        result = self.judgeDays(response)
        if result[0]:
            lg_data['pn'] = str(response.meta['next'])
            yield Request(response.url, data=lg_data, headers=self.headers, parse="parse_list")
        else:
            index = result[1]

        for id in positionIdlist[:index]:
            url = origin_url.format(positionId=id)
            yield Request(url, headers=self.headers, parse="parse_detail")

    # 解析详情页
    def parse_detail(self, response):
        html = etree.HTML(response.content)
        # print type(html)
        # 招聘岗位
        position = html.xpath('/html/body/div[2]/div/div[1]/div/span/text()')
        # 公司名称
        company = html.xpath('//*[@id="job_company"]/dt/a/div/h2/text()')
        # 职位月薪
        salary = html.xpath("/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()")
        # 招聘人数
        number = 1
        # 工作地点
        workposition1 = html.xpath("//*[@id='job_detail']/dd[3]/div[1]/a/text()")
        if len(workposition1):
            workposition1 = workposition1[:-1]
            workposition1 = ''.join(workposition1)
        workposition2 = html.xpath("//*[@id='job_detail']/dd[3]/div[1]/text()")
        if len(workposition2):
            workposition2 = ''.join(workposition2)
            workposition2 = workposition2.split('-')
            workposition2 = ''.join(workposition2).strip()
        work_location = workposition1 + workposition2
        # 任职要求
        jobrequirements = html.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
        if len(jobrequirements):
            jobrequirements_str = ''.join(jobrequirements).strip()
        else:
            jobrequirements_str = None

        try:
            item = Item(spider=Spider.name, position=position, company=company, salary=salary, number=number, worklocation=work_location, jobrequirements=jobrequirements_str)
            result = item.data
            print result
        except Exception, e:
            print "[ERR]: 拉勾数据提取失败....",
            print e
