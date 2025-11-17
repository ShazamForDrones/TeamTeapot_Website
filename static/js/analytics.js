async function loadAnalytics(){
try{
const response=await fetch('/api/analytics');
if(!response.ok){
console.error('Response not ok:', response.status);
return;
}
const data=await response.json();
if(document.getElementById('total-devices'))document.getElementById('total-devices').textContent=data.total_devices;
if(document.getElementById('active-devices'))document.getElementById('active-devices').textContent=data.active_devices;
if(document.getElementById('threats-detected'))document.getElementById('threats-detected').textContent=data.threats_detected;
if(document.getElementById('system-status'))document.getElementById('system-status').textContent=data.system_status;
if(document.getElementById('accuracy'))document.getElementById('accuracy').textContent=data.detection_accuracy.toFixed(1)+'%';
if(document.getElementById('false-positives'))document.getElementById('false-positives').textContent=data.false_positive_rate.toFixed(1)+'%';
const accuracyBar=document.getElementById('accuracy-bar');
if(accuracyBar)accuracyBar.style.width=data.detection_accuracy+'%';
const fpBar=document.getElementById('fp-bar');
if(fpBar)fpBar.style.width=data.false_positive_rate+'%';
}catch(e){
console.error('Error loading analytics:',e);
}
}

async function loadDeviceStatus(){
try{
const response=await fetch('/api/device-status');
if(!response.ok){
console.error('Response not ok:', response.status);
return;
}
const data=await response.json();
if(document.getElementById('connected-count'))document.getElementById('connected-count').textContent=data.connected;
if(document.getElementById('offline-count'))document.getElementById('offline-count').textContent=data.offline;
if(document.getElementById('pending-count'))document.getElementById('pending-count').textContent=data.pending;
}catch(e){
console.error('Error loading device status:',e);
}
}

async function loadThreats(){
try{
const response=await fetch('/api/threats');
if(!response.ok){
console.error('Response not ok:', response.status);
return;
}
const data=await response.json();
const threatsList=document.getElementById('threats-list');
if(threatsList){
if(data.threats.length===0){
threatsList.innerHTML='<p class="text-gray-400">No threats detected</p>';
return;
}
threatsList.innerHTML=data.threats.map(t=>`
<div class="bg-gray-800 rounded p-3 border-l-4 border-red-500">
<p class="text-red-400 font-bold">${t.threat_type||'Unknown Threat'}</p>
<p class="text-gray-300 text-sm">${t.description||'No description'}</p>
<p class="text-gray-500 text-xs">${new Date(t.created_at).toLocaleString()}</p>
</div>
`).join('');
}
}catch(e){
console.error('Error loading threats:',e);
}
}

document.addEventListener('DOMContentLoaded',()=>{
const analyticsTab=document.getElementById('tab-analytics');
if(analyticsTab&&!analyticsTab.classList.contains('hidden')){
loadAnalytics();
loadDeviceStatus();
loadThreats();
}
const observer=new MutationObserver((mutations)=>{
mutations.forEach((mutation)=>{
if(mutation.attributeName==='class'){
if(!analyticsTab.classList.contains('hidden')){
loadAnalytics();
loadDeviceStatus();
loadThreats();
setInterval(()=>{
loadAnalytics();
loadDeviceStatus();
loadThreats();
},30000);
}
}
});
});
if(analyticsTab){
observer.observe(analyticsTab,{attributes:true});
}
});
