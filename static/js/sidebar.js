const sidebar = document.getElementById('sidebar');
const sidebarUl = document.getElementById('sidebarUl');
let currentTab = document.getElementById('tab-dashboard');
const content = document.getElementById('content');

const tabMap = new Map();
tabMap.set("sidebarDashboard", "tab-dashboard");
tabMap.set("sidebarAnalytics", "tab-analytics");
tabMap.set("sidebarThreats", "tab-threats");
tabMap.set("sidebarDevices", "tab-devices");
tabMap.set("sidebarServers", "tab-servers");
tabMap.set("sidebarLiveMap", "tab-live-map");

// Expand when mouse enters
sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.add('expanded');
});

// Collapse when mouse leaves
sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.remove('expanded');
});

// tab nav
for (sidebarEl of sidebarUl.children) {
    sidebarEl.addEventListener('click', () => {
        console.log('woa');
        tabId = tabMap.get(sidebarEl);

        currentTab.classList.add('tab-content-hidden');
        currentTab = document.getElementById(tabId);
        currentTab.classList.remove('tab-content-hidden');
    });
};

// threats
