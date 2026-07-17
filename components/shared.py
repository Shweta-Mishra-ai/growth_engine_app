import streamlit as st
import streamlit.components.v1 as cv1
from services.text_parser import char_count_status


def copy_button(content: str, key: str, label: str = "📋 Copy"):
    if st.button(label, key=key):
        safe = content.replace("`", "\\`").replace("$", "\\$")
        cv1.html(f"""<script>
navigator.clipboard.writeText(`{safe}`).catch(()=>{{
  const t=document.createElement('textarea');t.value=`{safe}`;
  document.body.appendChild(t);t.select();document.execCommand('copy');document.body.removeChild(t);
}});</script>""", height=0)
        st.toast("✅ Copied!", icon="✅")


def platform_badge(label: str, css_class: str):
    st.markdown(f'<span class="badge-{css_class}">{label}</span>', unsafe_allow_html=True)


def empty_state(icon: str, text: str):
    st.markdown(f'<div class="empty-card"><div class="empty-card-icon">{icon}</div><div class="empty-card-text">{text}</div></div>', unsafe_allow_html=True)


def render_char_counter(text: str, limit: int):
    s = char_count_status(text, limit)
    cls = "char-over" if s["is_over"] else ""
    st.markdown(f'<div class="char-counter {cls}">{s["count"]:,} / {limit:,} chars</div>', unsafe_allow_html=True)


def copy_and_share_linkedin_button(content: str, key: str):
    import urllib.parse
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
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        cursor: pointer;
        width: 100%;
        text-align: center;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(10, 102, 194, 0.2);
        font-family: 'Inter', sans-serif;
    }}
    .custom-share-btn:hover {{
        background: linear-gradient(135deg, #004182, #002244);
        box-shadow: 0 6px 16px rgba(10, 102, 194, 0.4);
        transform: translateY(-1px);
    }}
    </style>
    """
    import streamlit.components.v1 as cv1
    cv1.html(html_code, height=45)


def copy_and_share_twitter_button(content: str, key: str):
    import urllib.parse
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
        background: linear-gradient(135deg, #15202b, #000000);
        color: white;
        border: 1px solid #333;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        cursor: pointer;
        width: 100%;
        text-align: center;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        font-family: 'Inter', sans-serif;
    }}
    .custom-share-btn-tw:hover {{
        background: #000;
        border-color: #555;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
        transform: translateY(-1px);
    }}
    </style>
    """
    import streamlit.components.v1 as cv1
    cv1.html(html_code, height=45)

