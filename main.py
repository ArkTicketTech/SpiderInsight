#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import json
import requests

from flask import Flask
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin

from getFollowUser import getFollowUser
from getUserMovie import getUserMovie
from getMovieUser import getMovieUser

dataList = []
linksList = []

def mdataParser(data):
    obj = {
        "name": "",
        "symbolSize": 9,
        "category": "movie",
        "draggable": "true"
    }
    obj["name"] = data[1]
    return obj

def fdataParser(data):
    obj = {
        "name": "",
        "symbolSize": 9,
        "category": "user",
        "draggable": "true",
        "img": "",
        "attr": ""
    }
    obj["img"] = data[2]
    obj["name"] = data[1]
    obj["attr"] = {}
    d = json.loads(data[3])
    if (len(d['faces'])>0):
        obj["attr"] = d['faces'][0]['attributes']
    return obj  

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

def face_detect(imgurl):
    url = 'https://v1-api.visioncloudapi.com/face/detection'
    pl = {'api_id': 'bdd94d86390c46b99879406d61b70b0f', 'api_secret': 'b59326aeaec84c9eb0d9bda89a77cf63', 'url': imgurl,'attributes':1}
    r = requests.post(url, params=pl)
    return r.content

# user's following's following
def processUUU():
    uid = 'nulland'
    mid = '26210985'
    fu = getFollowUser(uid, 0)
    foo = fu.getUsers()
    tmp = foo.pop(0)
    l = 5 if len(foo) > 5 else len(foo)
    foo = random.sample(foo, l)

    global dataList
    global linksList

    dataList = []
    linksList = []
    
    dataList.append(dataParser(tmp))
    source = tmp[1]

    for each in foo:
        each = [each[0],each[1],each[2],face_detect(each[2])]
        dataList.append(fdataParser(each))
        linksList.append(linkParser(source, each[1]))
        fu = getFollowUser(each[0], 0)
        foo = fu.getUsers()
        l = 5 if len(foo) > 5 else len(foo)
        foo = random.sample(foo, l)
        foo.pop(0)
        for child in foo:
            dataList.append(dataParser(child))
            linksList.append(linkParser(each[1], child[1]))

# user's movies' user
def processUMU():
    uid = 'nulland'
    mid = '26210985'
    um = getUserMovie(uid)
    foo = um.getMovies()
    tmp = foo.pop(0)
    l = 7 if len(foo) > 7 else len(foo)
    foo = random.sample(foo, l)

    global dataList
    global linksList

    dataList = []
    linksList = []
    
    dataList.append(dataParser(tmp))
    source = tmp[1]

    for each in foo:
        dataList.append(mdataParser(each))
        linksList.append(linkParser(source, each[1]))
        mu = getMovieUser(each[0])
        foo = mu.getUsers()
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


app = Flask(__name__)
CORS(app)

@app.route('/data')
def getdata():
    global dataList, linksList
    processUUU()
    obj = {
        "data": dataList,
        "links": linksList
    }
    return jsonify(obj)

@app.route('/mdata')
def getmdata():
    global dataList, linksList
    processUMU()
    obj = {
        "data": dataList,
        "links": linksList
    }
    return jsonify(obj)

@app.route('/')
def hi():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()