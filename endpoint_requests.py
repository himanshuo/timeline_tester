#from django.test import TestCase
from unittest import TestCase

__author__ = 'himanshu'

#from osf.models import Timeline,History

import requests
import urllib
import datetime
import time
from datetime import tzinfo
import calendar
#--data "csrfmiddlewaretoken=QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1
# &_content_type=application%2Fx-www-form-urlencoded
# &_content=author%3Da2%26wiki%3Dw2%26project_id%3D2%26date%3D09-21-2014"
#
#
# http://localhost:8000/update_project/



def create_project(project_id, date, title, wiki, author, port):
    payload = {'project_id': project_id, 'date': date,'title':title, 'wiki':wiki, 'author':author}
    payload = urllib.urlencode(payload) # date=09-20-2014&wiki=w1&project_id=3&author=a1&title=t1   ???correct????

    #print payload
    data = {'csrfmiddlewaretoken':'QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1',
            '_content_type':'application/x-www-form-urlencoded',
            '_content': payload}#after application, not sure if %2F or /
    r = requests.post('http://localhost:'+str(port)+'/create_new_project/', data=data)
    #returns a list? can you turn it into json?
    #print r.status_code
    ret=r.json()
    if ret[str(project_id)] == "Project Created." and r.status_code < 300:
        ret[project_id] = "Project Created."
        del ret[str(project_id)]
        return ret
    return ret


def get_project(project_id,port, date=None, ):
    if date is None:
        payload = {'project_id': project_id}
        r = requests.get('http://localhost:'+str(port)+'/project_detail/', params=payload)
        if r.status_code<300:
            return r.json()
        else:
            return {project_id:"status code was not 2xx"}
    else:
        payload = {'project_id': project_id, 'date': date}
        r = requests.get('http://localhost:'+str(port)+'/project_detail/', params=payload)
        if r.status_code<300:
            return r.json()
        else:
            return {project_id:"status code was not 2xx"}





def update_project(project_id, date, port, title=None, wiki=None, author=None):
    #buid payload
    payload=dict()
    payload['project_id']= project_id
    payload['date']= date
    if title is not None:
        payload['title']=title
    if wiki is not None:
        payload['wiki']=wiki
    if author is not None:
        payload['author']=author

    payload = urllib.urlencode(payload) # date=09-20-2014&wiki=w1&project_id=3&author=a1&title=t1   ???correct????

    #print payload
    data = {'csrfmiddlewaretoken':'QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1',
            '_content_type':'application/x-www-form-urlencoded',
            '_content': payload}#after application, not sure if %2F or /
    r = requests.post('http://localhost:'+str(port)+'/update_project/', data=data)
    ret= r.json()
    if ret[str(project_id)] == "Project Updated." and r.status_code < 300:
        ret[project_id] = "Project Updated."
        del ret[str(project_id)]
        return ret
    return ret


def delete_project(project_id, port):
#csrfmiddlewaretoken=zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP&_method=DELETE
    payload={'project_id':int(project_id)}
    payload = urllib.urlencode(payload)
    data = {'csrfmiddlewaretoken':'zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP',
            '_method':'DELETE',
            'project_id': int(project_id)}#after application, not sure if %2F or /
    r = requests.delete('http://localhost:'+str(port)+'/delete_project/', data=data)

def delete_all_projects_in_range(start, end, port):
    for i in range(start, end):
        delete_project(i, port)

def delete_all_projects(port):
    payload={}
    payload = urllib.urlencode(payload)
    data = {'csrfmiddlewaretoken':'zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP',
            '_method':'DELETE'}
    r = requests.delete('http://localhost:'+str(port)+'/delete_all_projects/', data=data)



#can make more complex.
def convert_utc_format(month, day, year):
    #2014-09-20T00:00:00
    return year+"-"+month+"-"+day+"T"+"00:00:00"


#to get the avg time easier
def determine_avg_time(list_of_times, num_times):
    return str(float(sum(list_of_times))/float(num_times))
