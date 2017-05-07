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
Id_pattern = re.compile('href="https://movie.douban.com/subject/(.*?)/"')
Name_pattern = re.compile('\<em\>(.*?)\</em>')
Count_pattern = re.compile('\(\d+\)')
UserName_pattern = re.compile('<h1>(.*?)看过的电影')
UserPic_pattern = re.compile('src="(.*?)"')

class getUserMovie:
    def __init__(self, id):
        self.id = id
    
    def parser_movie_info(self, title):
        Id = re.findall(Id_pattern, title)[0]
        Name = re.findall(Name_pattern, title)[0]
        Content = (Id, Name)
        return Content

    def getMovies(self):
        url = 'https://movie.douban.com/people/' + str(self.id) + '/collect'
        res = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(res.content, 'lxml')
        
        # Container
        movie_Title_Container = bsObj.findAll('li', {'class': 'title'})
        movie_User_Container = str(bsObj.findAll('div', {'id': 'db-usr-profile'})[0])
        movie_UserPic_Container = str(bsObj.findAll('div', {'id': 'db-usr-profile'})[0].findAll('div', {'class': 'pic'})[0])
        userMovies = []
        
        user_Movies_Count = re.findall(Count_pattern, movie_User_Container)[0].strip('(').strip(')')
        user_Movies_Count = int(user_Movies_Count)

        user_Name = re.findall(UserName_pattern, movie_User_Container)[0]
        user_Pic = re.findall(UserPic_pattern, movie_UserPic_Container)[0]

        user_Movies_Page_Count = user_Movies_Count / 15
        if (user_Movies_Page_Count > 2):
            user_Movies_Page_Count = 2

        userMovies.append((self.id, user_Name, user_Pic))
        for each in movie_Title_Container:
            each = str(each)
            userMovies.append(self.parser_movie_info(each))

        print(userMovies)

        for i in range(user_Movies_Page_Count):
            target = url + "?start=" + str((i+1)*15) + "&sort=time&rating=all&filter=all&mode=grid"
            res = requests.get(target, headers=headers)
            bsObj = BeautifulSoup(res.content, 'lxml')
            movie_Title_Container = bsObj.findAll('li', {'class': 'title'})
            for each in movie_Title_Container:
                each = str(each)
                userMovies.append(self.parser_movie_info(each))
        
        return userMovies
