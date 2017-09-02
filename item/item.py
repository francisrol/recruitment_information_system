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
            self, spider = None, position = None, company = None, number = None, salary = None,
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
        item["position"] = self.filter(self._position)
        item["company"] = self.filter(self._company)
        item["number"] = self.filter(self._number)
        item["salary_min"], item["salary_max"] = self.filter_salary(self._salary)
        item["work_location"] = self.filter(self._work)
        item["pub_date"] = self.filter(self._releasedata)
        #item["worknature"] = self.filter(self._worknature)
        item["work_background"] = self.filter(self._workbackground)
        item["education"] = self.filter(self._education)
        item["position_category"] = self._positioncategory if self._positioncategory else None
        item["jobrequirements"] = self.filter(self._jobrequirements)
        item["work_location"] = self.filter(self._jobaddress)
        item["company_size"] = self.filter(self._companysize)
        item["companynature"] = self.filter(self._companynature)
        item["industry"] = self.filter(self._companyindustry)
        item["homepage"] = self.filter(self._companyhome)
        item["address"] = self.filter(self._companyaddress)
        return item


    #生成组装的字段字典
    @property
    def data(self):
        return self._gen_item()

    def filter(self, temp, index=0, replace=None):
        return temp[index].strip() if temp else replace

    def filter_salary(self, salary):
        salary_min = 0
        salary_max = 0
        if self._spider == "qc_job":
            if len(salary):
                # 找到万
                salary_index1 = self._salary.find('万')
                # 找到千
                salary_index2 = self._salary.find('千')
                # 找到天
                salary_index3 = self._salary.find('天')
                # 找到年
                salary_index4 = self._salary.find('年')

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

                if salary_index3 != -1:
                    salary_str = self._salary[:salary_index3-4]
                    salary_min = int(salary_str)*22
                    salary_max = salary_min

                if salary_index4 != -1:
                    salary_str = self._salary[:salary_index4-1]
                    salary_min = salary_str
                    salary_max = salary_min

            else:
                salary_min = 0
                salary_max = 0


        elif self._spider == "zl_job":
            pass

        return salary_min, salary_max












