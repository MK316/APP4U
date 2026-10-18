import streamlit as st

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="Study Apps", page_icon="🧰", layout="centered")

# ---- 링크할 앱 목록: url이 None이면 'Coming Soon'으로 표시됩니다 ----
APPS = [
    {
        "title": "Vocabulary APP",
        "url": "https://md33.lovable.app/",
        "desc": "MD-33 Dictionary: vocabulary study for the teacher certification exam (임용).",
    },
    {
        "title": "Voca practice",
        "url": "Voca-practice",   # 같은 앱의 17_🧩_Voca-practice.py 페이지 (새 탭)
        "desc": "MD-33 quiz practice: read the part of speech and meanings, then choose the word.",
    },
    {"title": "App 3", "url": None, "desc": "Coming Soon"},
    {"title": "App 4", "url": None, "desc": "Coming Soon"},
]

st.markdown(
    """
    <style>
      .app-card { border: 1px solid #d9d4ca; border-radius: 12px; padding: 18px 18px 16px; margin-bottom: 16px; min-height: 140px; }
      .app-card p { margin: 10px 0 0; font-size: 0.92rem; color: #5d5a54; }
      a.app-btn, span.app-btn {
        display: block; text-align: center; font-weight: 600; font-size: 1.05rem;
        padding: 12px 16px; border-radius: 10px; text-decoration: none;
      }
      a.app-btn { background: #1b2a4e; color: #ffffff !important; }
      a.app-btn:hover { background: #24386a; }
      span.app-btn { background: #e7e4dd; color: #8a867e; cursor: not-allowed; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Study Apps")
st.caption("Click a button to open the app in a new tab.")

cols = st.columns(2)
for i, app in enumerate(APPS):
    with cols[i % 2]:
        if app["url"]:
            button = (f'<a class="app-btn" href="{app["url"]}" target="_blank" '
                      f'rel="noopener noreferrer">{app["title"]} ↗</a>')
        else:
            button = f'<span class="app-btn" aria-disabled="true">{app["title"]}</span>'
        st.markdown(f'<div class="app-card">{button}<p>{app["desc"]}</p></div>', unsafe_allow_html=True)
