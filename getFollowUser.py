#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from lxml import html
import re
from config import headers

# get user's followers
# [(id, avatar), ...] as userFollowers

# pattern
IdName_pattern = re.compile('<a href="https://www.douban.com/people/(.*?)/">(.*?)</a>')
Img_pattern = re.compile('class="m_sub_img" src="(.*?)"/>')
UserImg_pattern = re.compile('src="(.*?)"')
UserName_pattern = re.compile('alt="(.*?)"')
Count_pattern = re.compile('\(\d+\)')

class getFollowUser:
    def __init__(self, id, follow): # follow = 1 ? followed(rev_contact) : following(contact)
        self.id = id
        self.follow = follow
    
    def parser_follow_info(self, user):
        Id, Name = re.findall(IdName_pattern, user)[0]
        Img = re.findall(Img_pattern, user)[0]
        Content = [Id, Name, Img]
        return Content

    def getUsers(self):
        url = 'https://www.douban.com/people/' + str(self.id) + '/' + ('rev_' if self.follow else '') + 'contacts'
        res = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(res.content, 'lxml')
        
        # Container
        user_Info_Container = str(bsObj.findAll('div', {'id': 'db-usr-profile'})[0])
        user_Followers_List_Container = bsObj.findAll('dl', {'class': 'obu'})
        user_Followers_Page_Count = bsObj.findAll('span', {'class': 'count'}) # 只有人数超过单页显示范围才会有值
        userFollowers = []
        # to check whether has more pages
        user_Info_Img = re.findall(UserImg_pattern, user_Info_Container)[0]
        user_Info_Name = re.findall(UserName_pattern, user_Info_Container)[0]
        user_Followers_Count = re.findall(Count_pattern, user_Info_Container)[0].strip('(').strip(')')
        user_Followers_Count = int(user_Followers_Count)

        if (len(user_Followers_Page_Count)>0):
            user_Followers_Page_Count = user_Followers_Count / 70
        else:
            user_Followers_Page_Count = 0

        if (user_Followers_Page_Count > 2):
            user_Followers_Page_Count = 2

        userFollowers.append([self.id, user_Info_Name, user_Info_Img])

        for each in user_Followers_List_Container:
            each = str(each)
            userFollowers.append(self.parser_follow_info(each))

        for i in range(user_Followers_Page_Count):
            target = url + "?start=" + str((i+1)*70)
            res = requests.get(url, headers=headers)
            bsObj = BeautifulSoup(res.content, 'lxml')
            user_Followers_List_Container = bsObj.findAll('dl', {'class': 'obu'})
            for each in user_Followers_List_Container:
                each = str(each)
                userFollowers.append(self.parser_follow_info(each))
        
        return userFollowers
