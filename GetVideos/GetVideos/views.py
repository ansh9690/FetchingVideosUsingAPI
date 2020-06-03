import requests
from django.shortcuts import render
from django.conf import settings


# Create your views here.
def home(request):
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    videos_url = "https://www.googleapis.com/youtube/v3/videos"

    videos_list = []
    channel_params = {
        'part': 'contentDetails',
        # 'forUsername': 'TechGuyWeb',
        'id': 'UCdGQeihs84hyCssI2KuAPmA',
        'key': settings.YOUTUBE_DATA_API_KEY,
    }
    r = requests.get(channel_url, params=channel_params)
    results = r.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part': 'snippet',
        'playlistId': results,
        'maxResults': 5,
    }
    p = requests.get(playlist_url, params=playlist_params)
    results1 = p.json()['items']

    for result in results1:
        print(results)
        videos_list.append(result['snippet']['resourceId']['videoId'])

    videos_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part': 'snippet',
        'id': ','.join(videos_list)
    }

    v = requests.get(videos_url, params=videos_params)
    results2 = v.json()['items']
    videos = []
    for res in results2:
        video_data = {
            'id': res['id'],
            'title': res['snippet']['title'],
        }

        videos.append(video_data)
    print(videos)
    context = {
        'videos': videos,
    }

    return render(request, 'home.html', context)
