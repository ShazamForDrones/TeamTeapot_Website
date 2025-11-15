const sidebar = document.getElementById('sidebar');
const sidebarUl = document.getElementById('sidebarUl');
let currentTab = document.getElementById('tab-dashboard');
const content = document.getElementById('content');

const tabDashboard = document.getElementById('tab-dashboard');
const tabAnalytics = document.getElementById('tab-analytics');
const tabThreats = document.getElementById('tab-threats');
const tabDevices = document.getElementById('tab-devices');
const tabServers = document.getElementById('tab-servers');
const tabLiveMap = document.getElementById('tab-live-map');

const sidebarDashboard = document.getElementById('sidebarDashboard');
const sidebarAnalytics = document.getElementById('sidebarAnalytics');
const sidebarThreats = document.getElementById('sidebarThreats');
const sidebarDevices = document.getElementById('sidebarDevices');
const sidebarServers = document.getElementById('sidebarServers');
const sidebarLiveMap = document.getElementById('sidebarLiveMap');

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

function loadPage(newPage) {
    currentTab.classList.add('tab-content-hidden');
    currentTab = newPage;
    currentTab.classList.remove('tab-content-hidden');
};

sidebarDashboard.addEventListener('click', () => {
    loadPage(tabDashboard);
});
sidebarAnalytics.addEventListener('click', () => {
    loadPage(tabAnalytics);
});
sidebarThreats.addEventListener('click', () => {
    loadPage(tabThreats);
});
sidebarDevices.addEventListener('click', () => {
    loadPage(tabDevices);
});
sidebarServers.addEventListener('click', () => {
    loadPage(tabServers);
});
sidebarLiveMap.addEventListener('click', () => {
    loadPage(tabLiveMap);
});

// threats


