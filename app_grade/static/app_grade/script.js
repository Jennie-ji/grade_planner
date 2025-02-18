function handleTryIt() {
    alert('Try It button clicked!');
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.content-section').forEach(section => {
    observer.observe(section);
});

let audio = document.getElementById('bgMusic');

function toggleMusic() {
    if (audio.paused) {
        audio.play();
        document.querySelector('.music-icon').textContent = '🔊';
    } else {
        audio.pause();
        document.querySelector('.music-icon').textContent = '🔈';
    }
}


