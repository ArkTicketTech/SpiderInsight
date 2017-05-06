#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from lxml import html
import re
from config import headers


# get user's followers

IdName_pattern = re.compile('<a class="nbg" href="https://www.douban.com/people/(.*?)/">')
Img_pattern = re.compile('class="m_sub_img" src="(.*?)"/>')
def parser_follow_info(user):
    Id = re.findall(IdName_pattern, user)[0]
    Img = re.findall(Img_pattern, user)[0]
    Content = (Id, Img)
    return Content

url = 'https://www.douban.com/people/3986760/rev_contacts'
res = requests.get(url, headers=headers)
bsObj = BeautifulSoup(res.content, 'lxml')
user_Followers_List_Container = bsObj.findAll('dl', {'class': 'obu'})
user_Followers_Count = bsObj.findAll('span', {'class': 'count'}) # 只有人数超过单页显示范围才会有值
userFollowers = []

# print(user_Followers_Count)
# print(user_Followers_List_Container)


for each in user_Followers_List_Container:
    each = str(each)
    userFollowers.append(parser_follow_info(each))

print(userFollowers)



    

