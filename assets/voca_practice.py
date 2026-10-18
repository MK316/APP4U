"""Voca practice (MD-33 quiz) — Study-Apps 페이지에서 불러 쓰는 모듈입니다. 페이지가 아닙니다.

사용: Study-Apps 페이지가 ?app=voca 로 열리면 render()를 호출합니다.
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
HTML_PATH = ASSETS / "voca_practice.html"
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


@st.cache_data
def _load_html(path: str, mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


def render() -> None:
    try:
        if LOCAL_CSV.exists():
            rows = _load_local(str(LOCAL_CSV), LOCAL_CSV.stat().st_mtime)
        else:
            rows = _load_drive()
    except Exception as e:
        st.error(f"Could not load the MD-33 data: {e}")
        return
    html = _load_html(str(HTML_PATH), HTML_PATH.stat().st_mtime).replace(
        "/*__DATA__*/[]", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    )
    _embed(html, 900)
