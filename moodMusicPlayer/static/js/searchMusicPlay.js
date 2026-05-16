document.addEventListener('DOMContentLoaded', function () {
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach((audio, index) => {
            audio.addEventListener('play', function () {
                const trackId = audio.dataset.trackId;
                console.log(`Track id ${trackId} `);
                var songSection = audio.closest('.song-section');
                if (!songSection) {
    console.warn('No parent .song-section for audio:', audio);
    return;
}
                console.log(`song section from  searchMusicPlay.js :${songSection}`);
                const imageSrc = songSection.querySelector('img').src;
                const audioSrc = audio.querySelector('source').src;
                const duration = audio.duration;
                const trackName = songSection.querySelector('h3')?.innerText || '';
                const artistName = songSection.querySelector('p:nth-of-type(1)')?.innerText.replace('Artist: ', '') || '';
                const albumName = songSection.querySelector('p:nth-of-type(2)')?.innerText.replace('Album: ', '') || '';
                const releaseDate = songSection.querySelector('p:nth-of-type(3)')?.innerText.replace('Released: ', '') || '';
                
                console.log("sending data from js searchMusicPlay: ")
                console.log({
    track_id: trackId,
    track_name: trackName,
    artist_name: artistName,
    album_name: albumName,
    releasedate: releaseDate,
    image_url: imageSrc,
    audio_url: audioSrc,
    duration: duration
});

                fetch('/trackPlayed/', {
                    method: 'POST',
                    headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                            track_id: trackId,
                            track_name: trackName,
                            artist_name: artistName,
                            album_name: albumName,
                            releasedate: releaseDate,
                            image_url: imageSrc,
                            audio_url: audioSrc,
                            duration: duration
                })
            }).then(response => response.json())
              .then(data => {
                console.log('Server response:', data)
                console.log("inside searchMusicPlay.js fetch for trackPlayed")
              })
              .catch(error => console.error('Error:', error));
        })

        
    })

    document.querySelectorAll('.bookmark-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // stop page reload

            const trackId = this.dataset.trackId;
            console.log('Bookmark response triggered');

            fetch('/bookmarkTrack/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    track_id: trackId
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log('Bookmark response:', data);

                // Optional UI change
                // const icon = this.querySelector('i');
                // icon.style.color = data.bookmarked ? '#1db954' : '#c0bfbf';
            })
            .catch(err => console.error(err));
        });
    });

});

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }