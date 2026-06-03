document.addEventListener('DOMContentLoaded', () => {
  // Check if touch device
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  // ─── HERO INTRO ANIMATION ───
  const introOverlay = document.getElementById('intro-overlay');

  if (introOverlay) {
    document.body.classList.add('intro-active');

    // Add glowing state after logo reveals
    setTimeout(() => {
      introOverlay.classList.add('glow-pulse');
    }, 300);

    // Automatically transition to the Hero Section after the animation completes
    setTimeout(() => {
      introOverlay.classList.add('intro-closing');
      document.body.classList.remove('intro-active');
      document.body.classList.add('intro-completed');
      
      setTimeout(() => {
        introOverlay.style.display = 'none';
      }, 800); // Allow closing transition to complete
    }, 1100); // 1.1 seconds duration
  } else {
    document.body.classList.add('intro-completed');
  }

  // ─── CUSTOM CURSOR PERFORMANCE OPTIMIZATION ───
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');

  if (!isTouchDevice && (dot || ring)) {
    let mouseX = -100;
    let mouseY = -100;
    let dotX = -100;
    let dotY = -100;
    let ringX = -100;
    let ringY = -100;
    let mouseMoved = false;
    let loopActive = false;

    // Track mouse position on move
    window.addEventListener('mousemove', e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      mouseMoved = true;
      if (!loopActive) {
        loopActive = true;
        requestAnimationFrame(updateCursor);
      }
    }, { passive: true });

    // Smooth position updates using requestAnimationFrame + translate3d (GPU accelerated)
    const updateCursor = () => {
      // Linear interpolation (lerp) for smooth lag/trailing effect
      dotX += (mouseX - dotX) * 0.25;
      dotY += (mouseY - dotY) * 0.25;
      ringX += (mouseX - ringX) * 0.12;
      ringY += (mouseY - ringY) * 0.12;

      if (dot) {
        dot.style.transform = `translate3d(${dotX}px, ${dotY}px, 0) translate(-50%, -50%)`;
      }
      if (ring) {
        ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate(-50%, -50%)`;
      }

      // Check distance to stop frame loop when idle
      const dotDist = Math.hypot(mouseX - dotX, mouseY - dotY);
      const ringDist = Math.hypot(mouseX - ringX, mouseY - ringY);

      if (dotDist < 0.15 && ringDist < 0.15 && !mouseMoved) {
        loopActive = false;
      } else {
        mouseMoved = false;
        requestAnimationFrame(updateCursor);
      }
    };

    // Initialize cursor positions instantly on first entry
    window.addEventListener('mouseenter', e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dotX = mouseX;
      dotY = mouseY;
      ringX = mouseX;
      ringY = mouseY;
      if (!loopActive) {
        loopActive = true;
        requestAnimationFrame(updateCursor);
      }
    }, { once: true });

    // Dynamic hover states using event delegation (highly optimized)
    document.addEventListener('mouseover', e => {
      const interactive = e.target.closest('a, button, input, select, textarea, .glow-card, .category-tab, [role="button"]');
      if (interactive && ring) {
        ring.classList.add('hovered');
      }
    }, { passive: true });

    document.addEventListener('mouseout', e => {
      const interactive = e.target.closest('a, button, input, select, textarea, .glow-card, .category-tab, [role="button"]');
      if (interactive && ring) {
        ring.classList.remove('hovered');
      }
    }, { passive: true });
  } else {
    // Hide cursor elements on mobile/tablet or if touch device
    if (dot) dot.style.display = 'none';
    if (ring) ring.style.display = 'none';
    document.body.style.cursor = 'auto';
  }

  // ─── OPTIMIZED SPOTLIGHT HOVER FOR CARDS ───
  if (!isTouchDevice) {
    // Cache bounding rect on mouseenter to avoid getBoundingClientRect layout thrashing on mousemove
    document.addEventListener('mouseenter', e => {
      const card = e.target.closest('.glow-card');
      if (card) {
        card._rect = card.getBoundingClientRect();
      }
    }, true); // Capture phase required as mouseenter doesn't bubble

    document.addEventListener('mousemove', e => {
      const card = e.target.closest('.glow-card');
      if (card && card._rect) {
        const x = e.clientX - card._rect.left;
        const y = e.clientY - card._rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      }
    }, { passive: true });
  }

  // ─── DYNAMIC PROJECTS SYSTEM ───
  const projectsGrid = document.getElementById('dynamic-projects');
  const searchInput = document.getElementById('project-search');
  const categoryTabs = document.querySelectorAll('.category-tab');

  if (projectsGrid && typeof projectsData !== 'undefined') {
    let currentCategory = 'all';
    let searchQuery = '';

    const renderProjects = () => {
      const filtered = projectsData.filter(proj => {
        const matchesCategory = currentCategory === 'all' || proj.category === currentCategory;
        const matchesSearch = proj.title.toLowerCase().includes(searchQuery) ||
                              proj.description.toLowerCase().includes(searchQuery) ||
                              proj.tags.some(t => t.toLowerCase().includes(searchQuery));
        return matchesCategory && matchesSearch;
      });

      if (filtered.length === 0) {
        projectsGrid.innerHTML = `
          <div style="grid-column: span 12; text-align: center; padding: 5rem 1rem; color: var(--text-muted);">
            <i class="fa-solid fa-folder-open mb-3" style="font-size: 2.5rem; opacity: 0.5;"></i>
            <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">No projects found</h4>
            <p style="font-size: 0.88rem; margin: 0;">Try adjusting your filters or search query.</p>
          </div>
        `;
        return;
      }

      projectsGrid.innerHTML = filtered.map((proj, idx) => {
        const tagHTML = proj.tags.map(t => `<span class="project-tag">${t}</span>`).join('');
        return `
          <div class="col-md-6 col-lg-4 fade-up visible" style="animation-delay: ${idx * 0.05}s;">
            <div class="glow-card bento-project" style="height: 100%; display: flex; flex-direction: column;">
              <div class="card-content d-flex flex-grow-1 flex-column">
                <div class="project-img-wrapper" style="position: relative; height: 190px; overflow: hidden; border-bottom: 1px solid var(--card-border); background: #000;">
                  <img src="${proj.image}" alt="${proj.title}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;">
                  <div style="position: absolute; top: 0.75rem; right: 0.75rem; background: rgba(5,5,8,0.75); backdrop-filter: blur(10px); padding: 0.25rem 0.65rem; border-radius: 50px; font-size: 0.7rem; border: 1px solid var(--card-border); font-weight: 600; color: var(--text-main);">
                    ${proj.category}
                  </div>
                </div>
                <div class="project-info" style="padding: 1.5rem; flex: 1; display: flex; flex-direction: column;">
                  <h4 style="margin: 0 0 0.75rem 0; font-size: 1.15rem; font-weight: 700; color: var(--text-main);">${proj.title}</h4>
                  <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
                    ${proj.description}
                  </p>
                  <div class="project-tags mb-4" style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
                    ${tagHTML}
                  </div>
                  <div style="display: flex; gap: 0.75rem; margin-top: auto;">
                    <a href="${proj.github}" class="advance-btn advance-btn-outline" style="flex: 1; font-size: 0.8rem; padding: 0.55rem 0.75rem; border-radius: 8px; justify-content: center;" target="_blank">
                      <i class="fa-brands fa-github"></i> GitHub
                    </a>
                    <a href="${proj.live}" class="advance-btn" style="flex: 1; font-size: 0.8rem; padding: 0.55rem 0.75rem; border-radius: 8px; justify-content: center; background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)); color: #fff;" target="_blank">
                      <i class="fa-solid fa-arrow-up-right-from-square"></i> Live Demo
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      }).join('');
    };

    renderProjects();

    if (searchInput) {
      searchInput.addEventListener('input', e => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderProjects();
      });
    }

    categoryTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        categoryTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentCategory = tab.dataset.category;
        renderProjects();
      });
    });
  }

  // ─── CINEMATIC SCROLL REVEAL (Intersection Observer) ───
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px', // slightly offset trigger line for better visual flow
    threshold: 0.05
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target); // Trigger once
      }
    });
  }, observerOptions);

  const fadeElements = document.querySelectorAll('.fade-up');
  fadeElements.forEach(el => observer.observe(el));
});
