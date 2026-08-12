/* ═════════════════════════════════════════════════════════════════
   Project Levity — Anti-Gravity Physics & Visual Experience
   ═════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  initHeroParticleCanvas();
  initScrollPhysics();
  initCenterOutEmergence();
  initHapticClickEffect();
  initInvisibleDetailIllumination();
  initScreensaverCanvas();
});

/* ─── 1. Zero-Gravity Hero Particle System ───────────────────── */
function initHeroParticleCanvas() {
  const canvas = document.getElementById('antigravity-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  let mouse = { x: null, y: null, radius: 180 };

  function resize() {
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
  }

  window.addEventListener('resize', resize);
  resize();

  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.4; // slow 0-G drift
      this.vy = (Math.random() - 0.5) * 0.4;
      this.radius = Math.random() * 2 + 0.5;
      this.baseAlpha = Math.random() * 0.6 + 0.2;
      this.alpha = this.baseAlpha;
      this.pulseSpeed = Math.random() * 0.02 + 0.005;
      this.pulseAngle = Math.random() * Math.PI * 2;
    }

    update() {
      // Float drift physics
      this.pulseAngle += this.pulseSpeed;
      this.alpha = this.baseAlpha + Math.sin(this.pulseAngle) * 0.25;

      // Mouse repulsion momentum
      if (mouse.x !== null && mouse.y !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          const force = (mouse.radius - dist) / mouse.radius;
          const angle = Math.atan2(dy, dx);
          this.x -= Math.cos(angle) * force * 1.5;
          this.y -= Math.sin(angle) * force * 1.5;
        }
      }

      this.x += this.vx;
      this.y += this.vy;

      // Wrap boundaries smoothly
      if (this.x < 0) this.x = width;
      if (this.x > width) this.x = 0;
      if (this.y < 0) this.y = height;
      if (this.y > height) this.y = 0;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(100, 216, 255, ${Math.max(0.1, this.alpha)})`;
      ctx.shadowBlur = this.radius * 4;
      ctx.shadowColor = '#64D8FF';
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  // Generate 80 floating stardust particles
  const particleCount = Math.min(Math.floor((width * height) / 12000), 90);
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Draw faint constellations between nearby particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 110) {
          const lineAlpha = (1 - dist / 110) * 0.12;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(100, 216, 255, ${lineAlpha})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }

    // Update & draw particles
    particles.forEach(p => {
      p.update();
      p.draw();
    });

    requestAnimationFrame(animate);
  }

  animate();
}

/* ─── 2. Antigravity Hero Scroll Physics ─────────────────────── */
function initScrollPhysics() {
  const hero = document.querySelector('.hero-levity');
  const heroContent = document.querySelector('.hero-content');
  if (!hero || !heroContent) return;

  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        const heroHeight = hero.offsetHeight;
        const progress = Math.min(1, Math.max(0, scrollY / heroHeight));

        if (progress <= 1) {
          // Subtly scale down and blur hero as drifting into deep space
          const scale = 1 - progress * 0.12;
          const blur = progress * 10;
          const opacity = 1 - progress * 1.2;

          heroContent.style.transform = `scale(${scale}) translateY(${scrollY * 0.35}px)`;
          heroContent.style.filter = `blur(${blur}px)`;
          heroContent.style.opacity = Math.max(0, opacity);
        }

        ticking = false;
      });
      ticking = true;
    }
  });
}

/* ─── 3. Center-Out Emergence Observer ──────────────────────── */
function initCenterOutEmergence() {
  const cards = document.querySelectorAll('.ceramic-card');
  if (!cards.length) return;

  const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const delay = (Array.from(cards).indexOf(card) % 3) * 150;
        setTimeout(() => {
          card.classList.add('emerged');
        }, delay);
        obs.unobserve(card);
      }
    });
  }, observerOptions);

  cards.forEach(card => observer.observe(card));
}

/* ─── 4. Haptic Click Visual Pulse Effect ────────────────────── */
function initHapticClickEffect() {
  document.addEventListener('click', (e) => {
    const target = e.target.closest('.btn-pill-glass, .ceramic-card, .stat-glass-card, .btn-pill-secondary');
    if (!target) return;

    const rect = target.getBoundingClientRect();
    const pulse = document.createElement('span');
    pulse.className = 'haptic-pulse';

    const size = Math.max(rect.width, rect.height);
    pulse.style.width = pulse.style.height = `${size}px`;
    pulse.style.left = `${e.clientX - rect.left - size / 2}px`;
    pulse.style.top = `${e.clientY - rect.top - size / 2}px`;

    target.appendChild(pulse);

    setTimeout(() => {
      pulse.remove();
    }, 600);
  });
}

/* ─── 5. The Invisible Detail: Inside Cyan Outline Illumination ─ */
function initInvisibleDetailIllumination() {
  const elements = document.querySelectorAll('.ceramic-card, .stat-glass-card, .btn-pill-glass, .nav-brand-levity');

  elements.forEach(el => {
    el.classList.add('illuminated');
    
    el.addEventListener('mouseenter', () => {
      el.classList.add('active-glow');
    });

    el.addEventListener('mouseleave', () => {
      el.classList.remove('active-glow');
    });
  });
}

/* ─── 6. Screensaver Cosmic Backdrop Canvas ──────────────────── */
function initScreensaverCanvas() {
  const canvas = document.getElementById('screensaver-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let stars = [];

  function resize() {
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
  }

  window.addEventListener('resize', resize);
  resize();

  for (let i = 0; i < 60; i++) {
    stars.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 2 + 0.5,
      alpha: Math.random() * 0.7 + 0.2,
      speed: Math.random() * 0.015 + 0.005,
      phase: Math.random() * Math.PI * 2
    });
  }

  function renderScreensaver() {
    ctx.clearRect(0, 0, width, height);

    // Deep space gradient backdrop
    const grad = ctx.createRadialGradient(
      width / 2, height / 2, 10,
      width / 2, height / 2, width * 0.6
    );
    grad.addColorStop(0, 'rgba(26, 46, 61, 0.35)');
    grad.addColorStop(0.5, 'rgba(100, 216, 255, 0.05)');
    grad.addColorStop(1, 'rgba(5, 10, 13, 0.9)');

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    // Breathing stars
    stars.forEach(s => {
      s.phase += s.speed;
      const opacity = s.alpha + Math.sin(s.phase) * 0.3;

      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(100, 216, 255, ${Math.max(0.05, opacity)})`;
      ctx.fill();
    });

    requestAnimationFrame(renderScreensaver);
  }

  renderScreensaver();
}
