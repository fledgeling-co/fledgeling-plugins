"""Generate the one-page HTML question form the person fills in.

    python3 build_form.py --spec questions.json --out questions.html \
        --title "Jane Doe — résumé questions" --key jane-resume-v1

One file, no network, no dependencies: the person opens it, answers, and presses Copy or
Download. Answers persist in localStorage under --key so a half-finished form survives a
closed tab.

Four things make it answerable rather than homework, and all four came out of the source
session: a suggested default on a multiple-choice question, marked and sourced, so the
person is confirming rather than composing; tap-to-fill example answers under every free-text
field, so a blank box is never the only option; a "why this is being asked" line per
question, which is where the research citation goes; and a visible count of questions the
person has looked at. The count is of questions touched, not questions with a value: a form
whose suggested defaults are pre-selected would otherwise read as finished before it is opened.
A suggested default the person never touched is exported as `[suggested default, not touched]`.

An example the person taps and leaves unchanged is their answer. The copied transcript marks
it `[example text, unchanged]` so you can see which answers were composed and which were
selected — not so you can discount them. In the source session fifteen answers came back as
unchanged examples, were treated as unverified, and the person's relay overturned that in one sentence. Ask before assuming.

`questions.json`:

    {"questions": [
      {"section": "Your current role",
       "q": "Which of these describes what you own?",
       "why": "Three of the five ads ask for backlog ownership. From your LinkedIn export.",
       "multi": false,
       "options": [["One backlog in a squad", "suggested", "from your answers, 14 Nov"],
                   ["The squad's whole backlog", "", ""]],
       "fields": [["What the team delivered", "", "your résumé",
                   ["Example answer one", "Example answer two"]]]}
    ]}

An option is [label, "suggested" or "", source note]. A field is [label, prefilled value,
source note, [examples]]. A field becomes a textarea when its label is over 60 characters or
asks for a sentence, a result or an outcome.
"""
import json, html, re, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--title", required=True)
ap.add_argument("--key", required=True, help="localStorage key, e.g. jane-resume-v1")
ap.add_argument("--intro", default="Answer what you can. Anything you skip stays a gap "
                                   "rather than being guessed at.")
ap.add_argument("--download-name", default="answers.txt")
a = ap.parse_args()

spec = json.load(open(a.spec))
def js_json(value):
    """JSON that is safe inside a <script> block: a question containing "</script>" or "<!--"
    would otherwise end the script and run as markup."""
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


Q = js_json(spec["questions"])

CSS = """
:root{--ink:#16181D;--ink2:#3D4350;--ink3:#C3C8D2;--bg:#F6F7F9;--blue:#1F2B5B;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
main,.q,.f{min-width:0}
main{max-width:720px;margin:0 auto;padding:24px 16px 120px}
h1{font-size:26px;line-height:1.2;margin:0 0 8px;color:var(--blue)}
.intro{color:var(--ink2);margin:0 0 24px}
h2{font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:var(--blue);
 margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--ink3)}
.q{background:var(--card);border:1px solid var(--ink3);border-radius:10px;
 padding:16px 16px 12px;margin:0 0 14px}
.qt{font-weight:600;margin:0 0 4px}
.why{color:var(--ink2);font-size:14px;margin:0 0 12px}
label.o{display:flex;gap:10px;align-items:flex-start;padding:8px 10px;border-radius:7px;
 cursor:pointer}
label.o:hover{background:#F0F2F6}
label.o input{margin-top:4px}
.f{margin:12px 0 4px}
.f label{display:block;font-size:14px;color:var(--ink2);margin-bottom:5px}
.f span{overflow-wrap:anywhere}
input[type=text],textarea{width:100%;min-width:0;font:inherit;padding:10px 12px;
 border:1px solid var(--ink3);border-radius:6px;background:#fff;color:var(--ink)}
textarea{min-height:72px;resize:vertical}
input:focus-visible,textarea:focus-visible,button:focus-visible,
label.o:focus-within{outline:2px solid var(--blue);outline-offset:2px}
.rec{display:inline-block;margin-left:8px;padding:1px 7px;border-radius:99px;
 background:#E4EAFB;color:var(--blue);font-size:12px;font-weight:600}
.src{display:block;color:var(--ink2);font-size:12.5px}
.ex{margin-top:8px}
.exl{display:block;color:var(--ink2);font-size:13px;margin-bottom:6px}
.exb{display:block;width:100%;text-align:left;font:inherit;font-size:14px;margin-bottom:6px;
 padding:8px 10px;border:1px dashed var(--ink3);border-radius:6px;background:#FBFCFE;
 color:var(--ink2);cursor:pointer}
.exb:hover{background:#F0F2F6;color:var(--ink)}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--card);
 border-top:1px solid var(--ink3);padding:12px 16px;display:flex;gap:10px;align-items:center;
 justify-content:center;flex-wrap:wrap}
.bar span{color:var(--ink2);font-size:14px;margin-right:auto}
.bar button{font:inherit;padding:9px 16px;border-radius:7px;border:1px solid var(--ink3);
 background:#fff;cursor:pointer}
.bar button.p{background:var(--blue);border-color:var(--blue);color:#fff}
@media (max-width:620px){.bar span{width:100%;margin:0 0 6px}.bar button{flex:1}}
"""

JS = """
const Q=__Q__, K=__KEY__, TITLE=__TITLE__, DL=__DL__;
let A={};try{A=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
const T=A._touched||(A._touched={});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const longField=f=>f[0].length>60||/sentence|result|evidence|outcome|what you|happened/i.test(f[0]);
let h="",sec="";
Q.forEach((q,i)=>{
  if(q.section&&q.section!==sec){sec=q.section;h+=`<h2>${esc(sec)}</h2>`}
  h+=`<div class="q" data-i="${i}"><p class="qt">${i+1}. ${esc(q.q)}</p>`;
  if(q.why)h+=`<p class="why">${esc(q.why)}</p>`;
  (q.options||[]).forEach((o,j)=>{
    const id=`q${i}o${j}`;
    const on=id in A?A[id]:o[1]==="suggested";
    h+=`<label class="o"><input type="${q.multi?"checkbox":"radio"}" name="q${i}" id="${id}"`
      +`${on?" checked":""}><span>${esc(o[0])}`
      +`${o[1]==="suggested"?'<span class="rec">suggested</span>':""}`
      +`${o[2]?`<span class="src">${esc(o[2])}</span>`:""}</span></label>`});
  (q.fields||[]).forEach((f,j)=>{
    const id=`q${i}f${j}`, v=id in A?A[id]:(f[1]||"");
    h+=`<div class="f"><label for="${id}"><span>${esc(f[0])}`
      +`${f[2]?`<span class="src">default from ${esc(f[2])}</span>`:""}</span></label>`
      +(longField(f)?`<textarea id="${id}">${esc(v)}</textarea>`
                    :`<input type="text" id="${id}" value="${esc(v)}">`)
      +((f[3]||[]).length?`<div class="ex" role="group" aria-label="Examples for ${esc(f[0])}">`
        +`<span class="exl">Examples, tap to use then edit:</span>`
        +f[3].map(x=>`<button type="button" class="exb" data-for="${id}">${esc(x)}</button>`).join("")
        +`</div>`:"")+`</div>`});
  h+="</div>"});
document.getElementById("qs").innerHTML=h;
const EX={};
Q.forEach((q,i)=>(q.fields||[]).forEach((f,j)=>{EX[`q${i}f${j}`]=f[3]||[]}));
function collect(){
  let out=TITLE+"\\n\\n",n=0;
  Q.forEach((q,i)=>{
    const lines=[];
    (q.options||[]).forEach((o,j)=>{const e=document.getElementById(`q${i}o${j}`);
      A[e.id]=e.checked;
      if(e.checked)lines.push("  [x] "+o[0]+(o[1]==="suggested"&&!T[i]?"  [suggested default, not touched]":""))});
    (q.fields||[]).forEach((f,j)=>{const e=document.getElementById(`q${i}f${j}`);
      A[e.id]=e.value; const v=e.value.trim();
      if(v){const tag=(EX[e.id]||[]).some(x=>x.trim()===v)?"  [example text, unchanged]":"";
        lines.push("  "+f[0]+": "+v+tag)}});
    if(T[i])n++;
    out+=`${i+1}. ${q.q}\\n${lines.join("\\n")||"  (not answered)"}\\n\\n`});
  try{localStorage.setItem(K,JSON.stringify(A))}catch(e){}
  document.getElementById("count").textContent=`${n} of ${Q.length} looked at`;
  return out}
const touch=e=>{const c=e.target.closest&&e.target.closest(".q");
  if(c&&e.target.closest("input,textarea,label,button")){T[c.dataset.i]=1}};
document.addEventListener("input",e=>{touch(e);collect()});
document.addEventListener("click",e=>{
  touch(e);
  if(e.target.classList.contains("exb")){
    const f=document.getElementById(e.target.dataset.for);
    f.value=e.target.textContent; f.focus();
    f.dispatchEvent(new Event("input",{bubbles:true}))}
  else if(e.target.closest(".q"))collect()});
document.getElementById("copy").onclick=async e=>{
  const t=collect();
  try{await navigator.clipboard.writeText(t);e.target.textContent="Copied"}
  catch(x){e.target.textContent="Copy failed: use Download"}
  setTimeout(()=>e.target.textContent="Copy answers",2500)};
document.getElementById("dl").onclick=()=>{
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([collect()],{type:"text/plain"}));
  a.download=DL;a.click()};
collect();
"""

js = (JS.replace("__Q__", Q)
        .replace("__KEY__", js_json(a.key))
        .replace("__TITLE__", js_json(a.title))
        .replace("__DL__", js_json(a.download_name)))

open(a.out, "w").write(
    f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
    f'<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{html.escape(a.title)}</title><style>{CSS}</style></head><body>\n'
    f'<main><h1>{html.escape(a.title)}</h1>'
    f'<p class="intro">{html.escape(a.intro)}</p><div id="qs"></div></main>\n'
    f'<div class="bar"><span id="count">0 looked at</span>'
    f'<button class="p" id="copy" type="button">Copy answers</button>'
    f'<button id="dl" type="button">Download as text</button></div>\n'
    f'<script>{js}</script></body></html>')
print(f"wrote {a.out}  questions={len(spec['questions'])}  "
      f"examples={sum(len(f[3]) if len(f) > 3 else 0 for q in spec['questions'] for f in q.get('fields', []))}")
