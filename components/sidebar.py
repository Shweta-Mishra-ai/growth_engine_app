import streamlit as st

VOICE_MAP = {
    "Professional & Formal":      "Write in a professional, formal tone. Polished language, avoid slang.",
    "Casual & Conversational":    "Write casually, like talking to a smart friend. Use contractions, keep it warm.",
    "Humorous & Witty":           "Use clever humor and wit. Make it entertaining without being cringe.",
    "Inspirational & Motivational": "Write in an uplifting, motivational tone. Inspire action.",
    "Technical & Analytical":    "Use precise, data-driven language. Back every claim with logic.",
    "Startup / Founder":         "Write like a confident founder — bold, direct, mission-driven, zero corporate speak.",
    "Custom":                    "",
}


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown('<div style="padding:1rem 0 0.5rem;font-family:\'Space Grotesk\',sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;">⚙️ Settings</div>', unsafe_allow_html=True)

        opts = list(VOICE_MAP.keys())
        st.caption("BRAND VOICE")
        sel = st.selectbox("Brand voice", opts, label_visibility="collapsed",
                           index=opts.index(st.session_state.get("brand_voice", "Professional & Formal"))
                           if st.session_state.get("brand_voice") in opts else 0,
                           key="brand_voice_select")
        st.session_state["brand_voice"] = sel

        if sel == "Custom":
            cv = st.text_area("Describe your voice",
                              value=st.session_state.get("custom_voice", ""),
                              placeholder="e.g., Like a startup mentor — direct, empathetic, zero fluff",
                              key="custom_voice_input")
            st.session_state["custom_voice"] = cv
            voice = cv
        else:
            voice = VOICE_MAP[sel]

        if st.session_state.get("voice_dna_profile"):
            if st.checkbox("Use my extracted Voice DNA", value=False, key="use_voice_dna"):
                voice = st.session_state["voice_dna_profile"]
                st.caption("✅ Using Voice DNA")

        st.divider()
        st.caption("📜 HISTORY")
        hist = st.session_state.get("history", [])
        if hist:
            st.write(f"{len(hist)} items")
            if st.button("🗑️ Clear History", key="clear_hist"):
                st.session_state["history"] = []
                st.rerun()
        else:
            st.caption("Generate content to build history.")

        st.divider()
        st.caption("Growth Engine AI v3")

    return voice
