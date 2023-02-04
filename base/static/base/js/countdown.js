function secondsToDhms(seconds) {
    if (seconds < 0) {
        document.getElementById("counter").style.display = "None";
    }
    seconds = Number(seconds);
    var d = Math.floor(seconds / (3600*24));
    var h = Math.floor(seconds % (3600*24) / 3600);
    var m = Math.floor(seconds % 3600 / 60);
    var s = Math.floor(seconds % 60);
    if (d == 0) {
        document.getElementById("days").parentElement.classList.add("hidden");
        document.getElementById("seconds").parentElement.classList.remove("hidden");
    }
    document.getElementById("days").innerText = d ;
    document.getElementById("hours").innerText = h ;
    document.getElementById("mins").innerText = m ;
    document.getElementById("seconds").innerText = s ;
}

function startTimer() {
    setInterval(countdown,1000)
}

function countdown() {
    let seconds = document.getElementById('time_diff').innerText;
    document.getElementById('time_diff').innerText = seconds - 1;
    // console.log(seconds)
    secondsToDhms(seconds)
}

document.addEventListener('DOMContentLoaded', startTimer());