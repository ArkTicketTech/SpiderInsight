#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import random
from getFollowUser import getFollowUser
from getUserMovie import getUserMovie
from getMovieUser import getMovieUser


def dataParser(data):
    obj = {
        "name": "",
        "symbolSize": 9,
        "category": "user",
        "draggable": "true",
        "img": ""
    }
    obj["img"] = data[2]
    obj["name"] = data[1]
    return obj

def linkParser(source, target):
    obj = {
        "source": "",
        "target": ""
    }
    obj["source"] = source
    obj["target"] = target
    return obj

def main():
    uid = 'nulland'
    uname = 'nulland'
    uimg = 'https://img3.doubanio.com/icon/u1926553-164.jpg'
    mid = '26210985'
    fu = getFollowUser(uid, 0)
    foo = fu.getUsers()
    l = 5 if len(foo) > 5 else len(foo)
    foo = random.sample(foo, l)

    dataList = []
    linksList = []
    dataList.append(dataParser(foo.pop(0)))
    source = uname

    for each in foo:
        dataList.append(dataParser(each))
        linksList.append(linkParser(source, each[1]))
        fu = getFollowUser(each[0], 0)
        foo = fu.getUsers()
        l = 5 if len(foo) > 5 else len(foo)
        foo = random.sample(foo, l)
        foo.pop(0)
        for child in foo:
            dataList.append(dataParser(child))
            linksList.append(linkParser(each[1], child[1]))
         
    
    print(dataList)
    print(linksList)
        





    # um = getUserMovie(uid)
    # print(um.getMovies())

    # mu = getMovieUser(mid)
    # print(mu.getUsers())



main()
