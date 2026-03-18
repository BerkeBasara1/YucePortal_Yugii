// Confetti Effects
function createConfettiEffect() {
    function createConfetti(x) {
        confetti({
            particleCount: 50,
            startVelocity: 40,
            angle: 90,
            spread: 500,
            gravity: 1,
            origin: { x, y: 0 },
            colors: ['#78faae', '#0e3a2f']
        });
    }
    for (let i = 0; i <= 1; i += 0.1) {
        createConfetti(i);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    window.addEventListener('load', function() {
        document.body.classList.remove('hidden-until-loaded');
    });
});

// DARK MODE

// Utility to add/remove .dark-mode on all relevant elements
function toggleDarkMode(enable) {
  const elems = [
    document.body,
    document.querySelector('.navbar'),
    ...document.querySelectorAll(
      '.dropdown-menu, .container, .form-control, .modal-content, ' +
      '.pagination a, .stock-box, .tabs button, .editBtn, ' +
      '.close-modal-btn, .department, .dropdown-item'
    ),
    document.getElementById('platformContainer'),
    document.getElementById('rpaPlatform'),
    document.getElementById('addFileButton')
  ];

  elems.forEach(el => {
    if (!el) return;
    el.classList[enable ? 'add' : 'remove']('dark-mode');
  });
}

// Check current hour and apply dark if between 19:00–06:00
function applyAutoTheme() {
  const hour = new Date().getHours();
  const shouldBeDark = hour >= 18|| hour < 6;
  toggleDarkMode(shouldBeDark);
  document.getElementById('darkModeToggle').checked = shouldBeDark;
}

document.addEventListener('DOMContentLoaded', () => {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const autoThemeToggle = document.getElementById('autoThemeToggle');

  // Read saved preferences
  const autoOn   = localStorage.getItem('autoThemeEnabled') === 'true';
  const manualOn = localStorage.getItem('darkMode') === 'true';

  // Initialize toggle states
  autoThemeToggle.checked = autoOn;
  darkModeToggle.checked = manualOn;

  // On page load: auto wins over manual
  if (autoOn) {
    applyAutoTheme();
  } else {
    toggleDarkMode(manualOn);
  }

  // When user toggles auto-theme
  autoThemeToggle.addEventListener('change', () => {
    const enabled = autoThemeToggle.checked;
    localStorage.setItem('autoThemeEnabled', enabled);
    if (enabled) {
      applyAutoTheme();
    }
    // If they turn it OFF, do nothing further—keep current mode
  });

  // When user toggles dark-mode manually
  darkModeToggle.addEventListener('change', () => {
    // Disable auto-mode whenever user makes a manual choice
    autoThemeToggle.checked = false;
    localStorage.setItem('autoThemeEnabled', 'false');

    const isEnabled = darkModeToggle.checked;
    toggleDarkMode(isEnabled);
    localStorage.setItem('darkMode', isEnabled);
  });
});


// HOVER USER INFO TOOLTIP
document.addEventListener('DOMContentLoaded', function () {
    const hoverElements = document.querySelectorAll('.UserOnHover');

    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', async () => {
            const username = el.dataset.username;
            if (!username) return;
        
            showUserTooltip(el, 'loading'); 
        
            try {
                const res = await fetch(`/get_user_info?username=${encodeURIComponent(username)}`);
                const data = await res.json();
        
                if (res.ok) {
                    showUserTooltip(el, `
                        <strong>${data.name}</strong><br>
                        <small>${data.department}</small><br>
                        <small>${data.title}</small>
                    `);
                } else {
                    showUserTooltip(el, 'Kullanıcı bulunamadı.');
                }
            } catch (err) {
                showUserTooltip(el, 'Hata oluştu.');
            }
        });

        el.addEventListener('mouseleave', () => {
            hideUserTooltip();
        });
    });
});

// Gerçek lazy loading: IntersectionObserver ile sadece ekrana giren resimler yüklenir.
// Eski yöntem tüm resimleri sayfa açılışında yüklüyordu.
document.addEventListener('DOMContentLoaded', function () {
  const lazyImages = document.querySelectorAll('img.lazy-photo');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const src = img.getAttribute('data-src');
          if (src) { img.src = src; img.removeAttribute('data-src'); }
          obs.unobserve(img);
        }
      });
    }, { rootMargin: '200px 0px' }); // 200px önceden yüklemeye başla

    lazyImages.forEach(img => observer.observe(img));
  } else {
    // Eski tarayıcılar için fallback
    lazyImages.forEach(img => {
      const src = img.getAttribute('data-src');
      if (src) { img.src = src; }
    });
  }
});

window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('confetti') === 'true') {
        createConfettiEffect();
        urlParams.set('confetti', 'false');
    }
}

let tooltipEl = null;
function showUserTooltip(targetElement, content) {
    if (!tooltipEl) {
        tooltipEl = document.createElement("div");
        tooltipEl.id = "user-tooltip";
        document.body.appendChild(tooltipEl);
    }

    tooltipEl.innerHTML = content === 'loading'
        ? `<div class="tooltip-spinner"></div>`
        : content;

    const rect = targetElement.getBoundingClientRect();
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = `${rect.left + window.scrollX}px`;
    tooltipEl.style.top = `${rect.bottom + window.scrollY + 5}px`;
}

function hideUserTooltip() {
    if (tooltipEl) {
        tooltipEl.style.display = 'none';
    }
}

// Jelly Effects — null guard eklendi (her sayfada .box7 olmayabilir)
const box7 = document.querySelector(".box7");
if (box7) {
  box7.addEventListener("mouseenter", () => box7.classList.add("jelly"));
  box7.addEventListener("mouseleave", () => box7.classList.remove("jelly"));
}

function showPopUpModal(message, type, callback) {
    const modal = document.getElementById('PopUpModal');
    const popUpText = modal.querySelector('#popUpText');
    const popUpIcon = modal.querySelector('#popUpIcon');

    if (modal && popUpText) {
        popUpText.innerHTML = message;

        if (type === 'alert') {
            popUpIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color: #F7B046;"></i>';
        } else if (type === 'question') {
            popUpIcon.innerHTML = '<i class="fa-regular fa-circle-question" style="color: #394748;"></i>';
        } else if (type === 'error') {
            popUpIcon.innerHTML = '<i class="fa-solid fa-xmark" style="color: #F15252;"></i>';
        } else if (type === 'check') {
            popUpIcon.innerHTML = '<i class="fa-regular fa-circle-check" style="color: #0961A1"></i>';
        }

        modal.style.display = 'flex';

        const closeButton = modal.querySelector('.btn-primary');
        const closeModal = () => {
            modal.style.display = 'none';
            document.removeEventListener('keydown', keyHandler); // clean up
            if (callback) callback();
        };

        closeButton.onclick = closeModal;

        window.onclick = function(event) {
            if (event.target === modal) {
                closeModal();
            }
        };

        // Handle Enter and Esc key presses
        function keyHandler(event) {
            if (event.key === "Enter" || event.key === "Escape") {
                closeModal();
            }
        }

        document.addEventListener('keydown', keyHandler);

    } else {
        console.error("Modal or popUpText element not found");
    }
}


function showChoicePopUpModal(message, type, callback) {
    const modal = document.getElementById('ChoicePopUpModal');
    const popUpText = modal.querySelector('#popUpText');
    const popUpIcon = modal.querySelector('#popUpIcon');
    if (modal && popUpText) {
        popUpText.innerHTML = message;

        if (type == 'alert') {
            popUpIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color: #F7B046;"></i>'
        }
        else if (type == 'question') {
            popUpIcon.innerHTML = '<i class="fa-regular fa-circle-question" style="color: #394748;"></i>'
        }
        else if (type == 'error') {
            popUpIcon.innerHTML = '<i class="fa-solid fa-xmark" style="color: #F15252;"></i>'
        }
        else if (type == 'check') {
            popUpIcon.innerHTML = '<i class="fa-regular fa-circle-check" style="color: #0961A1"></i>'
        }

        modal.style.display = 'flex';

        const confirmButton = modal.querySelector('.confirm');
        confirmButton.onclick = function() {
            modal.style.display = 'none';
            if (callback) callback();
        };

        const denyButton = modal.querySelector('.deny');
        denyButton.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    } else {
        console.error("Modal or popUpText element not found");
    }
}

function openModal(modal){
    if(!modal) return;
    modal.style.display = 'flex';          // make it part of the flow
    requestAnimationFrame(()=>{            // next paint => trigger transition
        modal.classList.add('show');
    });
}

function closeModal(modal){
    if(!modal) return;
    modal.classList.remove('show');        // start fade‑out / scale‑down
    setTimeout(()=>{ modal.style.display = 'none'; }, 300);   // tidy up
}

function triggerBubbleEffect(container) {
    for (let i = 0; i < 10; i++) {
        const bubble = document.createElement("span");
        bubble.className = "bubble";
        const size = Math.random() * 6 + 4;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        const angle = Math.random() * 2 * Math.PI;
        const distance = Math.random() * 40 + 20;
        bubble.style.setProperty('--dx', `${Math.cos(angle) * distance}px`);
        bubble.style.setProperty('--dy', `${Math.sin(angle) * distance}px`);
        container.appendChild(bubble);
        bubble.addEventListener("animationend", () => bubble.remove());
    }
}