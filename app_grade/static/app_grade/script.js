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
<<<<<<< HEAD

function toggleMusic() {
    if (audio.paused) {
        audio.play();
        document.querySelector('.music-icon').textContent = '🔊';
    } else {
        audio.pause();
        document.querySelector('.music-icon').textContent = '🔈';
    }
}

const tabButtons = document.querySelectorAll('.tab_btn');
const line = document.querySelector('.line');
let activeIndex = 0;

tabButtons.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        document.querySelector('.tab_btn.active').classList.remove('active');
        btn.classList.add('active');
        line.style.left = `calc(20% * ${index})`;
        activeIndex = index;
    });
});

// Initialize line position
line.style.left = `calc(20% * ${activeIndex})`;


=======
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
>>>>>>> 9c3f7592d7063574d22b40c478e3643e45492956
