/* One persistent architecture canvas; authored steps, optional browser voice, no progress writes. */
(() => {
  'use strict';
  const player = document.querySelector('[data-visual-story]');
  if (!player) return;
  const lesson = (window.CCS_VISUAL_STORIES || {})[player.dataset.visualStory];
  if (!lesson) return;
  const pilot=lesson.teachingEdition==='integrated-v2'; let tracing=false, traceViewport=null;
  const $ = s => player.querySelector(s);
  const make = (tag, cls, text) => { const el=document.createElement(tag); if(cls)el.className=cls; if(text!==undefined)el.textContent=text; return el; };
  const NS='http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs, text) => { const el=document.createElementNS(NS,tag); Object.entries(attrs||{}).forEach(([k,v])=>el.setAttribute(k,String(v))); if(text!==undefined)el.textContent=text; return el; };
  const svg=$('.vl-map'), frame=$('.vl-map-frame'), reference=document.querySelector('.vl-reference');
  let index=0, scale=1, phase='setup', narration='', speaking=false, paused=false, utterance=null, voiceToken=0;
  const chosen=new Map(); let inspected=null, connection=0, pinned=null;
  const surface=document.createElement('div');frame.parentNode.insertBefore(surface,frame);surface.append(frame);const annotations=window.CCS_DiagramAnnotations.attach(surface,frame,{ignoreOutside:'.vl-technical',onHide(){pinned=null;showConnection();}});
  const focusGuide=make('section','vl-local-focus');surface.insertBefore(focusGuide,frame);
  const extent=make('p','vl-map-extent');extent.setAttribute('aria-live','polite');frame.after(extent);function updateExtent(){const right=frame.scrollWidth-frame.clientWidth-frame.scrollLeft>8,down=frame.scrollHeight-frame.clientHeight-frame.scrollTop>8,left=frame.scrollLeft>8,up=frame.scrollTop>8;extent.textContent=[left?'← More map':'',right?'More map →':'',up?'↑ More map':'',down?'More map ↓':''].filter(Boolean).join(' · ')+(right||down||left||up?' · Scroll inside the diagram or choose Overview to see the whole layer.':'Whole current layer is visible.');}frame.addEventListener('scroll',updateExtent);const synth=window.speechSynthesis;
  const available=!!(synth && window.SpeechSynthesisUtterance);
  function stopVoice() { voiceToken++; if(synth)synth.cancel(); utterance=null; speaking=false;paused=false;$('.vl-play').textContent='Listen';$('.vl-stop').disabled=true; }
  function voice() {
    if(!available)return;
    if(speaking&&!paused){synth.pause();paused=true;$('.vl-play').textContent='Resume';return;}
    if(paused){synth.resume();paused=false;$('.vl-play').textContent='Pause';return;}
    stopVoice(); const token=voiceToken;
    utterance=new SpeechSynthesisUtterance(narration); utterance.rate=.94; utterance.lang='en-US';
    utterance.onend=()=>{if(token!==voiceToken)return;speaking=false;paused=false;$('.vl-play').textContent='Listen again';$('.vl-stop').disabled=true;};
    utterance.onerror=e=>{if(token!==voiceToken)return;stopVoice();if(e.error!=='interrupted'&&e.error!=='canceled')$('.vl-audio-status').textContent='Voice is unavailable here. The visible narration contains the same explanation.';};
    speaking=true;$('.vl-play').textContent='Pause';$('.vl-stop').disabled=false;$('.vl-audio-status').textContent='Reading the visible narration. You can pause or stop at any time.';synth.speak(utterance);
  }
  $('.vl-play').addEventListener('click',voice);$('.vl-stop').addEventListener('click',stopVoice);
  if(!available){$('.vl-play').disabled=true;$('.vl-audio-status').textContent='Browser voice is unavailable. Read the same narration below; the whole lesson still works.';}
  function nodeDescription(id){return (state().nodeDescriptions||{})[id]||lesson.nodes[id].description;}
  function state() {const s=lesson.stages[index];return phase==='repair'?{...s,...s.repair}:s;}
  function geometry() {
    const notes=lesson.focusNotes[index][phase==='repair'?'repair':'setup'];
    const compact=frame.clientWidth<600;
    if(pilot&&lesson.layout){const layout=lesson.layout,nodes=Object.fromEntries(Object.entries(lesson.nodes).map(([id,n])=>[id,{...n,...layout.nodes[id],h:124,note:''}]));return {width:layout.width,nodes};}
    if(player.dataset.visualStory==='as-03-grounded-assistant'){const positions={ask:[40,40],search:[340,40],guard:[40,240],catalog:[340,240],answer:[640,240],owner:[640,440]};return {width:880,nodes:Object.fromEntries(Object.entries(lesson.nodes).map(([id,n])=>[id,{...n,x:positions[id][0],y:positions[id][1],h:124,note:''}]))};}
    const slots=[[15,30],[235,30],[235,170],[15,170],[235,310],[235,450],[15,310],[15,450],[15,590],[235,590]];
    const nodes=Object.fromEntries(Object.entries(lesson.nodes).map(([id,n])=>{
      const note=notes[id]||'';const height=note?280:124;
      if(!compact){const row=n.y>500?3:Math.max(0,Math.round((n.y-60)/170));return [id,{...n,y:60+row*330,h:height,note}];}
      const col=Math.max(0,Math.min(2,Math.round((n.x-50)/335)));
      const row=n.y>500?3:Math.max(0,Math.min(2,Math.round((n.y-60)/170)));
      const point=slots[Math.min(9,row*3+col)];return [id,{...n,x:point[0],y:60+Math.round((point[1]-30)/140)*330,h:height,note}];
    }));
    return {nodes,width:compact?440:960};
  }
  function resize(mode='reading') {
    const st=state(), geo=geometry(), nodes=st.visible.map(id=>geo.nodes[id]);
    const currentRoutes=pilot&&lesson.layout?(st.edges||[]).flatMap(([a,b])=>lesson.layout.routes[a+'>'+b]||[]):[];const height=Math.max(300,...nodes.map(n=>n.y+n.h+35),...currentRoutes.map(p=>(Array.isArray(p)?p[1]:p.y)+24));svg.setAttribute('viewBox',`0 0 ${geo.width} ${height}`);
    if(mode==='fit'||mode==='readable')scale=Math.min(1.25,(frame.clientWidth-20)/geo.width,(frame.clientWidth<600?320:420)/height);
    else if(mode==='reading'||mode==='teaching')scale=Math.min(1,(frame.clientWidth-20)/geo.width);
    if(pilot&&mode==='readable')scale=frame.clientWidth<600?1:Math.min(1,(frame.clientWidth-20)/geo.width);
    svg.style.width=(geo.width*scale)+'px';svg.style.height=(height*scale)+'px';
    if(mode==='focus'||mode==='reading'||mode==='teaching'){
      const ids=mode==='teaching'?st.highlight:(st.focus&&st.focus.length?st.focus:st.highlight);
      let target=ids&&ids.length?geo.nodes[ids[0]]:geo.nodes[st.visible[0]];
      if(mode==='reading'){const links=(st.edges||[]).filter(([a,b])=>st.visible.includes(a)&&st.visible.includes(b));const link=links[connection];if(link){const a=geo.nodes[link[0]],b=geo.nodes[link[1]];target={x:(a.x+b.x)/2,y:(a.y+b.y)/2};}}
      if(target)frame.scrollTo({left:Math.max(0,(target.x+95)*scale-frame.clientWidth/2),top:Math.max(0,mode==='teaching'?(target.y+(target.h||124)+30)*scale-frame.clientHeight:(target.y+(target.h||124)/2)*scale-frame.clientHeight/2),behavior:'instant'});
    }else if(mode==='fit'||mode==='readable')frame.scrollTo({left:0,top:0,behavior:'instant'});updateExtent();
  }
  function patternCard(row,contextual=false,compact=false){
    const course=lesson.courseConnections[row.course_index],card=make('article','vl-pattern-card');card.dataset.courseIndex=row.course_index;
    const heading=make('h3','',compact?(row.decision_title||row.what):''),link=make('a','',course.title);link.href=course.url;if(!compact)heading.append(link);card.append(heading);if(compact){const source=make('p','vl-context-label');source.append(link);card.append(source,make('p','',row.decision_reason||row.why));}
    (compact?[]:[['Situation',row.what],['Why this choice matters',row.why]]).forEach(([label,text])=>{const p=make('p','');p.append(make('strong','',label+' — '),document.createTextNode(text));card.append(p);});
    const revealed=!contextual||phase==='repair'||!lesson.stages[index].question;
    if(revealed){const how=make('p','');how.append(make('strong','','Apply it here — '),document.createTextNode(row.how));if(!compact)card.append(how);
      const detail=make('details','vl-pattern-artifact');detail.append(make('summary','',compact?'Explore the choice and technical example':'Technical design record and acceptance evidence'),...(compact?[how]:[]),make('p','',row.technical_artifact.label),make('pre','',row.technical_artifact.pseudocode),make('p','', 'Evidence to obtain: '+row.evidence),make('p','', 'Scope: '+row.not_demonstrated));if(row.protocol_example)detail.append(make('p','',row.protocol_label),make('pre','',row.protocol_example));if(row.source_url){const primary=make('a','','Official mechanism reference');primary.href=row.source_url;detail.append(primary);}card.append(detail);
    }else card.append(make('p','vl-context-label','Use the current question to choose the boundary. After your choice, compare the applied mechanism and evidence here.'));
    return card;
  }
  function designQuestion(q){
    const card=make('section','vl-design-question');card.append(make('h3','',q.title),make('p','vl-eyebrow','Original unscored architecture decision · choose one'),make('pre','',q.context),make('h4','',q.stem));const feedback=make('div','vl-design-feedback');feedback.hidden=true;feedback.setAttribute('aria-live','polite');
    q.options.forEach((text,i)=>{const button=make('button','vl-design-option',String.fromCharCode(65+i)+'. '+text);button.type='button';button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>{card.querySelectorAll('.vl-design-option').forEach((b,j)=>b.setAttribute('aria-pressed',String(i===j)));feedback.replaceChildren(make('p','',i===q.answer?'That fits these constraints.':'Compare the requirement with the boundary.'));q.explanations.forEach((why,j)=>feedback.append(make('p','',(j===q.answer?'✓ ':'')+String.fromCharCode(65+j)+'. '+why)));feedback.hidden=false;});card.append(button);});card.append(feedback);return card;
  }
  function showPathPatterns(){
    if(!pilot||!lesson.pathApplications)return;let section=$('.vl-context-patterns');if(!section){section=make('section','vl-context-patterns');$('.vl-coach').append(section);}section.replaceChildren();
    const rows=lesson.pathApplications.filter(row=>row.where==='layer-'+(index+1)&&![0,1].includes(row.course_index));if(!rows.length){section.hidden=true;return;}section.hidden=false;section.append(make('h2','','Apply the wider architect toolkit at this layer'));
    rows.forEach(row=>section.append(patternCard(row,true,true)));
  }
  function showFluency(){
    if(!pilot||!lesson.fluencyLayers)return;
    let card=$('.vl-fluency');if(!card){card=make('section','vl-fluency');$('.vl-coach').insertBefore(card,$('.tb-stage'));}
    const unit=lesson.fluencyLayers[index],bridge=unit.integration;
    card.replaceChildren(make('h3','','Capability → judgment → architecture'));
    const parts=bridge?[['What · '+bridge.concept,bridge.what],['Why · '+unit.focus,bridge.why],[phase==='repair'?'How · applied here':'How · think it through',phase==='repair'?bridge.repair:bridge.setup]]:[['AI Fluency · '+unit.focus,unit.plain]];
    parts.forEach(([label,text])=>{const p=make('p','');p.append(make('strong','',label+' — '),document.createTextNode(text));card.append(p);});
    if(bridge&&(phase==='repair'||index===0)){const proof=make('p','');proof.append(make('strong','','Evidence check — '),document.createTextNode(bridge.proof));card.append(proof);}
    const more=make('details',''),summary=make('summary','','Connect these concepts to the official courses');more.append(summary);
    const links=make('p','');unit.courses.forEach((i,n)=>{if(n)links.append(document.createTextNode(' · '));const c=lesson.courseConnections[i],a=make('a','',c.title);a.href=c.url;links.append(a);});more.append(links);card.append(more);
    narration=state().narration+' '+parts.map(([label,text])=>label+'. '+text).join(' ')+(bridge&&(phase==='repair'||index===0)?' Evidence check. '+bridge.proof:'');
    if(available)$('.vl-audio-status').textContent='Listen reads the scene and its What, Why and How explanation. The same words are visible here.';
  }
  function showTechnical(){const item=lesson.technicalStages[index],b=item[phase==='repair'?'repair':'setup'];const block=$('.tb-stage'),key=index+':'+phase;if(block.dataset.phaseKey===key)return;block.dataset.phaseKey=key;block.innerHTML='<h2>Plain explanation ↔ technical mechanism · '+(phase==='repair'?'repair revealed':'current situation')+'</h2><p><a href="#visual-diagram">Back to the diagram ↑</a></p>'+window.CCS_RenderTechnicalBridge(b,item.objective_id);if(pilot){const plain=block.querySelector('.tb-plain');if(plain){const recap=make('details','vl-plain-recap');recap.append(make('summary','','Plain-language recap and limits'),plain);block.querySelector('.tb-pair').prepend(recap);}}}
  function activeLink(){const st=state();return (st.edges||[]).filter(([a,b])=>st.visible.includes(a)&&st.visible.includes(b))[connection];}
  function connectionInfo(a,b,label){const original=(lesson.connectionDetails||{})[a+'>'+b+'|'+label],st=state();let detail={...original,payload:'CURRENT '+(phase==='repair'?'REPAIR':'SETUP')+' FIXTURE (illustrative application evidence):\n'+(st.packet?.body||'No outcome supplied')+'\n\nSENDER OUTPUT CONTRACT: '+lesson.nodes[a].output+'\nRECEIVER INPUT CONTRACT: '+lesson.nodes[b].input};
    if(index===0&&player.dataset.visualStory==='as-01-action-service'){const readTrace={'screen>backend':'Fictional application request: {case_id: C17, order_id: O4, question: delivery/damage}. No credit requested by this read-only implementation.','backend>claude':'Messages request supplies the user question, permitted order/policy evidence, and optionally the read-only tools definition. See the actual tool definition and message shapes in the technical bridge below.','claude>backend':'Actual response content may contain text or a tool_use block. Example: {"type":"tool_use","id":"toolu_O4","name":"lookup_order","input":{"order_id":"O4"}}. This is a read request, not an issue_credit call.','backend>orders':'Application-owned authorized lookup: lookup_order({order_id: O4}). The business datastore API is not a Claude API message.','orders>backend':'Observed fictional lookup evidence: O4 delivery_status=delivered, damage_reported=true. No payment call or credit receipt exists in this stage.'};if(readTrace[a+'>'+b])detail={...detail,payload:readTrace[a+'>'+b]};}
return detail;}
  function showConnection(){
    if(pilot&&!tracing){$('.vl-technical').hidden=true;return;}
    $('.vl-technical').hidden=false;
    const edge=activeLink(),box=$('.vl-connection-detail');if(!edge)return;
    const [a,b,label]=edge,detail=connectionInfo(a,b,label);
    $('.vl-inspector').hidden=true;box.hidden=false;
    $('.vl-detail-status').textContent='· Connection '+(connection+1);

    box.querySelector('h3').textContent=lesson.nodes[a].label[0]+' → '+lesson.nodes[b].label[0];
    box.querySelector('.vl-technical-summary').textContent=detail?detail.summary:label;
    box.querySelector('pre').textContent=detail?detail.payload:lesson.nodes[a].output;
    const dl=box.querySelector('dl');dl.replaceChildren();
    [['Instruction / responsibility',detail?detail.instruction:lesson.nodes[b].input],['Receiving check / evidence',detail?detail.check:lesson.nodes[b].description]].forEach(([k,v])=>dl.append(make('dt','',k),make('dd','',v)));
    svg.querySelectorAll('[data-node]').forEach(g=>g.setAttribute('aria-pressed','false'));
  }
  function isIntroBoundary(kind,id){return index===0&&!!lesson.introDecision&&((kind==='node'&&['backend','claude'].includes(id))||(kind==='edge'&&['backend>claude','claude>backend'].includes(id.split('|')[0])));}
  function boundaryCue(kind,id){const cue=lesson.boundaryCues[kind==='node'?'nodes':'edges'][id];return isIntroBoundary(kind,id)?{...cue,prompt:'Which client action follows an assistant tool_use block, and how must the observed result be correlated in message history?',why_here:lesson.introDecision.translation}:cue;}
  function cueScope(kind,id,cue){return isIntroBoundary(kind,id)?'Current read-only tool interaction':cue.target_stage===null?'Context only':cue.target_stage>index?'Related decision in a later layer '+(cue.target_stage+1):cue.target_stage<index?'Related decision from an earlier layer '+(cue.target_stage+1):'Related decision in this layer';}
  function boundaryContent(kind,id,edge=null){
    const cue=boundaryCue(kind,id),wrap=make('section','vl-boundary-study');
    wrap.append(make('p','vl-boundary-context','Selected boundary · Stage '+(index+1)+' · '+(phase==='repair'?'repair revealed':'current setup')+' · '+cueScope(kind,id,cue)));
    wrap.append(make('h4','','Architect’s question at this boundary'),make('p','vl-boundary-prompt',cue.prompt),make('p','', 'In ordinary language: '+cue.why_here));
    const artifact=make('details','vl-boundary-evidence'),summary=make('summary','','Inspect the current scene evidence');
    artifact.append(summary,make('p','','Illustrative application fixture for the current scene; not a claim that every field crosses this selected connection.'),make('pre','',edge?connectionInfo(...edge).payload:(state().packet?.body||'No observed result at this stage.')));wrap.append(artifact);
    const intro=isIntroBoundary(kind,id);
    const target=cue.target_stage,q=intro?lesson.introDecision:target===null?null:lesson.stages[target].question;
    if(!q){wrap.append(make('p','', 'Context only: '+cue.reason));return wrap;}
    const disclosure=make('details','vl-boundary-question'),header=make('summary','','Practise a related technical decision · '+(intro?'this read-only tool interaction':target>index?'later layer '+(target+1):target<index?'earlier layer '+(target+1):'this layer'));
    disclosure.append(header,make('p','vl-eyebrow','Original unscored exam-style practice · not an official exam question'));
    if(!intro)disclosure.append(make('p','', 'Separate practice situation: the fixture below belongs to Stage '+(target+1)+'. It does not change the diagram or establish an outcome in the current scene.'));
    if(q.context)disclosure.append(make('pre','vl-boundary-fixture',q.context));
    disclosure.append(make('h4','',q.stem));
    const feedback=make('div','vl-boundary-feedback');feedback.hidden=true;feedback.setAttribute('aria-live','polite');
    q.options.forEach((o,i)=>{const btn=make('button','vl-boundary-option',String.fromCharCode(65+i)+'. '+o.text);btn.type='button';btn.setAttribute('aria-pressed','false');btn.addEventListener('click',()=>{disclosure.querySelectorAll('.vl-boundary-option').forEach((b,j)=>b.setAttribute('aria-pressed',String(i===j)));feedback.replaceChildren(make('p','',i===q.answer?'That mechanism fits this practice requirement.':'Compare the requirement with the mechanism.'));q.options.forEach((opt,j)=>feedback.append(make('p','',(j===q.answer?'✓ ':'')+String.fromCharCode(65+j)+'. '+opt.why)));if(q.variant)feedback.append(make('h4','','Change one constraint'),make('p','',q.variant.constraint||q.variant.changed_constraint),make('p','',q.variant.prompt||q.variant.decision));(q.sources||[]).forEach(ref=>{const link=make('a','',ref.title);link.href=ref.url;feedback.append(link,document.createTextNode(' '));});feedback.hidden=false;});disclosure.append(btn);});
    const translation=make('details','');translation.append(make('summary','','What is this question asking?'),make('p','',q.translation));disclosure.append(translation,feedback);
    if(!intro){const go=make('button','vl-boundary-go','Open the complete worked layer '+(target+1)+' →');go.type='button';go.addEventListener('click',()=>{const saved={index,phase,connection};index=target;render(true);let back=$('.vl-boundary-return');if(!back){back=make('button','vl-boundary-return','← Return to the original boundary');back.type='button';$('.vl-controls').append(back);}back.onclick=()=>{index=saved.index;render();phase=saved.phase;connection=saved.connection;$('.vl-narration').textContent=state().narration;showPacket();draw();back.remove();if(kind==='node')inspect(id,true);else{const selected=[...svg.querySelectorAll('[data-edge-key]')].find(g=>g.dataset.edgeKey===id);selected?.dispatchEvent(new MouseEvent('click',{bubbles:true}));}};});disclosure.append(go);}
    wrap.append(disclosure);if(pilot&&!intro&&target!==index){const related=make('details','vl-related-later'),label=make('summary','','Related study · '+lesson.stages[target].title);related.append(label,wrap);const current=make('section','');current.append(make('p','', 'Current scene: '+(edge?connectionInfo(...edge).summary:nodeDescription(id))),related);return current;}return wrap;
  }
  function inspect(id,pin=false){
    const anchor=svg.querySelector('[data-node="'+id+'"]'),node=lesson.nodes[id],technical=lesson.technicalNodes[id];
    if(anchor&&annotations.show(anchor,{title:node.label[0],purpose:nodeDescription(id),rows:[['Technical role',technical.meaning],['Exact terms',technical.terms.join(' · ')],[pilot?'Required input contract':'Input contract',node.input],[pilot?'Required output contract · see scene for actual result':'Output contract',node.output],['Owner',node.owner]],content:pin?boundaryContent('node',id):null,technical:{bridge:window.CCS_TECHNICAL_BRIDGES[technical.objective_id],href:'#technical-current-stage'}},pin)===false)return;
    if(!pin)return;inspected=id;pinned=id;svg.querySelectorAll('[data-node]').forEach(g=>g.setAttribute('aria-pressed',String(pinned===g.dataset.node)));
  }
  $('.vl-inspector-close').addEventListener('click',()=>{const id=inspected;pinned=null;showConnection();const trigger=svg.querySelector('[data-node="'+id+'"]');if(trigger)trigger.focus({preventScroll:true});annotations.hide();showConnection();});
  player.addEventListener('keydown',event=>{if(event.key==='Escape'){pinned=null;showConnection();}});
  function route(a,b,nodes,width) {
    if(pilot){const k=Object.keys(lesson.nodes).find(id=>lesson.nodes[id].label===a.label)+'>'+Object.keys(lesson.nodes).find(id=>lesson.nodes[id].label===b.label);if(lesson.layout?.routes?.[k])return lesson.layout.routes[k].map(p=>Array.isArray(p)?{x:p[0],y:p[1]}:p);const paths={'ask>search':[[230,102],[340,102]],'search>answer':[[530,102],[735,102],[735,240]],'ask>guard':[[135,164],[135,240]],'guard>search':[[230,302],[280,302],[280,102],[340,102]],'search>catalog':[[435,164],[435,240]],'catalog>answer':[[530,302],[640,302]],'answer>owner':[[735,364],[735,440]]};if(paths[k])return paths[k].map(([x,y])=>({x,y}));}

    const ports=n=>{const left={x:n.x,y:n.y+50,dx:-12,dy:0},right={x:n.x+190,y:n.y+50,dx:12,dy:0};return [...(n.x>width/2?[left,right]:[right,left]),{x:n.x+95,y:n.y,dx:0,dy:-12},{x:n.x+95,y:n.y+n.h,dx:0,dy:12}];};
    const boxes=nodes.map(n=>({l:n.x-5,r:n.x+195,t:n.y-5,b:n.y+n.h+5}));
    const clear=(p,q)=>!boxes.some(r=>p.x===q.x?p.x>r.l&&p.x<r.r&&Math.max(p.y,q.y)>r.t&&Math.min(p.y,q.y)<r.b:p.y>r.t&&p.y<r.b&&Math.max(p.x,q.x)>r.l&&Math.min(p.x,q.x)<r.r);
    const xs=[8,width-8,...nodes.flatMap(n=>[n.x-12,n.x+202])].filter(x=>x>=3&&x<=width-3);
    const ys=[8,...nodes.flatMap(n=>[n.y-14,n.y+n.h+14])].filter(y=>y>=3);
    let best=null,score=Infinity;
    for(const p of ports(a))for(const q of ports(b)){
      const u={x:p.x+p.dx,y:p.y+p.dy},v={x:q.x+q.dx,y:q.y+q.dy};
      if(u.x<0||v.x<0||u.x>width||v.x>width)continue;
      const candidates=[[u,{x:v.x,y:u.y},v],[u,{x:u.x,y:v.y},v]];
      for(const x of xs)candidates.push([u,{x,y:u.y},{x,y:v.y},v]);
      for(const y of ys)candidates.push([u,{x:u.x,y},{x:v.x,y},v]);
      for(const path of candidates){if(path.slice(1).some((z,i)=>!clear(path[i],z)))continue;const points=[{x:p.x+p.dx/4,y:p.y+p.dy/4},...path,{x:q.x+q.dx*0.5,y:q.y+q.dy*0.5}];let terminal=0;for(let i=points.length-1;i>0;i--){const z=points[i],prev=points[i-1];if(q.dx?z.y!==prev.y:z.x!==prev.x)break;terminal+=Math.abs(z.x-prev.x)+Math.abs(z.y-prev.y);}const cost=points.slice(1).reduce((sum,z,i)=>sum+Math.abs(z.x-points[i].x)+Math.abs(z.y-points[i].y),0)+path.length*18+Math.max(0,26-terminal)*4;if(cost<score){best=points;score=cost;}}
    }
    if(!best)throw new Error('No clear diagram route');
    return best.filter((p,i,all)=>!i||p.x!==all[i-1].x||p.y!==all[i-1].y);
  }
  function draw(teaching=false){
    annotations.hide();
    const st=state(), geo=geometry();svg.classList.toggle('is-compact',geo.width===440);svg.replaceChildren();
    const links=(st.edges||[]).filter(([a,b])=>st.visible.includes(a)&&st.visible.includes(b));
    if(connection<0){connection=links.findIndex(([a,b])=>(st.highlight||[]).includes(b));if(connection<0)connection=0;}
    connection=Math.max(0,Math.min(connection,links.length-1));
    const active=links[connection];
    const connections=$('.vl-connections ul');connections.replaceChildren();
    links.forEach(([a,b,label],i)=>{const li=make('li'),button=make('button','vl-connection-link',(i+1)+'. '+lesson.nodes[a].label[0]+' → '+lesson.nodes[b].label[0]+': '+label);button.type='button';button.setAttribute('aria-current',i===connection?'step':'false');button.addEventListener('click',()=>{connection=i;pinned=null;if(pilot){$('.vl-trace-tool').open=true;tracing=true;}draw();});li.append(button);connections.append(li);});
    focusGuide.replaceChildren();for(const id of st.highlight||[]){const note=lesson.focusNotes[index][phase==='repair'?'repair':'setup'][id];if(note){const item=make('div','');item.append(make('strong','',lesson.nodes[id].label[0]+' · Why this matters now'),make('p','',note));focusGuide.append(item);}}
    $('.vl-flow-caption').textContent=teaching?'Stage focus: '+(st.highlight||[]).map(id=>lesson.nodes[id].label[0]).join(' + ')+'. Use Previous / Next connection to trace the data.':active?`Connection ${connection+1} of ${links.length}: ${lesson.nodes[active[0]].label[0]} → ${lesson.nodes[active[1]].label[0]} · ${active[2]}`:'No connection at this stage';
    $('.vl-flow-prev').disabled=connection===0;$('.vl-flow-next').disabled=connection>=links.length-1;
    const defs=svgEl('defs');const marker=svgEl('marker',{id:'vl-arrow',viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:9,markerHeight:9,markerUnits:'userSpaceOnUse',orient:'auto'});marker.append(svgEl('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:'currentColor'}));defs.append(marker);svg.append(defs);
    const edges=svgEl('g'),edgeLabels=svgEl('g',{'aria-hidden':'true'});
    const shownLinks=pilot&&!tracing?links:(active?[active]:[]);
    const labelBoxes=[];
    for(const shownLink of shownLinks){
      const [from,to,label]=shownLink,points=route(geo.nodes[from],geo.nodes[to],st.visible.map(id=>geo.nodes[id]),geo.width);
      const edge=svgEl('g',{role:'button',tabindex:0,'aria-label':label+'. '+lesson.nodes[from].label[0]+' to '+lesson.nodes[to].label[0]+'. Show connection details','aria-controls':'vl-technical','data-edge-key':from+'>'+to+'|'+label});
      const d=points.map((p,i)=>(i?'L':'M')+p.x+','+p.y).join(' ');
      edge.append(svgEl('path',{class:'vl-edge-hit',d}),svgEl('path',{class:'vl-edge',d,'marker-end':'url(#vl-arrow)'}));
      edge.append(svgEl('title',{},label+' · Hover, focus or select for technical details'));
      const displayLabel=pilot&&st.edgeStatus?.[from+'>'+to]?st.edgeStatus[from+'>'+to]:label;
      if(pilot&&st.edgeStatus?.[from+'>'+to])edge.classList.add('vl-undelivered');
      const text=displayLabel.length>60?displayLabel.slice(0,57)+'…':displayLabel;
      const segments=points.slice(1).map((q,i)=>({p:points[i],q,len:Math.abs(q.x-points[i].x)+Math.abs(q.y-points[i].y)})).sort((a,b)=>b.len-a.len);
      let location=null,lines=[text],w=0,h=0;
      const wrapLabel=(value,max)=>{const out=[];let line='';for(const word of value.replace(/([/–—-])/g,'$1 ').split(/\s+/).flatMap(word=>word.length>max?word.match(new RegExp('.{1,'+max+'}','g')):[word])){if(line&&(line+' '+word).length>max){out.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)out.push(line);return out;};
      for(const max of [26,16,10,8]){lines=wrapLabel(text,max);w=Math.max(62,...lines.map(t=>t.length*6.7+16));h=lines.length*16+12;
        for(const seg of segments){const cx=(seg.p.x+seg.q.x)/2,cy=(seg.p.y+seg.q.y)/2;for(const [x,y]of [[cx-w/2,cy-h/2],[cx-w/2,cy-h-10],[cx+14,cy-h/2],[cx-w-14,cy-h/2],[cx-w/2,cy+10]]){if(x<3||x+w>geo.width-3||y<3)continue;if(labelBoxes.some(r=>x<r.x+r.w+6&&x+w>r.x-6&&y<r.y+r.h+6&&y+h>r.y-6))continue;if(st.visible.some(id=>{const n=geo.nodes[id];return x<n.x+194&&x+w>n.x-4&&y<n.y+n.h+4&&y+h>n.y-4;}))continue;location={x,y};break;}if(location)break;}if(location)break;
      }
      if(!location){const seg=segments[0];location={x:Math.max(4,Math.min(geo.width-w-4,(seg.p.x+seg.q.x)/2-w/2)),y:Math.max(4,(seg.p.y+seg.q.y)/2-h/2)};edge.dataset.labelNeedsReview='true';}
      const labelGroup=svgEl('g');edgeLabels.append(labelGroup);labelBoxes.push({...location,w,h});labelGroup.append(svgEl('rect',{class:'vl-inline-label-bg',x:location.x,y:location.y,width:w,height:h,rx:5}));lines.forEach((line,i)=>labelGroup.append(svgEl('text',{class:'vl-inline-label',x:location.x+w/2,y:location.y+18+i*16,'text-anchor':'middle'},line)));
      const reveal=(select=false)=>{if(pinned&&!select)return;const detail=connectionInfo(from,to,label);annotations.show(edge,{title:lesson.nodes[from].label[0]+' → '+lesson.nodes[to].label[0],purpose:detail.summary,rows:[['Data or instruction',detail.payload],['Receiving boundary',detail.check]],content:select?boundaryContent('edge',from+'>'+to+'|'+label,[from,to,label]):null},select);};labelGroup.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch'&&matchMedia('(hover:hover)').matches)reveal();});labelGroup.addEventListener('click',()=>reveal(true));edge.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch'&&matchMedia('(hover:hover)').matches)reveal();});let edgeTouch=false;edge.addEventListener('pointerdown',e=>{edgeTouch=e.pointerType==='touch';});edge.addEventListener('pointercancel',()=>{edgeTouch=false;});edge.addEventListener('focus',()=>{if(!edgeTouch)reveal();});edge.addEventListener('click',()=>{edgeTouch=false;reveal(true);});edge.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();reveal(true);}});edges.append(edge);
      if(!pilot){let cueBox=$('.vl-flow-decision');if(!cueBox){cueBox=make('div','vl-flow-decision');$('.vl-flow').append(cueBox);}const cueKey=from+'>'+to+'|'+label,cue=boundaryCue('edge',cueKey);cueBox.replaceChildren(make('strong','',cueScope('edge',cueKey,cue)),make('p','',cue.prompt));const read=make('button','','Read and practise this handoff');read.type='button';read.addEventListener('click',()=>reveal(true));cueBox.append(read);}
    }
    svg.append(edges,edgeLabels);
    for(const id of st.visible){const n=geo.nodes[id],labels=[((st.nodeLabels||{})[id]||n.label)[0],lesson.technicalNodes[id].short],isNew=(st.highlight||[]).includes(id);const g=svgEl('g',{class:'vl-node kind-'+n.kind+(isNew?' is-new':'')+(active&&active[0]===id?' is-sender':'')+(active&&active[1]===id?' is-receiver':''),'data-node':id,transform:`translate(${n.x},${n.y})`,role:'button',tabindex:0,'aria-pressed':'false','aria-controls':'vl-technical','aria-label':labels.join('. ')+'. Details: hover or focus to preview; select to pin'});
      g.append(svgEl('title',{},nodeDescription(id)+' Input: '+n.input+' Output: '+n.output));
      g.append(svgEl('rect',{width:190,height:n.h,rx:8}));g.append(svgEl('text',{x:180,y:116,'text-anchor':'end',class:'vl-node-affordance'},'Details ⓘ'));
      const wrap=(text,max)=>{const lines=[];let line='';for(const word of text.split(/\s+/)){if(line&&(line+' '+word).length>max){lines.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)lines.push(line);return lines;};
      const titleLines=wrap(labels[0],22);const subtitleLines=labels.slice(1).flatMap(t=>wrap(t,27));
      const all=[...titleLines.map(text=>({text,cls:'vl-node-title'})),...subtitleLines.map(text=>({text,cls:'vl-node-subtitle'}))];
      const spacing=Math.min(17,42/Math.max(1,all.length));const start=27-(all.length-1)*spacing/2+5;
      all.forEach((line,i)=>g.append(svgEl('text',{x:95,y:start+i*spacing,'text-anchor':'middle',class:line.cls,style:all.length>3?'font-size:12px':''},line.text)));
      const purpose=wrap(lesson.purposes[id],27);purpose.forEach((line,i)=>g.append(svgEl('text',{x:95,y:66+i*14,'text-anchor':'middle',class:'vl-node-purpose'},line)));
      if(n.note){g.append(svgEl('line',{x1:12,x2:178,y1:128,y2:128,class:'vl-why-divider'}),svgEl('text',{x:12,y:148,class:'vl-why-label'},'WHY THIS MATTERS NOW'));wrap(n.note,25).forEach((line,i)=>g.append(svgEl('text',{x:12,y:168+i*15,class:'vl-why-text'},line)));}
      if(isNew)g.append(svgEl('text',{x:180,y:-10,'text-anchor':'end',class:'vl-new-label'},'+ In focus'));
      g.addEventListener('pointerenter',()=>{if(window.matchMedia('(hover: hover)').matches)inspect(id);});let nodeTouch=false;g.addEventListener('pointerdown',e=>{nodeTouch=e.pointerType==='touch';});g.addEventListener('pointercancel',()=>{nodeTouch=false;});g.addEventListener('focus',()=>{if(!nodeTouch)inspect(id);});g.addEventListener('click',()=>{nodeTouch=false;inspect(id,true);});g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();inspect(id,true);}});svg.append(g);
    }
    resize(pilot&&!tracing?'readable':teaching?'teaching':'reading');showConnection();showTechnical();showFluency();showPathPatterns();if(pinned&&st.visible.includes(pinned))inspect(pinned,true);
  }
  function repair(q,selection){
    stopVoice();phase='repair';connection=-1;pinned=null;chosen.set(index,selection);
    const stage=lesson.stages[index];narration=stage.repair.narration;$('.vl-narration').textContent=narration;
    const selected=Number(selection),feedback=$('.vl-feedback');feedback.hidden=false;feedback.replaceChildren();
    feedback.append(make('p','vl-feedback-title',selected===q.answer?'That fits this requirement.':'Compare the mechanism with the requirement.'));
    q.options.forEach((opt,i)=>feedback.append(make('p','',(i===q.answer?'✓ ':'')+String.fromCharCode(65+i)+'. '+opt.why)));
    if(q.sources&&q.sources.length){const refs=make('p','vl-source-links','Mechanism references: ');q.sources.forEach((source,i)=>{if(i)refs.append(document.createTextNode(' · '));const a=make('a','',source.title);a.href=source.url;refs.append(a);});feedback.append(refs);if(q.sourceNote)feedback.append(make('p','vl-source-note',q.sourceNote));}
    $('.vl-question').querySelectorAll('button.vl-option').forEach((button,i)=>{button.classList.toggle('is-selected',i===selected);button.classList.toggle('is-correct',i===q.answer);button.classList.toggle('is-wrong',i===selected&&i!==q.answer);button.setAttribute('aria-pressed',String(i===selected));});
    $('.vl-map-status').textContent='Repair revealed · '+stage.title;showPacket();draw(true);
  }
  function showPacket(){const packet=state().packet||{};$('.vl-packet > span').textContent=packet.label||'Data at this step';$('.vl-packet pre').textContent=packet.body||'';}
  function render(focus=false){
    stopVoice();connection=0;pinned=null;const stage=lesson.stages[index];phase='setup';$('.vl-inspector').hidden=true;
    $('.vl-kicker').textContent=stage.kicker;$('.vl-title').textContent=stage.title;$('.vl-map-status').textContent=stage.kicker;$('.vl-step-count').textContent=(index+1)+' / '+lesson.stages.length;
    narration=stage.narration;$('.vl-narration').textContent=narration;
    if(available)$('.vl-audio-status').textContent='The text above is the narration. Listen if you prefer.';
  player.querySelectorAll('[data-stage]').forEach((btn,i)=>{if(i===index)btn.setAttribute('aria-current','step');else btn.removeAttribute('aria-current');});
    $('.vl-prev').disabled=index===0;$('.vl-next').disabled=index===lesson.stages.length-1;$('.vl-progress').textContent='Stage '+(index+1)+' of '+lesson.stages.length;
    const area=$('.vl-decision');area.replaceChildren();const q=stage.question;
    if(q){const question=make('section','vl-question');if(q.context){question.append(make('p','vl-context-label','Given this implementation'),make('pre','vl-context',q.context));}question.append(make('p','vl-eyebrow','Original exam-style decision · Choose one'),make('h3','',q.stem));q.options.forEach((opt,i)=>{const button=make('button','vl-option',String.fromCharCode(65+i)+'. '+opt.text);button.type='button';button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>repair(q,i));question.append(button);});const hint=make('details','vl-translation');hint.append(make('summary','','What is this asking?'),make('p','',q.translation));const feedback=make('div','vl-feedback');feedback.hidden=true;feedback.setAttribute('aria-live','polite');area.append(question,hint,feedback);}
    showPacket();draw(true);if(q&&chosen.has(index))repair(q,chosen.get(index));
    if(pilot){$('.vl-technical').hidden=!tracing;$('.vl-next').textContent='Next problem →';$('.vl-prev').textContent='← Previous problem';}
    if(focus)$('.vl-title').focus({preventScroll:true});
  }
  $('.vl-flow-prev').addEventListener('click',()=>{connection--;pinned=null;draw();});$('.vl-flow-next').addEventListener('click',()=>{connection++;pinned=null;draw();});
  player.querySelectorAll('[data-stage]').forEach(button=>button.addEventListener('click',()=>{index=Number(button.dataset.stage);render();}));
  $('.vl-prev').addEventListener('click',()=>{if(index>0){index--;render(true);}});$('.vl-next').addEventListener('click',()=>{if(index<lesson.stages.length-1){index++;render(true);}});
  $('.vl-replay').addEventListener('click',()=>{chosen.delete(index);render();});
  player.querySelectorAll('[data-zoom]').forEach(button=>button.addEventListener('click',()=>{const mode=button.dataset.zoom;if(mode==='in'||mode==='out'){scale=Math.max(.3,Math.min(2,scale*(mode==='in'?1.2:1/1.2)));resize('zoom');}else resize(mode);}));
  document.querySelector('.vl-course-toggle').addEventListener('click',event=>{const expanded=document.body.classList.toggle('visual-show-course');event.currentTarget.setAttribute('aria-expanded',String(expanded));});
  function openDeepLink(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const target=document.getElementById(id);if(target&&reference.contains(target)){reference.open=true;let parent=target.parentElement;while(parent&&parent!==reference){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}requestAnimationFrame(()=>target.scrollIntoView());}}
  reference.open=false;window.addEventListener('hashchange',openDeepLink);window.addEventListener('pagehide',stopVoice);document.addEventListener('visibilitychange',()=>{if(document.hidden)stopVoice();});
  let observedWidth=frame.clientWidth;
  if(window.ResizeObserver)new ResizeObserver(()=>{const width=frame.clientWidth;if(Math.abs(width-observedWidth)>1){observedWidth=width;draw();}}).observe(frame);
  if(pilot){
    player.classList.add('vl-pilot');
    const flow=$('.vl-flow'),details=make('details','vl-trace-tool'),summary=make('summary','','Trace a request · optional technical inspection');flow.parentNode.insertBefore(details,flow);details.append(summary,flow);
    details.addEventListener('toggle',()=>{if(details.open)traceViewport={scale,left:frame.scrollLeft,top:frame.scrollTop};tracing=details.open;pinned=null;draw(true);if(!tracing&&traceViewport){scale=traceViewport.scale;resize('zoom');frame.scrollTo({left:traceViewport.left,top:traceViewport.top});}});
    const bridge=$('.tb-stage');if(bridge){$('.vl-coach').insertBefore($('.vl-decision'),$('.vl-technical'));$('.vl-coach').insertBefore(bridge,$('.vl-technical'));}
    $('.vl-map-toolbar span').textContent=frame.clientWidth<600?'Scroll map horizontally · Overview fits the whole layer':'Complete current layer · hover or select for technical details';
    const fit=$('[data-zoom="fit"]');fit.textContent='Overview';const readable=make('button','','Readable size');readable.type='button';readable.addEventListener('click',()=>resize('readable'));fit.after(readable);
  }
  if(pilot&&lesson.courseConnections){
    const map=make('section','vl-course-connections');map.id='official-course-connections';map.append(make('h2','','Connect this case to the official architect path'),make('p','','These are our learning connections to the official course summaries, checked 22 October 2026—not a claim that this example teaches all eleven courses. The foundational path links onward to separate certification preparation.'));
    const path=make('a','','Open the official architect path');path.href='https://anthropic-partners.skilljar.com/path/claude-architect';map.append(path);
    const before=make('details','vl-foundation-choices');before.append(make('summary','','Before writing a prompt: entry point, capabilities, model and context'));
    lesson.foundationDecisions.forEach(([name,text])=>before.append(make('h3','',name),make('p','',text)));map.append(before);
    const catalog=make('details','vl-course-map');catalog.append(make('summary','','All 11 courses → what to connect here or study next'));
    const list=make('ol','');lesson.courseConnections.forEach(c=>{const row=make('li',''),a=make('a','',c.title);a.href=c.url;row.append(a,make('p','',c.connection));const local=make('a','','Continue in our related concept lesson →');local.href=c.local;row.append(local);list.append(row);});catalog.append(list);map.append(catalog);
    const recall=make('details','');recall.append(make('summary','','Recall the 4Ds before designing another scenario'));
    [['Delegation','What may Claude do, and what must code or a person own?'],['Description','Have I specified the task, context, constraints and success criteria?'],['Discernment','What evidence lets me judge the output and its limits?'],['Diligence','Am I handling access, accountability and consequences responsibly?']].forEach(([name,text])=>recall.append(make('h3','',name),make('p','',text)));
    recall.append(make('p','','These are connected collaboration competencies, not four API operations or additional exam domains.'));const ref=make('a','','Anthropic AI Fluency framework');ref.href='https://www.anthropic.com/ai-fluency/overview';recall.append(ref);map.append(recall);player.after(map);
  }
  if(pilot&&lesson.pathApplications){
    const prelude=make('section','vl-design-chapter');prelude.id='architecture-design-start';prelude.append(make('p','vl-eyebrow','Before the first request'),make('h2','',lesson.designTitle||('Choose the design: '+lesson.title)),make('p','',lesson.designIntro||'The technician already uses an authenticated maintenance application. The first job is one approved manual and a cited explanation. Decide the surface, capabilities and scope before adding an agent framework. These are proposed design choices, not an executed service.'));
    const flow=make('ol','vl-service-route');(lesson.overviewRoute||['Technician application · sends question','Backend · checks access and prepares context','Approved model endpoint · interprets supplied evidence','Backend · checks support or preserves the gap','Technician application · displays answer and sources']).forEach(text=>flow.append(make('li','',text)));const jump=make('a','vl-start-now','Start with the evolving diagram →');jump.href='#visual-diagram';prelude.append(jump);prelude.append(flow,make('p','vl-context-label',lesson.overviewNote||'The application owns permitted evidence and service access. This is a proposed design, not an executed trace; conditional paths depend on their stated requirements.'));
    const grid=make('div','vl-pattern-grid');lesson.pathApplications.filter(row=>row.where==='before').forEach(row=>grid.append(patternCard(row,false,true)));prelude.append(grid);(lesson.designReviewQuestions||[]).filter(q=>q.position==='before').forEach(q=>{const optional=make('details','vl-optional-design');optional.append(make('summary','','Optional: challenge the initial integration choice'),designQuestion(q));prelude.append(optional);});const start=make('a','','Continue: watch the design fail and improve →');start.href='#visual-diagram';prelude.append(start);player.before(prelude);
    const delivery=make('section','vl-design-chapter');delivery.id='architecture-production-review';delivery.append(make('p','vl-eyebrow','After the '+lesson.stages.length+' learning layers'),make('h2','',lesson.deliveryTitle||'Build, deploy and prove the design works'),make('p','',lesson.deliveryIntro||'A sound explanation is a starting point. Now turn the same Atlas case into an implementation and delivery plan: verify code, endpoint boundaries, user outcomes and unresolved risks. No API, cloud account or command execution is required for this paper design review.'));
    const post=make('div','vl-pattern-grid');lesson.pathApplications.filter(row=>row.where==='after').forEach(row=>post.append(patternCard(row,false,true)));delivery.append(post);(lesson.designReviewQuestions||[]).filter(q=>q.position==='after').forEach(q=>{const challenge=make('details','vl-optional-design');challenge.append(make('summary','','Optional: test the changed deployment constraint'),designQuestion(q));delivery.append(challenge);});const again=make('a','','Return to the evolving architecture ↑');again.href='#visual-diagram';delivery.append(again);document.querySelector('.vl-course-connections').before(delivery);
  }
  render();openDeepLink();
})();
