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
Id_pattern = re.compile('href="https://www.douban.com/people/(.*?)/"')
NameImg_pattern = re.compile('<img alt="(.*?)" class="" src="(.*?)"/>')
Count_pattern = re.compile('(\d+)')

class getMovieUser:
    def __init__(self, id):
        self.id = id
    
    def parser_user_info(self, user):
        Id = re.findall(Id_pattern, user)[0]
        Name, Img = re.findall(NameImg_pattern, user)[0]
        Content = (Id, Name, Img)
        return Content

    def getUsers(self):
        url = 'https://movie.douban.com/subject/' + str(self.id) + '/collections'
        res = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(res.content, 'lxml')
        
        # Container
        movie_Count_Container = str(bsObj.findAll('span', {'id': 'collections_bar'})[0])
        movie_User_Container = bsObj.findAll('div', {'class': 'sub_ins'})[0].findAll('tr')
        movieUsers = []
        
        movie_Users_Count = re.findall(Count_pattern, movie_Count_Container)[0]
        movie_Users_Count = int(movie_Users_Count)
        
        # user_Movies_Page_Count = user_Movies_Count / 15
        
        # if (user_Movies_Page_Count > 5):
        #     user_Movies_Page_Count = 5


        for each in movie_User_Container:
            each = str(each)
            movieUsers.append(self.parser_user_info(each))

        # for i in range(user_Movies_Page_Count):
        #     target = url + "?start=" + str((i+1)*15) + "&sort=time&rating=all&filter=all&mode=grid"
        #     res = requests.get(target, headers=headers)
        #     bsObj = BeautifulSoup(res.content, 'lxml')
        #     movie_Title_Container = bsObj.findAll('li', {'class': 'title'})
        #     for each in movie_Title_Container:
        #         each = str(each)
        #         userMovies.append(self.parser_movie_info(each))
        
        return movieUsers
