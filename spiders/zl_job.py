#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: zl_job.py
@time: 17/8/3 13:53
@desc:
'''

import urllib
import requests
from lxml import etree

# from database.mongodb import resultdb
from item.item import *
from frame.http.request import Request
from settings import CITY, KEYWORDS

class Spider(object):
    '''
    zlgw_params = {
        "pd": "7",   # 发布时间
        "jl": "北京",  # 地区条件
        "kw": "python",  # 搜索
        "sm": "0",
        "p": "1",
        "sf": "0",
        "st": "99999",
        "isadv": "1"
    }
    '''
    name = "zl_job"
    # 智联job
    update_time_code = {
        "no-limit": "1",
        "1d": "1",
        "3d": "3",
        "7d": "7",
        "30d": "30"
    }
    city_code = {
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
    year_of_working_code = {
        "no_limit": "0",
        "0": "0000",
        "0-1": "0001",
        "1-3": "0103",
        "3-5": "0305",
        "5-10": "0510",
        "9999": "1099",
    }
    params = {
        "pd": "7",  # 发布时间
        "jl": "北京",  # 地区
        "kw": "python",  # 搜索条件
        "sm": "0",
        "p": "1",
        "sf": "0",
        "st": "99999",
        "isadv": "1"
    }

    def __init__(self, db):
        self.header = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Cookie":"utype=667215829; JSSearchModel=0; LastCity%5Fid=530; LastCity=%e5%8c%97%e4%ba%ac; __zpWAM=1500882341291.157319.1500882341.1501222889.2; rt=a83bdd59b2e54ef9a816dcd2b0ad88a8; urlfrom=121113803; urlfrom2=121113803; adfcid=pzzhubiaoti1; adfcid2=pzzhubiaoti1; adfbid=0; adfbid2=0; pcc=r=1016943274&t=0; dywez=95841923.1501392744.12.4.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1500285062,1500882338,1501222887,1501392744; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1501392744; __xsptplusUT_30=1; __utmt=1; _jzqx=1.1500388298.1501392744.4.jzqsr=passport%2Ezhaopin%2Ecom|jzqct=/.jzqsr=zhaopin%2Ecom|jzqct=/; _jzqckmp=1; __xsptplus30=30.3.1501392743.1501392743.1%234%7C%7C%7C%7C%7C%23%23OoUAupP2XFipk5yaMZsWbAJwDqgsa5QC%23; _qzja=1.1611096924.1500991727805.1501034418578.1501392748741.1501392748741.1501392757191.0.0.0.5.3; _qzjb=1.1501392748741.2.0.0.0; _qzjc=1; _qzjto=2.1.0; _jzqa=1.2227694574987069200.1500382797.1501222888.1501392744.8; _jzqc=1; _jzqb=1.3.10.1501392744.1; dywea=95841923.622839591287027100.1500284941.1501222887.1501392744.12; dywec=95841923; dyweb=95841923.6.9.1501392787832; __utma=269921210.503941949.1500284941.1501222887.1501392744.12; __utmb=269921210.6.9.1501392787836; __utmc=269921210; __utmz=269921210.1501392744.12.4.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/; LastJobTag=%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e5%8c%85%e4%bd%8f%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e9%a4%90%e8%a1%a5%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e6%88%bf%e8%a1%a5%7c%e5%8c%85%e5%90%83%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4; LastSearchHistory=%7b%22Id%22%3a%22844da611-16d5-4f70-891b-5810d2c1c974%22%2c%22Name%22%3a%22java+%2b+%e5%8c%97%e4%ba%ac%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d%25e5%258c%2597%25e4%25ba%25ac%26kw%3djava%26p%3d1%26isadv%3d0%22%2c%22SaveTime%22%3a%22%5c%2fDate(1501392788071%2b0800)%5c%2f%22%7d; SubscibeCaptcha=1A8F1C5B7DAF096DA168803AAA087B43",
            "Host":"sou.zhaopin.com",
            "Pragma":"no-cache",
            "Referer":"http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=java&p=1&isadv=0",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
        self.db = db
        self.baseURL = "http://sou.zhaopin.com/jobs/searchresult.ashx"

    #发送requests请求
    def start_requests(self):
        #add

        # 请求参数  add
        # zl_params = {
        #     "pd": "7",  # 发布时间
        #     "jl": "北京",  # 地区
        #     "kw": "python",  # 搜索条件
        #     "sm": "0",
        #     "p": "1",
        #     "sf": "0",
        #     "st": "99999",
        #     "isadv": "1"
        # }

        for city in CITY:
            for keyword in KEYWORDS:
                self.params['pd'] = self.update_time_code['7d']
                self.params['jl'] = self.city_code[city]
                self.params['kw'] = urllib.quote(keyword.encode("utf-8"))

                yield Request(self.baseURL, params=self.params, headers=self.headers, parse="parse_list")

    def get_list_response(self, city, keywords, pub_date="7d"):
        # 查询参数
        params = {
            "pd": "7",  # 发布时间
            "jl": "北京",  # 地区
            "kw": "python",  # 搜索条件
            "sm": "0",
            "p": "1",
            "sf": "0",
            "st": "99999",
            "isadv": "1"
        }
        params['pd'] = self.update_time_code[pub_date]
        params['jl'] = self.city_code[city]
        params['kw'] = keywords
        # 请求url
        url = "http://sou.zhaopin.com/jobs/searchresult.ashx"
        # 发起请求
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=2)
        except:
            print('try more time')
            return self.get_list_response(city, keywords)
        else:
            return response

    def get_total_num(self, *args, **kwargs):
        response = self.get_list_response(*args, **kwargs)
        html = etree.HTML(response.content)
        # 提取总数
        num = html.xpath('//div[@class="main"]//span[@class="search_yx_tj"]//em/text()')
        return int(num[0])

    #解析当前页面中的列表链接a[href]    add
    def parse_list(self, response):
        html = etree.HTML(response.content)
        detail_links = html.xpath('//div[@class = "newlist_list_content"]/table/tr/td/div/a/@href')
        # print link_list
        # print len(link_list)
        for link in detail_links:
            if link.endswith('.htm'):
                yield Request(link, headers=self.headers, parse="parse_detail")

        next_link = html.xpath("/html/body/div[3]/div[3]/div[3]/form/div[1]/div[1]/div[3]/ul/li[12]/a/@href")
        if next_link:
            yield Request(next_link[0], headers=self.headers, parse="parse_list")

    #解析详情页      add
    def parse_detail(self, response):
        html = etree.HTML(response.content)
        # print response.content
        # 招聘岗位
        position = html.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()')
        # 公司名称
        company = html.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()')
        # 职位月薪
        salary = html.xpath("/html/body/div[6]/div[1]/ul/li[1]/strong/text()")
        # 工作地点
        work_location = html.xpath('//div[@class = "tab-inner-cont"]/h2/text()')
        # 招聘人数
        number = html.xpath("/html/body/div[6]/div[1]/ul/li[7]/strong/text()")
        # 任职要求
        jobrequirements = html.xpath('//div[@class = "tab-inner-cont"]/p/text()')
        if len(jobrequirements):
            jobrequirements = jobrequirements[:-4]
        else:
            jobrequirements = None

        try:
            item = Item(spider=Spider.name,position=position, company=company, number=number, salary=salary, worklocation=work_location, jobrequirements=jobrequirements)
            result = item.data
            print result

        except Exception, e:
            print "[ERR]: 智联数据提取失败....",
            print e
            raise


    #验证提取的url是否有效
    # def validate(self, url):
    #     flag = True



