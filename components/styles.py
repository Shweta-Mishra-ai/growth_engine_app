import streamlit as st


def inject_custom_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
:root{--bg:#0d0f14;--surface:#161a22;--surface2:#1e2330;--border:#2a3040;--accent:#6366f1;--accent2:#8b5cf6;--gold:#f59e0b;--text:#e2e8f0;--muted:#64748b;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.5rem 2rem 3rem!important;max-width:1400px!important;}
.ge-header{background:linear-gradient(135deg,#1a1f2e 0%,#0d0f14 100%);border:1px solid var(--border);border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;position:relative;overflow:hidden;}
.ge-header::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--accent2),var(--gold));}
.ge-title{font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:700;color:#fff;margin:0;}
.ge-subtitle{color:var(--muted);font-size:0.9rem;margin-top:0.25rem;}
.stTabs [data-baseweb="tab-list"]{background:var(--surface)!important;border-radius:12px;padding:4px;border:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;border-radius:8px!important;font-size:0.85rem;font-weight:500;padding:8px 14px!important;}
.stTabs [aria-selected="true"]{background:var(--accent)!important;color:#fff!important;}
.sec-head{font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:600;color:var(--text);margin:0 0 1rem 0;}
.output-box{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:1.25rem;font-size:0.88rem;line-height:1.7;white-space:pre-wrap;color:var(--text);min-height:80px;margin-bottom:0.5rem;}
.char-counter{font-size:0.75rem;color:var(--muted);text-align:right;margin-bottom:0.5rem;}
.char-over{color:#ef4444!important;font-weight:600;}
.badge-li{display:inline-block;background:#0a66c211;border:1px solid #0a66c244;color:#4fa3e0;border-radius:6px;padding:3px 10px;font-size:0.75rem;font-weight:600;margin-bottom:8px;}
.badge-tw{display:inline-block;background:#1d9bf011;border:1px solid #1d9bf044;color:#1d9bf0;border-radius:6px;padding:3px 10px;font-size:0.75rem;font-weight:600;margin-bottom:8px;}
.badge-ig{display:inline-block;background:#e1306c11;border:1px solid #e1306c44;color:#e1306c;border-radius:6px;padding:3px 10px;font-size:0.75rem;font-weight:600;margin-bottom:8px;}
.stButton>button{border-radius:8px!important;font-weight:600!important;font-size:0.85rem!important;height:2.6em!important;border:none!important;width:100%;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:#fff!important;}
.stButton>button[kind="secondary"]{background:var(--surface2)!important;color:var(--text)!important;border:1px solid var(--border)!important;}
section[data-testid="stSidebar"]{border-right:1px solid var(--border)!important;}
.empty-card{text-align:center;padding:3rem 1rem;background:var(--surface);border:1px solid var(--border);border-radius:12px;}
.empty-card-icon{font-size:2rem;margin-bottom:0.75rem;}
.empty-card-text{color:#64748b;font-size:0.9rem;}
.card{background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin-bottom:1rem;}
.score-badge{display:inline-block;font-family:'Space Grotesk',sans-serif;font-size:2.5rem;font-weight:700;color:var(--gold);}
</style>""", unsafe_allow_html=True)
