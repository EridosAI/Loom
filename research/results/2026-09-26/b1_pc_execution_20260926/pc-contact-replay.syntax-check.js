(()=>{
    const root=document.getElementById('loom-pc-contact-replay');
    const data=JSON.parse(root.querySelector('[data-replay-data]').textContent);
    const svg=root.querySelector('svg');
    const play=root.querySelector('[data-control="play"]');
    const view=root.querySelector('[data-control="view"]');
    const speed=root.querySelector('[data-control="speed"]');
    const slider=root.querySelector('[data-control="time"]');
    const clock=root.querySelector('[data-field="time"]');
    const detail=root.querySelector('[data-field="detail"]');
    const contact=root.querySelector('[data-field="contact"]');
    const frames=data.frames, last=frames.length-1;
    slider.max=String(last);
    let index=0, playing=false, raf=0, startWall=0, startTime=0;
    const ns='http://www.w3.org/2000/svg';
    function el(tag,attrs,parent=svg,text){const e=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(text!==undefined)e.textContent=text;parent.appendChild(e);return e;}
    function save(){if(window.openai?.setWidgetState)window.openai.setWidgetState({modelContent:{case:'PC-CONTACT',recorded_time:frames[index].t,view:view.value,passive_replay:true},privateContent:{index,view:view.value,speed:speed.value}}).catch(()=>{});}
    function restore(s){const p=s?.privateContent;if(!p)return;index=Math.max(0,Math.min(last,Number.isInteger(p.index)?p.index:0));if(['close','arena'].includes(p.view))view.value=p.view;if(['0.25','1'].includes(p.speed))speed.value=p.speed;}
    function stop(){playing=false;cancelAnimationFrame(raf);play.textContent=index===last?'Replay':'Play';}
    function draw(announce=true){
      const f=frames[index], w=Math.max(280,root.clientWidth), h=Math.min(460,Math.max(300,w*.64));
      svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.setAttribute('height',h);svg.replaceChildren();
      const b=view.value==='close'?data.close_bounds:[-.3,data.world.side+.3,-.3,data.world.side+.3];
      const padding=24, scale=Math.min((w-2*padding)/(b[1]-b[0]),(h-2*padding)/(b[3]-b[2]));
      const x0=(w-(b[1]-b[0])*scale)/2, y0=(h-(b[3]-b[2])*scale)/2;
      const X=x=>x0+(x-b[0])*scale, Y=y=>h-y0-(y-b[2])*scale;
      el('desc',{},svg,`Saved sample at ${f.t.toFixed(2)} seconds. ${f.contact?'Contact recorded.':'No contact in this native sample.'} No simulation is executed.`);
      const clipId='loom-pc-contact-clip'; const defs=el('defs',{}); const cp=el('clipPath',{id:clipId},defs);el('rect',{x:x0,y:y0,width:(b[1]-b[0])*scale,height:(b[3]-b[2])*scale},cp);
      const scene=el('g',{'clip-path':`url(#${clipId})`});
      el('rect',{x:X(0),y:Y(data.world.side),width:data.world.side*scale,height:data.world.side*scale,fill:'var(--background)',stroke:'var(--foreground)','stroke-width':2},scene);
      if(view.value==='close')el('text',{x:X(0)+8,y:y0+22},svg,'Boundary wall');
      for(const disk of data.world.disks)el('circle',{cx:X(disk[0]),cy:Y(disk[1]),r:disk[2]*scale,fill:'var(--muted)',stroke:'var(--muted-foreground)','stroke-width':1},scene);
      for(const r of data.world.rectangles)el('rect',{x:X(r[0]),y:Y(r[3]),width:(r[1]-r[0])*scale,height:(r[3]-r[2])*scale,fill:'var(--muted)',stroke:'var(--muted-foreground)','stroke-width':1},scene);
      const m=f.mover;el('rect',{x:X(m[0]),y:Y(m[3]),width:(m[1]-m[0])*scale,height:(m[3]-m[2])*scale,fill:'var(--secondary)',stroke:'var(--muted-foreground)','stroke-width':1},scene);
      const path=frames.slice(0,index+1).map((p,j)=>`${j?'L':'M'} ${X(p.x)} ${Y(p.y)}`).join(' ');
      el('path',{d:path,fill:'none',stroke:'var(--muted-foreground)','stroke-width':1.5,'stroke-dasharray':'3 3'},scene);
      const r=data.world.body_radius, radius=r*scale;
      el('circle',{cx:X(f.x),cy:Y(f.y),r:radius,fill:'var(--viz-series-1)','fill-opacity':.18,stroke:'var(--viz-series-1)','stroke-width':2},scene);
      const tip=[X(f.x+r*.94*Math.cos(f.a)),Y(f.y+r*.94*Math.sin(f.a))];
      el('line',{x1:X(f.x),y1:Y(f.y),x2:tip[0],y2:tip[1],stroke:'var(--viz-series-1)','stroke-width':3},scene);
      el('circle',{cx:tip[0],cy:tip[1],r:3,fill:'var(--viz-series-1)'},scene);
      if(f.contact){el('circle',{cx:X(0),cy:Y(f.y),r:5,fill:'var(--viz-series-2)'},scene);if(view.value==='close')el('text',{x:X(f.x)+radius+10,y:Y(f.y)},svg,'Contact');}
      const bar=Math.min(1,(b[1]-b[0])*.25), bx=x0+10, by=h-y0-12;
      el('line',{x1:bx,y1:by,x2:bx+bar*scale,y2:by,stroke:'var(--foreground)','stroke-width':2});
      el('text',{x:bx,y:by-8},svg,`${bar.toFixed(2).replace(/0+$/,'').replace(/\.$/,'')} body diameters`);
      slider.value=String(index);clock.textContent=`${f.t.toFixed(2)} / ${frames[last].t.toFixed(2)} s`;
      if(announce)detail.textContent=`Commands L ${f.u[0].toFixed(2)} · R ${f.u[1].toFixed(2)} | E ${f.e.toFixed(6)} · I ${f.i.toFixed(6)}`;
      contact.textContent=`Contact 0 (front): ${f.c[0].toFixed(6)} · Contact 1 (front-left): ${f.c[1].toFixed(6)} · ${f.contact?'Contact in this sample':'No contact in this sample'}`;
      if(!playing)play.textContent=index===last?'Replay':'Play';
    }
    function tick(now){if(!playing)return;const t=startTime+(now-startWall)/1000*Number(speed.value);while(index<last&&frames[index+1].t<=t)index++;draw(false);if(index===last){stop();draw(true);save();return;}raf=requestAnimationFrame(tick);}
    play.addEventListener('click',()=>{if(playing){stop();draw(true);save();return;}if(index===last)index=0;playing=true;play.textContent='Pause';startWall=performance.now();startTime=frames[index].t;raf=requestAnimationFrame(tick);});
    slider.addEventListener('input',()=>{stop();index=Number(slider.value);draw(true);});slider.addEventListener('change',save);
    view.addEventListener('change',()=>{draw(true);save();});
    speed.addEventListener('change',()=>{if(playing){startTime=frames[index].t;startWall=performance.now();}save();});
    restore(window.openai?.widgetState);
    window.addEventListener('openai:set_globals',e=>{if(e.detail?.globals?.widgetState){stop();restore(e.detail.globals.widgetState);draw(true);}});
    new ResizeObserver(()=>draw(false)).observe(root);draw(true);
  })();