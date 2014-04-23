#! /usr/bin/env python
# -*- coding: utf-8 -*-


import re
import sys
import time
import datetime
import urllib
import urllib2
import cookielib
#from common.constant import *

class Singleton(object):
    class __Singleton:
        def __init__(self):
            self.val = None
            
    def __str__(self):
        return `self` + self.val
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Singleton.instance:
            Singleton.instance = Singleton.__Singleton()
        return Singleton.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

singleton = Singleton()

"""Common utilities for project, Unrelated business."""
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):   
    """Handle the redirect response when return the HTTP code of 301, 302."""
    def http_error_301(cls, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(cls, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       

    def http_error_302(cls, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_302(cls, req, fp, code, msg, headers)              
        result.status = code      
        return result   


def cur_time_with_format():
    """Return the formated time with format of '[YYYY-MM-DD HH:MM:SS]'."""
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

def encode_str(str, format=None):
    """Format the string with coded.
    
    Arguments:
    
    str - string to code. 
    format - the coding format you want. Default is the system coding.
    """
    if format:
        return str.decode('UTF-8').encode(format) 
    else:
        return str.decode('UTF-8').encode(sys.getfilesystemencoding()) 

def search_text(pattern, src_str, group_match=False, multiline=True):
    '''Search text with the regular expression.
    
    If the group_match argument was true which the result of tuple consist of 
    one or more than one lists.
    
    Arguments:
    
    pattern - regular pattern
    src_str - the string to find within pattern
    group_match - whether search used group
    multiline - search in multi-line mode
    '''
    result_list = list()
 
    if multiline:
        match_list = list(re.finditer(pattern, src_str, re.S))
    else:
        match_list = list(re.finditer(pattern, src_str))
    if len(match_list) > 0:
        for match in match_list:
            if not group_match:
                result_list.append(match.group())
            else:
                tmp_list = list()
                for index in range(get_group_size(pattern)):
                    tmp_list.append(match.group(index + 1))
                    pass
                result_list.append(tmp_list)
    return tuple(result_list)

def get_group_size(src_str):
    '''Count no leading backslash parenthesis of the pattern.
    
     Arguments:
     
     src_str - the pattern
     '''
    pattern = '(\\\\)?\('
    count = 0 
    for match in re.finditer(pattern, src_str):
        if not match.group(0).startswith('\\'):
            count = count + 1
    return count

def get_proxies():
    proxies= {'http':'http://proxy.jpn.hp.com:8080'}
    return urllib2.ProxyHandler(proxies)

def get_cookie():
    cookies = cookielib.CookieJar()
    return urllib2.HTTPCookieProcessor(cookies)

def trim_str(str):
    """Remove both sides of non-word character of the string"""
    return str.lstrip().rstrip()

def get_opener(proxy=False):
    if not singleton.val:
        if proxy:
            singleton.val = urllib2.build_opener(get_cookie(), SmartRedirectHandler(), get_proxies())
        else:
            singleton.val = urllib2.build_opener(get_cookie(), SmartRedirectHandler())
        singleton.val.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]
        
    return singleton.val
    
def get_verify(page_content):
    verify = search_text('g_verify\s?=\s?\"([^\"]*)\"', page_content, True)

    if len(verify) > 0:
        return unicode(verify[0][0])
    else:
        return None

def read_page(appand_url, method='GET', data=None):
    
    timeout_sec = 20
    sleep_count = 0
    sleep_per_sec = 1
    
    opener = get_opener()
    
    '''Request the specified address from cookies to get the page content.'''
    #url = urllib.basejoin(address, appand_url)
    url=appand_url
    if method == 'GET':
        request = urllib2.Request(url)
    elif method == 'POST':
        request = urllib2.Request(url, urllib.urlencode(data))
        
    f = opener.open(request)
    while True:
        indexStr = f.read()
        if len(indexStr) != 0:
            break;
        
        # TODO timeout read from conf
        time.sleep(sleep_per_sec);
        if sleep_per_sec * sleep_count > timeout_sec:
            break;
    
    return indexStr

def test():
    x = Singleton()
    x.val = None
    print x
    y = Singleton()
    y.val = 'eggs'
    print y
    z = Singleton()
    z.val = 'spam'
    print z.val
    print x
    print y
    pass

if __name__ == '__main__':
    test()
    

    
