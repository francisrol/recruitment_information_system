#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: qc_job.py
@time: 17/8/3 13:53
@desc:
'''

import requests
import urllib
from lxml import etree
from item.item import *


from frame.http.request import Request
from settings import CITY, KEYWORDS

class Spider(object):
    '''
    qcgw_params = {
        "location":"010000",
        "pub_date": "2",
        "search_words": "python",
        "workyear": "99",
    }
    '''

    name = 'qc_job'
    # 前程job
    update_time_code = {
        "no-limit": "00",
        "1d": "0",
        "3d": "1",
        "7d": "2",
        "30d": "3",
        "999d": "4",
    }
    city_code = {
        u"北京": "010000",
        u"上海": "020000",
        u"广州": "030200",
        u"深圳": "040000",
        u"武汉": "180200",
        u"成都": "090200",
        u"重庆": "060000",
        u"郑州": "170200",
        u"杭州": "080200",
        u"济南": "120200",
        u"南京": "070200",
        u"西安": "200200",
        u"长沙": "190200",
        u"哈尔滨": "220200",
        u"石家庄": "160200",
        u"合肥": "150200",
        u"太原": "210200",
    }
    year_of_working_code = {
        "no_limit": "99",
        "0": "01",
        "1-3": "02",
        "3-5": "03",
    }
    params = {
        "location": "010000",
        "pub_date": "2",
        "search_words": "python",
        "workyear": "99",
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # "Content-Length": "129",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "guid=15009938436398250028; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0Bs4p00uiAsaV8cKu000000IML1300000LY9fSg.THLZ_Q5n1VeHksK85yF9pywd0ZnqujbkPHT3Pjfsnj0kuW-hu0Kd5RnvwDRznW6LnDR3nYD3rDFanWwjPWIanH0YwHbvwD7K0ADqI1YhUyPGujY1njD3rH0dPjDLFMKzUvwGujYkP6K-5y9YIZ0lQzqYTh7Wui3dnyGEmB4WUvYEIZF9mvR8TA9s5v7bTv4dUHYLrjbzn1nhmyGs5y7cRWKWwAqvHjPbnvw4Pj7PNLKvyybdphcznZufn-G4mWcsrN-VwMKpi7uLuyTq5iuo5HK-nHRzPjfzuj9Bm1bdnARdrHuBm1fvnH-WuWbsuhuB0APzm1YYP1bvnf%2526tpl%253Dtpl_10085_15730_1%2526l%253D1054828295%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m7ad13823%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D25%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526oq%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526rqlang%253Dcn%26%7C%26adsnum%3D789233; 51job=cenglish%3D0; search=jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1501726212%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA2%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%B2%DF%BB%AE%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1501651367%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch2%7E%601%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%B2%DF%BB%AE%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1501651364%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch3%7E%601%A1%FB%A1%FA230300%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%B2%DF%BB%AE%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1501651358%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch4%7E%601%A1%FB%A1%FA230300%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAjava%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1501651282%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D",
        "Host": "search.51job.com",
        "Origin": "http://search.51job.com",
        "Pragma": "no-cache",
        "Referer": "http://search.51job.com/list/010000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }


    #发送requests请求
    def start_requests(self):
        # 请求参数
        qcgw_params = {
            "location":"010000",
            "pub_date": "2",
            "keyword": "python",
            "workyear": "99",
            "page": "1"  #add
        }
        for city in CITY:
            for keyword in KEYWORDS:
                qcgw_params['pub_date'] = self.update_time_code['7d']
                qcgw_params['location'] = self.city_code[city]
                qcgw_params['keyword'] = urllib.quote(keyword.encode("utf-8"))
                # url模板
                origin_url = u'http://search.51job.com/list/{location},000000,0000,00,{pub_date},99,{keyword},2,1.html?lang=c&stype=1&postchannel=0000&workyear={workyear}&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
                # 组成url
                url = origin_url.format(location=qcgw_params["location"], pub_date=qcgw_params["pub_date"], keyword=qcgw_params["keyword"], workyear=qcgw_params["workyear"])
                #yield Request(url, headers=self.headers, parser="parse_list")
                yield Request(url, headers=self.headers, parse="parse_list")

    #解析当前页中的列表链接a[href]
    def parse_list(self, response):

        html = etree.HTML(response.content)
        # parse detail page links
        detail_links = html.xpath('//*[@id="resultList"]/div/p/span/a/@href')
        for link in detail_links:
            yield Request(link, headers=self.headers, parse="parse_detail")

        # parse next page link
        next_link = html.xpath("//li[@class='bk'][2]/a/@href")
        if next_link:
            yield Request(next_link[0], headers=self.headers, parse="parse_list")

    #解析详情页信息
    def parse_detail(self, response):
        html = etree.HTML(response.content)
        # 招聘岗位
        position_name = html.xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/h1/text()')
        # 公司名称
        company_name = html.xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/p[1]/a/text()')
        # 职位月薪
        salary = html.xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/strong/text()")
        # 工作经验   最低学历 招聘人数 发布时间 英语 专业 ---提取招聘人数
        result = html.xpath('/html/body/div[2]/div[2]/div[3]/div[1]/div/div/span/text()')
        # 上班地址
        work_location = html.xpath("/html/body/div[2]/div[2]/div[3]/div[5]/div/p/text()")[1].strip()
        # work_location = self.filterfirst(work_location)
        # 任职要求
        try:
            jobrequirements = html.xpath('/html/body/div[2]/div[2]/div[3]/div[4]/div/text()')
        except:
            jobrequirements = "无"
        jobrequirements_str = ''.join(jobrequirements).strip()

        try:
            item = Item(spider=Spider.name, position=position_name, company=company_name, salary=salary, number=result, worklocation=work_location, jobrequirements=jobrequirements_str)
            result = item.data
            print result

        except Exception, e:
            print "[ERR]: 前程数据提取失败....",
            print e
            raise

    # def dealerror(self, temp, replace=None):
    #     if temp:
    #         return temp
    #     else:
    #         return replace
    #
    # def handle_requirements_info(self, temp, replace = None):
    #     if len(temp):
    #         res = "".join(temp).strip()
    #         print "信息：", res
    #         # 找工作经验
    #         index = res.find("经验")
    #         # 找本科
    #         index1 = res.find("科")
    #         # 找大专
    #         index11 = res.find("专")
    #         # 找硕士或是博士
    #         index2 = res.find("士")
    #         # 找招聘人数
    #         index3 = res.find("聘")
    #         # 找发布时间
    #         index4 = res.find("发布")
    #
    #         # 工作经验
    #         if index != -1:
    #             workbackground = res[:index]
    #             # print "workbackground--", workbackground
    #         else:
    #             workbackground = None
    #             # print "workbackground--", workbackground
    #
    #         # 专科或是本科  硕士或是博士
    #         if index1 != -1:
    #             education = res[index1 - 1:index1 + 1]
    #             # print "education--", education
    #         elif index2 != -1:
    #             education = res[index2 - 1:index2 + 1]
    #             # print "education++", education
    #         elif index11 != -1:
    #             education = res[index11 - 1:index11 + 1]
    #             # print "education11", education
    #         else:
    #             education = None
    #             # print "education==", education
    #
    #         # 招聘人数
    #         if index3 != -1:
    #             if res.find("若干") != -1:
    #                 number = 1
    #                 # print "number--", number
    #             else:
    #                 number = res[index3 + 1:index3 + 2]
    #                 # print "number++", number
    #         else:
    #             number = None
    #             # print "number==", number
    #
    #         # 发布时间
    #         if index4 != -1:
    #             releasedata = res[index4 - 5:index4]
    #             # print "releasedata--", releasedata
    #         else:
    #             releasedata = None
    #             # print "releasedata++", releasedata
    #     else:
    #         return replace
    #
    #     return number
    #
    # def dealinfo(self, info, replace = None):
    #     if len(info):
    #         info_list = info.split('|')
    #
    #         # 公司性质
    #         companynature = info_list[0].strip()
    #
    #         # 公司规模
    #         companysize = info_list[1].strip()
    #
    #         companyindustry = info_list[2].strip()
    #
    #     else:
    #         companynature = None
    #         companysize = None
    #         companyindustry = None
    #         return companynature,companysize,companyindustry
    #     return companynature, companysize,companyindustry

if __name__ == '__main__':
    pass