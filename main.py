#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from getFollowUser import getFollowUser

def main():
    name = 'nulland'
    fu = getFollowUser(name, 1)
    print(fu.getUsers())

main()
