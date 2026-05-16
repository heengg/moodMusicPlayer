document.addEventListener("DOMContentLoaded", function() {
  let song = document.getElementById("playingSong");
  // if (!song) {console.warn("Audio element not found!");
  //   return;}
  let progress = document.getElementById("songProgress")
  let control =  document.getElementById("controlMusic")


song.onloadedmetadata = function (){
    progress.max = song.duration;
    progress.value = song.currentTime;
}

control.addEventListener('click', playPause);
function playPause(){
    if(control.classList.contains("fa-play")){
        song.play();
        control.classList.replace("fa-play", "fa-pause");
    }
    else{
        song.pause();
        control.classList.replace("fa-pause", "fa-play");
    }
}


 function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  }

    progress.addEventListener("input", function () {
        song.currentTime = progress.value;
        progress.max = song.duration;
        document.querySelector(".musicDuration").textContent = `${formatTime(progress.value)}`
        document.querySelector(".musicMax").textContent = `${formatTime(progress.max)}`
    });

if (song.play()){
  setInterval(()=>{
    progress.value = song.currentTime;
    progress.max = song.duration;
    document.querySelector(".musicDuration").textContent = `${formatTime(progress.value)}`
    document.querySelector(".musicMax").textContent = `${formatTime(progress.max)}`
  });
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