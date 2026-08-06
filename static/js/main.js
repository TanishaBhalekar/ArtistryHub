/**
 * ArtistryHub Theme Manager & Interactive UI Scripts
 */

const STORAGE_KEY = 'artistryhub-theme';

// Utility to get saved theme or default to 'dark'
function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY) || 'dark';
}

// Utility to apply data-theme attribute on <html> element
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
}

// Update theme toggle button UI (icon & text)
function updateToggleButton(theme) {
    const btn = document.getElementById('theme-toggle-btn');
    if (!btn) return;

    if (theme === 'light') {
        btn.innerHTML = '<i class="bi bi-sun-fill text-warning"></i> <span>Light Mode</span>';
        btn.setAttribute('aria-label', 'Switch to Dark Mode');
    } else {
        btn.innerHTML = '<i class="bi bi-moon-stars-fill text-info"></i> <span>Dark Mode</span>';
        btn.setAttribute('aria-label', 'Switch to Light Mode');
    }
}

// Main toggle function
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || getSavedTheme();
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
    updateToggleButton(nextTheme);
}

// Ensure theme attribute is set immediately on load
applyTheme(getSavedTheme());

// Wrap DOM manipulation & event listener bindings inside DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    const activeTheme = getSavedTheme();
    applyTheme(activeTheme);
    updateToggleButton(activeTheme);

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleTheme);
    }
});

// Expose globally
window.toggleTheme = toggleTheme;
