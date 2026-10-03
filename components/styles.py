import streamlit as st


def inject_custom_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Design Tokens ─────────────────────────────── */
:root {
  --bg:        #0a0c12;
  --surface:   #12151e;
  --surface2:  #1a1f2b;
  --surface3:  #222736;
  --border:    #252b3b;
  --border2:   #2e3547;
  --accent:    #6366f1;
  --accent2:   #8b5cf6;
  --accent3:   #a78bfa;
  --gold:      #f59e0b;
  --green:     #10b981;
  --red:       #ef4444;
  --text:      #e2e8f0;
  --text2:     #94a3b8;
  --muted:     #64748b;
  --li:        #0a66c2;
  --tw:        #1d9bf0;
  --ig:        #e1306c;
}

/* ── Base ────────────────────────────────────── */
.stApp, .main { background: var(--bg) !important; }
html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.25rem 2rem 3rem !important; max-width: 1440px !important; }

/* ── Header ──────────────────────────────────── */
.ge-header {
  background: linear-gradient(135deg, #141824 0%, #0a0c12 100%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.75rem 2.25rem;
  margin-bottom: 1.25rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}
.ge-header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent2), var(--gold), var(--green));
}
.ge-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.95rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  letter-spacing: -0.5px;
}
.ge-subtitle { color: var(--muted); font-size: 0.9rem; margin-top: 0.35rem; }
.ge-version {
  position: absolute; top: 1.25rem; right: 1.5rem;
  font-size: 0.72rem; color: #a78bfa; font-weight: 600;
  background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3);
  padding: 3px 10px; border-radius: 20px;
}
.header-pills {
  display: flex; gap: 8px; flex-wrap: wrap; margin-top: 1rem;
}
.header-pill {
  font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 6px;
  background: var(--surface2); border: 1px solid var(--border); color: var(--text2);
}

/* ── Tabs ────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid var(--border) !important;
  gap: 2px !important;
  display: flex;
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border-radius: 8px !important;
  font-size: 0.83rem !important;
  font-weight: 500 !important;
  padding: 8px 14px !important;
  transition: all 0.15s ease !important;
  border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--text) !important;
  background: var(--surface2) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0.75rem 0 0 !important; }

/* ── Section Headings & Cards ────────────────── */
.sec-head {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 0.875rem 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}

/* ── Output Box ──────────────────────────────── */
.output-box {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.125rem 1.25rem;
  font-size: 0.875rem;
  line-height: 1.75;
  white-space: pre-wrap;
  color: var(--text);
  min-height: 80px;
  margin-bottom: 0.5rem;
}

/* ── Counters ────────────────────────────────── */
.counter-row {
  font-size: 0.75rem;
  color: var(--muted);
  text-align: right;
  margin-top: -0.25rem;
  margin-bottom: 0.625rem;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.counter-over { color: var(--red) !important; font-weight: 600; }
.counter-warn { color: var(--gold) !important; }
.counter-ok   { color: var(--green) !important; }

/* ── Quality Score Badge ─────────────────────── */
.score-ring {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.82rem;
  margin-bottom: 8px;
}
.score-A { color: var(--green); font-weight: 700; }
.score-B { color: var(--accent3); font-weight: 700; }
.score-C { color: var(--gold); font-weight: 700; }
.score-D { color: var(--red); font-weight: 700; }
.score-badge {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--gold);
}

/* ── Platform Badges ─────────────────────────── */
.badge-li { display:inline-block; background:#0a66c21a; border:1px solid #0a66c240; color:#4fa3e0; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; margin-bottom:8px; }
.badge-tw { display:inline-block; background:#1d9bf01a; border:1px solid #1d9bf040; color:#1d9bf0; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; margin-bottom:8px; }
.badge-ig { display:inline-block; background:#e1306c1a; border:1px solid #e1306c40; color:#e1306c; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; margin-bottom:8px; }
.badge-gen { display:inline-block; background:#6366f11a; border:1px solid #6366f140; color:#a78bfa; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; margin-bottom:8px; }

/* ── Platform Feed Preview Cards ─────────────── */
.preview-li {
  background: #ffffff; border: 1px solid #e0dfdc;
  border-radius: 10px; padding: 1.25rem 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 0.88rem; line-height: 1.6; color: #191919;
  white-space: pre-wrap; margin-bottom: 0.5rem;
}
.preview-tw {
  background: #000000; border: 1px solid #2f3336;
  border-radius: 10px; padding: 1.25rem 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 0.88rem; line-height: 1.6; color: #e7e9ea;
  white-space: pre-wrap; margin-bottom: 0.5rem;
}
.preview-label {
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px;
  text-transform: uppercase; color: var(--muted); margin-bottom: 6px;
}

/* ── Buttons ─────────────────────────────────── */
.stButton > button {
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 0.84rem !important;
  height: 2.6em !important;
  transition: all 0.15s ease !important;
  border: none !important;
  width: 100%;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
  color: #fff !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.25) !important;
}
.stButton > button[kind="primary"]:hover {
  opacity: 0.94 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--surface2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--surface3) !important;
  border-color: var(--border2) !important;
}

/* ── Action Links ────────────────────────────── */
.platform-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none !important;
  font-size: 0.83rem;
  font-weight: 600;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}
.platform-link:hover { opacity: 0.9; transform: translateY(-1px); }
.link-li { background: linear-gradient(135deg, #0a66c2, #004182); color: #fff !important; }
.link-tw { background: #000; color: #fff !important; border: 1px solid #333; }
.link-ig { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: #fff !important; }

/* ── Tweet Cards ─────────────────────────────── */
.tweet-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--tw);
  border-radius: 0 9px 9px 0;
  padding: 0.875rem 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.65;
  white-space: pre-wrap;
  color: var(--text);
}
.tweet-card.over-limit {
  border-left-color: var(--red) !important;
  background: rgba(239, 68, 68, 0.05);
}
.tweet-num {
  font-size: 0.7rem; font-weight: 600;
  color: var(--muted); margin-bottom: 4px;
  text-transform: uppercase; letter-spacing: 0.5px;
}

/* ── Form Inputs ─────────────────────────────── */
.stTextArea textarea, .stTextInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-size: 0.875rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}

/* ── Empty Card ──────────────────────────────── */
.empty-card {
  text-align: center;
  padding: 3rem 1.5rem;
  background: var(--surface);
  border: 1px dashed var(--border2);
  border-radius: 12px;
}
.empty-icon { font-size: 2.25rem; margin-bottom: 0.75rem; }
.empty-text { color: var(--muted); font-size: 0.875rem; line-height: 1.6; }

/* ── Sidebar ─────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}

/* ── Schedule Card ───────────────────────────── */
.schedule-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.schedule-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.78rem;
  color: var(--muted);
}
.schedule-pill {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

/* ── Scrollbars ──────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
</style>""", unsafe_allow_html=True)
