import requests
from lxml import etree
import time
from random import randint
import pandas as pd
import os
class huawei():
    number=0
    cookies={
       'cookie':'_T_WM=d3846d997c691b351a75b4606cb7a320; SUB=_2A25wt4NwDeRhGeFN6VoQ9C7Kwz-IHXVQWy04rDV6PUJbkdAKLUH9kW1NQFhynyWcVLHI7B8WRaOkJKpLQpOBZc9A; SUHB=09P9wzYhKgc9GK; SCF=AjeTxA7qxItjcl9GJ8eEiZtjhc0stdzi7J4ODu5bLblrfBN3y5WpWlB2da14NhQYvqaaBHTgb1DKtZtwpKWT15A.; SSOLoginState=1572074272'

             }

    def trys(self):
        url = "https://weibo.cn/u/2836883273?page=1"
        content = requests.get(url, cookies=self.cookies).content
        selector=etree.HTML(content)
        ids=selector.xpath('//div[@class="c"]/@id')
        id_improve=[]
        for i in ids:
            i=i[2:]
            id_improve.append(i)
        return id_improve
    def comment_page(self):
        ids=self.trys()
        users_improve_total = []
        for i in ids:
                url = "https://weibo.cn/comment/%s?uid=2836883273&rl=0#cmtfrm" % (i)
                content = requests.get(url, cookies=self.cookies).content
                selector = etree.HTML(content)
                users = selector.xpath('//body/div[@class="c"]/a/@href')
                users_improve = []
                for user in users:
                    justice = '/u/' in user
                    justices = '/u/2836883273' in user
                    if justice == False or justices == True:
                        continue
                    else:
                        if len(user) == 13:
                            user = user[3:]
                            users_improve.append(user)
                for user_improve in users_improve:
                    users_improve_total.append(user_improve)


        users_improve_total = list(dict.fromkeys(users_improve_total))
        print(users_improve_total)
        return users_improve_total

    def comment_page_try(self):
        url = 'https://weibo.cn/comment/Id9gvBaYz?uid=2836883273&rl=0#cmtfrm'
        content = requests.get(url, cookies=self.cookies).content
        selector = etree.HTML(content)
        users = selector.xpath('//body/div[@class="c"]/a/@href')
        users_improve = []
        for user in users:
            justice = '/u/' in user
            justices = '/u/2836883273' in user
            if justice == False or justices == True:
                continue
            else:
                if len(user) == 13:
                    user = user[3:]
                    users_improve.append(user)

        users_improve = list(dict.fromkeys(users_improve))
        print(users_improve)
        return users_improve

    def info(self):
        user_list = self.comment_page()
        for user in user_list:
            try:
                information_list=[]
                url = 'https://weibo.cn/%s/info' % (user)
                content = requests.get(url, cookies=self.cookies).content
                selector = etree.HTML(content)
                infos = selector.xpath('/html/body/div[6]/text()')
                for info in infos:
                    try:
                        justice = '昵称:' in info
                        justice_1 = '性别:' in info
                        justice_2 = '地区:' in info
                        if justice == True:
                            nickname = info[3:]
                        if justice_1 == True:
                            sex = info[3:]
                        if justice_2 == True:
                            address = info[3:]
                    except:print('error_1')
                information = {
                    'userid':user,
                    'nickname': nickname,
                    'sex': sex,
                    'address': address
                }
                print(information)
                information_list.append(information)
                df = pd.DataFrame(information_list)
                df.to_csv('csv.csv', mode='a', header=False)

            except:print('error_2')




d=huawei()
d.info()