from pathlib import Path
p=Path('/data/lapka-app/app.js')
s=p.read_text()
start=s.index("  const KEY='lapka-prototype-v1';")
end=s.index("  let route='home'", start)
replacement="""  const KEY='lapka-public-v2', OLD_KEY='lapka-prototype-v1';
  const now=new Date();
  const iso=(d)=>{const x=new Date(d);return `${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}-${String(x.getDate()).padStart(2,'0')}`};
  const addDays=(date,n)=>{const d=new Date(`${date}T12:00:00`);d.setDate(d.getDate()+n);return iso(d)};
  const today=iso(now);
  const uid=()=>Math.random().toString(36).slice(2,9);
  const esc=(v='')=>String(v).replace(/[&<>\\\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\\"':'&quot;',\"'\":'&#39;'}[c]));
  const emptyState=()=>({version:2,activePetId:null,pets:[],events:[],foodEntries:[],documents:[],photos:[],settings:{onboardingDone:false,city:'',profileVisible:false,showCity:false,showApprox:false,allowMessages:false},community:{blocked:[],requests:[],reports:[],messages:[]}});
  function loadState(){
    try{const saved=localStorage.getItem(KEY);if(saved)return {...emptyState(),...JSON.parse(saved),version:2,settings:{...emptyState().settings,...JSON.parse(saved).settings},community:{...emptyState().community,...JSON.parse(saved).community}}}catch{}
    try{const raw=localStorage.getItem(OLD_KEY);if(raw){const old=JSON.parse(raw),keepPets=(old.pets||[]).filter(x=>!x.demo),ids=new Set(keepPets.map(x=>x.id)),st=emptyState();st.pets=keepPets;st.activePetId=ids.has(old.activePetId)?old.activePetId:(keepPets[0]?.id||null);st.events=(old.events||[]).filter(x=>!x.demo&&ids.has(x.petId));st.foodEntries=(old.foodEntries||[]).filter(x=>!x.demo&&ids.has(x.petId));st.documents=(old.documents||[]).filter(x=>ids.has(x.petId));st.photos=(old.photos||[]).filter(x=>ids.has(x.petId));st.settings={...st.settings,...old.settings};st.community={...st.community,...old.community,requests:[],blocked:[]};localStorage.setItem(KEY,JSON.stringify(st));localStorage.removeItem(OLD_KEY);return st}}catch{}
    return emptyState();
  }
  let state=loadState();
  if(!Array.isArray(state.pets))state.pets=[];
  if(!state.pets.some(p=>p.id===state.activePetId))state.activePetId=state.pets[0]?.id||null;
"""
s=s[:start]+replacement+s[end:]
s=s.replace("let route='home', subroute='timeline', modal=null, toastTimer=null;","let route='home', subroute='timeline', modal=null, toastTimer=null, foodFilter='all';")
p.write_text(s)
