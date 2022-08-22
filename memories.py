import json
import os
import requests

from multiprocessing import Pool
from time import perf_counter



def download_memory(memory):
    date = memory['Date'].replace(' ', '_').replace(':', '-')
    is_video = memory['Media Type'] == 'Video'
    url = memory['Download Link']
    filename = os.path.join('videos', date + '.mp4') if is_video else os.path.join('images/', date + '.jpg')
    
    response = requests.post(url)
    
    if response.status_code != 200:
        print('Error occured with: ' + date)
        return
    
    video_url = response.text
    
    stream = requests.get(video_url, stream = True)
    
    if os.path.exists(filename):
        print('File exists, renaming: ' + date)
        
        filename = filename[:-4] + '(1)' + filename[-4:]

    with open(filename, 'wb') as s:
        for chunk in stream.iter_content(chunk_size=1024):
            if chunk:
                s.write(chunk)
                
    print('Downloaded ' + ('video' if is_video else 'image') + ': ' + date)



def main():
    if os.path.exists('videos'):
        os.rename('videos', 'videos_old')

    if os.path.exists('images'):
        os.rename('images', 'images_old')
        

    os.mkdir('videos')
    os.mkdir('images')


    memories = []

    with open(os.path.join('json', 'memories_history.json')) as f:
        memories = json.load(f)['Saved Media']
        
    print('Memories laoded')

    starting_time = perf_counter()

    with Pool() as pool:
        pool.map(download_memory, memories)
            
    ending_time = perf_counter()

    print(f'Executed for : {(ending_time - starting_time):.2f}s')
    print(f'Downloaded {len(memories)} files')
    
    
if __name__ == '__main__':
    main()
