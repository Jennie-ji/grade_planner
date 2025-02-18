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


