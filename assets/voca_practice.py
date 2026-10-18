"""Voca practice (MD-33 quiz) — Study-Apps 페이지에서 불러 쓰는 모듈입니다. 페이지가 아닙니다.

사용: Study-Apps 페이지가 ?app=voca 로 열리면 render()를 호출합니다.
화면(HTML)은 이 파일 맨 아래 HTML 변수에 들어 있어 별도 파일이 필요 없습니다.
데이터: assets/md33.csv 가 있으면 우선 사용, 없으면 구글 드라이브에서 내려받습니다.
"""
import csv
import io
import json
import urllib.request
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ASSETS = Path(__file__).resolve().parent
LOCAL_CSV = ASSETS / "md33.csv"
DRIVE_ID = "135Vhhudwg0Jv8Rixvam37n1Qss43NJd6"
DRIVE_URL = f"https://drive.google.com/uc?export=download&id={DRIVE_ID}"
COLUMNS = ["Initial", "SID", "Word", "POS", "WME", "WMK", "WIC", "WICK", "SEM-REL"]


def _embed(html: str, height: int) -> None:
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=height, scrolling=True)


def _parse_csv(text: str) -> list:
    reader = csv.DictReader(io.StringIO(text.lstrip("﻿")))
    reader.fieldnames = [(f or "").strip() for f in reader.fieldnames or []]
    missing = [c for c in COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ValueError(f"CSV is missing column(s): {', '.join(missing)}")
    rows = []
    for r in reader:
        row = {c: (r.get(c) or "").strip() for c in COLUMNS}
        if row["Word"]:
            rows.append(row)
    return rows


@st.cache_data
def _load_local(path: str, mtime: float) -> list:
    return _parse_csv(Path(path).read_text(encoding="utf-8-sig"))


@st.cache_data(ttl=3600)
def _load_drive() -> list:
    req = urllib.request.Request(DRIVE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        text = resp.read().decode("utf-8-sig")
    if text.lstrip().startswith("<"):
        raise ValueError("Google Drive returned a web page instead of the CSV. "
                         "Share the file as 'Anyone with the link'.")
    return _parse_csv(text)


def render() -> None:
    try:
        if LOCAL_CSV.exists():
            rows = _load_local(str(LOCAL_CSV), LOCAL_CSV.stat().st_mtime)
        else:
            rows = _load_drive()
    except Exception as e:
        st.error(f"Could not load the MD-33 data: {e}")
        return
    html = HTML.replace(
        "/*__DATA__*/[]", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    )
    _embed(html, 900)


# ---- 퀴즈 화면 (self-contained HTML) ----
HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Voca Practice</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;700&family=Noto+Sans+KR:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f6f4ef; --paper: #ffffff; --ink: #1b1b1b; --muted: #5d5a54; --line: #d9d4ca;
    --navy: #1b2a4e; --navy-ink: #ffffff; --yellow: #ffd84d; --soft: #eef2f8;
    --ok: #1d7a46; --ok-bg: #e7f5ec; --bad: #b3261e; --bad-bg: #fbeceb;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #151515; --paper: #1f1f1f; --ink: #ececec; --muted: #a7a39b; --line: #3a3a3a;
      --navy: #7fa8e6; --navy-ink: #0e1a2b; --soft: #22293a;
      --ok: #6fd39a; --ok-bg: #16301f; --bad: #f2928b; --bad-bg: #3a1c1a;
    }
  }
  :root[data-theme="dark"] {
    --bg: #151515; --paper: #1f1f1f; --ink: #ececec; --muted: #a7a39b; --line: #3a3a3a;
    --navy: #7fa8e6; --navy-ink: #0e1a2b; --soft: #22293a;
    --ok: #6fd39a; --ok-bg: #16301f; --bad: #f2928b; --bad-bg: #3a1c1a;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: "Noto Sans KR", system-ui, sans-serif; font-size: 16px; line-height: 1.6; }
  .wrap { max-width: 760px; margin: 0 auto; padding: 20px 14px 48px; }
  h1 { font-size: 1.3rem; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 0.9rem; margin: 0 0 14px; }
  .panel { background: var(--paper); border: 1px solid var(--line); border-radius: 12px; padding: 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
  label { display: block; font-size: 0.85rem; color: var(--muted); margin-bottom: 4px; }
  select, input[type=number] { font: inherit; width: 100%; color: var(--ink); background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 8px 10px; }
  .hint { font-size: 0.85rem; color: var(--muted); margin: 10px 0 0; }
  .btn { font: inherit; font-weight: 600; font-size: 0.95rem; border-radius: 8px; padding: 10px 18px; cursor: pointer; border: 1px solid var(--navy); background: var(--paper); color: var(--navy); }
  .btn.primary { background: var(--navy); color: var(--navy-ink); }
  .btn.small { border-color: var(--line); color: var(--ink); padding: 8px 14px; }
  .btn:disabled { opacity: 0.45; cursor: default; }
  .btn:focus-visible, select:focus, input:focus { outline: 2px solid var(--navy); outline-offset: 1px; }
  .row { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 16px; }
  .right { margin-left: auto; color: var(--muted); font-size: 0.9rem; }
  .clue { display: grid; gap: 8px; margin-bottom: 16px; }
  .clue div { background: var(--soft); border-radius: 10px; padding: 10px 14px; }
  .clue small { display: block; font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); }
  .clue .en { font-family: "Noto Serif", serif; font-size: 1.1rem; }
  .opts { display: grid; gap: 8px; }
  .opt { font: inherit; font-family: "Noto Serif", serif; font-size: 1.1rem; text-align: left; padding: 11px 14px; border: 1.5px solid var(--line); border-radius: 10px; background: var(--paper); color: var(--ink); cursor: pointer; }
  .opt:hover:not(:disabled) { border-color: var(--navy); }
  .opt.ok { border-color: var(--ok); background: var(--ok-bg); color: var(--ok); font-weight: 700; }
  .opt.bad { border-color: var(--bad); background: var(--bad-bg); color: var(--bad); }
  .opt:disabled { cursor: default; }
  .wic { margin-top: 14px; padding: 12px 14px; border-left: 4px solid var(--navy); background: var(--soft); border-radius: 0 10px 10px 0; font-family: "Noto Serif", serif; }
  .wic .ko { font-family: "Noto Sans KR", sans-serif; font-size: 0.9rem; color: var(--muted); margin-top: 4px; }
  .blank { display: inline-block; min-width: 4em; border-bottom: 1.5px solid var(--ink); }
  .msg { margin-top: 12px; padding: 10px 14px; border-radius: 8px; font-weight: 600; }
  .msg.ok { background: var(--ok-bg); color: var(--ok); }
  .msg.bad { background: var(--bad-bg); color: var(--bad); }
  .progress { height: 6px; background: var(--line); border-radius: 3px; overflow: hidden; margin-bottom: 16px; }
  .progress span { display: block; height: 100%; background: var(--navy); }
  .big { font-size: 2.2rem; font-weight: 700; text-align: center; margin: 6px 0; }
  .card-word { font-family: "Noto Serif", serif; font-size: 2rem; font-weight: 700; }
  .card-meta { color: var(--muted); font-size: 0.9rem; }
  dl.dict { margin: 14px 0 0; display: grid; grid-template-columns: max-content 1fr; gap: 8px 16px; }
  dl.dict dt { font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); padding-top: 3px; }
  dl.dict dd { margin: 0; }
  dl.dict dd.en { font-family: "Noto Serif", serif; }
  @media (max-width: 520px) { dl.dict { grid-template-columns: 1fr; gap: 2px; } dl.dict dd { margin-bottom: 8px; } }
  .error { color: var(--bad); }
  [hidden] { display: none !important; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Voca Practice</h1>
  <p class="sub">MD-33 vocabulary quiz: read the part of speech and meanings, then choose the word.</p>
  <section class="panel" id="stage"></section>
</div>

<script>
// Rows from the MD-33 CSV, injected by the Streamlit page.
// Columns: Initial, SID, Word, POS, WME, WMK, WIC, WICK, SEM-REL
const DATA = /*__DATA__*/[];

const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

const ROWS = DATA.map(r => ({ ...r, SID: Number(r.SID) })).filter(r => r.Word && !Number.isNaN(r.SID));
const INITIALS = [...new Set(ROWS.map(r => String(r.Initial || r.Word[0]).trim().toUpperCase()))].sort();
const ALL_WORDS = [...new Set(ROWS.map(r => r.Word.trim()))];
const st = { setup: { initial: "ALL", from: null, to: null, count: 10 }, quiz: [], i: 0, answered: null, showWic: false, results: [], review: [], ri: 0 };

function pool() {
  const s = st.setup;
  return ROWS.filter(r => (s.initial === "ALL" || String(r.Initial || r.Word[0]).trim().toUpperCase() === s.initial)
    && (s.from == null || r.SID >= s.from) && (s.to == null || r.SID <= s.to))
    .sort((a, b) => a.SID - b.SID);
}
function sidBounds(initial) {
  const rows = ROWS.filter(r => initial === "ALL" || String(r.Initial || r.Word[0]).trim().toUpperCase() === initial);
  const sids = rows.map(r => r.SID);
  return sids.length ? [Math.min(...sids), Math.max(...sids)] : [0, 0];
}

// Hide the target word (and simple inflections) in the example until the question is answered.
function maskWord(sentence, word) {
  let stem = word.trim();
  if (stem.length > 4 && /[ey]$/i.test(stem)) stem = stem.slice(0, -1);
  const rx = new RegExp(`\\b${stem.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\w*`, "gi");
  return esc(sentence).replace(rx, '<span class="blank">&nbsp;</span>');
}

// ---------- Setup ----------
function renderSetup() {
  if (!ROWS.length) { $("stage").innerHTML = `<p class="error">No vocabulary data was loaded. Check the CSV file.</p>`; return; }
  const s = st.setup;
  const [lo, hi] = sidBounds(s.initial);
  if (s.from == null || s.from < lo || s.from > hi) s.from = lo;
  if (s.to == null || s.to > hi || s.to < lo) s.to = hi;
  const n = pool().length;
  $("stage").innerHTML = `
    <div class="grid">
      <div><label for="ini">Alphabet</label><select id="ini"><option value="ALL">All letters</option>${INITIALS.map(x => `<option ${x === s.initial ? "selected" : ""}>${x}</option>`).join("")}</select></div>
      <div><label for="from">SID from</label><input type="number" id="from" min="${lo}" max="${hi}" value="${s.from}"></div>
      <div><label for="to">SID to</label><input type="number" id="to" min="${lo}" max="${hi}" value="${s.to}"></div>
      <div><label for="cnt">Number of questions</label><select id="cnt">${[5, 10, 20, 30, 50, 0].map(c => `<option value="${c}" ${c === s.count ? "selected" : ""}>${c || "All"}</option>`).join("")}</select></div>
    </div>
    <p class="hint">SID range for ${s.initial === "ALL" ? "all letters" : "letter " + s.initial}: ${lo}–${hi}. <strong>${n}</strong> word(s) in the selected range.</p>
    <div class="row"><button class="btn primary" id="start" ${n ? "" : "disabled"}>Start quiz</button></div>`;
  $("ini").onchange = e => { s.initial = e.target.value; s.from = s.to = null; renderSetup(); };
  $("from").onchange = e => { s.from = Number(e.target.value); renderSetup(); };
  $("to").onchange = e => { s.to = Number(e.target.value); renderSetup(); };
  $("cnt").onchange = e => { s.count = Number(e.target.value); };
  $("start").onclick = startQuiz;
}

// ---------- Quiz ----------
function startQuiz() {
  const p = shuffle(pool());
  const items = st.setup.count ? p.slice(0, st.setup.count) : p;
  st.quiz = items.map(row => {
    const wrong = shuffle(ALL_WORDS.filter(w => w.toLowerCase() !== row.Word.trim().toLowerCase())).slice(0, 4);
    return { row, options: shuffle([row.Word.trim(), ...wrong]) };
  });
  st.i = 0; st.results = []; st.answered = null; st.showWic = false;
  renderQuestion();
}

function renderQuestion() {
  const q = st.quiz[st.i], r = q.row, done = st.answered !== null;
  const pct = Math.round((st.i / st.quiz.length) * 100);
  const correct = st.results.filter(x => x.ok).length;
  let h = `<div class="progress"><span style="width:${pct}%"></span></div>
    <div class="row" style="margin-top:0;margin-bottom:12px"><strong>Question ${st.i + 1} of ${st.quiz.length}</strong><span class="right">Score: ${correct} / ${st.results.length}</span></div>
    <div class="clue">
      <div><small>POS</small>${esc(r.POS)}</div>
      <div><small>Meaning (English) · WME</small><span class="en">${esc(r.WME)}</span></div>
      <div><small>Meaning (Korean) · WMK</small>${esc(r.WMK)}</div>
    </div>
    <div class="opts">${q.options.map(o => {
      let cls = "";
      if (done) { if (o === r.Word.trim()) cls = "ok"; else if (o === st.answered) cls = "bad"; }
      return `<button class="opt ${cls}" data-o="${esc(o)}" ${done ? "disabled" : ""}>${esc(o)}</button>`;
    }).join("")}</div>`;
  if (st.showWic) {
    h += `<div class="wic">${r.WIC ? (done ? esc(r.WIC) : maskWord(r.WIC, r.Word)) : "<em>No example sentence for this word.</em>"}${done && r.WICK ? `<div class="ko">${esc(r.WICK)}</div>` : ""}</div>`;
  }
  if (done) {
    const ok = st.answered === r.Word.trim();
    h += `<div class="msg ${ok ? "ok" : "bad"}">${ok ? "✅ Correct!" : `❌ The answer is <strong>${esc(r.Word)}</strong>.`}</div>`;
  }
  h += `<div class="row"><button class="btn" id="wic">${st.showWic ? "Hide WIC" : "WIC (example)"}</button>`;
  if (done) h += `<button class="btn primary" id="next">${st.i === st.quiz.length - 1 ? "See results" : "Next"}</button>`;
  h += `<button class="btn small" id="quit">Quit</button><button class="btn small" id="setup">↺ Choose range</button></div>`;
  $("stage").innerHTML = h;

  $("stage").querySelectorAll(".opt").forEach(b => b.onclick = () => {
    st.answered = b.dataset.o;
    st.results.push({ row: r, ok: st.answered === r.Word.trim(), chosen: st.answered });
    renderQuestion();
  });
  $("wic").onclick = () => { st.showWic = !st.showWic; renderQuestion(); };
  if (done) $("next").onclick = () => {
    if (st.i === st.quiz.length - 1) return renderResults();
    st.i++; st.answered = null; st.showWic = false; renderQuestion();
  };
  $("quit").onclick = () => st.results.length ? renderResults() : renderSetup();
  $("setup").onclick = renderSetup;
}

// ---------- Results & review ----------
function renderResults() {
  const correct = st.results.filter(x => x.ok).length;
  st.review = st.results.filter(x => !x.ok).map(x => x.row);
  $("stage").innerHTML = `
    <p style="text-align:center;margin:0;color:var(--muted)">Your score</p>
    <div class="big">${correct} / ${st.results.length}</div>
    ${st.results.length < st.quiz.length ? `<p style="text-align:center;margin:0 0 6px;color:var(--muted)">Quit early: answered ${st.results.length} of ${st.quiz.length} questions.</p>` : ""}
    <p style="text-align:center;margin:0">${st.review.length ? `You missed ${st.review.length} word(s).` : "🎉 Perfect score!"}</p>
    <div class="row" style="justify-content:center">
      ${st.review.length ? `<button class="btn primary" id="review">Study missed words</button>` : ""}
      <button class="btn" id="again">↺ Choose range</button>
    </div>`;
  if (st.review.length) $("review").onclick = () => { st.ri = 0; renderCard(); };
  $("again").onclick = renderSetup;
}

function renderCard() {
  const r = st.review[st.ri];
  const field = (label, val, cls = "") => val ? `<dt>${label}</dt><dd class="${cls}">${esc(val)}</dd>` : "";
  $("stage").innerHTML = `
    <div class="row" style="margin-top:0;margin-bottom:10px"><strong>Missed word ${st.ri + 1} of ${st.review.length}</strong><span class="right">${esc(r.Initial)} · SID ${esc(r.SID)}</span></div>
    <div class="card-word">${esc(r.Word)}</div>
    <div class="card-meta">${esc(r.POS)}</div>
    <dl class="dict">
      ${field("Meaning (EN)", r.WME, "en")}
      ${field("Meaning (KO)", r.WMK)}
      ${field("Example", r.WIC, "en")}
      ${field("Example (KO)", r.WICK)}
      ${field("Related words", r["SEM-REL"], "en")}
    </dl>
    <div class="row">
      <button class="btn small" id="prev" ${st.ri === 0 ? "disabled" : ""}>← Previous</button>
      <button class="btn primary" id="nextc">${st.ri === st.review.length - 1 ? "Finish" : "Next →"}</button>
      <button class="btn small" id="setup" style="margin-left:auto">↺ Choose range</button>
    </div>`;
  $("prev").onclick = () => { st.ri--; renderCard(); };
  $("setup").onclick = renderSetup;
  $("nextc").onclick = () => { if (st.ri === st.review.length - 1) return renderResults(); st.ri++; renderCard(); };
}

renderSetup();
</script>
</body>
</html>
'''
