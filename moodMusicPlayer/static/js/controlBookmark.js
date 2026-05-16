document.addEventListener("DOMContentLoaded", function() {
    console.log("Bookmark js file activated")
  let bookmarks = document.querySelectorAll(".songBookmark");
bookmarks.forEach(bookmark => {
bookmark.addEventListener('click', function()
  {
    bookMarkSong(this);
  });
});

function bookMarkSong(bookmark){
  // const trackId = "{{ PlayedTrack}}";
  const trackId = bookmark.dataset.playedTrackId;  
  if (!trackId) {
    console.warn("No track ID found, skipping bookmark");
    return;
  }
  console.log("Track ID:", trackId);

  console.log("track id from bookmark")
  console.log("This is being sent from template :")
  console.log(trackId)

    const data = {
        track_id: trackId,
    };
    console.log("data from control play js bookmark")
    console.log("before bookmark change")
    
    if(bookmark.classList.contains("fa-regular")){
      bookmark.classList.replace("fa-regular", "fa-solid");
      console.log("before change")
    fetch('/bookmarked/', {
              method: 'POST',
              headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify(data)
        }).then(response => response.json())
              .then(data =>{
                console.log('Server response:', data)
                console.log("this is inside fetch")
              } 
            )
              .catch(error => console.error('Error:', error))
      }
      else{
        bookmark.classList.replace("fa-solid", "fa-regular");
        console.log("inside else of bookmark icon change")
      }
      console.log("after bookmark change")
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

});