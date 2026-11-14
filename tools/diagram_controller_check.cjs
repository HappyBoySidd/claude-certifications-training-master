// Run from repository root: node tools/diagram_controller_check.cjs
// Executes the actual controller with synthetic geometry. Does not assert browser/CSS acceptance.
const fs = require('fs'), vm = require('vm');
const source = fs.readFileSync('site/assets/viewer.js', 'utf8');
const start = source.indexOf('  function controller(');
const end = source.indexOf('\n  function toolbar(', start);
if (start < 0 || end < 0) throw Error('Controller extraction boundary changed');
const viewport = {innerHeight:900, innerWidth:1200, ResizeObserver:true};
const context = {
  window:viewport,
  getComputedStyle:()=>({paddingLeft:'16px',paddingRight:'16px'}),
  ResizeObserver:class {observe(){}}, STEP:1.25, MIN:.2, MAX:4,
  MAXH:()=>Math.max(260,Math.min(viewport.innerHeight*.7,640))
};
vm.createContext(context);
vm.runInContext(source.slice(start,end),context);
function make(width,naturalWidth,naturalHeight,modal=false,nodeCenter=null) {
  const classes = new Set();
  const status = {textContent:''};
  const svg = {viewBox:{baseVal:{width:naturalWidth,height:naturalHeight}},style:{},removeAttribute(){},
    querySelector:()=>nodeCenter===null?null:{getBoundingClientRect:()=>({left:101+nodeCenter-frame.scrollLeft-10,width:20})}};
  const frame = {clientWidth:width,clientLeft:1,scrollTop:0,addEventListener(){},closest:()=>modal?{}:null,
    getBoundingClientRect:()=>({left:100}),
    classList:{toggle(name,on){if(on)classes.add(name);else classes.delete(name);}}};
  let offset=0;
  Object.defineProperty(frame,'scrollLeft',{get:()=>offset,set:value=>{
    const rendered=parseFloat(svg.style.width)||0;
    offset=Math.max(0,Math.min(Math.max(0,rendered+32-frame.clientWidth),value));
  }});
  return {c:context.controller(frame,()=>svg,status),svg,status,frame,classes};
}
const results=[];
function check(name,condition){if(!condition)throw Error(name);results.push({name,result:'PASS'});}
let sample=make(800,300,1800);sample.c.reset();
check('vertical starts natural reading size',sample.c.scale===1&&sample.svg.style.width==='300px'&&sample.status.textContent.includes('scroll inside'));
check('portrait classification follows natural aspect',sample.classes.has('dv-portrait'));
sample.c.fit();
check('explicit overview bounds dimensions and warns',sample.c.scale<=768/300&&sample.c.scale<.85&&sample.status.textContent.includes('zoom in to read'));
sample.c.zoom(1.25);let scale=sample.c.scale;sample.c.refresh();
check('chosen zoom retained',scale===sample.c.scale);
sample=make(200,1000,500);sample.c.reset();
check('narrow frame keeps85percent floor',sample.c.scale===.85&&sample.svg.style.width==='850px');
check('landscape has no portrait class',!sample.classes.has('dv-portrait'));
sample=make(900,600,2000,true);sample.c.fit();let first=sample.c.scale;viewport.innerHeight=600;sample.c.refresh();
check('modal fit reevaluates viewport height',sample.c.scale<first);
sample=make(0,400,500);sample.c.reset();
check('hidden frame defers sizing',!sample.svg.style.width);
sample.frame.clientWidth=800;sample.c.refresh();
check('revealed frame initializes',sample.svg.style.width==='400px');
sample=make(200,1000,500,false,600);sample.c.reset();
check('reading reset centers first flow node',sample.frame.scrollLeft===500);
sample.c.refresh();check('repeated initial refresh does not accumulate offset',sample.frame.scrollLeft===500);
sample.frame.scrollLeft=350;sample.c.zoom(1.25);sample.c.refresh();
check('manual zoom does not recenter node',sample.frame.scrollLeft===350);
sample.c.reset();check('explicit reset restores first node and top',sample.frame.scrollLeft===500&&sample.frame.scrollTop===0);
sample=make(200,1000,500,false,2000);sample.c.reset();
check('browser scroll bounds clamp far right',sample.frame.scrollLeft===682);
sample=make(200,1000,500,false,0);sample.c.reset();
check('browser scroll bounds clamp far left',sample.frame.scrollLeft===0);
sample=make(200,2000,10000);sample.c.fit(); const tinyFit=sample.c.scale;sample.c.zoom(.8);
check('zoom out never enlarges an overview below manual minimum',sample.c.scale<=tinyFit);
console.log(JSON.stringify({passed:results.length,scope:'Synthetic controller geometry only',results},null,2));
