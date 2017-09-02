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
number          招聘人数
salary_min      最低薪资
salary_max      最高薪资
worklocation    工作地点
jobrequirements 任职要求

releasedata     发布时间
worknature      工作性质
workbackground  工作经验
education       最低学历
positioncategory职位类别
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
            worklocation=None,jobrequirements=None, releasedata = None,worknature = None,
            workbackground = None, education = None,positioncategory = None,  jobaddress = None, companysize = None,
            companynature = None,companyindustry = None, companyhome = None, companyaddress = None
    ):
        self._spider = spider
        self._position = position
        self._company = company
        self._number = number
        self._salary = salary
        self._worklocation = worklocation
        self._jobrequirements = jobrequirements

        #暂时不用
        self._releasedata = releasedata
        self._worknature = worknature
        self._workbackground = workbackground
        self._education = education
        self._positioncategory = positioncategory
        self._jobaddress = jobaddress
        self._companysize = companysize
        self._companynature = companynature
        self._companyindustry = companyindustry
        self._companyhome = companyhome
        self._companyaddress = companyaddress

    #
    def _gen_item(self):
        item = {}
        item["position_name"] = self.filter(self._position)
        item["company_name"] = self.filter(self._company)
        item["number"] = self.filter_number(self._number)
        item["salary_min"], item["salary_max"] = self.filter_salary(self._salary)
        item["work_location"] = self.filter(self._workloction)
        item["job_requirements"] = self._jobrequirements()

        return item


    #生成组装的字段字典
    @property
    def data(self):
        return self._gen_item()

    def filter(self, temp, replace=None):
        if self._spider == "qc_job":
            return temp[1].strip() if temp else replace
        elif self._spider == "zl_job":
            return temp[0].strip() if temp else replace
        elif self._spider == "lg_job":
            return temp[0].strip() if temp else replace

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
                salary_min = 0
                salary_max = 0
        elif self._spider == "lg_job":
            if len(salary):
                salary = salary.replace("k", "000")
                salary_list = salary.split("-")
                salary_min = int(salary_list[0])
                salary_max = int(salary_list[1])
            else:
                salary_min = 0
                salary_max = 0

        return salary_min, salary_max

    def filter_number(self, number):
        if self._spider == "qc_job":
            if len(number):
                res = "".join(number).strip()
                # 找招聘人数
                index3 = res.find("聘")
                # 招聘人数
                if index3 != -1:
                    if res.find("若干") != -1:
                        number = 1
                        # print "number--", number
                    else:
                        number = res[index3 + 1:index3 + 2]
                        # print "number++", number
                else:
                    number = None
        elif self._spider == "zl_job":
            if len(number):
                number = int(number[0].strip()[:-1].encode("utf-8"))
            else:
                number = None
        elif self._spider == "lg_job":
            number = 1

        return number

    def handle_requirements_info(self, temp, replace = None):
        if len(temp):
            res = "".join(temp).strip()
            print "信息：", res
            # 找工作经验
            index = res.find("经验")
            # 找本科
            index1 = res.find("科")
            # 找大专
            index11 = res.find("专")
            # 找硕士或是博士
            index2 = res.find("士")
            # 找招聘人数
            index3 = res.find("聘")
            # 找发布时间
            index4 = res.find("发布")

            # 工作经验
            if index != -1:
                workbackground = res[:index]
                # print "workbackground--", workbackground
            else:
                workbackground = None
                # print "workbackground--", workbackground

            # 专科或是本科  硕士或是博士
            if index1 != -1:
                education = res[index1 - 1:index1 + 1]
                # print "education--", education
            elif index2 != -1:
                education = res[index2 - 1:index2 + 1]
                # print "education++", education
            elif index11 != -1:
                education = res[index11 - 1:index11 + 1]
                # print "education11", education
            else:
                education = None
                # print "education==", education

            # 招聘人数
            if index3 != -1:
                if res.find("若干") != -1:
                    number = 1
                    # print "number--", number
                else:
                    number = res[index3 + 1:index3 + 2]
                    # print "number++", number
            else:
                number = None
                # print "number==", number

            # 发布时间
            if index4 != -1:
                releasedata = res[index4 - 5:index4]
                # print "releasedata--", releasedata
            else:
                releasedata = None
                # print "releasedata++", releasedata
        else:
            return replace

        return number










