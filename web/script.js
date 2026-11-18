const N=6, PARS=[2,2,5,5,9,5,5,3,3,3,3,3,3,4,4,4,4,5,7,7];
const LEVELS=[[[2,1,2,"h"],[1,1,2,"h"],[4,3,2,"v"],[2,4,2,"v"]],[[2,0,2,"h"],[5,3,3,"h"],[2,3,3,"v"],[4,0,2,"h"],[1,4,2,"v"],[2,2,2,"v"]],[[2,0,2,"h"],[3,0,3,"h"],[4,2,2,"v"],[4,0,2,"h"],[0,3,2,"v"],[5,3,3,"h"],[1,4,3,"v"],[1,5,3,"v"]],[[2,0,2,"h"],[1,4,3,"v"],[4,1,2,"v"],[4,2,2,"v"],[1,5,3,"v"],[0,2,3,"h"],[3,0,3,"h"],[5,3,2,"h"],[1,0,2,"h"]],[[2,1,2,"h"],[4,2,2,"v"],[0,0,3,"v"],[3,0,3,"h"],[0,5,3,"v"],[4,3,3,"h"],[5,0,2,"h"],[0,4,3,"v"],[1,1,2,"h"],[5,4,2,"h"]],[[2,1,2,"h"],[5,4,2,"h"],[4,2,2,"v"],[1,4,3,"v"],[1,5,2,"v"],[3,1,3,"h"],[1,2,2,"h"],[1,0,3,"v"],[0,3,3,"h"],[0,1,2,"v"],[4,3,2,"h"]],[[2,0,2,"h"],[3,0,2,"v"],[0,4,3,"v"],[3,5,2,"v"],[4,2,2,"h"],[0,1,3,"h"],[4,1,2,"v"],[2,2,2,"v"],[1,5,2,"v"],[1,3,2,"v"],[3,3,2,"h"]],[[2,0,2,"h"],[3,3,3,"v"],[4,0,3,"h"],[1,3,2,"h"],[4,5,2,"v"],[1,2,2,"v"],[0,4,2,"h"],[4,4,2,"v"],[0,0,2,"v"],[3,1,2,"h"],[1,5,2,"v"],[0,1,2,"h"]]];
LEVELS.push(
  [[2,0,2,"h"],[1,2,2,"v"],[5,2,2,"h"],[1,3,2,"v"],[0,1,2,"v"],[3,2,3,"h"],[1,5,3,"v"],[0,3,3,"h"],[3,1,3,"v"],[4,3,3,"h"],[4,0,2,"v"]],
  [[2,0,2,"h"],[1,2,2,"v"],[3,0,2,"v"],[5,1,3,"h"],[4,2,3,"h"],[3,2,3,"h"],[0,4,2,"h"],[0,3,2,"v"],[2,4,2,"h"]],
  [[2,0,2,"h"],[2,2,2,"v"],[2,4,2,"h"],[4,4,2,"h"],[3,3,2,"h"],[1,3,3,"h"],[0,0,2,"v"]],
  [[2,0,2,"h"],[1,3,2,"v"],[2,2,2,"v"],[1,4,2,"v"],[3,5,3,"v"],[3,4,2,"v"],[5,0,3,"h"],[1,5,2,"v"]],
  [[2,0,2,"h"],[1,2,2,"v"],[2,5,2,"v"],[3,1,2,"v"],[5,2,2,"h"],[4,5,2,"v"],[1,4,3,"v"],[1,0,2,"h"],[0,4,2,"h"]],
  [[2,0,2,"h"],[2,3,3,"v"],[2,4,3,"v"],[5,4,2,"h"],[3,1,3,"v"],[1,5,3,"v"],[0,4,2,"h"],[0,0,2,"h"],[3,0,2,"v"]],
  [[2,0,2,"h"],[2,3,2,"v"],[1,2,2,"h"],[0,0,2,"v"],[2,4,2,"v"],[4,3,3,"h"],[2,5,2,"v"],[2,2,3,"v"],[3,1,3,"v"],[0,3,3,"h"],[5,2,3,"h"]],
  [[2,0,2,"h"],[1,2,2,"v"],[2,3,3,"v"],[0,4,2,"v"],[3,0,3,"h"],[2,4,2,"h"],[3,5,3,"v"],[5,0,3,"h"]],
  [[2,0,2,"h"],[1,3,2,"v"],[0,1,2,"h"],[3,5,2,"v"],[3,0,2,"v"],[1,1,2,"h"],[5,3,2,"h"],[1,4,3,"v"],[3,1,3,"v"],[3,2,2,"v"],[4,3,2,"h"]],
  [[2,0,2,"h"],[1,3,2,"v"],[1,5,3,"v"],[3,3,3,"v"],[3,1,3,"v"],[1,4,3,"v"],[0,2,2,"v"],[4,4,2,"h"]],
  [[2,0,2,"h"],[0,2,3,"v"],[4,3,2,"h"],[1,3,3,"h"],[3,1,3,"v"],[2,4,2,"v"],[0,0,2,"h"],[0,4,2,"h"],[4,5,2,"v"],[5,2,3,"h"]],
  [[2,0,2,"h"],[1,2,2,"v"],[2,3,3,"v"],[0,1,2,"h"],[1,5,3,"v"],[5,4,2,"h"],[4,1,2,"h"],[1,4,3,"v"],[4,4,2,"h"]]
);
const EXTRA_LEVEL_ORDER=[0,1,2,3,10,4,5,6,7,8,9,11];
const extraLevels=LEVELS.splice(8);
LEVELS.push(...EXTRA_LEVEL_ORDER.map(index=>extraLevels[index]));
const CHAPTERS=["Courtyard","Pillar Hall","Royal Archive","Sunken Sanctum"];
const $=id=>document.getElementById(id), boardEl=$("board");
let level=0, pieces=[], moves=0, history=[], cs=60, locked=false, solved=new Set();
try{JSON.parse(localStorage.getItem("slideout")||"[]").forEach(i=>{if(Number.isInteger(i)&&i>=0&&i<LEVELS.length)solved.add(i)})}catch(e){}
function save(){try{localStorage.setItem("slideout",JSON.stringify([...solved]))}catch(e){}}

function showScreen(id){document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id===id))}
function unlockedLevelCount(){let count=1;while(count<LEVELS.length&&solved.has(count-1))count++;return count}
function updateHomeProgress(){
  const count=solved.size;
  $("homeProgress").textContent=count?`${count} of ${LEVELS.length} trials cleared`:"Your first chamber is waiting";
}
function renderLevelMap(){
  const map=$("levelMap"),unlocked=unlockedLevelCount();
  map.innerHTML="";
  CHAPTERS.forEach((name,chapterIndex)=>{
    const start=chapterIndex*5,chapter=document.createElement("section");
    chapter.className="chapter-card";
    const heading=document.createElement("div");heading.className="chapter-heading";
    const label=document.createElement("span");label.className="chapter-kicker";label.textContent=`CHAMBER ${String(chapterIndex+1).padStart(2,"0")}`;
    const title=document.createElement("h2");title.textContent=name;
    const count=document.createElement("span");count.className="chapter-count";
    count.textContent=`${Array.from({length:5},(_,i)=>solved.has(start+i)).filter(Boolean).length} / 5`;
    heading.append(label,title,count);chapter.appendChild(heading);
    const grid=document.createElement("div");grid.className="level-grid";
    for(let i=start;i<start+5;i++){
      const available=i<unlocked,complete=solved.has(i),button=document.createElement("button");
      button.className=`level-card${complete?" complete":""}${!available?" locked":""}`;
      button.disabled=!available;
      button.setAttribute("aria-label",available?`Level ${i+1}${complete?", completed":""}`:`Level ${i+1}, locked`);
      const number=document.createElement("span");number.className="level-number";number.textContent=String(i+1).padStart(2,"0");
      const state=document.createElement("span");state.className="level-state";
      state.textContent=complete?"CLEARED":available?"PLAY":"LOCKED";
      button.append(number,state);
      if(available)button.onclick=()=>load(i);
      grid.appendChild(button);
    }
    chapter.appendChild(grid);map.appendChild(chapter);
  });
  $("mapProgressText").textContent=`${solved.size} / ${LEVELS.length} trials cleared`;
  $("mapProgressFill").style.width=`${solved.size/LEVELS.length*100}%`;
  $("mapProgressFill").parentElement.setAttribute("aria-valuenow",solved.size);
  updateHomeProgress();
}
function openLevelSelect(){renderLevelMap();showScreen("levelScreen")}

function size(){cs=Math.floor(Math.min(innerWidth-70,430)/N);const w=cs*N+24;document.documentElement.style.setProperty("--w",w+"px")}
function load(i){
  if(i<0||i>=unlockedLevelCount())return;
  level=i;size();locked=false;moves=0;history=[];$("ov").classList.remove("show");
  showScreen("gameScreen");
  boardEl.innerHTML="";boardEl.style.width=boardEl.style.height=cs*N+"px";
  for(let r=0;r<N;r++)for(let c=0;c<N;c++){const d=document.createElement("div");d.className="cell";Object.assign(d.style,{left:c*cs+2+"px",top:r*cs+2+"px",width:cs-4+"px",height:cs-4+"px"});boardEl.appendChild(d)}
  const door=document.createElement("div");door.className="door";Object.assign(door.style,{top:2*cs+4+"px",height:cs-8+"px"});boardEl.appendChild(door);
  const ar=document.createElement("div");ar.className="arrow";ar.textContent="➜";ar.style.top=2*cs+cs/2-12+"px";boardEl.appendChild(ar);
  pieces=LEVELS[i].map((p,k)=>{const el=document.createElement("div");el.className="piece "+(p[3]==="h"?"horizontal":"vertical")+(k?"":" red");boardEl.appendChild(el);
    const o={r:p[0],c:p[1],len:p[2],dir:p[3],el};place(o);attach(o);return o});
  hud();
}
function place(p,dx=0,dy=0){const e=p.el.style;e.left=p.c*cs+4+"px";e.top=p.r*cs+4+"px";
  e.width=(p.dir==="h"?p.len*cs:cs)-8+"px";e.height=(p.dir==="v"?p.len*cs:cs)-8+"px";e.transform=`translate(${dx}px,${dy}px)`}
function hud(){$("lv").textContent=level+1;$("mv").textContent=moves;$("par").textContent=PARS[level];$("undo").disabled=!history.length;
  $("chapter").textContent=`${CHAPTERS[Math.floor(level/5)]} · ${Math.floor(level/5)+1}`;
  $("progressText").textContent=`${level+1} / ${LEVELS.length}`;
  $("progressFill").style.width=`${(level+1)/LEVELS.length*100}%`;
  $("gameProgress").setAttribute("aria-valuenow",level+1)}
function grid(skip){const g=Array.from({length:N},()=>Array(N).fill(false));
  pieces.forEach(p=>{if(p===skip)return;for(let i=0;i<p.len;i++)g[p.dir==="v"?p.r+i:p.r][p.dir==="h"?p.c+i:p.c]=true});return g}
function attach(p){
  p.el.addEventListener("pointerdown",ev=>{
    if(locked)return;ev.preventDefault();p.el.setPointerCapture(ev.pointerId);
    const g=grid(p),h=p.dir==="h",pos=h?p.c:p.r;let back=0,fwd=0;
    while(pos-back-1>=0&&!(h?g[p.r][pos-back-1]:g[pos-back-1][p.c]))back++;
    while(pos+p.len+fwd<N&&!(h?g[p.r][pos+p.len+fwd]:g[pos+p.len+fwd][p.c]))fwd++;
    const start=h?ev.clientX:ev.clientY;let off=0;p.el.classList.add("drag");
    const move=e=>{off=Math.max(-back*cs,Math.min(fwd*cs,(h?e.clientX:e.clientY)-start));place(p,h?off:0,h?0:off)};
    const up=()=>{p.el.removeEventListener("pointermove",move);p.el.removeEventListener("pointerup",up);p.el.removeEventListener("pointercancel",up);
      p.el.classList.remove("drag");const step=Math.round(off/cs);
      if(step){history.push({p,r:p.r,c:p.c});if(h)p.c+=step;else p.r+=step;moves++}
      place(p);hud();if(step&&pieces[0].c+2===N)win()};
    p.el.addEventListener("pointermove",move);p.el.addEventListener("pointerup",up);p.el.addEventListener("pointercancel",up);
  });
}
function win(){
  locked=true;const red=pieces[0];red.el.classList.add("out");place(red,cs*2.2,0);
  solved.add(level);save();renderLevelMap();
  const par=PARS[level],stars=moves<=par?3:moves<=par*1.5?2:1;
  setTimeout(()=>{$("st").textContent="★".repeat(stars)+"☆".repeat(3-stars);
    $("mm").textContent=`You used ${moves} moves. Best possible: ${par}.`;
    const last=level===LEVELS.length-1;$("mt").textContent=last?"Temple conquered!":"Chamber complete!";
    $("next").textContent=last?"Return to chambers":"Next level →";$("ov").classList.add("show")},650);
}
$("startGame").onclick=openLevelSelect;
$("levelsBack").onclick=()=>showScreen("homeScreen");
$("gameBack").onclick=openLevelSelect;
$("next").onclick=()=>level===LEVELS.length-1?openLevelSelect():load(level+1);
$("reset").onclick=()=>load(level);
$("undo").onclick=()=>{if(locked||!history.length)return;const h=history.pop();h.p.r=h.r;h.p.c=h.c;place(h.p);moves++;hud()};
addEventListener("resize",()=>{if(!locked&&$("gameScreen").classList.contains("active"))load(level)});
renderLevelMap();
showScreen("homeScreen");
