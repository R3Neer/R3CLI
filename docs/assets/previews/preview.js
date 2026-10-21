"use strict";
const screen=document.querySelector('.screen'),initial=screen.innerHTML;
const frames=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'];
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const captureMode=new URLSearchParams(location.search).has('capture');
let timer=null,frame=0,completed=12,wantsMotion=!captureMode&&!reducedMotion.matches;
function syncMotion(){
  const active=screen.querySelector('.frame')!==null;
  const running=wantsMotion&&active;
  if(running&&timer===null)timer=setInterval(tick,100);
  if(!running&&timer!==null){clearInterval(timer);timer=null;}
  const button=document.querySelector('#play');
  if(button){button.disabled=!active;button.textContent=running?'Pause animation':'Play animation';button.setAttribute('aria-pressed',String(running));}
  if(window.previewStatus)window.previewStatus.animationPaused=timer===null;
}
function tick(){frame=(frame+1)%frames.length;screen.querySelectorAll('.frame').forEach(e=>e.textContent=frames[frame]);}
document.querySelector('#play')?.addEventListener('click',()=>{wantsMotion=!wantsMotion;syncMotion();});
document.querySelector('#reset')?.addEventListener('click',()=>{
  screen.innerHTML=initial;frame=0;completed=12;wantsMotion=!captureMode&&!reducedMotion.matches;
  for(const id of ['leader-label','leader-width','leader-pattern']){const input=document.getElementById(id);if(input)input.value=input.defaultValue;}
  fitRules();fitLeaders();syncMotion();
});
document.querySelector('#update')?.addEventListener('click',()=>{
  completed=25;
  screen.querySelectorAll('.counts').forEach(e=>e.textContent='25/40 files · 63%');
  screen.querySelectorAll('.bar').forEach(e=>{e.replaceChildren();for(const [cls,text]of [['text','━'.repeat(13)],['muted','━'.repeat(7)]]){const span=document.createElement('span');span.className=cls;span.textContent=text;e.append(span);}});
  const activity=document.querySelector('#activity-region');
  if(activity)activity.innerHTML='<div class="line"><span class="success">✓</span> Resolving dependencies</div>';
  const stage=document.querySelector('#stage-first');
  if(stage)stage.innerHTML='<div class="line"><span class="success">✓</span> Resolve dependencies</div>';
  const view=document.querySelector('#view-region');
  if(view)view.innerHTML=document.body.dataset.slug==='structure'?'<div class="block task" data-progress="true"><div class="line"><span class="accent frame">⠋</span> Reading metadata <span class="muted counts">12/40 files · 30%</span></div><div class="line">  <span class="bar"><span class="text">━━━━━━</span><span class="muted">━━━━━━━━━━━━━━</span></span></div></div>':'<div class="line"><span class="muted">Files: </span>25</div>';
  syncMotion();
});
document.querySelector('#remove')?.addEventListener('click',()=>{document.querySelector('#view-region')?.replaceChildren();syncMotion();});
reducedMotion.addEventListener('change',()=>{wantsMotion=!captureMode&&!reducedMotion.matches;syncMotion();});
window.addEventListener('pagehide',()=>{if(timer!==null)clearInterval(timer);timer=null;});

document.querySelector('#content')?.addEventListener('input',e=>{const first=screen.querySelector('.line');const target=first?.querySelector('span')||first;if(target)target.textContent=e.target.value;});
function fitRules(){document.querySelectorAll('.rule').forEach(e=>{const span=e.firstElementChild;const canvas=document.createElement('canvas');const ctx=canvas.getContext('2d');ctx.font=getComputedStyle(span).font;const capacity=Math.max(0,Math.floor((e.getBoundingClientRect().width+0.01)/ctx.measureText('M').width));span.textContent=repeatPattern(e.dataset.pattern,capacity,false).replace(/ +$/u,'');});}
new ResizeObserver(()=>{fitRules();fitLeaders();}).observe(screen);
document.fonts.ready.then(()=>{fitRules();fitLeaders();window.previewStatus={ready:true,animationPaused:true};syncMotion();});

// Documentary browser approximation of terminal cells, not backend layout code.
function cellWidth(text) {
  const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
  ctx.font=getComputedStyle(screen).font;
  const unit=ctx.measureText('M').width;
  const graphemes=new Intl.Segmenter('en',{granularity:'grapheme'}).segment(text);
  return Array.from(graphemes,part=>Math.max(0,Math.round(ctx.measureText(part.segment).width/unit))).reduce((a,b)=>a+b,0);
}
function repeatPattern(pattern,cells,pad){
  const graphemes=Array.from(new Intl.Segmenter('en',{granularity:'grapheme'}).segment(pattern),part=>part.segment);
  let fill='',remaining=cells,index=0;
  while(remaining>0&&graphemes.length){
    const next=graphemes[index%graphemes.length],width=cellWidth(next);
    if(width<=0||width>remaining)break;
    fill+=next;remaining-=width;index++;
  }
  return fill+(pad?' '.repeat(remaining):'');
}
function fitLeaders(){
  document.querySelectorAll('[data-leader]').forEach(owner=>{
    const prefix=owner.querySelector('.leader-prefix').textContent;
    const prefixCells=cellWidth(prefix);
    const exhausted=prefixCells>=Number(owner.dataset.width);
    const gap=Math.max(1,Number(owner.dataset.width)-prefixCells);
    const pattern=owner.dataset.pattern||' ';
    owner.querySelector('.leader-fill').textContent=exhausted?' ':repeatPattern(pattern,gap,true);
    owner.dataset.prefixCells=String(cellWidth(prefix));
    owner.dataset.gapCells=String(gap);
  });
}
for(const id of ['leader-label','leader-width','leader-pattern']){
  document.getElementById(id)?.addEventListener('input',()=>{
    const owner=document.querySelector('[data-leader]');
    const width=Number(document.getElementById('leader-width').value);
    if(!Number.isInteger(width)||width<0)return;
    owner.querySelector('.leader-prefix').textContent=document.getElementById('leader-label').value;
    owner.dataset.width=String(width);
    owner.dataset.pattern=document.getElementById('leader-pattern').value;
    fitLeaders();
  });
}

// Documentary palette switching only; no terminal query or R3CLI code runs here.
function applyDocumentaryTheme(){
  const selected=document.querySelector('#theme-preset')?.value || 'catppuccin-mocha';
  const preset=window.documentaryThemes[selected];
  screen.style.setProperty('--reference-background',preset['reference-background']);
  for(const [token,value]of Object.entries(preset.tokens))screen.style.setProperty('--'+token.replaceAll('.','-'),value);
  screen.dataset.preset=selected;
}
document.querySelector('#theme-preset')?.addEventListener('change',applyDocumentaryTheme);
applyDocumentaryTheme();
