/* ============================================
   GuLIN AI - JavaScript
   Agente Inteligente Autónomo de TI
   ============================================ */

// Navbar scroll
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.pageYOffset > 50);
});

// Mobile menu
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.querySelector('.nav-links');
const navActions = document.querySelector('.nav-actions');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navLinks.classList.toggle('active');
    navActions.classList.toggle('active');
});

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navLinks.classList.remove('active');
        navActions.classList.remove('active');
    });
});

// Active nav link
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const top = section.offsetTop - 100;
        const height = section.clientHeight;
        if (pageYOffset >= top && pageYOffset < top + height) {
            current = section.getAttribute('id');
        }
    });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
    });
});

// ============================================
// Roles Tabs
// ============================================
const roleTabs = document.querySelectorAll('.role-tab');
const roleContents = document.querySelectorAll('.role-content');

roleTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active from all tabs
        roleTabs.forEach(t => t.classList.remove('active'));
        // Add active to clicked tab
        tab.classList.add('active');
        
        // Hide all content
        roleContents.forEach(c => c.classList.remove('active'));
        // Show selected content
        const role = tab.dataset.role;
        document.getElementById(`role-${role}`).classList.add('active');
    });
});

// ============================================
// FAQ Accordion
// ============================================
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close all
        faqItems.forEach(i => i.classList.remove('active'));
        
        // Toggle current
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// ============================================
// ROI Calculator
// ============================================
const teamSize = document.getElementById('teamSize');
const incidents = document.getElementById('incidents');
const hourlyRate = document.getElementById('hourlyRate');

const teamSizeValue = document.getElementById('teamSizeValue');
const incidentsValue = document.getElementById('incidentsValue');
const hourlyRateValue = document.getElementById('hourlyRateValue');
const hoursSaved = document.getElementById('hoursSaved');
const moneySaved = document.getElementById('moneySaved');

function calculateROI() {
    const team = parseInt(teamSize.value);
    const inc = parseInt(incidents.value);
    const rate = parseInt(hourlyRate.value);
    
    // Update display values
    teamSizeValue.textContent = `${team} ingenieros`;
    incidentsValue.textContent = `${inc} incidentes`;
    hourlyRateValue.textContent = `USD $${rate}/hr`;
    
    // Calculate: Assuming 40% MTTR reduction
    // Average incident resolution: 4 hours
    // Time saved per incident: 4 * 0.4 = 1.6 hours
    // Monthly time saved: incidents * 1.6
    // Annual time saved: monthly * 12
    const hoursPerIncident = 4;
    const reductionFactor = 0.4;
    const monthlyHoursSaved = inc * hoursPerIncident * reductionFactor;
    const annualHoursSaved = Math.round(monthlyHoursSaved * 12);
    const annualMoneySaved = annualHoursSaved * rate;
    
    hoursSaved.textContent = annualHoursSaved.toLocaleString();
    moneySaved.textContent = `$${annualMoneySaved.toLocaleString()}`;
}

teamSize.addEventListener('input', calculateROI);
incidents.addEventListener('input', calculateROI);
hourlyRate.addEventListener('input', calculateROI);

// Initial calculation
calculateROI();

// ============================================
// Modal
// ============================================
function openModal() {
    document.getElementById('authModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('authModal').classList.remove('active');
    document.body.style.overflow = '';
}

document.getElementById('authModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closeModal();
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
});

// Auth form
function handleAuth(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button[type="submit"]');
    
    btn.textContent = '';
    btn.classList.add('loading');

    setTimeout(() => {
        btn.classList.remove('loading');
        btn.innerHTML = '✓ Solicitud enviada';
        btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';

        setTimeout(() => {
            closeModal();
            event.target.reset();
            btn.innerHTML = 'Solicitar Demo <i class="fas fa-arrow-right"></i>';
            btn.style.background = '';
            showNotification('Te contactaremos pronto');
        }, 1500);
    }, 2000);
}

// Loading & Shake styles
const extraStyles = document.createElement('style');
extraStyles.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-4px); }
        40%, 80% { transform: translateX(4px); }
    }
    .btn.loading {
        position: relative;
        color: transparent;
        pointer-events: none;
    }
    .btn.loading::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255,255,255,0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.6s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(extraStyles);

// Notification
function showNotification(message) {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notif = document.createElement('div');
    notif.className = 'notification';
    notif.innerHTML = `
        <div class="notif-icon"><i class="fas fa-check-circle"></i></div>
        <span>${message}</span>
    `;
    document.body.appendChild(notif);

    const style = document.createElement('style');
    style.id = 'notif-style';
    if (!document.getElementById('notif-style')) {
        style.textContent = `
            .notification {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 1rem 1.5rem;
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 12px;
                box-shadow: var(--shadow);
                z-index: 3000;
                animation: notifIn 0.4s ease, notifOut 0.4s ease 2.6s forwards;
                font-size: 0.9rem;
                font-weight: 500;
            }
            .notif-icon {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 0.9rem;
                flex-shrink: 0;
            }
            @keyframes notifIn {
                from { transform: translateX(100px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes notifOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100px); opacity: 0; }
            }
            @media (max-width: 768px) {
                .notification {
                    left: 1rem;
                    right: 1rem;
                    bottom: 1rem;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setTimeout(() => notif.remove(), 3000);
}

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.problem-card, .role-content, .security-card, .impact-card, .faq-item, .section-header').forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
});

// ============================================
// Theme Toggle (Oscuro / Claro)
// ============================================
function toggleTheme() {
    const body = document.body;
    const icon = document.querySelector('#themeToggle i');
    const isLight = body.classList.toggle('light-mode');
    
    if (isLight) {
        icon.className = 'fas fa-sun';
        localStorage.setItem('gulin-theme', 'light');
    } else {
        icon.className = 'fas fa-moon';
        localStorage.setItem('gulin-theme', 'dark');
    }
}

// Cargar tema guardado o detectar preferencia del sistema
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('gulin-theme');
    const icon = document.querySelector('#themeToggle i');
    
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        if (icon) icon.className = 'fas fa-sun';
    } else if (savedTheme === 'dark') {
        document.body.classList.remove('light-mode');
        if (icon) icon.className = 'fas fa-moon';
    } else {
        // Detectar preferencia del sistema
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (prefersLight) {
            document.body.classList.add('light-mode');
            if (icon) icon.className = 'fas fa-sun';
        }
    }
});

// Console branding
console.log('%c GuLIN AI Agent ', 'background: linear-gradient(135deg, #8b5cf6, #6366f1); color: white; font-size: 18px; font-weight: bold; padding: 8px 16px; border-radius: 8px;');
console.log('%c Inteligencia Autónoma para TI Empresarial', 'color: #94a3b8; font-size: 13px;');

document.addEventListener('DOMContentLoaded', () => {
    console.log('⚡ GuLIN AI Agent - Inicializado');
});
