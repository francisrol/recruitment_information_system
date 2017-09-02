#!/usr/bin/env python
# encoding=utf-8

'''

@author: houxiaojun

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: Chinesejunzai@163.com

@software: garner

@file: item.py

@time: 17-8-30 下午5:27

@desc:

'''
#封装的提取字段类
'''
position        招聘岗位
company         公司名称
salary_min      最低薪资
salary_max      最高薪资
releasedata     发布时间
worknature      工作性质
workbackground  工作经验
education       最低学历
number          招聘人数
positioncategory职位类别
jobrequirements 任职要求
jobaddress      工作地址
companysize     公司规模
companynature   工作性质
companyindustry 公司行业
companyhome     公司主页链接
companyaddress  公司地址
'''


class Item(object):
    def __init__(
            self, spider, position, company, number, salary,
            releasedata = None,worknature = None, workbackground = None, education = None,
            positioncategory = None,jobrequirements = None,  jobaddress = None, companysize = None,
            companynature = None,companyindustry = None, companyhome = None, companyaddress = None
    ):
        self._spider = spider
        self._position = position
        self._company = company
        self._number = number
        self._salary = salary
        self._releasedata = releasedata
        self._worknature = worknature
        self._workbackground = workbackground
        self._education = education
        self._positioncategory = positioncategory
        self._jobrequirements = jobrequirements
        self._jobaddress = jobaddress
        self._companysize = companysize
        self._companynature = companynature
        self._companyindustry = companyindustry
        self._companyhome = companyhome
        self._companyaddress = companyaddress

    #
    def _gen_item(self):
        item = {}
        item["position"] = self._position if self._position else "NULL"
        item["company"] = self._company if self._company else "NULL"
        item["number"] = self._number if self._number else "NULL"
        # item["salary"] = salary if salary else "NULL"
        item["salary_min"], item["salary_max"] = self.filter_salary()
        # item["workposition"] = workposition if workposition else "NULL"
        item["releasedata"] = self._releasedata if self._releasedata else "NULL"
        item["worknature"] = self._worknature if self._worknature else "NULL"
        item["workbackground"] = self._workbackground if self._workbackground else "NULL"
        item["education"] = self._education if self._education else "NULL"
        item["positioncategory"] = self._positioncategory if self._positioncategory else "NULL"
        item["jobrequirements"] = self._jobrequirements if self._jobrequirements else "NULL"
        item["jobaddress"] = self._jobaddress if self._jobaddress else "NULL"
        item["companysize"] = self._companysize if self._companysize else "NULL"
        item["companynature"] = self._companynature if self._companynature else "NULL"
        item["companyindustry"] = self._companyindustry if self._companyindustry else "NULL"
        item["companyhome"] = self._companyhome if self._companyhome else "NULL"
        item["companyaddress"] = self._companyaddress if self._companyaddress else "NULL"

        return item


    #生成组装的字段字典
    @property
    def data(self):
        return self._gen_item()


    def filter_salary(self):
        salary_min = 0
        salary_max = 0
        if self._spider == "qc_job":
            salary_index1 = self._salary.find('万')
            # 找到千
            salary_index2 = self._salary.find('千')

            if salary_index1 != -1:
                salary_list = self._salary[:salary_index1].split('-')
                salary_min = int(float(salary_list[0]) * 10000)
                salary_max = int(float(salary_list[1]) * 10000)
                # print salary_min
                # print salary_max

            if salary_index2 != -1:
                salary_list = self._salary[:salary_index2].split('-')
                salary_min = int(float(salary_list[0]) * 1000)
                salary_max = int(float(salary_list[1]) * 1000)


        elif self._spider == "zl_job":
            pass

        return salary_min, salary_max







