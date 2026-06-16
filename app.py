import streamlit as st
import google.generativeai as genai
import urllib.parse
import json
import re
from datetime import datetime
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Growth Engine AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 2. CUSTOM CSS — Dark, premium, editorial feel
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

  /* ── Root tokens ── */
  :root {
    --bg:        #0d0f14;
    --surface:   #161a22;
    --surface2:  #1e2330;
    --border:    #2a3040;
    --accent:    #6366f1;
    --accent2:   #8b5cf6;
    --gold:      #f59e0b;
    --green:     #10b981;
    --red:       #ef4444;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --li-blue:   #0a66c2;
    --tw-blue:   #1d9bf0;
    --ig-pink:   #e1306c;
  }

  /* ── Base ── */
  .stApp, .main { background: var(--bg) !important; }
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

  /* ── Header ── */
  .ge-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d0f14 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .ge-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--gold));
  }
  .ge-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: -0.5px;
  }
  .ge-subtitle { color: var(--muted); font-size: 0.9rem; margin-top: 0.25rem; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
    gap: 2px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 8px 14px !important;
    transition: all 0.2s;
  }
  .stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

  /* ── Cards ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }
  .card-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.75rem;
  }

  /* ── Platform badges ── */
  .badge-li  { display:inline-block; background:#0a66c211; border:1px solid #0a66c244; color:#4fa3e0; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; }
  .badge-tw  { display:inline-block; background:#1d9bf011; border:1px solid #1d9bf044; color:#1d9bf0; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; }
  .badge-ig  { display:inline-block; background:#e1306c11; border:1px solid #e1306c44; color:#e1306c; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600; }

  /* ── Output text areas ── */
  .output-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre-wrap;
    color: var(--text);
    min-height: 120px;
    margin-bottom: 0.75rem;
  }
  .char-counter { font-size: 0.75rem; color: var(--muted); text-align: right; margin-top: -0.5rem; margin-bottom: 0.75rem; }
  .char-over { color: var(--red) !important; font-weight: 600; }

  /* ── Buttons ── */
  .stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    height: 2.6em !important;
    transition: all 0.2s !important;
    border: none !important;
    width: 100%;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
  }
  .stButton > button[kind="primary"]:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button[kind="secondary"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
  }

  /* ── Inputs ── */
  .stTextArea textarea, .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.88rem !important;
  }
  .stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #6366f122 !important;
  }
  .stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
  }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }
  section[data-testid="stSidebar"] .stSelectbox > div > div { background: var(--bg) !important; }

  /* ── Platform action links ── */
  .platform-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 600;
    transition: opacity 0.2s;
    margin-right: 8px;
    margin-bottom: 4px;
  }
  .platform-link:hover { opacity: 0.8; }
  .link-li { background: #0a66c2; color: #fff !important; }
  .link-tw { background: #000; color: #fff !important; border: 1px solid #333; }
  .link-ig { background: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); color:#fff !important; }

  /* ── Score display ── */
  .score-badge {
    display: inline-block;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--gold);
  }

  /* ── Dividers ── */
  hr { border-color: var(--border) !important; }

  /* ── History ── */
  .hist-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    cursor: pointer;
  }

  /* ── Alerts ── */
  .stAlert { border-radius: 10px !important; }

  /* ── Label ── */
  label, .stLabel { color: var(--muted) !important; font-size: 0.82rem !important; font-weight: 500 !important; }

  /* ── Section heading ── */
  .sec-head {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 1rem 0;
  }

  /* ── Spinner ── */
  .stSpinner > div { border-top-color: var(--accent) !important; }

  /* ── Hook cards ── */
  .hook-card {
    background: var(--surface2);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.87rem;
    line-height: 1.6;
  }
  .hook-style {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 4px;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. API SETUP — No startup probing
# ─────────────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash"

def init_model():
    """Initialize Gemini model once."""
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("google_api_key")
        if not api_key:
            return None, "API Key missing. Set 'GOOGLE_API_KEY' in .streamlit/secrets.toml"
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(MODEL_NAME), None
    except Exception as e:
        return None, str(e)

if "model" not in st.session_state:
    _model, _err = init_model()
    st.session_state["model"] = _model
    st.session_state["model_error"] = _err

model = st.session_state["model"]
if model is None:
    st.error(f"⚠️ {st.session_state['model_error']}")
    st.markdown("""
    **Setup steps:**
    1. Create file `.streamlit/secrets.toml`
    2. Add: `GOOGLE_API_KEY = "your_key_here"`
    3. Get key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    """)
    st.stop()


# ─────────────────────────────────────────────
# 4. HELPER FUNCTIONS
# ─────────────────────────────────────────────

def generate_content(prompt_text: str, max_tokens: int = 2048) -> str | None:
    """Wraps Gemini API call with clear error handling."""
    try:
        response = model.generate_content(
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.75
            )
        )
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower():
            st.error("⚠️ **API Quota Exceeded** — Free tier limit hit. Try again after midnight GMT, or create a new Google AI Studio key.")
        elif "401" in err or "API key not valid" in err:
            st.error("⚠️ **Invalid API Key** — Check your secrets.toml. [Get a new key →](https://aistudio.google.com/app/apikey)")
        elif "404" in err or "not found" in err.lower():
            st.error("⚠️ **Model Unavailable** — gemini-2.0-flash not accessible on this key. Ensure billing is enabled on Google Cloud.")
        else:
            st.error(f"API Error: {err}")
        return None


def extract_section(text: str, markers: list[str]) -> str:
    """
    Robustly extract a section. Tries multiple heading formats.
    markers: list of possible heading names, e.g. ['LINKEDIN', 'LinkedIn Post']
    """
    for marker in markers:
        # Try ### heading
        pattern = rf"(?:#+\s*{re.escape(marker)}\s*\n)(.*?)(?=\n#+\s*[A-Z]|\Z)"
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
        # Try plain label like "LINKEDIN:" or "**LINKEDIN**"
        pattern2 = rf"\*?\*?{re.escape(marker)}\*?\*?\s*:?\s*\n(.*?)(?=\n\*?\*?[A-Z]{{3,}}|\Z)"
        m2 = re.search(pattern2, text, re.IGNORECASE | re.DOTALL)
        if m2:
            return m2.group(1).strip()
    # Fallback: return whole text
    return text.strip()


def platform_links(linkedin_text: str = "", twitter_text: str = "", ig_text: str = "") -> str:
    """Generate HTML platform action links."""
    links = ""
    if linkedin_text:
        enc = urllib.parse.quote(linkedin_text[:3000])
        url = f"https://www.linkedin.com/feed/?shareActive=true&text={enc}"
        links += f'<a href="{url}" target="_blank" class="platform-link link-li">🔗 Post to LinkedIn</a>'
    if twitter_text:
        enc = urllib.parse.quote(twitter_text[:280])
        url = f"https://twitter.com/intent/tweet?text={enc}"
        links += f'<a href="{url}" target="_blank" class="platform-link link-tw">𝕏 Post to X/Twitter</a>'
    if ig_text:
        links += f'<a href="https://www.instagram.com/create/story/" target="_blank" class="platform-link link-ig">📸 Open Instagram</a>'
    return links


def copy_button(content: str, key: str, label: str = "📋 Copy"):
    """Real clipboard copy using JS injection."""
    if st.button(label, key=key):
        safe = content.replace("`", "\\`").replace("$", "\\$")
        components.html(
            f"""<script>
            navigator.clipboard.writeText(`{safe}`)
              .then(() => console.log('copied'))
              .catch(() => {{
                  const ta = document.createElement('textarea');
                  ta.value = `{safe}`;
                  document.body.appendChild(ta);
                  ta.select();
                  document.execCommand('copy');
                  document.body.removeChild(ta);
              }});
            </script>""",
            height=0
        )
        st.toast("✅ Copied to clipboard!", icon="✅")


def char_counter_html(text: str, limit: int) -> str:
    count = len(text)
    cls = "char-over" if count > limit else ""
    return f'<div class="char-counter {cls}">{count:,} / {limit:,} chars</div>'


def save_history(entry_type: str, content: str, meta: dict = None):
    if "history" not in st.session_state:
        st.session_state["history"] = []
    entry = {
        "id": len(st.session_state["history"]) + 1,
        "type": entry_type,
        "content": content,
        "meta": meta or {},
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    st.session_state["history"].insert(0, entry)
    st.session_state["history"] = st.session_state["history"][:50]


# ─────────────────────────────────────────────
# 5. SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "post_linkedin": "",
    "post_twitter": "",
    "hooks_raw": "",
    "hooks_parsed": [],
    "audit_raw": "",
    "hashtags_raw": "",
    "ig_caption": "",
    "brand_voice": "Professional & Formal",
    "custom_voice": "",
    "history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# 6. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;">
        ⚙️ Settings
      </div>
    </div>
    """, unsafe_allow_html=True)

    voice_options = [
        "Professional & Formal",
        "Casual & Conversational",
        "Humorous & Witty",
        "Inspirational & Motivational",
        "Technical & Analytical",
        "Startup / Founder",
        "Custom",
    ]
    st.caption("BRAND VOICE")
    selected_voice = st.selectbox("", voice_options, label_visibility="collapsed",
                                   index=voice_options.index(st.session_state["brand_voice"])
                                   if st.session_state["brand_voice"] in voice_options else 0)
    st.session_state["brand_voice"] = selected_voice

    if selected_voice == "Custom":
        cv = st.text_area("Describe your voice", value=st.session_state["custom_voice"],
                          placeholder="e.g., Like a startup mentor — direct, empathetic, zero fluff")
        st.session_state["custom_voice"] = cv

    voice_map = {
        "Professional & Formal": "Write in a professional, formal tone. Use polished language, avoid slang.",
        "Casual & Conversational": "Write casually, like talking to a friend. Use contractions, keep it warm.",
        "Humorous & Witty": "Use clever humor, wordplay, and wit. Make it entertaining without being cringe.",
        "Inspirational & Motivational": "Write in an uplifting, motivational tone. Inspire action.",
        "Technical & Analytical": "Use precise, data-driven language. Back claims with logic.",
        "Startup / Founder": "Write like a confident founder — bold, direct, mission-driven, no corporate speak.",
        "Custom": st.session_state["custom_voice"],
    }
    voice_instruction = voice_map.get(selected_voice, "")

    st.divider()

    # History
    st.caption("📜 HISTORY")
    if st.session_state["history"]:
        st.write(f"{len(st.session_state['history'])} entries")
        f_type = st.selectbox("Filter", ["All", "Post", "Hook", "Audit", "Hashtag", "Instagram"])
        for e in st.session_state["history"]:
            if f_type == "All" or e["type"] == f_type:
                with st.expander(f"{e['type']} · {e['ts']}"):
                    st.write(e["content"][:200] + "…")
                    if st.button(f"Restore #{e['id']}", key=f"hist_{e['id']}"):
                        if e["type"] == "Post":
                            st.session_state["post_linkedin"] = extract_section(e["content"], ["LINKEDIN", "LinkedIn Post"])
                            st.session_state["post_twitter"] = extract_section(e["content"], ["TWITTER", "Twitter Thread", "X Thread"])
                        elif e["type"] == "Hook":
                            st.session_state["hooks_raw"] = e["content"]
                        elif e["type"] == "Audit":
                            st.session_state["audit_raw"] = e["content"]
                        elif e["type"] == "Hashtag":
                            st.session_state["hashtags_raw"] = e["content"]
                        elif e["type"] == "Instagram":
                            st.session_state["ig_caption"] = e["content"]
                        st.rerun()

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("Clear All"):
                st.session_state["history"] = []
                st.rerun()
        with col_h2:
            if st.session_state["history"]:
                json_out = json.dumps(st.session_state["history"], indent=2)
                st.download_button("Export JSON", json_out,
                                   f"history_{datetime.now().strftime('%Y%m%d')}.json",
                                   "application/json")
    else:
        st.caption("Generate content to build history.")

    st.divider()
    st.caption("Built by Shweta Mishra · Growth Engine AI v2")


# ─────────────────────────────────────────────
# 7. MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="ge-header">
  <div class="ge-title">🚀 Growth Engine AI</div>
  <div class="ge-subtitle">
    Premium content for LinkedIn · X/Twitter · Instagram — crafted by AI, posted by you.
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 8. TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✍️  Post Generator",
    "🎣  Hook Smith",
    "🔍  Profile Auditor",
    "🏷️  Hashtag Lab",
    "📸  Instagram Caption",
])


# ═══════════════════════════════════════════════════
# TAB 1 — VIRAL POST GENERATOR (LinkedIn + Twitter)
# ═══════════════════════════════════════════════════
with tab1:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Your Idea</div>', unsafe_allow_html=True)

        topic = st.text_area(
            "What do you want to post about?",
            height=120,
            placeholder="e.g., I spent 30 days learning Python from scratch while holding a full-time job. Here's what actually worked...",
            key="post_topic"
        )
        tone = st.selectbox("Content angle / tone", [
            "Storytelling — Hero's Journey",
            "Contrarian — Hot Take",
            "Educational — Step-by-Step Guide",
            "Data-Driven — Share a Stat or Insight",
            "Personal Reflection — Lesson Learned",
            "List / Tips (Carousel-ready)",
            "Case Study — Before & After",
        ])
        audience = st.text_input("Target audience", placeholder="e.g., early-career developers, SaaS founders, marketing managers")
        include_cta = st.checkbox("Add a call-to-action at the end", value=True)

        if st.button("✨ Generate LinkedIn + Twitter Posts", type="primary", key="gen_posts"):
            if not topic.strip():
                st.warning("Enter your idea first.")
            else:
                cta_req = "End each post with a short, non-salesy call-to-action (ask a question, invite a comment, or share a resource)." if include_cta else "No explicit CTA."
                audience_line = f"Target audience: {audience}" if audience.strip() else ""

                prompt = f"""You are a world-class ghostwriter and content strategist for founders, executives, and builders on LinkedIn and X/Twitter.

Your writing is:
- Hook-driven: The first line MUST stop someone mid-scroll
- Value-dense: Every sentence earns its place
- Human: No corporate buzzwords, no AI-sounding phrases like "In the realm of..." or "Delve into..."
- Formatted for mobile: Short paragraphs (1-2 sentences max), strategic white space

VOICE: {voice_instruction}
{audience_line}
TOPIC: {topic}
TONE/ANGLE: {tone}
{cta_req}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK 1 — LINKEDIN POST
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Write one high-quality LinkedIn post following these rules:
1. First line: A powerful hook. No "I'm excited to share..." or "Great news!" Start with tension, a bold claim, a surprising fact, or a provocative question.
2. Short paragraphs with line breaks for scannability.
3. Emotional arc: Problem → Insight → Lesson or Story → Takeaway
4. Optional: 1-2 bullet points or a numbered list if it adds clarity
5. End with a strong close + CTA
6. 3-5 relevant hashtags on the final line
7. Max 1,800 characters (ideal), hard limit 3,000 chars
8. Do NOT use these banned phrases: "game-changer", "dive deep", "delve", "landscape", "leverage" (as a buzzword), "paradigm shift", "synergy", "excited to announce"

### LINKEDIN
[write the LinkedIn post here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK 2 — X / TWITTER THREAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Write an X/Twitter thread (5-7 tweets):
- Tweet 1 (HOOK): The most irresistible opener possible. Under 240 chars. No hashtags yet.
- Tweets 2-5 (VALUE): Each tweet delivers ONE clear insight, tip, or story beat. Each under 280 chars.
- Tweet 6 (CONCLUSION): Summarize the key takeaway
- Tweet 7 (ENGAGEMENT): End with a question to spark replies + 2-3 hashtags

Format exactly like:
1/ [tweet text]
2/ [tweet text]
...

### TWITTER
[write the thread here]
"""
                with st.spinner("Writing your posts…"):
                    result = generate_content(prompt, max_tokens=2500)

                if result:
                    li = extract_section(result, ["LINKEDIN", "LinkedIn Post", "LINKEDIN POST"])
                    tw = extract_section(result, ["TWITTER", "Twitter Thread", "X Thread", "TWITTER THREAD"])
                    st.session_state["post_linkedin"] = li
                    st.session_state["post_twitter"] = tw
                    save_history("Post", result, {"topic": topic, "tone": tone})
                    st.success("Posts generated!")

    with right:
        st.markdown('<div class="sec-head">Generated Content</div>', unsafe_allow_html=True)

        if st.session_state["post_linkedin"] or st.session_state["post_twitter"]:

            # ── LinkedIn output ──
            st.markdown('<span class="badge-li">LinkedIn</span>', unsafe_allow_html=True)
            li_text = st.session_state["post_linkedin"]
            st.markdown(f'<div class="output-box">{li_text}</div>', unsafe_allow_html=True)
            st.markdown(char_counter_html(li_text, 3000), unsafe_allow_html=True)

            enc_li = urllib.parse.quote(li_text[:3000])
            st.markdown(
                f'<a href="https://www.linkedin.com/feed/?shareActive=true&text={enc_li}" '
                f'target="_blank" class="platform-link link-li">🔗 Post to LinkedIn</a>',
                unsafe_allow_html=True
            )
            copy_button(li_text, "copy_li", "📋 Copy LinkedIn Post")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Twitter output ──
            st.markdown('<span class="badge-tw">X / Twitter</span>', unsafe_allow_html=True)
            tw_text = st.session_state["post_twitter"]

            # Render each tweet separately
            tweets = re.split(r'\n(?=\d+/)', tw_text)
            for tweet in tweets:
                if tweet.strip():
                    tweet_clean = tweet.strip()
                    char_cls = "char-over" if len(tweet_clean) > 280 else ""
                    border_col = "#ef4444" if len(tweet_clean) > 280 else "#2a3040"
                    st.markdown(
                        f'<div class="output-box" style="border-left:3px solid #1d9bf0; border-color-left:#1d9bf0; border: 1px solid {border_col}; border-left: 3px solid #1d9bf0;">'
                        f'{tweet_clean}</div>',
                        unsafe_allow_html=True
                    )

            hook_tweet = tweets[0].strip() if tweets else tw_text[:280]
            enc_tw = urllib.parse.quote(hook_tweet[:280])
            st.markdown(
                f'<a href="https://twitter.com/intent/tweet?text={enc_tw}" '
                f'target="_blank" class="platform-link link-tw">𝕏 Post Hook to X</a>',
                unsafe_allow_html=True
            )
            copy_button(tw_text, "copy_tw", "📋 Copy Full Thread")

        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem 1rem;">
              <div style="font-size:2rem;margin-bottom:0.75rem;">✍️</div>
              <div style="color:#64748b;font-size:0.9rem;">Enter your idea on the left and click Generate.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 2 — HOOK SMITH
# ═══════════════════════════════════════════════════
with tab2:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Your Opening Line</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b;font-size:0.85rem;">The hook is 80% of your post. Paste your boring first line — we\'ll rewrite it 7 different ways.</p>', unsafe_allow_html=True)

        boring = st.text_input("Current opening line:", placeholder="e.g., I wrote a new app today.", key="hook_input")
        context = st.text_input("What's the post about? (optional context)", placeholder="e.g., I built a SaaS in 48 hours")
        num_hooks = st.slider("Number of variations", 5, 10, 7)
        platform_hook = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Both"])

        if st.button("🔥 Rewrite My Hook", type="primary", key="gen_hooks"):
            if not boring.strip():
                st.warning("Enter your opening line first.")
            else:
                ctx_line = f"Post context: {context}" if context.strip() else ""
                prompt = f"""You are the world's best copywriter specializing in social media hooks that stop people mid-scroll.

Original (boring) line: "{boring}"
{ctx_line}
Platform: {platform_hook}
VOICE: {voice_instruction}

Rewrite this into {num_hooks} powerful hook variations. Use different psychological frameworks:

1. **The Curiosity Gap** — Make them NEED to know what comes next
2. **The Bold Claim** — An audacious statement they'll agree or argue with  
3. **The Empathy Hook** — Speak directly to their pain/desire
4. **The Number Hook** — Lead with a specific, surprising stat or number
5. **The Story Opener** — Drop them in the middle of the action
6. **The Counterintuitive** — Say the opposite of what they expect
7. **The Direct Question** — The question they've been afraid to ask
8. **The Social Proof Hook** — "What X people discovered about Y"
9. **The Confession** — Vulnerability that earns trust instantly
10. **The Provocation** — A hot take that splits the room

For each hook:
- Name the framework used
- Write the hook (under 150 chars for Twitter; under 200 chars for LinkedIn first line)
- Give a one-line note on WHY it works psychologically

Format:
**[Number]. [FRAMEWORK NAME]**
Hook: [the hook text]
Why it works: [brief psychology note]

RULES:
- No em-dashes (—) as the first character
- No "In today's world..."
- No starting with "I'm" 
- Make each one feel genuinely different
"""
                with st.spinner("Crafting your hooks…"):
                    result = generate_content(prompt, max_tokens=2000)
                if result:
                    st.session_state["hooks_raw"] = result
                    save_history("Hook", result, {"original": boring})
                    st.success("Hooks ready!")

    with right:
        st.markdown('<div class="sec-head">Hook Variations</div>', unsafe_allow_html=True)
        if st.session_state["hooks_raw"]:
            # Parse and display each hook in a card
            raw = st.session_state["hooks_raw"]
            # Split by numbered items
            blocks = re.split(r'\n(?=\*\*\d+\.)', raw)
            if len(blocks) <= 1:
                blocks = re.split(r'\n(?=\d+\.)', raw)

            for block in blocks:
                if block.strip():
                    # Extract framework name
                    frame_m = re.search(r'\*\*[\d]+\.\s*(.*?)\*\*', block)
                    frame = frame_m.group(1).strip() if frame_m else "Variation"
                    hook_m = re.search(r'Hook:\s*(.*?)(?:\n|$)', block, re.IGNORECASE)
                    hook_text = hook_m.group(1).strip() if hook_m else ""
                    why_m = re.search(r'Why it works?:\s*(.*?)(?:\n|$)', block, re.IGNORECASE)
                    why = why_m.group(1).strip() if why_m else ""

                    if hook_text:
                        st.markdown(f"""
                        <div class="hook-card">
                          <div class="hook-style">{frame}</div>
                          <div style="color:#e2e8f0;font-size:0.92rem;font-weight:500;margin-bottom:4px;">{hook_text}</div>
                          {'<div style="color:#64748b;font-size:0.78rem;margin-top:6px;">💡 ' + why + '</div>' if why else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Fallback: show raw block
                        st.markdown(f'<div class="hook-card">{block.strip()}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            copy_button(raw, "copy_hooks", "📋 Copy All Hooks")
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem 1rem;">
              <div style="font-size:2rem;margin-bottom:0.75rem;">🎣</div>
              <div style="color:#64748b;font-size:0.9rem;">Your hook rewrites will appear here.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 3 — PROFILE AUDITOR
# ═══════════════════════════════════════════════════
with tab3:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Bio Audit</div>', unsafe_allow_html=True)
        bio = st.text_area("Paste your current bio / headline:", height=120, key="audit_bio",
                           placeholder="e.g., Software Engineer @ XYZ | Passionate about tech | Let's connect!")
        audience_a = st.text_input("Who should this bio attract?", placeholder="e.g., Series A startup founders, Fortune 500 recruiters")
        platform_a = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Both"], key="audit_platform")
        goal_a = st.selectbox("Your primary goal with this profile", [
            "Get hired / job opportunities",
            "Attract clients / freelance work",
            "Build a personal brand / audience",
            "Networking / partnerships",
            "Thought leadership",
        ])

        if st.button("🔍 Audit My Profile", type="primary", key="gen_audit"):
            if not bio.strip():
                st.warning("Paste your bio first.")
            else:
                prompt = f"""You are a world-class Personal Brand Consultant. You've helped 500+ founders, executives, and creators craft bios that convert.

Bio to audit: "{bio}"
Target audience: {audience_a or "General professional audience"}
Platform: {platform_a}
Goal: {goal_a}
VOICE: {voice_instruction}

Provide a thorough audit in this EXACT structure:

### SCORE
Give a score out of 10 with one sentence explaining the rating.

### WEAKNESSES
List exactly 3 specific weaknesses. Be brutal but constructive. Don't be generic — reference the actual bio text.
- Weakness 1: [specific issue from the bio]
- Weakness 2: [specific issue]  
- Weakness 3: [specific issue]

### STRENGTHS
List exactly 2-3 genuine strengths from the bio (if none exist, say so honestly).
- Strength 1: [specific strength]

### REWRITE: PROFESSIONAL VERSION
Write a polished, credibility-forward version optimized for {platform_a}.
Appropriate length for {platform_a}.

### REWRITE: CONVERSATIONAL VERSION  
Write a warm, human version that still converts.
Same length guidelines.

### SEO KEYWORDS
List 3-5 keywords/phrases this person should naturally weave in for discoverability on {platform_a}.

### TOP ACTION
The single most important change they should make TODAY.
"""
                with st.spinner("Auditing your profile…"):
                    result = generate_content(prompt, max_tokens=2000)
                if result:
                    st.session_state["audit_raw"] = result
                    save_history("Audit", result, {"bio": bio[:80], "platform": platform_a})
                    st.success("Audit complete!")

    with right:
        st.markdown('<div class="sec-head">Audit Results</div>', unsafe_allow_html=True)
        if st.session_state["audit_raw"]:
            raw = st.session_state["audit_raw"]

            # Extract score and display prominently
            score_m = re.search(r'SCORE\s*\n+([\s\S]*?)(?=###|\Z)', raw, re.IGNORECASE)
            if score_m:
                score_text = score_m.group(1).strip()
                num_m = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', score_text)
                score_num = num_m.group(1) if num_m else "–"
                st.markdown(f"""
                <div class="card" style="text-align:center;">
                  <div style="color:#64748b;font-size:0.75rem;letter-spacing:1px;font-weight:600;margin-bottom:4px;">PROFILE SCORE</div>
                  <div class="score-badge">{score_num}<span style="font-size:1.2rem;color:#64748b;">/10</span></div>
                  <div style="color:#94a3b8;font-size:0.85rem;margin-top:0.5rem;">{score_text.replace(score_num + "/10","").replace(score_num+" / 10","").strip()}</div>
                </div>
                """, unsafe_allow_html=True)

            # Render remaining sections as markdown
            # Remove the score section and render rest
            rest = re.sub(r'###\s*SCORE\s*\n+[\s\S]*?(?=###)', '', raw, flags=re.IGNORECASE)
            st.markdown(rest)

            st.divider()
            copy_button(raw, "copy_audit", "📋 Copy Full Audit")
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem 1rem;">
              <div style="font-size:2rem;margin-bottom:0.75rem;">🔍</div>
              <div style="color:#64748b;font-size:0.9rem;">Paste your bio on the left to get a full audit with rewritten versions.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 4 — HASHTAG LAB
# ═══════════════════════════════════════════════════
with tab4:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Hashtag Research</div>', unsafe_allow_html=True)
        ht_topic = st.text_area("What is your post / content about?", height=100, key="ht_topic",
                                placeholder="e.g., Bootstrapping a SaaS to $10k MRR without VC funding")
        ht_platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "All three"], key="ht_platform")
        ht_niche = st.text_input("Your niche / industry", placeholder="e.g., B2B SaaS, health tech, creator economy")
        ht_count = st.slider("Total hashtags to generate", 10, 30, 20)

        if st.button("🔬 Research Hashtags", type="primary", key="gen_ht"):
            if not ht_topic.strip():
                st.warning("Enter your content topic first.")
            else:
                prompt = f"""You are a social media SEO expert with deep knowledge of hashtag strategy across platforms.

Content topic: {ht_topic}
Platform(s): {ht_platform}
Niche: {ht_niche or "General"}
Total hashtags needed: {ht_count}

Generate a strategic hashtag set organized into 3 tiers:

### TIER 1 — HIGH REACH (5-7 hashtags)
Broad hashtags with 500K–5M+ uses. High competition but maximum visibility.
Format: #Hashtag — Brief note on why/when to use it

### TIER 2 — MEDIUM REACH (8-10 hashtags)  
Niche hashtags with 50K–500K uses. Best engagement-to-competition ratio.
Format: #Hashtag — Brief note

### TIER 3 — TARGETED / COMMUNITY (5-7 hashtags)
Highly specific hashtags with 5K–50K uses. Smaller reach but laser-targeted audience.
Format: #Hashtag — Brief note

### PLATFORM STRATEGY
A 3-4 sentence note on how to use these hashtags differently per platform:
- LinkedIn: [how many, where to place them]
- Twitter/X: [how many, placement strategy]
- Instagram: [how many, comment vs caption strategy]

### READY-TO-COPY SETS
Provide 3 ready-to-paste hashtag sets:
**Set A (LinkedIn — 5 tags):** [5 tags optimized for LinkedIn]
**Set B (Twitter — 3 tags):** [3 tags for X/Twitter]
**Set C (Instagram — 20 tags):** [20 tags for Instagram]

IMPORTANT: Only generate real, commonly used hashtags. Do not invent hashtags.
"""
                with st.spinner("Researching hashtags…"):
                    result = generate_content(prompt, max_tokens=2000)
                if result:
                    st.session_state["hashtags_raw"] = result
                    save_history("Hashtag", result, {"topic": ht_topic, "platform": ht_platform})
                    st.success("Hashtag sets ready!")

    with right:
        st.markdown('<div class="sec-head">Hashtag Sets</div>', unsafe_allow_html=True)
        if st.session_state["hashtags_raw"]:
            st.markdown(st.session_state["hashtags_raw"])
            st.divider()
            copy_button(st.session_state["hashtags_raw"], "copy_ht", "📋 Copy All Hashtags")
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem 1rem;">
              <div style="font-size:2rem;margin-bottom:0.75rem;">🏷️</div>
              <div style="color:#64748b;font-size:0.9rem;">Platform-specific hashtag sets will appear here — organized by reach tier.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 5 — INSTAGRAM CAPTION GENERATOR
# ═══════════════════════════════════════════════════
with tab5:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Instagram Caption</div>', unsafe_allow_html=True)
        ig_topic = st.text_area("What is your post about?", height=100, key="ig_topic",
                                placeholder="e.g., Behind-the-scenes of my morning routine as a startup founder")
        ig_type = st.selectbox("Content type", [
            "Single image / photo",
            "Carousel (multi-slide)",
            "Reel / short video",
            "Story",
        ])
        ig_vibe = st.selectbox("Caption vibe", [
            "Inspirational & value-packed",
            "Raw & authentic / vulnerable",
            "Educational / informational",
            "Funny & entertaining",
            "Product / service focused",
            "Behind-the-scenes",
        ])
        ig_cta = st.selectbox("Call-to-action type", [
            "Save this post",
            "Share with a friend",
            "Drop a comment",
            "Follow for more",
            "Click the link in bio",
            "No CTA",
        ])
        ig_len = st.radio("Caption length", ["Short (< 100 words)", "Medium (100-200 words)", "Long (200-300 words)"], horizontal=True)

        if st.button("📸 Generate Instagram Caption", type="primary", key="gen_ig"):
            if not ig_topic.strip():
                st.warning("Enter what your post is about.")
            else:
                prompt = f"""You are a top Instagram content strategist who writes captions that drive saves, shares, and comments — the three signals that boost reach.

Post topic: {ig_topic}
Content type: {ig_type}
Vibe: {ig_vibe}
CTA goal: {ig_cta}
Length: {ig_len}
VOICE: {voice_instruction}

Write ONE polished Instagram caption following these rules:

1. **HOOK (first 1-2 lines):** Must make them tap "more". No starting with "I'm excited..." 
2. **BODY:** Deliver value, story, or emotion depending on the vibe. Use line breaks (not paragraphs — Instagram shows line breaks).
3. **CTA:** End with the specified CTA naturally — make it feel earned, not forced.
4. **HASHTAGS:** Add 15-20 hashtags AFTER the caption (separated by a line break). Mix popular + niche.
5. **EMOJIS:** Use strategically, not excessively. Max 5-6 emojis.

BANNED phrases: "In today's world", "game-changer", "So excited to share", "Link in bio!" as the opener

Also provide:
### CAPTION VERSION A (Main)
[the caption]

### CAPTION VERSION B (Alternative angle)
[a different approach to the same topic — different hook, different format]

### STORY HOOK
One-line teaser text for an Instagram Story to drive swipe-up / link clicks to this post.
"""
                with st.spinner("Writing your caption…"):
                    result = generate_content(prompt, max_tokens=1800)
                if result:
                    st.session_state["ig_caption"] = result
                    save_history("Instagram", result, {"topic": ig_topic, "type": ig_type})
                    st.success("Captions ready!")

    with right:
        st.markdown('<div class="sec-head">Instagram Captions</div>', unsafe_allow_html=True)
        if st.session_state["ig_caption"]:
            raw = st.session_state["ig_caption"]

            # Extract and show versions A and B separately
            ver_a = extract_section(raw, ["CAPTION VERSION A", "VERSION A", "Caption Version A"])
            ver_b = extract_section(raw, ["CAPTION VERSION B", "VERSION B", "Caption Version B"])
            story = extract_section(raw, ["STORY HOOK", "Story Hook"])

            st.markdown('<span class="badge-ig">Instagram</span>', unsafe_allow_html=True)

            st.markdown("**Version A — Main Caption**")
            st.markdown(f'<div class="output-box">{ver_a}</div>', unsafe_allow_html=True)
            st.markdown(char_counter_html(ver_a, 2200), unsafe_allow_html=True)
            copy_button(ver_a, "copy_ig_a", "📋 Copy Version A")

            st.markdown("**Version B — Alternative Angle**")
            st.markdown(f'<div class="output-box">{ver_b}</div>', unsafe_allow_html=True)
            copy_button(ver_b, "copy_ig_b", "📋 Copy Version B")

            if story and story != raw:
                st.markdown("**Story Hook Text**")
                st.markdown(f'<div class="output-box" style="border-left:3px solid var(--ig-pink);">{story}</div>', unsafe_allow_html=True)
                copy_button(story, "copy_ig_story", "📋 Copy Story Hook")

            st.markdown(
                '<a href="https://www.instagram.com/create/story/" target="_blank" class="platform-link link-ig">📸 Open Instagram</a>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem 1rem;">
              <div style="font-size:2rem;margin-bottom:0.75rem;">📸</div>
              <div style="color:#64748b;font-size:0.9rem;">Two caption variations + a Story hook text will appear here.</div>
            </div>
            """, unsafe_allow_html=True)
