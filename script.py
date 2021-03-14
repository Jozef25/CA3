from requests import get, post
import json
from dateutil import parser
import datetime
import requests
import lxml
import os
import numpy as np
from bs4 import BeautifulSoup
import bs4


GoogleDrive = "https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"
courseid = "5"
KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"
video_titles = []
links = []



#taking url for videos
def GdriveScrape(url):
    page = requests.get(url)    
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    videos = soup.find_all('div',class_ = 'Q5txwe')
    for video in videos:
        video_titles.append(video)
        links.append(video.parent.parent.parent.parent.attrs['data-id'])
    return links,video_titles
NewLinks, newVideoTitles = GdriveScrape(GoogleDrive)

class LocalUpdateSections(object):
    def __init__(self, cid, sectionsdata):
        self.updatesections = call(
            'local_wsmanagesections_update_sections', courseid=cid, sections=sectionsdata)
            
def call(fname, **kwargs):
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = post(URL + ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

def rest_api_parameters(in_args, prefix='', out_dict=None):
    if out_dict is None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

# take folder
def FolderSystem():
    global FileSystem
    FileSystem = next(os.walk('.'))[1]
    del FileSystem[-1]  
    FileSystem.pop(0)  
    


FolderSystem()  
global directorycounter
directorycounter = 1
try:
    for x in FileSystem:
        dir_name = 'wk' + str(directorycounter)  
        if os.path.exists(dir_name) and os.path.isdir(dir_name): 
            if not os.listdir(dir_name):  
                print("Skip empty directory")
                skip = True  
                directorycounter += 1
            else:
                skip = False  
            
                htmlfile = open("wk" + str(directorycounter) + "/index.html", encoding="utf8")
                soup = BeautifulSoup(htmlfile, 'lxml')
                soup = soup.title
                title = '<h2>' + str(soup) + '</h2>'
                powerpoint = '<a href="https://mikhail-cct.github.io/ooapp/wk' + str(directorycounter) + '/">' + '<img src=/><b><h3>Powerpoint</h3></b>' + '</a> '
                video = '<a href="' + "https://drive.google.com/file/d/"+NewLinks[directorycounter-1]+"/view?usp=sharing" + '"/>< ' \
                                                                        ' /><b><h3>Recording</h3></b></a> '                                                    
                pdf = '<a href="https://github.com/mikhail-cct/ca3-test/raw/master/wk{}/wk{}.pdf"><img '
                        '/<b><h3>PDF</h3></b</a>'.format(
                    str(directorycounter),
                    str(directorycounter))
                summary = title + '<hr> ' + video + '<hr> ' + powerpoint + '<hr> ' + pdf
                data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1, 'highlight': 0,
                            'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
                
                data[0]['summary'] = summary
            
                data[0]['section'] = directorycounter
            
                sec_write = LocalUpdateSections(courseid, data)
                if not skip:
                    print( "Sent section: "  + str(directorycounter))
                directorycounter += 1
        else:
            print("There is issue")
            directorycounter += 1
except:
    print("upload error")
FolderSystem()
print(FileSystem)
