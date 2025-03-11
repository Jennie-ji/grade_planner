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
audio.autoplay = false;

    window.addEventListener('load', function() {
        let isPlaying = localStorage.getItem('isPlaying');
        if (isPlaying === 'true') {
            audio.play();
            document.querySelector('.music-icon').textContent = '🔊';
        } else {
            audio.pause();
            document.querySelector('.music-icon').textContent = '🔈';
        }
    });

    function toggleMusic() {
        if (audio.paused) {
            audio.play();
            document.querySelector('.music-icon').textContent = '🔊';
            localStorage.setItem('isPlaying', 'true');
        } else {
            audio.pause();
            document.querySelector('.music-icon').textContent = '🔈';
            localStorage.setItem('isPlaying', 'false');
        }
    }
