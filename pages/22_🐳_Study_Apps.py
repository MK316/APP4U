import importlib.util
from pathlib import Path

import streamlit as st

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="Study Apps", page_icon="🧰", layout="centered")

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def load_module(name: str):
    """assets 폴더의 .py 파일을 모듈로 불러옵니다 (pages/ 밖에 있어 메뉴에는 나타나지 않음)."""
    spec = importlib.util.spec_from_file_location(name, ASSETS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- 앱 목록 ----
# url: 외부 사이트 주소 / app: 이 페이지 안에서 여는 앱 (assets/<app>.py 의 render())
# url과 app이 모두 None이면 'Coming Soon'으로 표시됩니다.
APPS = [
    {
        "title": "Vocabulary APP",
        "url": "https://md33.lovable.app/",
        "desc": "MD-33 Dictionary: vocabulary study for the teacher certification exam (임용).",
    },
    {
        "title": "Voca practice",
        "app": "voca_practice",
        "desc": "MD-33 quiz practice: read the part of speech and meanings, then choose the word.",
    },
    {"title": "App 3", "url": None, "desc": "Coming Soon"},
    {"title": "App 4", "url": None, "desc": "Coming Soon"},
]

# ---- ?app=voca_practice 로 열렸으면 해당 앱만 보여줍니다 (버튼이 새 탭에서 이 주소를 엽니다) ----
current = st.query_params.get("app")
internal = {a["app"]: a for a in APPS if a.get("app")}
if current in internal:
    st.title(internal[current]["title"])
    load_module(current).render()
    st.stop()

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
    href = app.get("url") or (f"?app={app['app']}" if app.get("app") else None)
    with cols[i % 2]:
        if href:
            button = (f'<a class="app-btn" href="{href}" target="_blank" '
                      f'rel="noopener noreferrer">{app["title"]} ↗</a>')
        else:
            button = f'<span class="app-btn" aria-disabled="true">{app["title"]}</span>'
        st.markdown(f'<div class="app-card">{button}<p>{app["desc"]}</p></div>', unsafe_allow_html=True)
