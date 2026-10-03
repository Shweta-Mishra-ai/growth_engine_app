import urllib.parse
import streamlit as st
import streamlit.components.v1 as cv1
from services.text_parser import char_count_status, word_count, score_linkedin_post


def copy_button(content: str, key: str, label: str = "📋 Copy"):
    """Copies content to clipboard with a toast notification."""
    if st.button(label, key=key, use_container_width=True):
        safe = (
            content.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("$", "\\$")
            .replace("\n", "\\n")
            .replace('"', '\\"')
        )
        cv1.html(
            f"""<script>
            if (navigator.clipboard) {{
                navigator.clipboard.writeText("{safe}").catch(function() {{
                    const ta = document.createElement('textarea');
                    ta.value = "{safe}";
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand('copy');
                    document.body.removeChild(ta);
                }});
            }} else {{
                const ta = document.createElement('textarea');
                ta.value = "{safe}";
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
            }}
            </script>""",
            height=0,
        )
        st.toast("✅ Copied to clipboard!", icon="📋")


def platform_badge(label: str, css_class: str):
    st.markdown(f'<span class="badge-{css_class}">{label}</span>', unsafe_allow_html=True)


def empty_state(icon: str, text: str):
    st.markdown(
        f'<div class="empty-card">'
        f'<div class="empty-icon">{icon}</div>'
        f'<div class="empty-text">{text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_char_counter(text: str, limit: int):
    s = char_count_status(text, limit)
    cls = "counter-over" if s["is_over"] else ""
    st.markdown(
        f'<div class="counter-row"><span class="{cls}">{s["count"]:,} / {limit:,} chars</span></div>',
        unsafe_allow_html=True,
    )


def render_counter(text: str, char_limit: int, ideal_words: tuple | None = None):
    chars = len(text)
    words = word_count(text)
    char_cls = "counter-over" if chars > char_limit else ""

    word_note = ""
    if ideal_words and text.strip():
        mn, mx = ideal_words
        if words < mn:
            word_note = f'<span class="counter-warn">⚠️ {words} words (min {mn})</span>'
        elif words <= mx:
            word_note = f'<span class="counter-ok">✓ {words} words (ideal)</span>'
        else:
            word_note = f'<span class="counter-ok">✓ {words} words</span>'

    char_display = f'<span class="{char_cls}">{chars:,} / {char_limit:,} chars</span>'
    st.markdown(
        f'<div class="counter-row">{word_note}&nbsp;&nbsp;{char_display}</div>',
        unsafe_allow_html=True,
    )


def render_quality_score(text: str):
    if not text.strip():
        return
    result = score_linkedin_post(text)
    grade = result["grade"]
    overall = result["overall"]
    feedback = result["feedback"]

    grade_cls = f"score-{grade}"
    st.markdown(
        f'<div class="score-ring">'
        f'Quality Score: <span class="{grade_cls}">{overall}/100 (Grade {grade})</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if feedback:
        with st.expander(f"💡 {len(feedback)} optimization tips to improve reach", expanded=False):
            for tip in feedback:
                st.markdown(f"• {tip}")


def render_post_preview(text: str, platform: str):
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )
    if platform == "LinkedIn":
        st.markdown(
            f'<div class="preview-label">LinkedIn Feed Simulation</div>'
            f'<div class="preview-li">{safe}</div>',
            unsafe_allow_html=True,
        )
    elif platform in ("Twitter/X", "Twitter"):
        st.markdown(
            f'<div class="preview-label">X / Twitter Feed Simulation</div>'
            f'<div class="preview-tw">{safe}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="output-box">{safe}</div>',
            unsafe_allow_html=True,
        )


def render_tweet_card(tweet: str, idx: int, total: int):
    s = char_count_status(tweet, 280)
    over_cls = "over-limit" if s["is_over"] else ""
    safe = tweet.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    st.markdown(
        f'<div class="tweet-card {over_cls}">'
        f'<div class="tweet-num">Tweet {idx}/{total}</div>'
        f'{safe}'
        f'</div>',
        unsafe_allow_html=True,
    )
    render_counter(tweet, 280)


def platform_action_link(url: str, label: str, css_class: str):
    st.markdown(
        f'<a href="{url}" target="_blank" class="platform-link link-{css_class}">{label}</a>',
        unsafe_allow_html=True,
    )


def copy_and_share_linkedin_button(content: str, key: str):
    safe = urllib.parse.quote(content)
    html_code = f"""
    <button id="{key}" class="custom-share-btn">📋 Copy Post & Open LinkedIn</button>
    <script>
    document.getElementById("{key}").addEventListener("click", function() {{
        const text = decodeURIComponent("{safe}");
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try {{
            document.execCommand("copy");
        }} catch (err) {{
            console.error(err);
        }}
        document.body.removeChild(ta);
        window.open("https://www.linkedin.com/feed/?shareActive=true", "_blank");
    }});
    </script>
    <style>
    .custom-share-btn {{
        background: linear-gradient(135deg, #0a66c2, #004182);
        color: white;
        border: none;
        padding: 9px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        width: 100%;
        text-align: center;
        display: inline-block;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }}
    .custom-share-btn:hover {{
        background: linear-gradient(135deg, #004182, #002244);
        transform: translateY(-1px);
    }}
    </style>
    """
    cv1.html(html_code, height=45)


def copy_and_share_twitter_button(content: str, key: str):
    safe = urllib.parse.quote(content)
    html_code = f"""
    <button id="{key}" class="custom-share-btn-tw">📋 Copy Thread & Open X/Twitter</button>
    <script>
    document.getElementById("{key}").addEventListener("click", function() {{
        const text = decodeURIComponent("{safe}");
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try {{
            document.execCommand("copy");
        }} catch (err) {{
            console.error(err);
        }}
        document.body.removeChild(ta);
        window.open("https://twitter.com/intent/tweet", "_blank");
    }});
    </script>
    <style>
    .custom-share-btn-tw {{
        background: #000000;
        color: white;
        border: 1px solid #333333;
        padding: 9px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        width: 100%;
        text-align: center;
        display: inline-block;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }}
    .custom-share-btn-tw:hover {{
        background: #111111;
        border-color: #555555;
        transform: translateY(-1px);
    }}
    </style>
    """
    cv1.html(html_code, height=45)
