import json
import os
import urllib.parse
from datetime import datetime

import streamlit as st

from config import (
    LINKEDIN, TWITTER, INSTAGRAM, LINKEDIN_FORMATS,
    MAX_HISTORY_ENTRIES, APP_VERSION,
    PLATFORM_IMAGE_SIZES, IMAGE_STYLES,
)
from prompts import (
    build_linkedin_prompt, build_linkedin_carousel_prompt,
    build_twitter_thread_prompt, build_single_tweet_prompt,
    build_instagram_caption_prompt, build_instagram_image_prompt_brief,
    build_hook_rewrite_prompt,
    build_voice_extraction_prompt, build_voice_matched_prompt,
    build_autopsy_prompt, build_apply_pattern_prompt,
    build_graphic_prompt, build_profile_audit_prompt,
    build_hashtag_research_prompt, build_engagement_analysis_prompt,
    build_video_storyboard_prompt,
)
from services import (
    GeminiService, GenerationResult,
    ImageService, ImageResult,
    extract_section, split_variations, split_numbered_tweets,
    char_count_status, word_count, score_linkedin_post,
    clean_image_prompt, build_content_markdown, build_content_json,
    load_scheduled_posts, save_scheduled_post,
    delete_scheduled_post, clear_scheduled_posts,
    export_scheduled_posts_csv, export_scheduled_posts_json,
    build_content_pdf, HAS_REPORTLAB,
)
from components import (
    inject_custom_css, render_sidebar,
    copy_button, platform_badge, empty_state, render_char_counter,
    render_counter, render_quality_score, render_post_preview,
    render_tweet_card, platform_action_link,
    copy_and_share_linkedin_button, copy_and_share_twitter_button,
)

# ── Setup ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Growth Engine AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_custom_css()


# ── Session State ─────────────────────────────────────────
_defaults = {
    "post_variations": [],
    "twitter_tweets": [],
    "hooks_raw": "",
    "ig_caption_raw": "",
    "voice_dna_profile": "",
    "autopsy_result": "",
    "history": [],
    "brand_voice": "Professional & Formal",
    "custom_voice": "",
    "audit_raw": "",
    "hashtags_raw": "",
    "video_storyboard_raw": "",
    "scheduled_posts": load_scheduled_posts(),
    "custom_api_key": "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def save_history(entry_type: str, platform: str, content: str):
    entry = {
        "type": entry_type,
        "platform": platform,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state["history"].insert(0, entry)
    st.session_state["history"] = st.session_state["history"][:MAX_HISTORY_ENTRIES]


# ── Gemini Service Initialization ─────────────────────────
def get_gemini() -> GeminiService | None:
    key = (
        st.session_state.get("custom_api_key")
        or st.secrets.get("GOOGLE_API_KEY")
        or st.secrets.get("google_api_key")
        or os.environ.get("GOOGLE_API_KEY")
    )
    if not key:
        return None
    try:
        return GeminiService(api_key=key)
    except Exception as e:
        st.session_state["init_error"] = str(e)
        return None


def get_image_service() -> ImageService:
    key = (
        st.session_state.get("custom_api_key")
        or st.secrets.get("GOOGLE_API_KEY")
        or st.secrets.get("google_api_key")
        or os.environ.get("GOOGLE_API_KEY")
    )
    return ImageService(google_api_key=key)


# ── Sidebar & Header ──────────────────────────────────────
voice_instruction = render_sidebar()

st.markdown(f"""
<div class="ge-header">
  <div class="ge-version">v{APP_VERSION}</div>
  <div class="ge-title">🚀 Growth Engine AI</div>
  <div class="ge-subtitle">Platform-native social velocity engine — LinkedIn · X/Twitter · Instagram · Visual Studio · Scheduler</div>
  <div class="header-pills">
    <span class="header-pill">💼 LinkedIn Studio</span>
    <span class="header-pill">🐦 Twitter/X Threads</span>
    <span class="header-pill">📸 Instagram Suite</span>
    <span class="header-pill">🎨 AI Visual Studio</span>
    <span class="header-pill">📅 Content Scheduler</span>
    <span class="header-pill">🧬 Voice DNA</span>
  </div>
</div>
""", unsafe_allow_html=True)

gemini = get_gemini()
image_svc = get_image_service()

if gemini is None:
    st.warning("⚠️ **Gemini API Key Needed to Generate Content**")
    st.info(
        "Please enter your Google Gemini API key in the sidebar under **⚙️ Settings → 🔑 API Configuration**, "
        "or add `GOOGLE_API_KEY = \"your_key\"` in `.streamlit/secrets.toml`.\n\n"
        "👉 [Click here to get a free API key at Google AI Studio](https://aistudio.google.com/app/apikey)"
    )


# ── Tabs ──────────────────────────────────────────────────
(
    tab_li, tab_tw, tab_ig, tab_hook,
    tab_voice, tab_autopsy, tab_audit,
    tab_hashtags, tab_visuals, tab_schedule, tab_export
) = st.tabs([
    "💼 LinkedIn", "🐦 Twitter/X", "📸 Instagram",
    "🎣 Hooks", "🧬 Voice DNA", "🔬 Post Autopsy",
    "🔍 Profile Auditor", "🏷️ Hashtag Lab",
    "🎨 Visual Studio", "📅 Schedule", "📄 Export"
])


# ════════════════════════════════════════════════════════
# 1. LINKEDIN TAB
# ════════════════════════════════════════════════════════
with tab_li:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">✍️ Post Creator</div>', unsafe_allow_html=True)
        li_topic = st.text_area(
            "What do you want to post about?", height=130, key="li_topic",
            placeholder="e.g., I spent 6 months building a SaaS that got 0 users. Here's what I learned the hard way..."
        )
        li_format = st.selectbox(
            "Post format",
            list(LINKEDIN_FORMATS.keys()),
            format_func=lambda k: LINKEDIN_FORMATS[k],
            key="li_format",
        )
        li_audience = st.text_input(
            "Target audience",
            placeholder="e.g., early-career developers, SaaS founders, product managers",
            key="li_audience",
        )
        li_vars = st.slider("Variations to generate", 1, 5, 2, key="li_vars")
        li_cta = st.checkbox("Add comment-driving question at the end", value=True, key="li_cta")

        if st.button("✨ Generate LinkedIn Post", type="primary", key="gen_li"):
            if not li_topic.strip():
                st.warning("Please enter your idea first.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Writing high-retention LinkedIn post…"):
                    if li_format == "carousel":
                        prompt = build_linkedin_carousel_prompt(li_topic, voice_instruction, num_slides=6)
                    else:
                        prompt = build_linkedin_prompt(
                            li_topic, voice_instruction, li_audience,
                            li_format, li_vars, li_cta,
                        )
                    result = gemini.generate(prompt, max_tokens=3000)

                if result.success:
                    variations = split_variations(result.text)
                    if not variations:
                        st.error("⚠️ AI returned empty — try rephrasing your topic.")
                    else:
                        st.session_state["post_variations"] = variations
                        save_history("LinkedIn Post", "LinkedIn", result.text)
                        st.success(f"✅ Generated {len(variations)} LinkedIn variation(s)!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">📱 Generated Posts & Optimization</div>', unsafe_allow_html=True)
        if st.session_state["post_variations"]:
            for i, post in enumerate(st.session_state["post_variations"], 1):
                if len(st.session_state["post_variations"]) > 1:
                    st.markdown(f"#### Variation {i}")
                platform_badge("LinkedIn", "li")

                # Quality Score Rubric
                render_quality_score(post)

                # Editable text area
                edited_post = st.text_area("Edit your post", value=post, height=240, key=f"edit_li_{i}")
                render_counter(edited_post, LINKEDIN.char_limit, LINKEDIN.ideal_words)

                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    copy_button(edited_post, f"copy_li_btn_{i}", "📋 Copy Post")
                with col_btn2:
                    copy_and_share_linkedin_button(edited_post, f"share_li_btn_{i}")

                # Live Feed Simulation
                with st.expander("👀 View LinkedIn Feed Simulation"):
                    render_post_preview(edited_post, "LinkedIn")

                # Visual Generator for LinkedIn
                with st.expander(f"🎨 Generate Banner / Visual for Post {i}"):
                    col_style, col_ratio = st.columns(2)
                    with col_style:
                        img_style = st.selectbox(
                            "Style",
                            ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art"],
                            key=f"img_style_li_{i}",
                        )
                    with col_ratio:
                        img_ratio = st.selectbox(
                            "Aspect Ratio",
                            ["Landscape (16:9)", "Square (1:1)", "Portrait (4:5)"],
                            key=f"img_ratio_li_{i}",
                        )

                    if st.button("✨ Generate Graphic", key=f"gen_img_btn_li_{i}"):
                        with st.spinner("Generating graphic prompt and rendering visual…"):
                            prompt_input = build_graphic_prompt(edited_post, "LinkedIn", img_style)
                            p_result = gemini.generate(prompt_input, max_tokens=300)

                            if p_result.success:
                                cleaned_p = clean_image_prompt(p_result.text)
                                st.caption(f"**Visual Prompt:** {cleaned_p}")
                                ratio_key = "16:9" if "16:9" in img_ratio else "4:5" if "4:5" in img_ratio else "1:1"
                                img_res = image_svc.generate(cleaned_p, platform="LinkedIn", ratio=ratio_key, model="flux")

                                if img_res.success and img_res.image_bytes:
                                    st.image(img_res.image_bytes, use_container_width=True)
                                    st.download_button(
                                        label="⬇️ Download Graphic",
                                        data=img_res.image_bytes,
                                        file_name=f"linkedin_post_{i}_graphic.png",
                                        mime="image/png",
                                        key=f"dl_img_li_{i}",
                                        use_container_width=True,
                                    )
                                else:
                                    st.error(f"Image generation error: {img_res.error_message}")
                            else:
                                st.error(f"Failed to generate prompt: {p_result.error_message}")

                # Engagement Analysis
                with st.expander(f"📊 Analyze Engagement Velocity for Post {i}"):
                    if st.button("🔬 Run In-Depth Analysis", key=f"eval_eng_li_{i}"):
                        with st.spinner("Analyzing readability and engagement hooks…"):
                            eng_prompt = build_engagement_analysis_prompt(edited_post, "LinkedIn")
                            eng_result = gemini.generate(eng_prompt, max_tokens=1000)
                        if eng_result.success:
                            st.markdown(eng_result.text)
                        else:
                            st.error(eng_result.error_message)

                # Scheduler
                with st.expander(f"📅 Schedule Post {i}"):
                    col_d, col_t = st.columns(2)
                    with col_d:
                        sch_date = st.date_input("Scheduled Date", key=f"sch_date_li_{i}")
                    with col_t:
                        sch_time = st.time_input("Scheduled Time", key=f"sch_time_li_{i}")

                    if st.button("📅 Add to Content Schedule", key=f"sch_btn_li_{i}", use_container_width=True):
                        saved_post = save_scheduled_post("LinkedIn", edited_post, sch_date, sch_time)
                        st.session_state["scheduled_posts"] = load_scheduled_posts()
                        st.success(f"✅ Added to schedule for {sch_date} at {sch_time}!")
                st.divider()
        else:
            empty_state("💼", "Fill in your idea on the left and click Generate to create LinkedIn posts.")


# ════════════════════════════════════════════════════════
# 2. TWITTER/X TAB
# ════════════════════════════════════════════════════════
with tab_tw:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">🐦 Thread Smith</div>', unsafe_allow_html=True)
        tw_topic = st.text_area(
            "What do you want to tweet about?", height=130, key="tw_topic",
            placeholder="e.g., The counterintuitive reason why most SaaS products fail in month 3..."
        )
        tw_type = st.radio("Account type", ["personal", "professional"], horizontal=True, key="tw_type")
        tw_num = st.slider("Thread length (tweets)", 3, 10, 6, key="tw_num")

        if st.button("✨ Generate Twitter Thread", type="primary", key="gen_tw"):
            if not tw_topic.strip():
                st.warning("Please enter your topic first.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Crafting viral Twitter/X thread…"):
                    prompt = build_twitter_thread_prompt(tw_topic, voice_instruction, tw_num, tw_type)
                    result = gemini.generate(prompt, max_tokens=2500)

                if result.success:
                    tweets = split_numbered_tweets(result.text)
                    if not tweets:
                        st.error("⚠️ Couldn't parse tweets. Try generating again.")
                    else:
                        st.session_state["twitter_tweets"] = tweets
                        save_history("Twitter Thread", "Twitter/X", result.text)
                        st.success(f"✅ Generated {len(tweets)}-tweet thread!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">🧵 Generated Thread & Cards</div>', unsafe_allow_html=True)
        if st.session_state["twitter_tweets"]:
            platform_badge("X / Twitter", "tw")
            full_thread = "\n\n".join(st.session_state["twitter_tweets"])

            # Editable thread text area
            edited_thread = st.text_area(
                "Edit full thread (separate tweets by double-newlines)",
                value=full_thread, height=220, key="edit_tw",
            )

            # Action buttons
            col_tw_btn1, col_tw_btn2 = st.columns(2)
            with col_tw_btn1:
                copy_button(edited_thread, "copy_full_tw_btn", "📋 Copy Entire Thread")
            with col_tw_btn2:
                copy_and_share_twitter_button(edited_thread, "share_tw_btn")

            # Per-tweet card previews with limits
            st.markdown("##### Tweet Breakdown & Limits")
            edited_tweets = [t.strip() for t in edited_thread.split("\n\n") if t.strip()]
            for j, tweet in enumerate(edited_tweets, 1):
                render_tweet_card(tweet, j, len(edited_tweets))
                col_sub1, _ = st.columns([1, 2])
                with col_sub1:
                    copy_button(tweet, f"copy_single_tw_{j}", f"📋 Copy Tweet {j}")

            # Thread Feed Preview
            with st.expander("👀 View X / Twitter Preview"):
                render_post_preview(edited_thread, "Twitter/X")

            # Thread Visual Generator
            with st.expander("🎨 Generate Visual for Thread"):
                col_style_tw, col_ratio_tw = st.columns(2)
                with col_style_tw:
                    img_style_tw = st.selectbox(
                        "Style",
                        ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art"],
                        key="img_style_tw",
                    )
                with col_ratio_tw:
                    img_ratio_tw = st.selectbox("Aspect Ratio", ["Landscape (16:9)", "Square (1:1)"], key="img_ratio_tw")

                if st.button("✨ Generate Thread Graphic", key="gen_img_btn_tw"):
                    with st.spinner("Designing thread graphic…"):
                        prompt_input = build_graphic_prompt(edited_thread[:1000], "Twitter/X", img_style_tw)
                        p_result = gemini.generate(prompt_input, max_tokens=300)

                        if p_result.success:
                            cleaned_p = clean_image_prompt(p_result.text)
                            st.caption(f"**Visual Prompt:** {cleaned_p}")
                            ratio_key = "16:9" if "16:9" in img_ratio_tw else "1:1"
                            img_res = image_svc.generate(cleaned_p, platform="Twitter/X", ratio=ratio_key, model="flux")

                            if img_res.success and img_res.image_bytes:
                                st.image(img_res.image_bytes, use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download Graphic",
                                    data=img_res.image_bytes,
                                    file_name="twitter_thread_graphic.png",
                                    mime="image/png",
                                    key="dl_img_tw",
                                    use_container_width=True,
                                )
                            else:
                                st.error(f"Image generation failed: {img_res.error_message}")
                        else:
                            st.error(f"Failed to generate prompt: {p_result.error_message}")

            # Engagement Analysis
            with st.expander("📊 Analyze Thread Engagement"):
                if st.button("🔬 Analyze Metrics", key="eval_eng_tw"):
                    with st.spinner("Analyzing thread hooks and retweatability…"):
                        eng_prompt = build_engagement_analysis_prompt(edited_thread, "Twitter/X")
                        eng_result = gemini.generate(eng_prompt, max_tokens=1000)
                    if eng_result.success:
                        st.markdown(eng_result.text)
                    else:
                        st.error(eng_result.error_message)

            # Scheduler for Twitter
            with st.expander("📅 Schedule Thread"):
                col_d, col_t = st.columns(2)
                with col_d:
                    sch_date_tw = st.date_input("Scheduled Date", key="sch_date_tw")
                with col_t:
                    sch_time_tw = st.time_input("Scheduled Time", key="sch_time_tw")

                if st.button("📅 Add to Content Schedule", key="sch_btn_tw", use_container_width=True):
                    saved_post = save_scheduled_post("Twitter/X", edited_thread, sch_date_tw, sch_time_tw)
                    st.session_state["scheduled_posts"] = load_scheduled_posts()
                    st.success(f"✅ Added to schedule for {sch_date_tw} at {sch_time_tw}!")
        else:
            empty_state("🐦", "Fill in your topic on the left and click Generate to create Twitter/X threads.")


# ════════════════════════════════════════════════════════
# 3. INSTAGRAM TAB
# ════════════════════════════════════════════════════════
with tab_ig:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">📸 Caption & Story Creator</div>', unsafe_allow_html=True)
        ig_topic = st.text_area(
            "What is your post about?", height=110, key="ig_topic",
            placeholder="e.g., Behind-the-scenes of launching my first product at 2am with zero sleep"
        )
        ig_type = st.selectbox(
            "Content type",
            ["Single image / photo", "Carousel (multi-slide)", "Reel / short video", "Story"],
            key="ig_type",
        )
        ig_vibe = st.selectbox(
            "Caption vibe",
            [
                "Inspirational & value-packed", "Raw & authentic / vulnerable",
                "Educational / informational", "Funny & entertaining",
                "Product / service focused", "Behind-the-scenes",
            ],
            key="ig_vibe",
        )
        ig_cta = st.selectbox(
            "Call-to-action",
            ["Save this post", "Share with a friend", "Drop a comment", "Follow for more", "Click the link in bio", "No CTA"],
            key="ig_cta",
        )
        ig_len = st.radio(
            "Length",
            ["Short (<100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
            horizontal=True, key="ig_len",
        )

        if st.button("✨ Generate Instagram Captions", type="primary", key="gen_ig"):
            if not ig_topic.strip():
                st.warning("Please enter what your post is about.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Crafting high-save Instagram captions…"):
                    prompt = build_instagram_caption_prompt(ig_topic, voice_instruction, ig_type, ig_vibe, ig_cta, ig_len)
                    result = gemini.generate(prompt, max_tokens=2000)

                if result.success:
                    st.session_state["ig_caption_raw"] = result.text
                    save_history("Instagram Caption", "Instagram", result.text)
                    st.success("✅ Captions generated!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">📱 Captions, Visuals & Storyboards</div>', unsafe_allow_html=True)
        if st.session_state["ig_caption_raw"]:
            raw = st.session_state["ig_caption_raw"]
            ver_a = extract_section(raw, ["CAPTION VERSION A", "VERSION A"])
            ver_b = extract_section(raw, ["CAPTION VERSION B", "VERSION B"])
            story = extract_section(raw, ["STORY TEASER", "STORY HOOK"])

            platform_badge("Instagram", "ig")

            # Version A
            st.markdown("##### Version A (Hook-Focused)")
            edited_ver_a = st.text_area("Edit Version A", value=ver_a, height=170, key="edit_ig_a")
            render_counter(edited_ver_a, INSTAGRAM.char_limit, INSTAGRAM.ideal_words)
            copy_button(edited_ver_a, "copy_ig_a_btn", "📋 Copy Version A")

            # Version B
            st.markdown("##### Version B (Story-Focused)")
            edited_ver_b = st.text_area("Edit Version B", value=ver_b, height=170, key="edit_ig_b")
            render_counter(edited_ver_b, INSTAGRAM.char_limit, INSTAGRAM.ideal_words)
            copy_button(edited_ver_b, "copy_ig_b_btn", "📋 Copy Version B")

            # Story Teaser
            if story and story != raw:
                st.markdown("##### Story Teaser")
                edited_story = st.text_area("Edit Story Teaser", value=story, height=90, key="edit_ig_story")
                copy_button(edited_story, "copy_ig_story_btn", "📋 Copy Story Teaser")

            col_ig_act1, col_ig_act2 = st.columns(2)
            with col_ig_act1:
                platform_action_link("https://www.instagram.com/", "📸 Open Instagram", "ig")
            with col_ig_act2:
                active_ver = st.selectbox("Process with:", ["Version A", "Version B"], key="ig_active_ver_sel")
            active_content = edited_ver_a if active_ver == "Version A" else edited_ver_b

            # Visual Generator for Instagram
            with st.expander("🎨 Generate Visual for Instagram"):
                col_style_ig, col_ratio_ig = st.columns(2)
                with col_style_ig:
                    img_style_ig = st.selectbox(
                        "Style",
                        ["Photorealistic", "Modern Illustration", "Minimalist Flat Design", "Professional 3D Render", "Neon Cyberpunk"],
                        key="img_style_ig",
                    )
                with col_ratio_ig:
                    img_ratio_ig = st.selectbox("Aspect Ratio", ["Square (1:1)", "Portrait (4:5)", "Story (9:16)"], key="img_ratio_ig")

                if st.button("✨ Generate Instagram Visual", key="gen_img_btn_ig"):
                    with st.spinner("Designing Instagram visual…"):
                        prompt_input = build_graphic_prompt(active_content, "Instagram", img_style_ig)
                        p_result = gemini.generate(prompt_input, max_tokens=300)

                        if p_result.success:
                            cleaned_p = clean_image_prompt(p_result.text)
                            st.caption(f"**Visual Prompt:** {cleaned_p}")
                            ratio_key = "4:5" if "4:5" in img_ratio_ig else "9:16" if "9:16" in img_ratio_ig else "1:1"
                            img_res = image_svc.generate(cleaned_p, platform="Instagram", ratio=ratio_key, model="flux")

                            if img_res.success and img_res.image_bytes:
                                st.image(img_res.image_bytes, use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download Visual",
                                    data=img_res.image_bytes,
                                    file_name="instagram_post_graphic.png",
                                    mime="image/png",
                                    key="dl_img_ig",
                                    use_container_width=True,
                                )
                            else:
                                st.error(f"Image generation failed: {img_res.error_message}")
                        else:
                            st.error(f"Failed to generate prompt: {p_result.error_message}")

            # Reels / TikTok Video Storyboarder
            with st.expander("📹 Reels / Short Video Storyboarder"):
                v_duration = st.slider("Video Duration (seconds)", 15, 60, 30, key="v_duration_ig")
                if st.button("🎬 Generate Storyboard & Script", key="gen_storyboard_btn"):
                    with st.spinner("Writing second-by-second storyboard…"):
                        v_prompt = build_video_storyboard_prompt(active_content[:1000], voice_instruction, v_duration)
                        v_result = gemini.generate(v_prompt, max_tokens=1500)
                    if v_result.success:
                        st.markdown(v_result.text)
                        copy_button(v_result.text, "copy_storyboard_btn", "📋 Copy Storyboard")
                    else:
                        st.error(v_result.error_message)

            # Scheduler for Instagram
            with st.expander("📅 Schedule Instagram Post"):
                col_d, col_t = st.columns(2)
                with col_d:
                    sch_date_ig = st.date_input("Scheduled Date", key="sch_date_ig")
                with col_t:
                    sch_time_ig = st.time_input("Scheduled Time", key="sch_time_ig")

                if st.button("📅 Add to Content Schedule", key="sch_btn_ig", use_container_width=True):
                    saved_post = save_scheduled_post("Instagram", active_content, sch_date_ig, sch_time_ig)
                    st.session_state["scheduled_posts"] = load_scheduled_posts()
                    st.success(f"✅ Added to schedule for {sch_date_ig} at {sch_time_ig}!")
        else:
            empty_state("📸", "Fill in your post details on the left and click Generate to create Instagram captions.")


# ════════════════════════════════════════════════════════
# 4. HOOKS TAB
# ════════════════════════════════════════════════════════
with tab_hook:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">🎣 Psychological Hook Lab</div>', unsafe_allow_html=True)
        st.caption("The opening line determines 80% of click-through rate and dwell time. Rewrite any opening into 7 psychological angles.")
        boring = st.text_input("Your draft opening line", placeholder="e.g., I launched a new product today.", key="hook_input")
        hook_ctx = st.text_input("Post context (optional)", placeholder="e.g., Lessons from an unexpected SaaS failure", key="hook_ctx")
        hook_plat = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="hook_plat")
        hook_n = st.slider("Number of hook variations", 3, 10, 7, key="hook_n")

        if st.button("🔥 Rewrite My Hook", type="primary", key="gen_hooks"):
            if not boring.strip():
                st.warning("Please enter your opening line first.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Engineering high-conversion hooks…"):
                    prompt = build_hook_rewrite_prompt(boring, hook_ctx, hook_plat, hook_n)
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["hooks_raw"] = result.text
                    save_history("Hooks", hook_plat, result.text)
                    st.success("✅ Hooks ready!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">✨ Psychological Hook Variations</div>', unsafe_allow_html=True)
        if st.session_state["hooks_raw"]:
            st.markdown(st.session_state["hooks_raw"])
            st.markdown("<br>", unsafe_allow_html=True)
            copy_button(st.session_state["hooks_raw"], "copy_hooks_btn", "📋 Copy All Hooks")
        else:
            empty_state("🎣", "Your rewrites will appear here — structured by psychological triggers (Curiosity Gap, Contrarian, Social Proof, etc.).")


# ════════════════════════════════════════════════════════
# 5. VOICE DNA TAB
# ════════════════════════════════════════════════════════
with tab_voice:
    st.markdown('<div class="sec-head">🧬 Voice DNA Extractor</div>', unsafe_allow_html=True)
    st.caption("Paste 2-5 of your top-performing past posts. The engine extracts your exact sentence cadence, vocabulary level, and structural quirks.")

    col_v_in, col_v_out = st.columns([1, 1], gap="large")
    with col_v_in:
        num_s = st.number_input("How many writing samples to analyze?", 1, 5, 2, key="num_voice_samples")
        samples = []
        for i in range(int(num_s)):
            s = st.text_area(f"Sample post {i+1}", height=95, key=f"voice_sample_{i}", placeholder="Paste a real post you wrote here...")
            if s.strip():
                samples.append(s)

        if st.button("🧬 Extract Voice Profile", type="primary", key="gen_voice_dna"):
            if not samples:
                st.warning("Please paste at least one sample post.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Analyzing linguistic patterns & sentence rhythm…"):
                    prompt = build_voice_extraction_prompt(samples)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.session_state["voice_dna_profile"] = result.text
                    st.success("✅ Voice DNA extracted! Check 'Apply my extracted Voice DNA' in the sidebar to activate.")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with col_v_out:
        if st.session_state["voice_dna_profile"]:
            st.markdown("##### Extracted Voice DNA Profile")
            st.markdown(st.session_state["voice_dna_profile"])
            copy_button(st.session_state["voice_dna_profile"], "copy_dna_profile_btn", "📋 Copy Voice Profile")
        else:
            empty_state("🧬", "Paste your writing samples on the left to extract your personalized Voice DNA profile.")

    if st.session_state["voice_dna_profile"]:
        st.divider()
        st.markdown('<div class="sec-head">✍️ Instant Sandbox: Write In My Voice</div>', unsafe_allow_html=True)
        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            v_topic = st.text_input("New topic to write about", placeholder="e.g., Why early optimization kills startups", key="voice_new_topic")
        with col_sb2:
            v_plat = st.selectbox("Target Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="voice_platform")

        if st.button("✨ Generate Voice-Matched Content", type="primary", key="gen_voice_matched"):
            if not v_topic.strip():
                st.warning("Please enter a topic.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Generating post in your signature voice…"):
                    prompt = build_voice_matched_prompt(st.session_state["voice_dna_profile"], v_topic, v_plat)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.markdown(f'<div class="output-box">{result.text}</div>', unsafe_allow_html=True)
                    copy_button(result.text, "copy_voice_matched_btn", "📋 Copy Content")
                    save_history("Voice-Matched Post", v_plat, result.text)
                else:
                    st.error(f"⚠️ {result.error_message}")


# ════════════════════════════════════════════════════════
# 6. POST AUTOPSY TAB
# ════════════════════════════════════════════════════════
with tab_autopsy:
    st.markdown('<div class="sec-head">🔬 Reverse-Engineer Viral Posts</div>', unsafe_allow_html=True)
    st.caption("Paste a post that earned unusually high engagement. Deconstruct the hook, psychological levers, and replicable structure.")

    col_a_in, col_a_out = st.columns([1, 1], gap="large")
    with col_a_in:
        a_post = st.text_area(
            "Paste high-performing post", height=150, key="autopsy_post",
            placeholder="Paste the post that went viral / got 500+ comments / high bookmarks..."
        )
        col_ap1, col_ap2 = st.columns(2)
        with col_ap1:
            a_plat = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="autopsy_platform")
        with col_ap2:
            a_perf = st.text_input("Performance metrics (optional)", placeholder="e.g., 400 comments, 50k impressions", key="autopsy_perf")

        if st.button("🔬 Analyze This Post", type="primary", key="gen_autopsy"):
            if not a_post.strip():
                st.warning("Please paste a post to analyze.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Deconstructing structural & psychological levers…"):
                    prompt = build_autopsy_prompt(a_post, a_perf, a_plat)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.session_state["autopsy_result"] = result.text
                    st.success("✅ Analysis complete!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with col_a_out:
        if st.session_state["autopsy_result"]:
            st.markdown("##### Autopsy Breakdown")
            st.markdown(st.session_state["autopsy_result"])
            copy_button(st.session_state["autopsy_result"], "copy_autopsy_btn", "📋 Copy Analysis")
        else:
            empty_state("🔬", "Paste your best-performing post on the left to extract its formula.")

    if st.session_state["autopsy_result"]:
        st.divider()
        st.markdown('<div class="sec-head">✨ Apply Winning Pattern to New Topic</div>', unsafe_allow_html=True)
        a_new = st.text_input("New topic", placeholder="e.g., Overcoming impostor syndrome as a technical lead", key="autopsy_new_topic")
        if st.button("✨ Apply Replicable Template", type="primary", key="gen_apply_pattern"):
            if not a_new.strip():
                st.warning("Please enter a new topic.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                pattern = extract_section(st.session_state["autopsy_result"], ["REPLICABLE PATTERN"])
                with st.spinner("Applying proven structure to your topic…"):
                    prompt = build_apply_pattern_prompt(pattern, a_new, voice_instruction)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.markdown(f'<div class="output-box">{result.text}</div>', unsafe_allow_html=True)
                    copy_button(result.text, "copy_autopsy_applied", "📋 Copy Post")
                    save_history("Pattern-Applied Post", a_plat, result.text)
                else:
                    st.error(f"⚠️ {result.error_message}")


# ════════════════════════════════════════════════════════
# 7. PROFILE AUDITOR TAB
# ════════════════════════════════════════════════════════
with tab_audit:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">🔍 Personal Brand Bio Auditor</div>', unsafe_allow_html=True)
        bio = st.text_area(
            "Paste your current bio / headline:", height=120, key="audit_bio",
            placeholder="e.g., Software Engineer @ XYZ | Passionate about AI & cloud | Let's connect!"
        )
        audience_a = st.text_input("Target Audience", placeholder="e.g., Seed-stage founders, VP of Engineering, tech recruiters", key="audit_audience")
        platform_a = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Both"], key="audit_platform")
        goal_a = st.selectbox(
            "Primary Goal",
            [
                "Attract clients & inbound freelance deals",
                "Get hired / discover executive job offers",
                "Build thought leadership & audience",
                "Founder networking & investor relations",
            ],
            key="audit_goal",
        )

        if st.button("🔍 Audit My Bio", type="primary", key="gen_audit"):
            if not bio.strip():
                st.warning("Please paste your bio first.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                prompt = build_profile_audit_prompt(bio, audience_a, platform_a, goal_a, voice_instruction)
                with st.spinner("Auditing positioning and authority markers…"):
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["audit_raw"] = result.text
                    save_history("Profile Audit", platform_a, result.text)
                    st.success("✅ Profile audit complete!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">📊 Audit Scorecard & Rewrites</div>', unsafe_allow_html=True)
        if st.session_state["audit_raw"]:
            raw_audit = st.session_state["audit_raw"]
            import re
            score_m = re.search(r'SCORE\s*\n+([\s\S]*?)(?=###|\Z)', raw_audit, re.IGNORECASE)
            if score_m:
                score_text = score_m.group(1).strip()
                num_m = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', score_text)
                score_num = num_m.group(1) if num_m else "–"
                st.markdown(f"""
                <div class="card" style="text-align:center;">
                  <div style="color:#64748b;font-size:0.75rem;letter-spacing:1px;font-weight:600;margin-bottom:4px;">PROFILE AUTHORITY SCORE</div>
                  <div class="score-badge">{score_num}<span style="font-size:1.2rem;color:#64748b;">/10</span></div>
                  <div style="color:#94a3b8;font-size:0.85rem;margin-top:0.5rem;">{score_text.replace(score_num + "/10","").replace(score_num+" / 10","").strip()}</div>
                </div>
                """, unsafe_allow_html=True)

            rest_audit = re.sub(r'###\s*SCORE\s*\n+[\s\S]*?(?=###)', '', raw_audit, flags=re.IGNORECASE)
            st.markdown(rest_audit)
            st.divider()
            copy_button(raw_audit, "copy_audit_btn", "📋 Copy Full Audit & Rewrites")
        else:
            empty_state("🔍", "Paste your headline or bio on the left to receive a /10 score and 3 rewritten versions.")


# ════════════════════════════════════════════════════════
# 8. HASHTAG LAB TAB
# ════════════════════════════════════════════════════════
with tab_hashtags:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">🏷️ Hashtag Matrix Research</div>', unsafe_allow_html=True)
        ht_topic = st.text_area(
            "What is your post / topic about?", height=100, key="ht_topic",
            placeholder="e.g., Bootstrapping a micro-SaaS to $15k MRR without venture capital funding"
        )
        ht_platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "All three"], key="ht_platform")
        ht_niche = st.text_input("Industry / Niche", placeholder="e.g., B2B SaaS, Creator Economy, AI Engineering", key="ht_niche")
        ht_count = st.slider("Total hashtags to generate", 10, 30, 20, key="ht_count")

        if st.button("🔬 Research Reach Sets", type="primary", key="gen_ht"):
            if not ht_topic.strip():
                st.warning("Please enter your topic first.")
            elif gemini is None:
                st.error("Please configure your Gemini API Key in the sidebar.")
            else:
                prompt = build_hashtag_research_prompt(ht_topic, ht_platform, ht_niche, ht_count)
                with st.spinner("Classifying hashtag reach tiers…"):
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["hashtags_raw"] = result.text
                    save_history("Hashtags", ht_platform, result.text)
                    st.success("✅ Hashtag matrix ready!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">📊 Tiered Hashtags (Broad · Niche · Micro)</div>', unsafe_allow_html=True)
        if st.session_state["hashtags_raw"]:
            st.markdown(st.session_state["hashtags_raw"])
            st.divider()
            copy_button(st.session_state["hashtags_raw"], "copy_ht_btn", "📋 Copy All Hashtags")
        else:
            empty_state("🏷️", "Hashtag sets will appear here — structured into High Reach, Niche Authority, and Community tiers.")


# ════════════════════════════════════════════════════════
# 9. VISUAL STUDIO TAB
# ════════════════════════════════════════════════════════
with tab_visuals:
    st.markdown('<div class="sec-head">🎨 Visual Studio — AI Graphic & Image Generator</div>', unsafe_allow_html=True)
    st.caption("Generate high-resolution social media graphics, 3D assets, and photorealistic visuals powered by Flux.")

    col_v_in, col_v_out = st.columns([1, 1], gap="large")

    with col_v_in:
        v_topic = st.text_area(
            "Describe the graphic concept or paste post text", height=130, key="v_topic_input",
            placeholder="e.g., A minimalist isometric workspace with glowing laptop screen, steaming espresso cup, and night city skyline..."
        )
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_style = st.selectbox(
                "Art Style",
                ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art", "Cyberpunk Digital Art", "Cinematic Photography", "Editorial"],
                key="v_style",
            )
            v_ratio = st.selectbox(
                "Aspect Ratio",
                ["Portrait (4:5) - LinkedIn/Instagram", "Square (1:1) - Carousels/IG", "Landscape (16:9) - Twitter/X/Header", "Story (9:16) - Reels/Stories"],
                key="v_ratio",
            )
        with col_v2:
            v_model = st.selectbox("AI Model", ["flux (Standard)", "flux-realism", "flux-anime"], key="v_model")
            v_nologo = st.checkbox("Remove AI Watermark", value=True, key="v_nologo")

        if st.button("✨ Generate AI Graphic", type="primary", key="gen_v_btn"):
            if not v_topic.strip():
                st.warning("Please describe your idea first.")
            else:
                with st.spinner("Designing high-fidelity visual prompt…"):
                    # Use Gemini if available to enhance the prompt, else fallback
                    if gemini:
                        p_in = f"Write a highly detailed, professional image generation prompt in art style '{v_style}' about: '{v_topic}'. Ensure there is no text in the image. Return ONLY the prompt text, zero preamble."
                        p_res = gemini.generate(p_in, max_tokens=300)
                        raw_p = p_res.text if p_res.success else v_topic
                    else:
                        raw_p = f"{v_style} style, {v_topic}, ultra high resolution, 4k"

                    final_p = clean_image_prompt(raw_p)
                    st.session_state["v_generated_prompt"] = final_p

                    ratio_key = "4:5" if "4:5" in v_ratio else "16:9" if "16:9" in v_ratio else "9:16" if "9:16" in v_ratio else "1:1"
                    img_res = image_svc.generate(
                        prompt=final_p,
                        platform="Instagram",
                        ratio=ratio_key,
                        model=v_model,
                        nologo=v_nologo,
                    )
                    st.session_state["v_image_result"] = img_res

    with col_v_out:
        st.markdown('<div class="sec-head">🖼️ Graphic Preview & Download</div>', unsafe_allow_html=True)
        img_res = st.session_state.get("v_image_result")
        if img_res and img_res.success and img_res.image_bytes:
            st.caption(f"**Visual Prompt:** {st.session_state.get('v_generated_prompt', '')}")
            st.caption(f"**Engine:** {img_res.provider}")
            st.image(img_res.image_bytes, use_container_width=True)
            st.download_button(
                label="⬇️ Download Graphic (.png)",
                data=img_res.image_bytes,
                file_name="growth_engine_graphic.png",
                mime="image/png",
                key="dl_v_image_btn",
                use_container_width=True,
            )
        elif img_res and not img_res.success:
            st.error(f"Image generation failed: {img_res.error_message}")
        else:
            empty_state("🎨", "Configure your style on the left and click Generate to produce visuals.")


# ════════════════════════════════════════════════════════
# 10. CONTENT SCHEDULE TAB (NEW)
# ════════════════════════════════════════════════════════
with tab_schedule:
    st.markdown('<div class="sec-head">📅 Content Schedule Manager</div>', unsafe_allow_html=True)
    st.caption("Manage, review, and export all scheduled posts across LinkedIn, X/Twitter, and Instagram.")

    scheduled = load_scheduled_posts()
    st.session_state["scheduled_posts"] = scheduled

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("Total Scheduled", len(scheduled))
    with col_stat2:
        st.metric("LinkedIn", sum(1 for p in scheduled if p.get("platform") == "LinkedIn"))
    with col_stat3:
        st.metric("Twitter/X", sum(1 for p in scheduled if p.get("platform") in ("Twitter/X", "Twitter")))
    with col_stat4:
        st.metric("Instagram", sum(1 for p in scheduled if p.get("platform") == "Instagram"))

    if scheduled:
        col_sch_flt, col_sch_exp = st.columns([1, 1])
        with col_sch_flt:
            platform_filter = st.selectbox("Filter by Platform", ["All", "LinkedIn", "Twitter/X", "Instagram"], key="filter_plat")
        with col_sch_exp:
            st.write("")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                csv_data = export_scheduled_posts_csv(scheduled)
                st.download_button(
                    "⬇️ Export Schedule (CSV)",
                    data=csv_data,
                    file_name=f"content_schedule_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="export_sch_csv",
                    use_container_width=True,
                )
            with col_e2:
                json_data = export_scheduled_posts_json(scheduled)
                st.download_button(
                    "⬇️ Export Schedule (JSON)",
                    data=json_data,
                    file_name=f"content_schedule_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    key="export_sch_json",
                    use_container_width=True,
                )

        filtered = [
            p for p in scheduled
            if platform_filter == "All" or p.get("platform") == platform_filter or (platform_filter == "Twitter/X" and p.get("platform") == "Twitter")
        ]

        st.markdown(f"**Showing {len(filtered)} scheduled post(s)**")

        for item in filtered:
            item_id = item.get("id")
            plat = item.get("platform", "General")
            badge_cls = "li" if "linkedin" in plat.lower() else "tw" if "twitter" in plat.lower() else "ig"

            with st.container():
                st.markdown(
                    f'<div class="schedule-card">'
                    f'<div class="schedule-meta">'
                    f'<div><span class="badge-{badge_cls}">{plat}</span></div>'
                    f'<div class="schedule-pill">🗓️ {item.get("date")} at {item.get("time")}</div>'
                    f'</div>'
                    f'<div style="font-size:0.875rem;line-height:1.6;color:#e2e8f0;margin-top:6px;">{item.get("content")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
                with col_c1:
                    copy_button(item.get("full_content", item.get("content")), f"copy_sch_item_{item_id}", "📋 Copy Content")
                with col_c2:
                    if plat == "LinkedIn":
                        platform_action_link("https://www.linkedin.com/feed/?shareActive=true", "🚀 Open LinkedIn", "li")
                    elif "Twitter" in plat or "X" in plat:
                        platform_action_link("https://twitter.com/intent/tweet", "🚀 Open X/Twitter", "tw")
                    else:
                        platform_action_link("https://www.instagram.com/", "📸 Open Instagram", "ig")
                with col_c3:
                    if st.button("🗑️ Cancel / Delete", key=f"del_sch_{item_id}", use_container_width=True):
                        delete_scheduled_post(item_id)
                        st.session_state["scheduled_posts"] = load_scheduled_posts()
                        st.rerun()

        st.divider()
        if st.button("🗑️ Clear Entire Schedule", key="clear_all_sch_btn"):
            clear_scheduled_posts()
            st.session_state["scheduled_posts"] = []
            st.success("Schedule cleared!")
            st.rerun()
    else:
        empty_state("📅", "No posts scheduled yet. Use the 'Schedule Post' dropdown in the LinkedIn, Twitter, or Instagram tabs to add posts here.")


# ════════════════════════════════════════════════════════
# 11. EXPORT TAB
# ════════════════════════════════════════════════════════
with tab_export:
    st.markdown('<div class="sec-head">📄 Export Your Content Library</div>', unsafe_allow_html=True)

    if not st.session_state["history"]:
        empty_state("📄", "Generate content across any tab and your library will be ready for export here.")
    else:
        st.caption(f"{len(st.session_state['history'])} total items in generation history")
        for i, e in enumerate(st.session_state["history"][:10], 1):
            with st.expander(f"{i}. {e['type']} · {e['platform']} · {e['timestamp']}"):
                st.text(e["content"][:400] + ("…" if len(e["content"]) > 400 else ""))

        col_ex1, col_ex2, col_ex3 = st.columns(3)
        with col_ex1:
            md_content = build_content_markdown(st.session_state["history"])
            st.download_button(
                "⬇️ Download as Markdown (.md)",
                data=md_content,
                file_name=f"growth_engine_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key="download_md",
                use_container_width=True,
            )
        with col_ex2:
            json_content = build_content_json(st.session_state["history"])
            st.download_button(
                "⬇️ Download as JSON (.json)",
                data=json_content,
                file_name=f"growth_engine_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="download_json",
                use_container_width=True,
            )
        with col_ex3:
            if HAS_REPORTLAB:
                try:
                    pdf_data = build_content_pdf(st.session_state["history"])
                    st.download_button(
                        "⬇️ Download as PDF (.pdf)",
                        data=pdf_data,
                        file_name=f"growth_engine_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        key="download_pdf",
                        use_container_width=True,
                    )
                except Exception as pdf_err:
                    st.caption(f"PDF creation failed: {pdf_err}")
            else:
                st.caption("ℹ️ ReportLab not installed for PDF export (Markdown & JSON available).")
