#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import json

from flask import Flask
from flask import render_template
from flask_cors import CORS, cross_origin

from getFollowUser import getFollowUser
from getUserMovie import getUserMovie
from getMovieUser import getMovieUser

dataList = []
linksList = []

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

def process():
    uid = 'nulland'
    uname = '\xe7\x94\xbb\xe5\xa4\xa9'
    mid = '26210985'
    fu = getFollowUser(uid, 0)
    foo = fu.getUsers()
    l = 5 if len(foo) > 5 else len(foo)
    foo = random.sample(foo, l)
    print(foo)

    global dataList
    global linksList

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
    
    print(linksList)

    # um = getUserMovie(uid)
    # print(um.getMovies())

    # mu = getMovieUser(mid)
    # print(mu.getUsers())


app = Flask(__name__)
CORS(app)

@app.route('/data')
def getdata():
    global dataList, linksList
    process()
    obj = {
        "data": dataList,
        "links": linksList
    }
    return json.dumps(obj)

@app.route('/')
def hi():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()