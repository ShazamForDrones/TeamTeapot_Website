const sidebar = document.getElementById('sidebar');

// Expand when mouse enters
sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.add('expanded');
});

// Collapse when mouse leaves
sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.remove('expanded');
});
