import json
import os
import requests

from time import time



if os.path.exists('videos'):
    os.rename('videos', 'videos_old')

if os.path.exists('images'):
    os.rename('images', 'images_old')
    

os.mkdir('videos')
os.mkdir('images')


with open(os.path.join('json', 'memories_history.json')) as f:
    memories = json.load(f)

    starting_time = time()
    
    for memory in memories['Saved Media']:
        date = memory['Date'].replace(' ', '_').replace(':', '-')
        is_video = memory['Media Type'] == 'Video'
        url = memory['Download Link']
        filename = os.path.join('videos', date + '.mp4') if is_video else os.path.join('images/', date + '.jpg')
        
        if os.path.exists(filename):
            print('File exists, renaming: ' + date)
            
            filename = filename[:-4] + '(1)' + filename[-4:]
        
        response = requests.post(url)
        
        if response.status_code != 200:
            print('Error occured with: ' + date)
            continue
        
        video_url = response.text
        
        stream = requests.get(video_url, stream = True)
    
        with open(filename, 'wb') as s:
            for chunk in stream.iter_content(chunk_size=1024):
                if chunk:
                    s.write(chunk)
                    
        print('Downloaded ' + ('video' if is_video else 'image') + ': ' + date)
            
    ending_time = time()

    print('Executed for :' + (ending_time - starting_time))
    print('Downloaded ' + memories.length + ' files')
