import os
import streamlit as st
from config import APP_VERSION

VOICE_MAP = {
    "Professional & Formal":        "Write in a professional, formal tone. Polished language, avoid slang, clear structure.",
    "Casual & Conversational":      "Write casually, like talking to a smart friend. Use contractions, keep it warm and direct.",
    "Humorous & Witty":             "Use clever humor and wit. Make it entertaining without being cringe.",
    "Inspirational & Motivational": "Write in an uplifting, motivational tone. Inspire action and ambition.",
    "Technical & Analytical":      "Use precise, data-driven language. Back every claim with logic and concrete technical evidence.",
    "Startup / Founder":           "Write like a confident founder — bold, direct, mission-driven, zero corporate fluff.",
    "Custom":                      "",
}


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            f'<div style="padding:0.75rem 0 0.25rem;font-family:\'Space Grotesk\',sans-serif;font-size:1.15rem;font-weight:700;color:#fff;">'
            f'⚙️ Growth Engine <span style="font-size:0.7rem;color:#818cf8;background:rgba(99,102,241,0.15);padding:2px 8px;border-radius:12px;">v{APP_VERSION}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── API Key Configuration ──────────────────────────────
        st.caption("🔑 API CONFIGURATION")
        existing_key = (
            st.session_state.get("custom_api_key")
            or st.secrets.get("GOOGLE_API_KEY")
            or st.secrets.get("google_api_key")
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )

        api_key_input = st.text_input(
            "Google Gemini API Key",
            value=existing_key,
            type="password",
            placeholder="AIzaSy...",
            help="Get your free API key at https://aistudio.google.com/app/apikey",
            key="api_key_field",
        )
        if api_key_input:
            st.session_state["custom_api_key"] = api_key_input
            st.markdown('<span style="font-size:0.75rem;color:#10b981;font-weight:600;">🟢 Gemini Key Active</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="font-size:0.75rem;color:#f59e0b;font-weight:600;">⚠️ Key Required for AI</span>', unsafe_allow_html=True)
            st.caption("[Get a free Gemini API key →](https://aistudio.google.com/app/apikey)")

        st.divider()

        # ── Brand Voice ────────────────────────────────────────
        st.caption("🎭 BRAND VOICE & TONE")
        opts = list(VOICE_MAP.keys())
        current_voice = st.session_state.get("brand_voice", "Professional & Formal")
        sel = st.selectbox(
            "Select Voice Preset",
            opts,
            index=opts.index(current_voice) if current_voice in opts else 0,
            key="brand_voice_select",
        )
        st.session_state["brand_voice"] = sel

        if sel == "Custom":
            cv = st.text_area(
                "Describe your custom voice",
                value=st.session_state.get("custom_voice", ""),
                placeholder="e.g., Like a veteran CTO — candid, empathetic, zero buzzwords, data-backed.",
                key="custom_voice_input",
            )
            st.session_state["custom_voice"] = cv
            voice = cv or VOICE_MAP["Professional & Formal"]
        else:
            voice = VOICE_MAP[sel]

        if st.session_state.get("voice_dna_profile"):
            use_dna = st.checkbox("Apply my extracted Voice DNA", value=False, key="use_voice_dna")
            if use_dna:
                voice = st.session_state["voice_dna_profile"]
                st.markdown('<span style="font-size:0.75rem;color:#a78bfa;font-weight:600;">🧬 Voice DNA Active</span>', unsafe_allow_html=True)

        st.divider()

        # ── Session Stats ──────────────────────────────────────
        st.caption("📊 SESSION STATS")
        hist_count = len(st.session_state.get("history", []))
        sched_count = len(st.session_state.get("scheduled_posts", []))
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Generated", f"{hist_count}")
        with col_s2:
            st.metric("Scheduled", f"{sched_count}")

        if hist_count > 0:
            if st.button("🗑️ Clear History", key="clear_hist", use_container_width=True):
                st.session_state["history"] = []
                st.rerun()

        st.divider()
        st.markdown(
            '<div style="font-size:0.75rem;color:#64748b;text-align:center;">'
            'Growth Engine AI · Human-In-The-Loop Content Velocity'
            '</div>',
            unsafe_allow_html=True,
        )

    return voice
