import streamlit as st
from datetime import datetime

from config import LINKEDIN, TWITTER, INSTAGRAM, LINKEDIN_FORMATS, MAX_HISTORY_ENTRIES
from prompts import (
    build_linkedin_prompt, build_twitter_thread_prompt,
    build_instagram_caption_prompt, build_hook_rewrite_prompt,
    build_voice_extraction_prompt, build_voice_matched_prompt,
    build_autopsy_prompt, build_apply_pattern_prompt,
    build_graphic_prompt, build_profile_audit_prompt,
    build_hashtag_research_prompt, build_engagement_analysis_prompt,
    build_video_storyboard_prompt,
)
from services import GeminiService, extract_section, split_variations, split_numbered_tweets, char_count_status
from services.pdf_export import build_content_pdf
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.shared import (
    copy_button, platform_badge, empty_state, render_char_counter,
    copy_and_share_linkedin_button, copy_and_share_twitter_button
)
import json
import os

# ── Setup ─────────────────────────────────────────────────
st.set_page_config(page_title="Growth Engine AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()


# ── Post Scheduler Backend ────────────────────────────────
def load_scheduled_posts():
    if os.path.exists("scheduled_posts.json"):
        try:
            with open("scheduled_posts.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_scheduled_post(platform, content, date, time):
    posts = load_scheduled_posts()
    new_post = {
        "id": len(posts) + 1,
        "platform": platform,
        "content": content[:150] + ("..." if len(content) > 150 else ""),
        "full_content": content,
        "date": str(date),
        "time": str(time),
        "status": "Scheduled"
    }
    posts.append(new_post)
    with open("scheduled_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    return new_post


# ── Gemini Service ────────────────────────────────────────
def get_gemini():
    if "gemini_service" not in st.session_state:
        key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("google_api_key")
        if not key:
            st.session_state["gemini_service"] = None
            st.session_state["init_error"] = "GOOGLE_API_KEY missing in Streamlit secrets."
        else:
            try:
                st.session_state["gemini_service"] = GeminiService(api_key=key)
                st.session_state["init_error"] = None
            except Exception as e:
                st.session_state["gemini_service"] = None
                st.session_state["init_error"] = str(e)
    return st.session_state["gemini_service"]


gemini = get_gemini()
if gemini is None:
    st.error(f"⚠️ {st.session_state.get('init_error')}")
    st.info("Go to Streamlit Cloud → your app → Settings → Secrets, and add: `GOOGLE_API_KEY = \"your_key\"`")
    st.stop()


# ── Session State ─────────────────────────────────────────
_defaults = {
    "post_variations": [], "twitter_tweets": [], "hooks_raw": "",
    "ig_caption_raw": "", "voice_dna_profile": "", "voice_samples": [],
    "autopsy_result": "", "history": [],
    "brand_voice": "Professional & Formal", "custom_voice": "",
    "audit_raw": "", "hashtags_raw": "", "video_storyboard_raw": "",
    "scheduled_posts": load_scheduled_posts()
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def save_history(entry_type: str, platform: str, content: str):
    entry = {"type": entry_type, "platform": platform, "content": content,
             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}
    st.session_state["history"].insert(0, entry)
    st.session_state["history"] = st.session_state["history"][:MAX_HISTORY_ENTRIES]


# ── Sidebar + Header ──────────────────────────────────────
voice_instruction = render_sidebar()

st.markdown("""
<div class="ge-header">
  <div class="ge-title">🚀 Growth Engine AI</div>
  <div class="ge-subtitle">Platform-native content in your voice — LinkedIn · X/Twitter · Instagram</div>
</div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────
tab_li, tab_tw, tab_ig, tab_hook, tab_voice, tab_autopsy, tab_audit, tab_hashtags, tab_visuals, tab_export = st.tabs([
    "💼 LinkedIn", "🐦 Twitter/X", "📸 Instagram",
    "🎣 Hooks", "🧬 Voice DNA", "🔬 Post Autopsy",
    "🔍 Profile Auditor", "🏷️ Hashtag Lab", "🎨 Visual Studio", "📄 Export"
])


# ════════════════════════════════════════════════════════
# LINKEDIN TAB
# ════════════════════════════════════════════════════════
with tab_li:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Your Idea</div>', unsafe_allow_html=True)
        li_topic = st.text_area(
            "What do you want to post about?", height=130, key="li_topic",
            placeholder="e.g., I spent 6 months building a SaaS that got 0 users. Here's what I learned the hard way..."
        )
        li_format = st.selectbox("Post format", list(LINKEDIN_FORMATS.keys()),
                                  format_func=lambda k: LINKEDIN_FORMATS[k], key="li_format")
        li_audience = st.text_input("Target audience",
                                     placeholder="e.g., early-career developers, SaaS founders, product managers",
                                     key="li_audience")
        li_vars = st.slider("Variations to generate", 1, 5, 2, key="li_vars")
        li_cta = st.checkbox("Add CTA question at the end", value=True, key="li_cta")

        if st.button("✨ Generate LinkedIn Post", type="primary", key="gen_li"):
            if not li_topic.strip():
                st.warning("Enter your idea first.")
            else:
                with st.spinner("Writing your LinkedIn post…"):
                    prompt = build_linkedin_prompt(
                        li_topic, voice_instruction, li_audience,
                        li_format, li_vars, li_cta
                    )
                    result = gemini.generate(prompt, max_tokens=3000)

                if result.success:
                    variations = split_variations(result.text)
                    if not variations:
                        st.error("⚠️ AI returned empty — try rephrasing your topic.")
                    else:
                        st.session_state["post_variations"] = variations
                        save_history("LinkedIn Post", "LinkedIn", result.text)
                        st.success(f"✅ {len(variations)} post(s) generated!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Generated Posts</div>', unsafe_allow_html=True)
        if st.session_state["post_variations"]:
            for i, post in enumerate(st.session_state["post_variations"], 1):
                if len(st.session_state["post_variations"]) > 1:
                    st.markdown(f"**Variation {i}**")
                platform_badge("LinkedIn", "li")
                st.markdown(f'<div class="output-box">{post}</div>', unsafe_allow_html=True)
                render_char_counter(post, LINKEDIN.char_limit)

                # Copy and Open LinkedIn
                copy_and_share_linkedin_button(post, f"copy_share_li_{i}")
                
                # Visual Generator for LinkedIn
                with st.expander(f"🎨 Generate Visual for Post {i}"):
                    col_style, col_ratio = st.columns(2)
                    with col_style:
                        img_style = st.selectbox("Style", ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art"], key=f"img_style_li_{i}")
                    with col_ratio:
                        img_ratio = st.selectbox("Aspect Ratio", ["Portrait (4:5)", "Square (1:1)", "Landscape (16:9)"], key=f"img_ratio_li_{i}")
                    
                    if st.button("✨ Generate Graphic", key=f"gen_img_btn_li_{i}"):
                        with st.spinner("Designing graphic prompt..."):
                            prompt_input = build_graphic_prompt(post, "LinkedIn", img_style)
                            p_result = gemini.generate(prompt_input, max_tokens=300)
                        
                        if p_result.success:
                            img_prompt = p_result.text.strip()
                            st.caption(f"**Visual Prompt:** {img_prompt}")
                            
                            import urllib.parse
                            encoded_prompt = urllib.parse.quote(img_prompt)
                            width, height = 800, 1000
                            if img_ratio == "Square (1:1)":
                                width, height = 1024, 1024
                            elif img_ratio == "Landscape (16:9)":
                                width, height = 1280, 720
                                
                            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"
                            
                            with st.spinner("Rendering image..."):
                                try:
                                    import requests
                                    img_data = requests.get(image_url, timeout=30).content
                                    st.image(img_data, use_container_width=True)
                                    st.download_button(
                                        label="⬇️ Download Graphic",
                                        data=img_data,
                                        file_name=f"linkedin_post_{i}_graphic.png",
                                        mime="image/png",
                                        key=f"dl_img_li_{i}"
                                    )
                                except Exception as img_err:
                                    st.error(f"Failed to load image: {img_err}")
                        else:
                            st.error(f"Failed to generate prompt: {p_result.error_message}")

                # Engagement Analysis
                with st.expander(f"📊 Analyze Engagement Rate for Post {i}"):
                    if st.button("🔬 Analyze Engagement", key=f"eval_eng_li_{i}"):
                        with st.spinner("Analyzing post metrics..."):
                            eng_prompt = build_engagement_analysis_prompt(post, "LinkedIn")
                            eng_result = gemini.generate(eng_prompt, max_tokens=1000)
                        if eng_result.success:
                            st.markdown(eng_result.text)
                        else:
                            st.error(eng_result.error_message)

                # Scheduler
                with st.expander(f"📅 Schedule Post {i}"):
                    col_d, col_t = st.columns(2)
                    with col_d:
                        sch_date = st.date_input("Date", key=f"sch_date_li_{i}")
                    with col_t:
                        sch_time = st.time_input("Time", key=f"sch_time_li_{i}")
                    
                    if st.button("📅 Save Schedule", key=f"sch_btn_li_{i}"):
                        saved_post = save_scheduled_post("LinkedIn", post, sch_date, sch_time)
                        st.success(f"✅ Successfully scheduled for {sch_date} at {sch_time}!")
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            empty_state("✍️", "Fill in your idea on the left and click Generate.")


# ════════════════════════════════════════════════════════
# TWITTER/X TAB
# ════════════════════════════════════════════════════════
with tab_tw:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Your Idea</div>', unsafe_allow_html=True)
        tw_topic = st.text_area(
            "What do you want to tweet about?", height=130, key="tw_topic",
            placeholder="e.g., The counterintuitive reason why most SaaS products fail in month 3..."
        )
        tw_type = st.radio("Account type", ["personal", "professional"], horizontal=True, key="tw_type")
        tw_num = st.slider("Thread length (tweets)", 3, 10, 6, key="tw_num")

        if st.button("✨ Generate Twitter Thread", type="primary", key="gen_tw"):
            if not tw_topic.strip():
                st.warning("Enter your idea first.")
            else:
                with st.spinner("Writing your thread…"):
                    prompt = build_twitter_thread_prompt(tw_topic, voice_instruction, tw_num, tw_type)
                    result = gemini.generate(prompt, max_tokens=2500)

                if result.success:
                    tweets = split_numbered_tweets(result.text)
                    if not tweets:
                        st.error("⚠️ Couldn't parse tweets. Try generating again.")
                    else:
                        st.session_state["twitter_tweets"] = tweets
                        save_history("Twitter Thread", "Twitter/X", result.text)
                        st.success(f"✅ {len(tweets)}-tweet thread generated!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Generated Thread</div>', unsafe_allow_html=True)
        if st.session_state["twitter_tweets"]:
            platform_badge("X / Twitter", "tw")
            full_thread = "\n\n".join(st.session_state["twitter_tweets"])

            for tweet in st.session_state["twitter_tweets"]:
                s = char_count_status(tweet, TWITTER.char_limit)
                border = "#ef4444" if s["is_over"] else "#1d9bf0"
                st.markdown(
                    f'<div class="output-box" style="border-left:3px solid {border};">{tweet}</div>',
                    unsafe_allow_html=True
                )
                render_char_counter(tweet, TWITTER.char_limit)

            st.markdown("<br>", unsafe_allow_html=True)

            # Copy and Open Twitter
            copy_and_share_twitter_button(full_thread, "copy_share_tw")
            
            # Engagement Analysis for Twitter
            with st.expander("📊 Analyze Thread Engagement"):
                if st.button("🔬 Analyze Engagement", key="eval_eng_tw"):
                    with st.spinner("Analyzing thread metrics..."):
                        eng_prompt = build_engagement_analysis_prompt(full_thread, "Twitter/X")
                        eng_result = gemini.generate(eng_prompt, max_tokens=1000)
                    if eng_result.success:
                        st.markdown(eng_result.text)
                    else:
                        st.error(eng_result.error_message)

            # Scheduler for Twitter
            with st.expander("📅 Schedule Thread"):
                col_d, col_t = st.columns(2)
                with col_d:
                    sch_date = st.date_input("Date", key="sch_date_tw")
                with col_t:
                    sch_time = st.time_input("Time", key="sch_time_tw")
                
                if st.button("📅 Save Schedule", key="sch_btn_tw"):
                    saved_post = save_scheduled_post("Twitter/X", full_thread, sch_date, sch_time)
                    st.success(f"✅ Successfully scheduled for {sch_date} at {sch_time}!")
            
            # Visual Generator for Twitter
            with st.expander("🎨 Generate Visual for Thread"):
                col_style, col_ratio = st.columns(2)
                with col_style:
                    img_style_tw = st.selectbox("Style", ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art"], key="img_style_tw")
                with col_ratio:
                    img_ratio_tw = st.selectbox("Aspect Ratio", ["Landscape (16:9)", "Square (1:1)"], key="img_ratio_tw")
                
                if st.button("✨ Generate Graphic", key="gen_img_btn_tw"):
                    with st.spinner("Designing graphic prompt..."):
                        prompt_input = build_graphic_prompt(full_thread[:1000], "Twitter/X", img_style_tw)
                        p_result = gemini.generate(prompt_input, max_tokens=300)
                    
                    if p_result.success:
                        img_prompt = p_result.text.strip()
                        st.caption(f"**Visual Prompt:** {img_prompt}")
                        
                        import urllib.parse
                        encoded_prompt = urllib.parse.quote(img_prompt)
                        width, height = 1280, 720
                        if img_ratio_tw == "Square (1:1)":
                            width, height = 1024, 1024
                            
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"
                        
                        with st.spinner("Rendering image..."):
                            try:
                                import requests
                                img_data = requests.get(image_url, timeout=30).content
                                st.image(img_data, use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download Graphic",
                                    data=img_data,
                                    file_name="twitter_thread_graphic.png",
                                    mime="image/png",
                                    key="dl_img_tw"
                                )
                            except Exception as img_err:
                                st.error(f"Failed to load image: {img_err}")
                    else:
                        st.error(f"Failed to generate prompt: {p_result.error_message}")
        else:
            empty_state("🐦", "Fill in your idea on the left and click Generate.")


# ════════════════════════════════════════════════════════
# INSTAGRAM TAB
# ════════════════════════════════════════════════════════
with tab_ig:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Your Post</div>', unsafe_allow_html=True)
        ig_topic = st.text_area("What is your post about?", height=100, key="ig_topic",
                                 placeholder="e.g., Behind-the-scenes of launching my first product at 2am")
        ig_type = st.selectbox("Content type",
                                ["Single image / photo", "Carousel (multi-slide)", "Reel / short video", "Story"],
                                key="ig_type")
        ig_vibe = st.selectbox("Caption vibe",
                                ["Inspirational & value-packed", "Raw & authentic / vulnerable",
                                 "Educational / informational", "Funny & entertaining",
                                 "Product / service focused", "Behind-the-scenes"],
                                key="ig_vibe")
        ig_cta = st.selectbox("Call-to-action",
                               ["Save this post", "Share with a friend", "Drop a comment",
                                "Follow for more", "Click the link in bio", "No CTA"],
                               key="ig_cta")
        ig_len = st.radio("Length", ["Short (<100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
                           horizontal=True, key="ig_len")

        if st.button("✨ Generate Instagram Caption", type="primary", key="gen_ig"):
            if not ig_topic.strip():
                st.warning("Enter what your post is about.")
            else:
                with st.spinner("Writing your captions…"):
                    prompt = build_instagram_caption_prompt(ig_topic, voice_instruction, ig_type, ig_vibe, ig_cta, ig_len)
                    result = gemini.generate(prompt, max_tokens=2000)

                if result.success:
                    st.session_state["ig_caption_raw"] = result.text
                    save_history("Instagram Caption", "Instagram", result.text)
                    st.success("✅ Captions ready!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Generated Captions</div>', unsafe_allow_html=True)
        if st.session_state["ig_caption_raw"]:
            raw = st.session_state["ig_caption_raw"]
            ver_a = extract_section(raw, ["CAPTION VERSION A", "VERSION A"])
            ver_b = extract_section(raw, ["CAPTION VERSION B", "VERSION B"])
            story = extract_section(raw, ["STORY TEASER", "STORY HOOK"])

            platform_badge("Instagram", "ig")
            st.markdown("**Version A**")
            st.markdown(f'<div class="output-box">{ver_a}</div>', unsafe_allow_html=True)
            render_char_counter(ver_a, INSTAGRAM.char_limit)
            copy_button(ver_a, "copy_ig_a", "📋 Copy Version A")

            st.markdown("<br>**Version B**")
            st.markdown(f'<div class="output-box">{ver_b}</div>', unsafe_allow_html=True)
            copy_button(ver_b, "copy_ig_b", "📋 Copy Version B")

            if story and story != raw:
                st.markdown("<br>**Story Teaser**")
                st.markdown(f'<div class="output-box">{story}</div>', unsafe_allow_html=True)
                copy_button(story, "copy_ig_story", "📋 Copy Story Teaser")

            # Visual Generator for Instagram
            with st.expander("🎨 Generate Visual for Instagram"):
                col_style_ig, col_ratio_ig = st.columns(2)
                with col_style_ig:
                    img_style_ig = st.selectbox("Style", ["Photorealistic", "Modern Illustration", "Minimalist Flat Design", "Professional 3D Render", "Neon Cyberpunk"], key="img_style_ig")
                with col_ratio_ig:
                    img_ratio_ig = st.selectbox("Aspect Ratio", ["Square (1:1)", "Portrait (4:5)"], key="img_ratio_ig")
                
                if st.button("✨ Generate Caption Graphic", key="gen_img_btn_ig"):
                    with st.spinner("Designing graphic prompt..."):
                        prompt_input = build_graphic_prompt(raw, "Instagram", img_style_ig)
                        p_result = gemini.generate(prompt_input, max_tokens=300)
                    
                    if p_result.success:
                        img_prompt = p_result.text.strip()
                        st.caption(f"**Visual Prompt:** {img_prompt}")
                        
                        import urllib.parse
                        encoded_prompt = urllib.parse.quote(img_prompt)
                        width, height = 1024, 1024
                        if img_ratio_ig == "Portrait (4:5)":
                            width, height = 800, 1000
                            
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"
                        
                        with st.spinner("Rendering image..."):
                            try:
                                import requests
                                img_data = requests.get(image_url, timeout=30).content
                                st.image(img_data, use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download Graphic",
                                    data=img_data,
                                    file_name="instagram_post_graphic.png",
                                    mime="image/png",
                                    key="dl_img_ig"
                                )
                            except Exception as img_err:
                                st.error(f"Failed to load image: {img_err}")
                    else:
                        st.error(f"Failed to generate prompt: {p_result.error_message}")

            # Engagement Analysis for Instagram
            with st.expander("📊 Analyze Instagram Engagement"):
                if st.button("🔬 Analyze Engagement", key="eval_eng_ig"):
                    with st.spinner("Analyzing caption metrics..."):
                        eng_prompt = build_engagement_analysis_prompt(raw, "Instagram")
                        eng_result = gemini.generate(eng_prompt, max_tokens=1000)
                    if eng_result.success:
                        st.markdown(eng_result.text)
                    else:
                        st.error(eng_result.error_message)

            # Scheduler for Instagram
            with st.expander("📅 Schedule Instagram Post"):
                col_d, col_t = st.columns(2)
                with col_d:
                    sch_date = st.date_input("Date", key="sch_date_ig")
                with col_t:
                    sch_time = st.time_input("Time", key="sch_time_ig")
                
                if st.button("📅 Save Schedule", key="sch_btn_ig"):
                    saved_post = save_scheduled_post("Instagram", raw, sch_date, sch_time)
                    st.success(f"✅ Successfully scheduled for {sch_date} at {sch_time}!")
            
            # Video Storyboarder for Reels/TikToks
            with st.expander("📹 Reels / Short Video Storyboarder"):
                v_duration = st.slider("Video Duration (seconds)", 15, 60, 30, key="v_duration_ig")
                if st.button("🎬 Generate Storyboard & Script", key="gen_storyboard_btn"):
                    with st.spinner("Writing video storyboard & script..."):
                        v_prompt = build_video_storyboard_prompt(raw[:1000], voice_instruction, v_duration)
                        v_result = gemini.generate(v_prompt, max_tokens=1500)
                    if v_result.success:
                        st.markdown(v_result.text)
                        copy_button(v_result.text, "copy_storyboard", "📋 Copy Storyboard")
                    else:
                        st.error(v_result.error_message)

            st.markdown(
                '<br><a href="https://www.instagram.com/create/story/" target="_blank" '
                'style="display:inline-block;background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);'
                'color:#fff;padding:6px 14px;border-radius:7px;text-decoration:none;font-size:0.82rem;font-weight:600;margin-top:10px;">📸 Open Instagram</a>',
                unsafe_allow_html=True
            )
        else:
            empty_state("📸", "Fill in your post topic on the left and click Generate.")


# ════════════════════════════════════════════════════════
# HOOKS TAB
# ════════════════════════════════════════════════════════
with tab_hook:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Rewrite Your Hook</div>', unsafe_allow_html=True)
        st.caption("The first line is 80% of your post. Paste your weak opener — we'll rewrite it using 7 different psychological frameworks.")
        boring = st.text_input("Your current opening line", placeholder="e.g., I launched a new product today.", key="hook_input")
        hook_ctx = st.text_input("Post context (optional)", placeholder="e.g., About lessons from a failed SaaS launch", key="hook_ctx")
        hook_plat = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="hook_plat")
        hook_n = st.slider("Number of rewrites", 3, 10, 7, key="hook_n")

        if st.button("🔥 Rewrite My Hook", type="primary", key="gen_hooks"):
            if not boring.strip():
                st.warning("Enter your opening line first.")
            else:
                with st.spinner("Crafting hooks…"):
                    prompt = build_hook_rewrite_prompt(boring, hook_ctx, hook_plat, hook_n)
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["hooks_raw"] = result.text
                    save_history("Hooks", hook_plat, result.text)
                    st.success("✅ Hooks ready!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Hook Variations</div>', unsafe_allow_html=True)
        if st.session_state["hooks_raw"]:
            st.markdown(st.session_state["hooks_raw"])
            st.markdown("<br>", unsafe_allow_html=True)
            copy_button(st.session_state["hooks_raw"], "copy_hooks", "📋 Copy All Hooks")
        else:
            empty_state("🎣", "Your hook rewrites will appear here — 7 different psychological frameworks.")


# ════════════════════════════════════════════════════════
# VOICE DNA TAB
# ════════════════════════════════════════════════════════
with tab_voice:
    st.markdown('<div class="sec-head">🧬 Extract Your Writing Voice</div>', unsafe_allow_html=True)
    st.caption("Paste 2-5 of your past posts — the AI will extract your exact voice so all future content sounds authentically like you, not generic AI.")

    num_s = st.number_input("How many samples to paste?", 1, 5, 2, key="num_voice_samples")
    samples = []
    for i in range(int(num_s)):
        s = st.text_area(f"Sample post {i+1}", height=100, key=f"voice_sample_{i}",
                          placeholder="Paste one of your real posts here...")
        if s.strip():
            samples.append(s)

    if st.button("🧬 Extract My Voice DNA", type="primary", key="gen_voice_dna"):
        if not samples:
            st.warning("Paste at least one sample post.")
        else:
            with st.spinner("Analyzing your writing style…"):
                prompt = build_voice_extraction_prompt(samples)
                result = gemini.generate(prompt, max_tokens=1500)
            if result.success:
                st.session_state["voice_dna_profile"] = result.text
                st.success("✅ Voice DNA extracted! Enable it in the sidebar to use it for all generations.")
            else:
                st.error(f"⚠️ {result.error_message}")

    if st.session_state["voice_dna_profile"]:
        st.divider()
        st.markdown("**Your Voice DNA Profile**")
        st.markdown(st.session_state["voice_dna_profile"])
        st.divider()
        st.markdown("**Generate Content In Your Exact Voice**")
        v_topic = st.text_input("New topic to write about", key="voice_new_topic")
        v_plat = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="voice_platform")
        if st.button("✨ Write In My Voice", type="primary", key="gen_voice_matched"):
            if not v_topic.strip():
                st.warning("Enter a topic.")
            else:
                with st.spinner("Writing in your voice…"):
                    prompt = build_voice_matched_prompt(st.session_state["voice_dna_profile"], v_topic, v_plat)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.markdown(f'<div class="output-box">{result.text}</div>', unsafe_allow_html=True)
                    copy_button(result.text, "copy_voice_matched", "📋 Copy")
                    save_history("Voice-Matched Post", v_plat, result.text)
                else:
                    st.error(f"⚠️ {result.error_message}")


# ════════════════════════════════════════════════════════
# POST AUTOPSY TAB
# ════════════════════════════════════════════════════════
with tab_autopsy:
    st.markdown('<div class="sec-head">🔬 Reverse-Engineer Your Best Post</div>', unsafe_allow_html=True)
    st.caption("Paste a post that got unusually high engagement. We'll break down exactly WHY it worked — then apply that formula to new topics.")

    a_post = st.text_area("Paste your best-performing post", height=150, key="autopsy_post",
                           placeholder="Paste the post that went viral / got the most comments / performed best...")
    a_plat = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram"], key="autopsy_platform")
    a_perf = st.text_input("Performance context (optional)",
                            placeholder="e.g., Got 300 comments, 10x my usual reach, went viral in my niche",
                            key="autopsy_perf")

    if st.button("🔬 Analyze This Post", type="primary", key="gen_autopsy"):
        if not a_post.strip():
            st.warning("Paste a post to analyze.")
        else:
            with st.spinner("Analyzing why this worked…"):
                prompt = build_autopsy_prompt(a_post, a_perf, a_plat)
                result = gemini.generate(prompt, max_tokens=1500)
            if result.success:
                st.session_state["autopsy_result"] = result.text
                st.success("✅ Analysis complete!")
            else:
                st.error(f"⚠️ {result.error_message}")

    if st.session_state["autopsy_result"]:
        st.divider()
        st.markdown(st.session_state["autopsy_result"])
        st.divider()
        st.markdown("**Apply This Pattern To a New Topic**")
        a_new = st.text_input("New topic", key="autopsy_new_topic",
                               placeholder="e.g., Building a personal brand as an introvert")
        if st.button("✨ Apply Winning Pattern", type="primary", key="gen_apply_pattern"):
            if not a_new.strip():
                st.warning("Enter a topic.")
            else:
                pattern = extract_section(st.session_state["autopsy_result"], ["REPLICABLE PATTERN"])
                with st.spinner("Applying the pattern…"):
                    prompt = build_apply_pattern_prompt(pattern, a_new, voice_instruction)
                    result = gemini.generate(prompt, max_tokens=1500)
                if result.success:
                    st.markdown(f'<div class="output-box">{result.text}</div>', unsafe_allow_html=True)
                    copy_button(result.text, "copy_autopsy_applied", "📋 Copy")
                    save_history("Pattern-Applied Post", a_plat, result.text)
                else:
                    st.error(f"⚠️ {result.error_message}")


# ════════════════════════════════════════════════════════
# PROFILE AUDITOR TAB
# ════════════════════════════════════════════════════════
with tab_audit:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Bio Audit</div>', unsafe_allow_html=True)
        bio = st.text_area("Paste your current bio / headline:", height=120, key="audit_bio",
                           placeholder="e.g., Software Engineer @ XYZ | Passionate about tech | Let's connect!")
        audience_a = st.text_input("Who should this bio attract?", placeholder="e.g., Series A startup founders, Fortune 500 recruiters", key="audit_audience")
        platform_a = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Both"], key="audit_platform")
        goal_a = st.selectbox("Your primary goal with this profile", [
            "Get hired / job opportunities",
            "Attract clients / freelance work",
            "Build a personal brand / audience",
            "Networking / partnerships",
            "Thought leadership",
        ], key="audit_goal")

        if st.button("🔍 Audit My Profile", type="primary", key="gen_audit"):
            if not bio.strip():
                st.warning("Paste your bio first.")
            else:
                prompt = build_profile_audit_prompt(bio, audience_a, platform_a, goal_a, voice_instruction)
                with st.spinner("Auditing your profile…"):
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["audit_raw"] = result.text
                    save_history("Audit", platform_a, result.text)
                    st.success("Audit complete!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Audit Results</div>', unsafe_allow_html=True)
        if st.session_state["audit_raw"]:
            raw_audit = st.session_state["audit_raw"]

            # Extract score and display prominently
            import re
            score_m = re.search(r'SCORE\s*\n+([\s\S]*?)(?=###|\Z)', raw_audit, re.IGNORECASE)
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
            rest_audit = re.sub(r'###\s*SCORE\s*\n+[\s\S]*?(?=###)', '', raw_audit, flags=re.IGNORECASE)
            st.markdown(rest_audit)

            st.divider()
            copy_button(raw_audit, "copy_audit", "📋 Copy Full Audit")
        else:
            empty_state("🔍", "Paste your bio on the left to get a full audit with rewritten versions.")


# ════════════════════════════════════════════════════════
# HASHTAG LAB TAB
# ════════════════════════════════════════════════════════
with tab_hashtags:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-head">Hashtag Research</div>', unsafe_allow_html=True)
        ht_topic = st.text_area("What is your post / content about?", height=100, key="ht_topic",
                                placeholder="e.g., Bootstrapping a SaaS to $10k MRR without VC funding")
        ht_platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "All three"], key="ht_platform")
        ht_niche = st.text_input("Your niche / industry", placeholder="e.g., B2B SaaS, health tech, creator economy", key="ht_niche")
        ht_count = st.slider("Total hashtags to generate", 10, 30, 20, key="ht_count")

        if st.button("🔬 Research Hashtags", type="primary", key="gen_ht"):
            if not ht_topic.strip():
                st.warning("Enter your topic first.")
            else:
                prompt = build_hashtag_research_prompt(ht_topic, ht_platform, ht_niche, ht_count)
                with st.spinner("Researching hashtags…"):
                    result = gemini.generate(prompt, max_tokens=2000)
                if result.success:
                    st.session_state["hashtags_raw"] = result.text
                    save_history("Hashtags", ht_platform, result.text)
                    st.success("Hashtags ready!")
                else:
                    st.error(f"⚠️ {result.error_message}")

    with right:
        st.markdown('<div class="sec-head">Hashtag Sets</div>', unsafe_allow_html=True)
        if st.session_state["hashtags_raw"]:
            st.markdown(st.session_state["hashtags_raw"])
            st.divider()
            copy_button(st.session_state["hashtags_raw"], "copy_ht", "📋 Copy All Hashtags")
        else:
            empty_state("🏷️", "Platform-specific hashtag sets will appear here — organized by reach tier.")


# ════════════════════════════════════════════════════════
# VISUAL STUDIO TAB
# ════════════════════════════════════════════════════════
with tab_visuals:
    st.markdown('<div class="sec-head">🎨 Visual Studio - AI Image & Graphic Generator</div>', unsafe_allow_html=True)
    st.caption("Generate high-quality visuals, illustrations, and photorealistic graphics for your social posts. No API keys needed!")
    
    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        v_topic = st.text_area("Describe the post topic or graphic idea", height=130, key="v_topic_input",
                               placeholder="e.g. A developer experiencing burnout staring at a glowing screen, coding at 3am with coffee cup...")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_style = st.selectbox("Art Style", ["Modern Illustration", "Photorealistic", "Minimalist Flat Design", "Professional 3D Render", "Tech Vector Art", "Cyberpunk Digital Art"], key="v_style")
            v_ratio = st.selectbox("Aspect Ratio", ["Portrait (4:5) - LinkedIn/Instagram", "Square (1:1) - Carousels", "Landscape (16:9) - Twitter/X/Blogs"], key="v_ratio")
        with col_v2:
            v_model = st.selectbox("AI Model", ["flux (Standard)", "flux-realism", "flux-anime"], key="v_model")
            v_nologo = st.checkbox("Remove AI Watermark", value=True, key="v_nologo")
            
        if st.button("✨ Generate AI Graphic", type="primary", key="gen_v_btn"):
            if not v_topic.strip():
                st.warning("Please describe your idea first.")
            else:
                with st.spinner("Designing your graphic prompt..."):
                    # Use Gemini to generate a highly detailed prompt from raw input
                    prompt_input = f"Write a highly detailed, professional image generation prompt in style '{v_style}' about the topic: '{v_topic}'. Ensure there is no text in the image. Return ONLY the prompt text, no intro/outro."
                    p_result = gemini.generate(prompt_input, max_tokens=300)
                    
                if p_result.success:
                    v_prompt = p_result.text.strip()
                    st.session_state["v_generated_prompt"] = v_prompt
                    
                    # Compute width/height
                    width, height = 1024, 1024
                    if "4:5" in v_ratio:
                        width, height = 800, 1000
                    elif "16:9" in v_ratio:
                        width, height = 1280, 720
                        
                    import urllib.parse
                    encoded_v_prompt = urllib.parse.quote(v_prompt)
                    model_param = v_model.split(" ")[0]
                    logo_param = "true" if v_nologo else "false"
                    
                    st.session_state["v_image_url"] = f"https://image.pollinations.ai/prompt/{encoded_v_prompt}?width={width}&height={height}&model={model_param}&nologo={logo_param}"
                else:
                    st.error(f"Failed to create prompt: {p_result.error_message}")
                    
    with col_right:
        st.markdown('<div class="sec-head">Result Preview</div>', unsafe_allow_html=True)
        if "v_image_url" in st.session_state and st.session_state["v_image_url"]:
            st.caption(f"**Generated Prompt:** {st.session_state.get('v_generated_prompt', '')}")
            
            with st.spinner("Rendering your image..."):
                try:
                    import requests
                    img_data = requests.get(st.session_state["v_image_url"], timeout=30).content
                    st.image(img_data, use_container_width=True)
                    st.download_button(
                        label="⬇️ Download Graphic",
                        data=img_data,
                        file_name="growth_engine_graphic.png",
                        mime="image/png",
                        key="dl_v_image"
                    )
                except Exception as e:
                    st.error(f"Could not load image: {e}")
        else:
            empty_state("🎨", "Configure your visual settings on the left and click Generate.")


# ════════════════════════════════════════════════════════
# EXPORT TAB
# ════════════════════════════════════════════════════════
with tab_export:
    st.markdown('<div class="sec-head">📄 Export Your Content</div>', unsafe_allow_html=True)

    if not st.session_state["history"]:
        empty_state("📄", "Generate some content first — it will appear here for download.")
    else:
        st.caption(f"{len(st.session_state['history'])} items in history")
        for i, e in enumerate(st.session_state["history"][:10]):
            with st.expander(f"{e['type']} · {e['platform']} · {e['timestamp']}"):
                st.text(e["content"][:300] + ("…" if len(e["content"]) > 300 else ""))

        st.divider()
        if st.button("📄 Download as PDF", type="primary", key="gen_pdf"):
            with st.spinner("Building PDF…"):
                pdf = build_content_pdf(st.session_state["history"])
            st.download_button(
                "⬇️ Download PDF",
                data=pdf,
                file_name=f"growth_engine_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                key="download_pdf"
            )
