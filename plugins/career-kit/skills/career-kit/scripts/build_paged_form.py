"""Build a one-question-per-screen answer form for a phone from the same spec build_form.py reads.

    python3 build_paged_form.py --spec questions.json --out questions.html \
        --title "Jane Doe — résumé questions" --key jane-resume-r2-v1 \
        --download-name jane-answers-round-two.txt --send-to Sam --intro "First paragraph" --intro "Second"

Screens: a start screen, one screen per question, and a review screen with Send answers (the
phone's share sheet, falling back to a box to copy). Progress and Download sit in the header on
every screen; the forward action is a full-width button at the bottom. Answers persist in
localStorage under --key, and the transcript has the same format as build_form.py's, so the
same reading rules apply to both.

Built in the source session after the person answered round five on a phone and asked for the
next form "as one question per screen"; rounds six and seven used it and came back complete.

Spec extensions over build_form.py:
- A wording question whose "why" reads "Now: … Suggested: … Why: …" shows the current line and
  the suggestion as two panels, each with a button that quotes it into the notes box.
- An option marked "recommended" (instead of "suggested") gets a Recommended label and is NOT
  selected; the question's "rec" string is shown beneath the options as the reason. A question
  with "rec" and no recommended option shows the reason under "No recommendation", for facts
  only the person knows. The transcript tags a chosen recommendation "[the recommended answer]".
- "suggested" still pre-selects, and an untouched one is exported as
  "[suggested default, not touched]".

Look: paper ground, white surfaces, hairlines, a forest accent, IBM Plex Sans and Mono, an ink
header band and 4px corners. The page loads Plex from ./fonts/ when that folder sits beside it
and falls back to the system sans when it does not.
"""
import argparse, html, json

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--title", required=True)
ap.add_argument("--key", required=True)
ap.add_argument("--download-name", default="answers.txt")
ap.add_argument("--intro", action="append", default=[])
ap.add_argument("--send-to", default="the person who sent you this form",
                help="who the answers go to, as the review screen names them, e.g. \"Sam\"")
a = ap.parse_args()

questions = json.load(open(a.spec, encoding="utf-8"))["questions"]
intro = "".join(f'<p class="lede">{html.escape(p)}</p>' for p in a.intro)
title = html.escape(a.title)
data = json.dumps(questions, ensure_ascii=False).replace("</", "<\\/")

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111615">
<title>__TITLE__</title><style>
@font-face{font-family:"IBM Plex Sans";src:url(fonts/ibm-plex-sans-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"IBM Plex Sans";src:url(fonts/ibm-plex-sans-latin-500-normal.woff2) format("woff2");font-weight:500;font-display:swap}
@font-face{font-family:"IBM Plex Sans";src:url(fonts/ibm-plex-sans-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"IBM Plex Sans";src:url(fonts/ibm-plex-sans-latin-700-normal.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"IBM Plex Mono";src:url(fonts/ibm-plex-mono-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"IBM Plex Mono";src:url(fonts/ibm-plex-mono-latin-500-normal.woff2) format("woff2");font-weight:500;font-display:swap}
:root{
 --bg:#faf8f4;--surface:#fff;--surface-alt:#f2efe8;
 --ink:#111615;--ink2:#49524f;--muted:#616b67;
 --line:#ded8cc;--line-strong:#c4bdb0;
 --accent:#14533c;--accent-hover:#0e3d2c;--accent-soft:#eaf3ef;
 --warn:#78350f;--warn-bg:#fef3c7;
 --paper-dim:rgba(250,248,244,.72);--paper-hover:rgba(250,248,244,.12);
 --r:4px;--s1:4px;--s2:8px;--s3:16px;--s4:24px;
 --sans:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
 --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
 --ease:cubic-bezier(.2,.7,.2,1)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:88px;scroll-padding-bottom:120px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans);-webkit-tap-highlight-color:transparent}
::selection{background:var(--accent-soft);color:var(--ink)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
[hidden]{display:none!important}

/* header band */
.top{position:sticky;top:0;z-index:3;background:var(--ink);color:var(--bg)}
.row{max-width:720px;margin:0 auto;display:grid;grid-template-columns:44px minmax(0,1fr) auto;align-items:center;
 gap:var(--s2);padding:var(--s1) var(--s2) 0}
.icon,.dl{font:inherit;color:var(--bg);background:var(--ink);border:0;min-height:44px;cursor:pointer;border-radius:var(--r);
 display:inline-flex;align-items:center;justify-content:center;gap:6px;transition:background .15s var(--ease)}
.icon{width:44px}
.icon.off{visibility:hidden}
.dl{padding:0 10px;font-size:14px;font-weight:600;letter-spacing:.01em}
.pos{margin:0;text-align:center;font:500 13px/1 var(--mono);letter-spacing:.08em;color:var(--paper-dim);background:var(--ink);text-transform:uppercase}
.pos b{color:var(--bg);background:var(--ink);font-weight:500}
.segs{max-width:720px;margin:0 auto;display:flex;gap:3px;align-items:center;height:22px;padding:0 var(--s3) 8px}
.seg{flex:1;height:4px;border-radius:1px;background:var(--muted);transition:height .15s var(--ease),background .15s var(--ease)}
.seg.done{background:var(--bg)}
.seg.cur{height:10px;background:var(--paper-dim)}
.seg.cur.done{background:var(--bg)}

/* screens */
main{max-width:720px;margin:0 auto;padding:var(--s4) var(--s3) 120px}
h1{font-size:clamp(30px,8vw,40px);line-height:1.08;letter-spacing:-.025em;font-weight:700;margin:0 0 var(--s3);text-wrap:balance}
.lede{color:var(--ink2);margin:0 0 var(--s3);max-width:62ch}
.inside{margin:var(--s4) 0 0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.inside li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:var(--s2);padding:12px 0;border-bottom:1px solid var(--line)}
.n{font:500 13px/1.9 var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink2);margin:0 0 var(--s2)}
.qt{font-size:24px;line-height:1.25;letter-spacing:-.02em;font-weight:700;margin:0 0 var(--s3);text-wrap:pretty}
.well{background:var(--surface-alt);border-radius:var(--r);padding:12px 14px;margin:0 0 var(--s2)}
.well p{margin:0}
.well.sug{background:var(--accent-soft)}
.wk{display:block;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
.sug .wk{color:var(--accent)}
.why{color:var(--ink2);font-size:15px;margin:var(--s3) 0}
.why .wk{display:inline;margin-right:6px}
.hint{font-size:13px;color:var(--muted);margin:var(--s4) 0 var(--s2)}

/* options */
.opts{display:grid;gap:var(--s2)}
.o{position:relative;display:grid;grid-template-columns:28px minmax(0,1fr);gap:12px;align-items:start;min-height:56px;
 padding:14px 14px;background:var(--surface);border:1px solid var(--line-strong);border-radius:var(--r);cursor:pointer;
 transition:border-color .15s var(--ease),box-shadow .15s var(--ease),background .15s var(--ease)}
.o input{position:absolute;inset:0;opacity:0;margin:0;cursor:pointer}
.key{display:grid;place-items:center;width:28px;height:28px;border:1px solid var(--line-strong);border-radius:var(--r);
 font:500 13px/1 var(--mono);color:var(--ink2);background:var(--bg);transition:background .15s var(--ease),color .15s var(--ease)}
.o .t{padding-top:2px}
.o.on{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.o.on .key{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.o:active{background:var(--surface-alt)}
.o:has(input:focus-visible){outline:2px solid var(--accent);outline-offset:2px}
.o.rec{border-color:var(--accent)}
.rtag{display:inline-block;margin:0 0 4px;font:600 11px/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);
 background:var(--accent-soft);border-radius:var(--r);padding:4px 6px}
.o .t .rtag{display:table}
.recwhy{font-size:15px;color:var(--ink2);background:var(--accent-soft);border-radius:var(--r);padding:12px 14px;margin:var(--s2) 0 0}
.recwhy.none{background:var(--surface-alt)}
.recwhy .wk{color:var(--accent)}
.recwhy.none .wk{color:var(--muted)}
.orow{display:grid}
.cp{justify-self:start;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 4px;margin:0 0 -6px -4px;
 font:inherit;font-size:14px;font-weight:600;color:var(--accent);background:none;border:0;border-radius:var(--r);cursor:pointer}
.cp span{text-decoration:underline;text-underline-offset:3px}
.well .cp{margin:2px 0 -10px -4px}

/* fields */
.f{margin:var(--s4) 0 0}
.f label{display:block;font-size:14px;font-weight:600;color:var(--ink2);margin-bottom:6px}
input[type=text],textarea{width:100%;min-width:0;font:inherit;font-size:16px;color:var(--ink);background:var(--surface);
 border:1px solid var(--line-strong);border-radius:var(--r);padding:12px 14px;transition:border-color .15s var(--ease)}
input[type=text]{min-height:56px;font-family:var(--mono)}
textarea{min-height:176px;resize:vertical;line-height:1.55}
input[type=text]:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
::placeholder{color:var(--muted)}

/* review */
.sum{display:flex;flex-wrap:wrap;gap:var(--s2);margin:0 0 var(--s3)}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:4px 10px;border-radius:var(--r)}
.chip.ok{background:var(--accent-soft);color:var(--accent)}
.chip.no{background:var(--warn-bg);color:var(--warn)}
.rev{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink)}
.rev li{display:grid;grid-template-columns:36px minmax(0,1fr);gap:var(--s2);padding:14px 0 10px;border-bottom:1px solid var(--line)}
.rq{margin:0 0 4px;font-size:14px;color:var(--ink2)}
.ra{margin:0;font-weight:600;white-space:pre-wrap}
.foot{display:flex;align-items:center;gap:var(--s2);margin-top:var(--s2)}
.chg{font:inherit;font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);background:var(--surface);
 border:1px solid var(--ink);border-radius:var(--r);min-height:44px;padding:0 14px;margin-left:auto;flex:none;cursor:pointer;
 transition:background .15s var(--ease),color .15s var(--ease)}
.status{margin:var(--s3) 0 0;font-weight:600;color:var(--accent)}
.status:empty{margin:0}
#out textarea{min-height:260px;font:13px/1.5 var(--mono)}

/* action bar */
.bar{position:fixed;left:0;right:0;bottom:0;z-index:3;background:var(--bg);border-top:1px solid var(--line);padding:12px var(--s3)}
.bar .in{max-width:688px;margin:0 auto}
.btns{display:flex;gap:var(--s2)}
.nudge{margin:0 0 var(--s2);font-size:14px;font-weight:600;color:var(--warn)}
.nudge:empty{margin:0}
.btn{width:100%;min-height:56px;font:inherit;font-size:17px;font-weight:600;color:#fff;background:var(--accent);border:0;
 border-radius:var(--r);cursor:pointer;display:flex;align-items:center;justify-content:space-between;padding:0 20px;
 transition:background .15s var(--ease)}
.btn:active{background:var(--accent-hover)}
.btn svg{flex:none}
.btn{flex:1}
.btn[aria-disabled=true]{background:var(--surface-alt);color:var(--ink2);box-shadow:inset 0 0 0 1px var(--line-strong);cursor:not-allowed}
.skip{flex:none;min-height:56px;padding:0 22px;font:inherit;font-size:17px;font-weight:600;color:var(--ink);
 background:var(--surface);border:1px solid var(--ink);border-radius:var(--r);cursor:pointer;transition:background .15s var(--ease)}
.skip:active{background:var(--surface-alt)}
body.kb textarea:not([readonly]){max-height:max(120px,calc(var(--vvh,100vh) - 220px));overflow:auto}
body.kb .top{position:static}
body.kb main{padding-bottom:calc(var(--kbh,0px) + 140px)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.top button:focus-visible{outline-color:var(--bg)}
@media (hover:hover){
 .icon:hover,.dl:hover{background:var(--paper-hover)}
 .o:hover{border-color:var(--ink2)}
 .btn:hover{background:var(--accent-hover)}
 .chg:hover{background:var(--ink);color:var(--bg)}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
@media (hover:hover){.skip:hover{background:var(--surface-alt)}.btn[aria-disabled=true]:hover{background:var(--surface-alt)}}
</style></head><body>
<header class="top"><div class="row">
<button class="icon" id="back" type="button" aria-label="Previous screen"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>
<p class="pos" id="pos"></p>
<button class="dl" id="dl" type="button"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>Download</button>
</div><div class="segs" id="segs" aria-hidden="true"></div></header>
<main id="screens"><section class="screen" id="s-start" data-state="start" hidden>
<h1 tabindex="-1">__TITLE__</h1>__INTRO__<ul class="inside" id="inside"></ul></section></main>
<div class="bar" id="bar"><div class="in"><p class="nudge" id="nudge" role="status"></p><div class="btns"><button class="skip" id="skip" type="button" hidden>Skip</button><button class="btn" id="next" type="button"><span id="nextL">Start</span><svg id="nextI" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></div></div></div>
<script>
const Q=__DATA__, K=__KEY__, TITLE=__TJS__, DL=__DLJS__;
let A={};try{A=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
const T=A._touched||(A._touched={});
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const pad=n=>String(n).padStart(2,"0");
const NEEDS_WORDS=/\((say|below)/i, NONE=/^None\b/;
const ORDER=["start",...Q.map((q,i)=>"q"+(i+1)),"review"];
const QUOTE_ICON='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7h4v4c0 3-1.4 5-4 6M14 7h4v4c0 3-1.4 5-4 6"/></svg>';
// Which field a quoted answer goes into: the question's Notes box, else its first free-text box.
const noteIdx=i=>{const fs=Q[i].fields||[];const n=fs.findIndex(f=>/^Notes/i.test(f[0]));return n>=0?n:fs.findIndex(f=>!/exact number/i.test(f[0]))};
// Instructions ("Something else (say in the note)") and bare Keep/None/Yes/No choices are not worth quoting.
const quotable=t=>!/\(/.test(t)&&!/^(Keep|None|No\b|Yes\b)/.test(t);
const cpBtn=(i,text,label,hide)=>`<button type="button" class="cp" data-q="${i}" data-text="${esc(text)}"${hide?" hidden":""}>${QUOTE_ICON}<span>${label}</span></button>`;
const quoted=t=>{t=t.trim().replace(/”[.,;:]$/,"”");return /^“[^“”]*”$/.test(t)?t:"“"+t.replace(/“/g,"‘").replace(/”/g,"’")+"”"};
function whyHtml(w,i){
  const m=w.match(/^Now:\s([\s\S]*?)(?:\sSuggested:\s([\s\S]*?))?\sWhy:\s([\s\S]*)$/);
  if(!m)return `<p class="why">${esc(w)}</p>`;
  const cp=t=>noteIdx(i)>=0?cpBtn(i,t,"Quote in your note",false):"";
  return `<div class="well"><span class="wk">Now</span><p>${esc(m[1])}</p>${cp(m[1])}</div>`
    +(m[2]?`<div class="well sug"><span class="wk">Suggested</span><p>${esc(m[2])}</p>${cp(m[2])}</div>`:"")
    +`<p class="why"><span class="wk">Why</span>${esc(m[3])}</p>`}
const secs=[];Q.forEach(q=>{const s=secs.find(x=>x.name===q.section);s?s.n++:secs.push({name:q.section,n:1})});
$("inside").innerHTML=secs.map(s=>`<li><span class="n">${pad(s.n)}</span><span>${esc(s.name)}</span></li>`).join("");
let h="";
Q.forEach((q,i)=>{
  h+=`<section class="screen" id="s-q${i+1}" data-i="${i}" data-state="question" hidden>`;
  if(q.section)h+=`<p class="eyebrow">${esc(q.section)}</p>`;
  h+=`<h2 class="qt" id="q${i}t" tabindex="-1"><span class="sr">Question ${i+1} of ${Q.length}. </span>${esc(q.q)}</h2>`;
  if(q.why)h+=whyHtml(q.why,i);
  h+=`<p class="hint" id="q${i}h">${q.multi?"Choose any that apply":"Choose one"}</p>`;
  h+=`<div class="opts" role="${q.multi?"group":"radiogroup"}" aria-labelledby="q${i}t" aria-describedby="q${i}h">`;
  (q.options||[]).forEach((o,j)=>{
    const id=`q${i}o${j}`, on=id in A?A[id]:o[1]==="suggested", rec=o[1]==="recommended";
    h+=`<div class="orow"><label class="o${on?" on":""}${rec?" rec":""}"><input type="${q.multi?"checkbox":"radio"}" name="q${i}" id="${id}"${on?" checked":""}>`
      +`<span class="key" aria-hidden="true">${String.fromCharCode(65+j)}</span><span class="t">${rec?'<span class="rtag">Recommended</span>':""}${esc(o[0])}${rec?'<span class="sr"> (recommended)</span>':""}</span></label>`
      +(quotable(o[0])&&noteIdx(i)>=0?cpBtn(i,o[0],"Quote this answer in your note",!on):"")+`</div>`});
  h+="</div>";
  // "recommended" marks an option and shows q.rec as the reason without selecting it; "suggested" pre-selects.
  if(q.rec){const r=(q.options||[]).findIndex(o=>o[1]==="recommended");
    h+=r>=0?`<p class="recwhy"><span class="wk">Why we recommend ${String.fromCharCode(65+r)}</span>${esc(q.rec)}</p>`
           :`<p class="recwhy none"><span class="wk">No recommendation</span>${esc(q.rec)}</p>`}
  (q.fields||[]).forEach((f,j)=>{
    const id=`q${i}f${j}`, v=id in A?A[id]:(f[1]||"");
    h+=`<div class="f"><label for="${id}">${esc(f[0])}</label>`
      +(/exact number/i.test(f[0])?`<input type="text" inputmode="numeric" id="${id}" value="${esc(v)}">`
                                   :`<textarea id="${id}">${esc(v)}</textarea>`)+`</div>`});
  h+="</section>"});
h+=`<section class="screen" id="s-review" data-state="review" hidden><p class="eyebrow">Before you send</p>`
  +`<h2 class="qt" id="revT" tabindex="-1">Check your answers</h2><div class="sum" id="sum"></div>`
  +`<p class="lede" id="revHelp">Press Change or Answer to go back to a question. When you are happy, press Send answers and choose how to send them to __SENDTO__.</p>`
  +`<p class="status" id="status" role="status"></p><ol class="rev" id="rev"></ol>`
  +`<div id="out" hidden><p class="lede">Sending didn't work on this phone. Press and hold in the box, choose Select All, `
  +`then Copy, and paste it into a message to __SENDTO__. Download also saves a copy.</p>`
  +`<textarea id="outText" readonly aria-label="Your answers, to copy"></textarea></div></section>`;
$("screens").insertAdjacentHTML("beforeend",h);
$("segs").innerHTML=Q.map(()=>'<span class="seg"></span>').join("");
const grow=e=>{if(e.tagName==="TEXTAREA"&&!e.readOnly){e.style.height="auto";e.style.height=Math.max(176,e.scrollHeight+2)+"px"}};
function answered(i){
  const q=Q[i];
  return (q.options||[]).some((o,j)=>$(`q${i}o${j}`).checked)
    ||(q.fields||[]).some((f,j)=>$(`q${i}f${j}`).value.trim())}
function lines(i){
  const q=Q[i], out=[];
  (q.options||[]).forEach((o,j)=>{if($(`q${i}o${j}`).checked)
    out.push("  [x] "+o[0]+(o[1]==="suggested"&&!T[i]?"  [suggested default, not touched]":"")+(o[1]==="recommended"?"  [the recommended answer]":""))});
  (q.fields||[]).forEach((f,j)=>{const v=$(`q${i}f${j}`).value.trim();if(v)out.push("  "+f[0]+": "+v)});
  return out}
let cur="start", fromReview=false;
function save(){
  Q.forEach((q,i)=>{
    (q.options||[]).forEach((o,j)=>{const e=$(`q${i}o${j}`);A[e.id]=e.checked;e.closest("label").classList.toggle("on",e.checked);
      const b=e.closest(".orow").querySelector(".cp");if(b)b.hidden=!e.checked});
    (q.fields||[]).forEach((f,j)=>{const e=$(`q${i}f${j}`);A[e.id]=e.value})});
  try{localStorage.setItem(K,JSON.stringify(A))}catch(e){}
  [...$("segs").children].forEach((s,i)=>{s.classList.toggle("done",answered(i));s.classList.toggle("cur",cur===`q${i+1}`)});
  updateFooter()}
function updateFooter(){
  const q=cur.startsWith("q"), ans=q&&answered(+cur.slice(1)-1), open=q&&!ans&&!fromReview;
  $("skip").hidden=!open;
  $("next").setAttribute("aria-disabled",open?"true":"false");
  if(!open)$("nudge").textContent=""}
function collect(){
  save();
  let out=TITLE+"\n\n";
  Q.forEach((q,i)=>{out+=`${i+1}. ${q.q}\n${lines(i).join("\n")||"  (not answered)"}\n\n`});
  return out}
const count=()=>Q.filter((q,i)=>answered(i)).length;
const ICON_OK='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>';
const ICON_NO='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5M12 16.5h.01"/></svg>';
function renderReview(){
  const n=count(), miss=Q.length-n;
  $("sum").innerHTML=`<span class="chip ok">${ICON_OK}${n} answered</span>`+(miss?`<span class="chip no">${ICON_NO}${miss} not answered</span>`:"");
  $("rev").innerHTML=Q.map((q,i)=>{const l=lines(i);
    return `<li><span class="n">${pad(i+1)}</span><div><p class="rq">${esc(q.q)}</p>`
      +(l.length?`<p class="ra">${esc(l.map(x=>x.trim().replace(/^\[x\] /,"")).join("\n"))}</p>`:"")
      +`<div class="foot">${l.length?"":`<span class="chip no">${ICON_NO}Not answered</span>`}`
      +`<button type="button" class="chg" data-go="q${i+1}" aria-label="${l.length?"Change answer to":"Answer"} question ${i+1}">${l.length?"Change":"Answer"}</button></div></div></li>`}).join("")}
function show(id){
  if(!ORDER.includes(id))id="start";
  if(id==="start")fromReview=false;
  document.querySelectorAll(".screen").forEach(s=>s.hidden=s.id!=="s-"+id);
  cur=id; A._at=id; save();
  const k=ORDER.indexOf(id);
  $("back").classList.toggle("off",k===0); $("back").disabled=k===0;
  $("pos").innerHTML=id==="start"?`${Q.length} questions`:id==="review"?"Review":`<b>${pad(k)}</b> / ${pad(Q.length)}`;
  let label;
  if(id==="start")label=count()?"Carry on":"Start";
  else if(id==="review"){label="Send answers";renderReview();$("status").textContent="";$("out").hidden=true;fromReview=false}
  else label=fromReview?"Back to review":k===Q.length?"Review answers":"Next";
  $("nextL").textContent=label;
  updateFooter();
  document.querySelectorAll(".screen:not([hidden]) textarea").forEach(grow);
  window.scrollTo(0,0);
  const head=document.querySelector(".screen:not([hidden]) [tabindex='-1']");if(head)head.focus({preventScroll:true})}
const go=id=>{if(location.hash==="#"+id)show(id);else location.hash=id};
window.addEventListener("hashchange",()=>show(location.hash.slice(1)));
document.addEventListener("change",e=>{
  const s=e.target.closest&&e.target.closest(".screen[data-i]");
  if(!s||e.target.type!=="radio"&&e.target.type!=="checkbox")return;
  const i=+s.dataset.i, q=Q[i], j=+e.target.id.split("o")[1], label=q.options[j][0];
  T[i]=1;
  if(q.multi&&e.target.checked)q.options.forEach((o,k)=>{
    if(k!==j&&(NONE.test(label)||NONE.test(o[0])))$(`q${i}o${k}`).checked=false});
  else if(e.target.checked&&NEEDS_WORDS.test(label)){const f=s.querySelector("textarea,input[type=text]");if(f)f.focus()}
  save()});
document.addEventListener("input",e=>{
  const s=e.target.closest&&e.target.closest(".screen[data-i]");if(s)T[s.dataset.i]=1;
  grow(e.target);save()});
document.addEventListener("click",e=>{
  const c=e.target.closest&&e.target.closest(".chg");if(c){fromReview=true;go(c.dataset.go);return}
  const b=e.target.closest&&e.target.closest(".cp");if(!b)return;
  const i=+b.dataset.q, f=$(`q${i}f${noteIdx(i)}`), add=quoted(b.dataset.text);
  f.value=f.value.trim()?f.value.replace(/\s+$/,"")+"\n"+add:add;
  T[i]=1; f.focus(); f.setSelectionRange(f.value.length,f.value.length); grow(f); save();
  const s=b.querySelector("span"), was=s.textContent; s.textContent="Added to your note";
  setTimeout(()=>{s.textContent=was},2000)});
// Keep the footer above the on-screen keyboard. iOS Safari and Chrome on Android shrink the visual
// viewport, not the layout one, so a bottom:0 bar would sit behind the keyboard; lift it by the gap.
const bar=$("bar"), head=document.querySelector(".top");
function placeBar(){
  const vv=window.visualViewport; if(!vv)return;
  const kb=Math.max(0,Math.round(document.documentElement.clientHeight-vv.height-vv.offsetTop));
  bar.style.transform=kb>1?`translateY(${-kb}px)`:"";
  document.body.classList.toggle("kb",kb>80);
  document.documentElement.style.setProperty("--vvh",vv.height+"px");
  document.documentElement.style.setProperty("--kbh",kb+"px");
  keepFieldVisible()}
function keepFieldVisible(){
  const el=document.activeElement;
  if(!el||!el.matches('input[type=text],textarea:not([readonly])'))return;
  const r=el.getBoundingClientRect(), top=bar.getBoundingClientRect().top, hb=document.body.classList.contains("kb")?0:head.getBoundingClientRect().bottom;
  if(r.bottom>top-8||r.top<hb)window.scrollBy(0,r.top-hb-(el.previousElementSibling?el.previousElementSibling.offsetHeight+14:12))}
if(window.visualViewport){visualViewport.addEventListener("resize",placeBar);visualViewport.addEventListener("scroll",placeBar)}
document.addEventListener("focusin",()=>setTimeout(keepFieldVisible,350));
$("back").onclick=()=>{const k=ORDER.indexOf(cur);if(k>0)go(ORDER[k-1])};
$("skip").onclick=()=>{const k=ORDER.indexOf(cur);if(k>0&&k<ORDER.length-1)go(ORDER[k+1])};
$("next").onclick=async()=>{
  if($("next").getAttribute("aria-disabled")==="true"){$("nudge").textContent="Choose an answer, or press Skip to leave this one blank.";return}
  const k=ORDER.indexOf(cur);
  if(cur==="start"){const i=Q.findIndex((q,x)=>!answered(x));go(count()&&i<0?"review":"q"+((count()?i:0)+1));return}
  if(cur!=="review"){go(fromReview?"review":ORDER[k+1]);return}
  const t=collect();
  if(navigator.share){
    try{await navigator.share({title:TITLE,text:t});$("status").textContent="Sent. If you change an answer, send again.";return}
    catch(x){if(x&&x.name==="AbortError")return}}
  try{await navigator.clipboard.writeText(t);
    $("status").textContent="Your answers are copied. Paste them into a message or email to __SENDTOJS__.";return}catch(x){}
  const o=$("out");o.hidden=false;$("outText").value=t;o.scrollIntoView({block:"start"});$("outText").focus();$("outText").select()};
$("dl").onclick=()=>{
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([collect()],{type:"text/plain"}));
  a.download=DL;document.body.appendChild(a);a.click();a.remove()};
const first=location.hash.slice(1)||A._at||"start";
history.replaceState(null,"","#"+(ORDER.includes(first)?first:"start"));
show(location.hash.slice(1));
</script></body></html>"""

# The name appears in HTML twice and once inside a JS string, so it is escaped for each.
send_html = html.escape(a.send_to)
send_js = json.dumps(a.send_to, ensure_ascii=False)[1:-1].replace("</", "<\\/")
out = (PAGE.replace("__SENDTOJS__", send_js).replace("__SENDTO__", send_html).replace("__TITLE__", title).replace("__INTRO__", intro).replace("__DATA__", data)
       .replace("__KEY__", json.dumps(a.key)).replace("__TJS__", json.dumps(a.title, ensure_ascii=False))
       .replace("__DLJS__", json.dumps(a.download_name)))
open(a.out, "w", encoding="utf-8").write(out)
print(f"wrote {a.out}: {len(questions)} questions, {len(out)} bytes")
