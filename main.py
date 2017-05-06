#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from lxml import html
import re
from config import headers

url = 'https://www.douban.com/people/3986760/rev_contacts'
res = requests.get(url, headers=headers)
print(res.content)