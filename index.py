#!/usr/bin/env python
# coding:utf-8
from signage import SignageDb
import random
import urllib.parse
import base64
import fcntl

VIDEO_PATH = '/var/nginx/'
VIDEO_FILE = VIDEO_PATH + 'out.jpg'
VIDEO_LOCK_FILE = VIDEO_PATH + 'lock'

ad_list = ['Ma-l2QCtjpM','GKQGJ9CjUZk', 'KNST_AtBb8I', 'O6moWDnQRms']

def get_next_ad_random():
    print('get_next_ad_random() is called')
    index = random.randrange(3)
    next_ad = ad_list[index]
    db = SignageDb()
    db.write_ad(next_ad)
    db.commit()
    db.close()
    return next_ad

def get_next_ad_fixed():
    print('get_next_ad_fixed() is called')
    return 'not_implemented'

def get_next_ad_learning():
    print('get_next_ad_learning() is called')
    db = SignageDb()
    try:
        id1, date1, gender, age = db.read_last('age_gender')
    except TypeError:
        db.close()
        return 'no_age_gender'

    try:
        id2, date2, m_0, f_0, m_1, f_1, m_2, f_2 = db.read_last('rule')
    except TypeError:
        db.close()
        return 'no_rule'

    if gender == 'M' and age == 0:
        next_ad =  m_0
    elif gender == 'M' and age == 1:
        next_ad =  m_1
    elif gender == 'M' and age == 2:
        next_ad =  m_2
    elif gender == 'F' and age == 0:
        next_ad =  f_0
    elif gender == 'F' and age == 1:
        next_ad =  f_1
    elif gender == 'F' and age == 2:
        next_ad =  f_2
    else:
        pass

    db.write_ad(next_ad)
    db.commit()
    db.close()
    return next_ad

def top(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])
    return b'Python app is successfully running'

def getNextVideo(env, start_response):
    print('getNextVideo() is called')
    query = urllib.parse.parse_qs(env['QUERY_STRING'])
    mode = query['mode'][0]
    next_ad = None
    if mode == 'random':
        next_ad = get_next_ad_random()
    elif mode == 'fixed':
        next_ad = get_next_ad_fixed()
    elif mode == 'learning':
        next_ad = get_next_ad_learning()
    else:
        pass

    print("mode=", mode, ",  next_video=", next_ad)
    start_response('200 OK', [('Content-Type','text/plain')])
    return next_ad.encode()

def dbInitialize(env, start_response):
    print('dbInitialize() is called')
    db = SignageDb()
    db.delete_tables()
    db.close()
    start_response('200 OK', [('Content-Type','text/plain')])
    return b'Create DB Succeed'

def getAgeGender(env, start_response):
    print('getAgeGender() is called')
    db = SignageDb()
    try:
        id1, date1, gender, age = db.read_last('age_gender')
        if gender == 'F':
            age_gender = 'Female/'
        elif gender == 'M':   
            age_gender = 'Female/'
        else:
            age_gender = '?/'

        if age == 0:
            age_gender = age_gender + 'Junior'
        elif age == 1:   
            age_gender = age_gender + 'Middle'
        elif age == 2:   
            age_gender = age_gender + 'Seniror'
        else:
            age_gender = age_gender + '?'
    except TypeError:
        age_gender = '-'

    db.close()
    start_response('200 OK', [('Content-Type','text/plain')])
    return age_gender.encode()

def getRating(env, start_response):
    print('getRating() is called')
    db = SignageDb()
    try:
        id, date, rating, dwell, watch = db.read_last('rating')
        rating = str(date) + '   [Rating] ' + str(rating) + '    [Dwell] ' + str(dwell) + '    [Watch] ' + str(watch);
    except TypeError:
        rating = '-'
    
    db.close()
    start_response('200 OK', [('Content-Type','text/plain')])
    return rating.encode()

def getRule(env, start_response):
    print('getRule() is called')
    db = SignageDb()
    try:
        id, date, m_0, f_0, m_1, f_1, m_2, f_2 = db.read_last('rule')
        rule = str(date) + '<br> ' + '   [Male/Junior] ' + str(m_0) + '    [Female/Junior] ' + str(f_0) + '    [Male/Middle] ' + str(m_1) + '   [Female/Middle] ' + str(f_1) + '   [Male/Senior] ' + str(m_2) + '   [Female/Senior] ' + str(f_2);
    except TypeError:
        rule = '-'
    
    db.close()
    start_response('200 OK', [('Content-Type','text/plain')])
    return rule.encode()

def postVideo(env, start_response):
    print('postVideo() is called')

    lock = open(VIDEO_LOCK_FILE, 'r+')

    body= ''  # b'' for consistency on Python 3.0
    try:
        length= int(env.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length= 0

    if length!=0:
        body= base64.b64decode(env['wsgi.input'].read(length))
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('lock')
        fd = open(VIDEO_FILE, 'wb+')
        fd.write(body)
        fd.close()
        fcntl.flock(lock, fcntl.LOCK_UN)
        print('unlock')

    
    start_response('200 OK', [('Content-Type','text/plain')])
    return b'get video'

def NotFound(env, start_response):
    start_response('404 Not Found', [('Content-Type','text/plain')])
    return b'not found'

def application(env, start_response):
    routes = {
            '/uwsgi/':top,
            '/uwsgi/get_next_video':getNextVideo,
            '/uwsgi/db_initialize':dbInitialize,
            '/uwsgi/get_age_gender':getAgeGender,
            '/uwsgi/get_rating':getRating,
            '/uwsgi/get_rule':getRule,
            '/uwsgi/post_video':postVideo,
    }
    return routes.get(env.get('PATH_INFO'), NotFound)(env, start_response)

