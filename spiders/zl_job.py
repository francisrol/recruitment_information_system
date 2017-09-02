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

import requests
from lxml import etree
# from database.mongodb import resultdb
from item.item import *
from frame.http.request import Request


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

    def __init__(self, db, city=None, keywords=None):
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

        #add
        self.baseURL = "http://sou.zhaopin.com/jobs/searchresult.ashx"

        # 请求参数  add
        self.params = {
            "pd": "7",  # 发布时间
            "jl": "北京",  # 地区
            "kw": "python",  # 搜索条件
            "sm": "0",
            "p": "1",
            "sf": "0",
            "st": "99999",
            "isadv": "1"
        }
        self.params['pd'] = '7'
        self.params['jl'] = city
        self.params['kw'] = keywords
        # self.params['p'] = page

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

    #获取响应页面     add
    def getlistresponse(self):

        try:
            response = requests.get(self.baseURL, params= self.params, headers = self.header, timeout = 2)
        except Exception, e:
            print e
            return self.getlistresponse()
        else:
            return response


    #解析当前页面中的列表链接a[href]    add
    def parselinklist(self, response):
        html = etree.HTML(response.content)
        link_list = html.xpath('//div[@class = "newlist_list_content"]/table/tr/td/div/a/@href')
        # print link_list
        # print len(link_list)

        return link_list


    #翻页解析提取详情页链接        add
    def getlinklists(self):

        link_lists = []
        p = 1
        while True:
            response = self.getlistresponse()
            links = self.parselinklist(response)
            len1 = len(links)
            if len(link_lists) <= 61:
                self.params['p'] = p
                # print "自加前", p
                p += 1
                # print "自加后", p
                for link in links:
                    link_lists.append(link)
                # print "第一次", len(link_lists)
                # return link_lists

            elif  link_lists[-1] != link_lists[-1-len1]:
                self.params['p'] = p
                p += 1
                # print "2222222", p
                for link in links:
                    link_lists.append(link)
            else:
                break

        return link_lists[:-len1]

    #获取详情页      add
    def getdetailsresponse(self, link_lists):
        i = 1
        for url in link_lists:
            if url.endswith('.htm'):
                response = requests.get(url, headers = self.header)
                print url
                print i
                self.parsedetails(response)
                i += 1


    #解析详情页      add
    def parsedetails(self, response):
        html = etree.HTML(response.content)
        print response.content
        # 招聘岗位
        position = html.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()')
        # print position
        if len(position):
            position = position[0].strip()
        else:
            position = None
        # 公司名称
        company = html.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()')
        # print company
        if len(company):
            company = company[0].strip()
        else:
            company = None
        # 职位月薪
        salary = html.xpath("/html/body/div[6]/div[1]/ul/li[1]/strong/text()")
        print salary
        if len(salary):
            if salary[0].find('面议') != -1:
                salary_min = 0
                salary_max = 0
            else:
                salary = salary[0].strip()[:-3].encode("utf-8")
                salary = salary.split('-')
                # global salary_min
                # global salary_max
                salary_min = int(salary[0])
                salary_max = int(salary[1])
                print "salary_min==", salary_min
                print "salary_max==", salary_max
        else:
            salary = None

        # 工作地点
        #workposition = html.xpath("/html/body/div[6]/div[1]/ul/li[2]/strong/a/text()")[0].strip()
        # print workposition
        # 发布时间
        releasedata = html.xpath('//*[@id="span4freshdate"]/text()')
        # print releasedata
        if len(releasedata):
            releasedata = releasedata[0].strip()
        else:
            releasedata = None
        # 工作性质
        worknature = html.xpath("/html/body/div[6]/div[1]/ul/li[4]/strong/text()")
        # print worknature
        if len(worknature):
            worknature = worknature[0].strip()
        else:
            worknature = None

        # 工作经验
        workbackground = html.xpath("/html/body/div[6]/div[1]/ul/li[5]/strong/text()")
        # print workbackground
        if len(workbackground):
            workbackground = workbackground[0].strip()
        else:
            workbackground = None

        # 最低学历
        education = html.xpath("/html/body/div[6]/div[1]/ul/li[6]/strong/text()")
        # print education
        if len(education):
            education = education[0].strip()
        else:
            education = None

        # 招聘人数
        number = html.xpath("/html/body/div[6]/div[1]/ul/li[7]/strong/text()")
        # print number
        if len(number):
            number = int(number[0].strip()[:-1].encode("utf-8"))
        else:
            number = None

        # 职位类别
        positioncategory = html.xpath("/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()")
        # print positioncategory
        if len(positioncategory):
            positioncategory = positioncategory[0].strip()
        else:
            positioncategory = None


        # 任职要求
        jobrequirements = html.xpath('//div[@class = "tab-inner-cont"]/p/text()')
        # print len(jobrequirements)
        # print type(jobrequirements)
        # print "===============",jobrequirements
        # for i in jobrequirements:
        #     print i
        if len(jobrequirements):
            jobrequirements = jobrequirements[:-4]
        else:
            jobrequirements = None


        # 工作地址

        jobaddress = html.xpath('//div[@class = "tab-inner-cont"]/h2/text()')
        if len(jobaddress):
            jobaddress = jobaddress[0].strip()
        else:
            jobaddress = None
        # print "+++++++++++++++",jobaddress

        # 公司规模
        companysize = html.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[1]/strong/text()')
        if len(companysize):
            companysize = companysize[0].strip()
        else:
            companysize = None
        # print "*****************",companysize

        # 公司性质
        companynature = html.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[2]/strong/text()')
        if len(companynature):
            companynature = companynature[0].strip()
        else:
            companynature = None

        # print "1111111111111111",companynature

        # 公司行业
        companyindustry = html.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[3]/strong/a/text()')
        if len(companyindustry):
            companyindustry = companyindustry[0].strip()
        else:
            companyindustry = None

        # print "2222222222222222222", companyindustry

        # 公司主页链接
        try:
            companyhome = html.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[4]/strong/a/@href')
            # print "33333333333333",companyhome
        except:
            companyhome = None


        # 公司地址
        companyaddress = html.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[5]/strong/text()')
        # print "44444444444444", companyaddress
        if len(companyhome):
            companyhome = companyhome[0].strip()
        else:
            companyhome = None

        try:
            # 将数据封装为字典形式进行存储
            # item = {}
            # item["position"] = position if position else "NULL"
            # item["company"] = company if company else "NULL"
            # # item["salary"] = salary if salary else "NULL"
            # item["salary_min"] = salary_min if salary_min else "NULL"
            # item["salary_max"] = salary_max if salary_max else "NULL"
            # # item["workposition"] = workposition if workposition else "NULL"
            # item["releasedata"] = releasedata if releasedata else "NULL"
            # item["worknature"] = worknature if worknature else "NULL"
            # item["workbackground"] = workbackground if workbackground else "NULL"
            # item["education"] = education if education else "NULL"
            # item["number"] = number if number else "NULL"
            # item["positioncategory"] = positioncategory if positioncategory else "NULL"
            # item["jobrequirements"] = jobrequirements if jobrequirements else "NULL"
            # item["jobaddress"] = jobaddress if jobaddress else "NULL"
            # item["companysize"] = companysize if companysize else "NULL"
            # item["companynature"] = companynature if companynature else "NULL"
            # item["companyindustry"] = companyindustry if companyindustry else "NULL"
            # item["companyhome"] = companyhome if companyhome else "NULL"
            # item["companyaddress"] = companyaddress if companyaddress else "NULL"
            #
            # print item
            #
            # with open("zhao.json", "w") as f:
            #     f.write(str(item))

            # 存入Mongo数据库
            # db = mongo.MongodbHandeler()
            # db.process_item(item)
            item = Item(position, company, number, salary_min, salary_max)
            result = item.data
            print result

        except Exception, e:
            print "[ERR]: 智联数据提取失败....",
            print e
            raise


    #验证提取的url是否有效
    # def validate(self, url):
    #     flag = True



