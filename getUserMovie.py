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
        userMovies = []
        
        user_Movies_Count = re.findall(Count_pattern, movie_User_Container)[0].strip('(').strip(')')
        user_Movies_Count = int(user_Movies_Count)

        user_Movies_Page_Count = user_Movies_Count / 15
        
        if (user_Movies_Page_Count > 5):
            user_Movies_Page_Count = 5


        for each in movie_Title_Container:
            each = str(each)
            userMovies.append(self.parser_movie_info(each))

        for i in range(user_Movies_Page_Count):
            target = url + "?start=" + str((i+1)*15) + "&sort=time&rating=all&filter=all&mode=grid"
            res = requests.get(target, headers=headers)
            bsObj = BeautifulSoup(res.content, 'lxml')
            movie_Title_Container = bsObj.findAll('li', {'class': 'title'})
            for each in movie_Title_Container:
                each = str(each)
                userMovies.append(self.parser_movie_info(each))
        
        return userMovies
