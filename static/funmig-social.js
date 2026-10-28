(function () {
    'use strict';
    var doc = document.documentElement;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia('(pointer: fine)').matches;
    doc.classList.add('fx-js');

    var header = document.querySelector('.site-header');
    var tabbar = document.querySelector('.fx-tabbar');
    var lastY = window.scrollY;
    function onScroll() {
        var y = window.scrollY;
        if (header) header.classList.toggle('fx-scrolled', y > 8);
        if (tabbar) {
            if (y > lastY + 6 && y > 200) tabbar.classList.add('fx-hide');
            else if (y < lastY - 6) tabbar.classList.remove('fx-hide');
        }
        lastY = y;
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    if (finePointer && !reduce) {
        document.addEventListener('pointermove', function (e) {
            var card = e.target.closest && e.target.closest('.post-card');
            if (!card) return;
            var r = card.getBoundingClientRect();
            card.style.setProperty('--fx-x', (e.clientX - r.left) + 'px');
            card.style.setProperty('--fx-y', (e.clientY - r.top) + 'px');
        }, { passive: true });
    }

    document.addEventListener('pointerdown', function (e) {
        if (reduce || !e.target.closest) return;
        var btn = e.target.closest('.btn-primary, .auth-form button, .pwa-btn');
        if (btn) {
            var r = btn.getBoundingClientRect();
            var size = Math.max(r.width, r.height);
            var ink = document.createElement('span');
            ink.className = 'fx-ripple';
            ink.style.width = ink.style.height = size + 'px';
            ink.style.left = (e.clientX - r.left - size / 2) + 'px';
            ink.style.top = (e.clientY - r.top - size / 2) + 'px';
            btn.appendChild(ink);
            setTimeout(function () { ink.remove(); }, 700);
        }
        var action = e.target.closest('.action-btn');
        if (action) {
            var icon = action.querySelector('img, svg') || action;
            icon.classList.remove('fx-pop');
            void icon.offsetWidth;
            icon.classList.add('fx-pop');
        }
    }, { passive: true });

    if ('IntersectionObserver' in window && !reduce) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fx-in');
                    (function (el) { setTimeout(function () { el.classList.remove('fx-reveal', 'fx-in'); }, 800); })(entry.target);
                    io.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -40px 0px', threshold: 0.06 });
        var watch = function (root) {
            (root.querySelectorAll ? root.querySelectorAll('.post-card, .card.group-card, .community-card') : []).forEach(function (el) {
                if (el.dataset.fxReveal) return;
                el.dataset.fxReveal = '1';
                var r = el.getBoundingClientRect();
                if (r.top < window.innerHeight) return; // already visible: don't hide it
                el.classList.add('fx-reveal');
                io.observe(el);
            });
        };
        watch(document);
        new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                m.addedNodes.forEach(function (n) {
                    if (n.nodeType !== 1) return;
                    if (n.matches && n.matches('.post-card')) watch(n.parentNode || document);
                    else watch(n);
                });
            });
        }).observe(document.body, { childList: true, subtree: true });
    }

    function openSearch() {
        if (typeof window.toggleSearchSection === 'function') {
            window.toggleSearchSection();
            setTimeout(function () { var i = document.getElementById('search-input'); if (i) i.focus(); }, 60);
        } else {
            window.location.href = '/search/';
        }
    }
    window.fxOpenSearch = openSearch;
    document.addEventListener('keydown', function (e) {
        var t = e.target;
        var typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
        if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) { e.preventDefault(); openSearch(); }
        else if (e.key === '/' && !typing) { e.preventDefault(); openSearch(); }
    });

    try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('compose') === '1' && typeof window.toggleMainPostSection === 'function') {
            window.addEventListener('load', function () {
                window.toggleMainPostSection();
                var box = document.getElementById('main-post-section');
                if (box) box.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
            });
        }
    } catch (err) {  }
    document.addEventListener('click', function (e) {
        var create = e.target.closest && e.target.closest('.fx-tab-create');
        if (create && typeof window.toggleMainPostSection === 'function') {
            e.preventDefault();
            window.toggleMainPostSection();
            var box = document.getElementById('main-post-section');
            if (box) box.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
        }
    });

    var bar = document.createElement('div');
    bar.className = 'fx-progress';
    document.body.appendChild(bar);
    document.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
        var a = e.target.closest && e.target.closest('a[href]');
        if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
        var href = a.getAttribute('href');
        if (!href || href.charAt(0) === '#' || href.indexOf('javascript:') === 0) return;
        if (a.origin !== window.location.origin) return;
        bar.style.opacity = '1';
        bar.style.width = '0';
        requestAnimationFrame(function () { bar.style.width = '70%'; });
    });
    window.addEventListener('pageshow', function () { bar.style.width = '0'; bar.style.opacity = '0'; });
})();
