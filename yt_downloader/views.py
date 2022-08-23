from django.shortcuts import render, redirect
from pytube import YouTube
from django.contrib import messages
import pathlib
import os

# Create your views here.
def home(request):
    if request.method == 'POST':
        if 'Search-url' in request.POST:
            url = request.POST.get('url')
            try:
                yt_obj = YouTube(url)
                video = yt_obj.streams.filter(progressive=True)
                return render(request, 'home.html', {'video_obj': video, 'thumbnail': yt_obj.thumbnail_url, 'url': url})
            except:
                messages.error(request, 'Invalid URL')
                return redirect('/')
            
        if 'download' in request.POST:
            url = request.POST.get('url')
            itag = request.POST.get('itag')
            context = {
                'itag': itag,
                'url': url,
            }
            return render(request, 'downloading.html', context)
        
        if 'confirm-download' in request.POST:
            url = request.POST.get('url')
            itag = request.POST.get('itag')
            if len(url) != 0 and len(itag) != 0:
                try:
                    path = pathlib.Path(pathlib.Path.home())
                    dirs = os.path.join(path, 'Downloads')
                    yt = YouTube(url)
                    yt.streams.get_by_itag(itag).download(dirs)
                    messages.success(request, 'Download successful'+str(dirs))
                    return redirect('/')
                except:
                    messages.error(request, 'Download failed')
                    return redirect('/')
        
    return render(request, 'home.html')




# if 'download' in request.POST:
#             url = request.POST.get('url')
#             itag = request.POST.get('itag')
#             if len(url) != 0 and len(itag) != 0:
#                 try:
#                     yt = YouTube(url)
#                     yt.streams.get_by_itag(itag).download()
#                     messages.success(request, 'Download successful')
#                     return redirect('/')
#                 except:
#                     messages.error(request, 'Download failed')
#                     return redirect('/')