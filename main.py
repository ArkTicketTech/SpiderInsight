#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from getFollowUser import getFollowUser
from getUserMovie import getUserMovie
from getMovieUser import getMovieUser

def main():
    uid = 'nulland'
    mid = '26210985'
    # fu = getFollowUser(uid, 1)
    # print(fu.getUsers())

    # um = getUserMovie(uid)
    # print(um.getMovies())

    mu = getMovieUser(mid)
    print(mu.getUsers())



main()
