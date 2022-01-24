import os
import sys

# os.system('mkdir played-matches')
# os.system('mkdir back-up')
# os.system('mkdir weekly-update')

try:
    import requests
except:
    print('requests')

    os.system('pip install requests')

try:
    import bs4
except:
    print('bs4')
    os.system('pip install bs4')

try:
    import selenium
except:
    print('selenium')
    os.system('pip install selenium')

try:
    import pandas
except:
    print('pandas')
    os.system('pip install pandas')

try:
    import numpy
except:
    print('numpy')
    os.system('pip install numpy')

try:
    import random
except:
    print('random')
    os.system('pip install random')

try:
    import sqlite3
except:
    print('sql')
    os.system('pip install sqlite3')

try:
    import re
except:
    print('re')
    os.system('pip install re')
