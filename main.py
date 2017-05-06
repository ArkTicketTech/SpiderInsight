#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from lxml import html
import re
from config import headers
from getFollowUser import getFollowUser

fu = getFollowUser('nulland', 1)
print(fu.getUsers())

# # get user's followers
# # [(id, avatar), ...] as userFollowers

# # pattern
# IdName_pattern = re.compile('<a href="https://www.douban.com/people/(.*?)/">(.*?)</a>')
# Img_pattern = re.compile('class="m_sub_img" src="(.*?)"/>')
# Count_pattern = re.compile('\(\d+\)')

# def parser_follow_info(user):
#     Id, Name = re.findall(IdName_pattern, user)[0]
#     Img = re.findall(Img_pattern, user)[0]
#     Content = (Id, Name, Img)
#     return Content

# url = 'https://www.douban.com/people/nulland/rev_contacts'
# res = requests.get(url, headers=headers)
# bsObj = BeautifulSoup(res.content, 'lxml')

# # Container
# user_Info_Container = str(bsObj.findAll('div', {'class': 'info'})[0])
# user_Followers_List_Container = bsObj.findAll('dl', {'class': 'obu'})
# user_Followers_Page_Count = bsObj.findAll('span', {'class': 'count'}) # 只有人数超过单页显示范围才会有值
# userFollowers = []
# # to check whether has more pages

# user_Followers_Count = re.findall(Count_pattern, user_Info_Container)[0].strip('(').strip(')')
# user_Followers_Count = int(user_Followers_Count)

# if (len(user_Followers_Page_Count)>0):
#     user_Followers_Page_Count = user_Followers_Count / 70
# else:
#     user_Followers_Page_Count = 0

# if (user_Followers_Page_Count > 5):
#     user_Followers_Page_Count = 5


# for each in user_Followers_List_Container:
#     each = str(each)
#     userFollowers.append(parser_follow_info(each))

# for i in range(user_Followers_Page_Count):
#     target = url + "?start=" + str((i+1)*70)
#     res = requests.get(url, headers=headers)
#     bsObj = BeautifulSoup(res.content, 'lxml')
#     user_Followers_List_Container = bsObj.findAll('dl', {'class': 'obu'})
#     for each in user_Followers_List_Container:
#         each = str(each)
#         userFollowers.append(parser_follow_info(each))

# print(userFollowers)



    

