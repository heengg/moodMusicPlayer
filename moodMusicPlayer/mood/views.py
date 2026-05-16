from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Moods, TrackPlayed, BookMarkedSong
from .forms import MoodsForm
from api.views import getsongView as getsongs
from api.songs import getTopArtist, mostPlayedSongs
from api.songs import fetch_songs_from_jamendo as search_songs
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.dateparse import parse_datetime

@login_required
def index(request):
    action = request.POST.get('action')
    if action == 'logout':
            logout(request)
            return redirect('login') 
    elif action == 'mood':
            form = MoodsForm(request.POST)
            if form.is_valid():
                mood_instance = form.save()
                request.session["selected_mood"] = mood_instance.type
                songs = getsongs(request,mood_instance)  
                return songs
            else:
                print("Form is not valid:", form.errors)
                return render(request, 'index.html', {
                        'form': form,
                        'error': 'Please select a valid mood.'})
    else:
        form = MoodsForm()
        return render(request, 'index.html', {'form': form})


def home(request):
    Artists = cache.get('artists')
    MostPlayedSongs = cache.get('most_played_songs')
    if not Artists:
        Artists = getTopArtist()
        cache.set('artists', Artists, timeout=900)
    if not MostPlayedSongs:
        MostPlayedSongs = mostPlayedSongs()
        cache.set('most_played_songs', MostPlayedSongs, timeout=2000)
    now_playing = request.session.get('now_playing_data')
    print("now playing from home view:", now_playing)
    if now_playing:
        played_track = now_playing
        print("played_track from home view if",played_track)

    else:
        played_track = TrackPlayed.objects.order_by('-played_at').first()
        print("played_track from view else",played_track)
    return render(request, "home.html",{ 'Artists':Artists, 'MostlyPlayed':MostPlayedSongs, 'PlayedTrack': played_track })


# @login_required
def bookmarked_song(request):
    if request.method == 'POST':
        user=request.user
        data = json.loads(request.body)
        print("data from bookmarked in view:", data)
        # track_id = data.get('track_id')

        bookmark, created = BookMarkedSong.objects.get_or_create(
            user=request.user,
            track_id=track_id,
        )
    return JsonResponse({"status": "bookmarked"})

# history of played songs
# @login_required
def recently_played(request):
    all_tracks = TrackPlayed.objects.filter(user=request.user).order_by('-played_at')
    # print("all tracks",all_tracks)
    
    for track in all_tracks:
        print("all tracks from recently_played view ")
        print(track.track_id, track.image_url, track.audio_url, track.duration)
    context = {
        'recent_tracks': all_tracks
    }
    return render(request, "recently_played.html", {"recentTracks":all_tracks})
    
@login_required
@csrf_exempt
def track_played(request):
    if request.method == 'POST':
        print("track played running (inside track_played)")
        try:
            data = json.loads(request.body)

            track_id = data.get('track_id')
            track_name = data.get('track_name')
            artist_name = data.get('artist_name')
            album_name = data.get('album_name')
            releasedate_str = data.get('releasedate')
            releasedate = parse_datetime(releasedate_str) if releasedate_str else None
            image_url = data.get('image_url')
            audio_url = data.get('audio_url')
            duration = data.get('duration') or 0.0 

            # print("track id ",  track_id)
            print("TRACK RECEIVED track_played view:", data)
            # print(f"Track Played: ID={track_id}, Image={image_url}, Audio={audio_url}, Duration={duration}")
            try:
                played_track = TrackPlayed.objects.create(
                        user = request.user,
                        track_id=track_id,
                    track_name=track_name,
                    artist_name=artist_name,
                    album_name=album_name,
                    releasedate=releasedate,
                        image_url=image_url,
                        audio_url=audio_url,
                        duration=duration
                    )
                print("track played from track_played view", played_track)
            except Exception as e:
                print("Error creating TrackPlayed:", e)
                raise
            request.session['now_playing_data'] = {
                'track_id': track_id,
                 'track_name': track_name,
                'artist_name': artist_name,
                'album_name': album_name,
                'releasedate': releasedate,
                'image_url': image_url,
                'audio_url': audio_url,
                'duration': duration,
            }
            request.session.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def search(request):
    mood = request.GET.get('mood')
    if not mood:
        return render(request, 'mood_result.html', {'error': 'No mood provided.'})
    cache_key = f'mood-_{mood.lower()}'
    music_info = cache.get(cache_key)
    
    if music_info:
        context = {'musicInfo': music_info}
        return render(request, 'mood_result.html', context)
    else:
        try:
            music_info = search_songs(mood)
            cache.set(cache_key, music_info, timeout=900)
            context = {'musicInfo': music_info}
        except Exception:
            songs = []
            return render(request, 'mood_result.html', {'error': 'no songs found.'})

    context = {'musicInfo': music_info}
    # print("Returning context:", context)
    return render(request, 'mood_result.html', context)    