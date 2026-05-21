import streamlit as st
import google.generativeai as genai
import urllib.parse
import json
from datetime import datetime
import re

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Growth Engine AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    .history-item {
        padding: 0.75rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        cursor: pointer;
    }
    .history-item:hover {
        background-color: #e9ecef;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    textarea {
        font-size: 14px !important;
    }
    .stTextArea textarea {
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. API SETUP (SECURE) ---
MODEL_LIST = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
working_model = None

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    try:
        api_key = st.secrets["google_api_key"]
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error("⚠️ API Key missing! Please set 'GOOGLE_API_KEY' in your .streamlit/secrets.toml file.")
        st.stop()

# Find which model works for this API key
available_models_list = []
for m_name in MODEL_LIST:
    try:
        test_model = genai.GenerativeModel(m_name)
        test_model.generate_content("test", generation_config=genai.types.GenerationConfig(max_output_tokens=1))
        working_model = test_model
        break
    except Exception as e:
        available_models_list.append(f"{m_name}: {str(e)}")
        continue

if working_model is None:
    st.error("❌ No compatible Gemini models found for this API key.")
    with st.expander("🔍 View Technical Details (Diagnostics)"):
        st.write("The following models were tested and failed:")
        for detail in available_models_list:
            st.write(detail)
    st.info("💡 Solution: Check your Google AI Studio project settings or try a different Google account.")
    st.stop()
else:
    model = working_model

# --- 3. HELPER FUNCTIONS ---

def generate_content(prompt_text, max_tokens=2048):
    """Wraps the API call with error handling."""
    try:
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(
                prompt_text,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7
                )
            )
            return response.text
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            st.error("⚠️ **API Quota Exceeded**\n\n"
                     "Free tier limit khatam ho gayi.\n\n"
                     "Solutions:\n"
                     "1. Kal try karo (midnight GMT reset)\n"
                     "2. Alti Google account se naya key banao\n"
                     "3. Google Cloud pe free billing enable karo")
        elif "API key not valid" in error_msg or "401" in error_msg:
            st.error("⚠️ **Invalid API Key**\n\n"
                     "Key galat hai ya revoke ho gayi hai.\n\n"
                     "Naya key banao: https://aistudio.google.com/app/apikey")
        elif "404" in error_msg or "not found" in error_msg.lower():
            st.error("⚠️ **Model Not Available**\n\n"
                     "Ye model tumhare key ke saath available nahi.")
        else:
            st.error(f"API Error: {e}")
        return None
        return None

def create_twitter_link(text):
    """Generates a direct 'Post to X' intent link."""
    base_url = "https://twitter.com/intent/tweet?text="
    encoded_text = urllib.parse.quote(text[:280])
    return f"{base_url}{encoded_text}"

def create_linkedin_link(text=""):
    """Generates a LinkedIn share link."""
    if text:
        encoded_text = urllib.parse.quote(text[:3000])
        return f"https://www.linkedin.com/feed/?text={encoded_text}"
    return "https://www.linkedin.com/feed/"

def extract_section(text, section_name):
    """Extract a specific section from generated content."""
    pattern = rf"###\s*{section_name}\s*\n(.*?)(?=###\s*[A-Z]|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def save_to_history(entry_type, content, metadata=None):
    """Save generated content to history."""
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    entry = {
        'id': len(st.session_state['history']) + 1,
        'type': entry_type,
        'content': content,
        'metadata': metadata or {},
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state['history'].insert(0, entry)
    
    # Keep only last 50 entries
    if len(st.session_state['history']) > 50:
        st.session_state['history'] = st.session_state['history'][:50]

def export_history():
    """Export history as JSON."""
    if 'history' not in st.session_state or not st.session_state['history']:
        return None
    
    json_data = json.dumps(st.session_state['history'], indent=2)
    return json_data

# --- 4. INITIALIZE SESSION STATE ---
if 'generated_post' not in st.session_state:
    st.session_state['generated_post'] = None
if 'generated_hooks' not in st.session_state:
    st.session_state['generated_hooks'] = None
if 'generated_audit' not in st.session_state:
    st.session_state['generated_audit'] = None
if 'generated_hashtags' not in st.session_state:
    st.session_state['generated_hashtags'] = None
if 'brand_voice' not in st.session_state:
    st.session_state['brand_voice'] = "Default"
if 'custom_voice' not in st.session_state:
    st.session_state['custom_voice'] = ""

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Brand Voice")
    voice_options = [
        "Default",
        "Professional & Formal",
        "Casual & Conversational",
        "Humorous & Witty",
        "Inspirational & Motivational",
        "Technical & Analytical",
        "Custom"
    ]
    selected_voice = st.selectbox("Choose your brand voice", voice_options, index=voice_options.index(st.session_state['brand_voice']))
    st.session_state['brand_voice'] = selected_voice
    
    if selected_voice == "Custom":
        custom_voice = st.text_area("Describe your brand voice", placeholder="e.g., Friendly but authoritative, like a mentor who uses analogies...", value=st.session_state['custom_voice'])
        st.session_state['custom_voice'] = custom_voice
    
    st.divider()
    
    st.subheader("📜 Content History")
    if 'history' in st.session_state and st.session_state['history']:
        st.write(f"Total entries: {len(st.session_state['history'])}")
        
        # Filter by type
        filter_type = st.selectbox("Filter by", ["All", "Post", "Hook", "Audit", "Hashtag"])
        
        for entry in st.session_state['history']:
            if filter_type == "All" or entry['type'] == filter_type:
                with st.expander(f"{entry['type']} - {entry['timestamp'][:10]}"):
                    st.write(entry['content'][:200] + "...")
                    if st.button(f"Load #{entry['id']}", key=f"load_{entry['id']}"):
                        if entry['type'] == 'Post':
                            st.session_state['generated_post'] = entry['content']
                        elif entry['type'] == 'Hook':
                            st.session_state['generated_hooks'] = entry['content']
                        elif entry['type'] == 'Audit':
                            st.session_state['generated_audit'] = entry['content']
                        elif entry['type'] == 'Hashtag':
                            st.session_state['generated_hashtags'] = entry['content']
                        st.rerun()
        
        if st.button("Clear History"):
            st.session_state['history'] = []
            st.rerun()
        
        if st.button("Export History as JSON"):
            json_data = export_history()
            if json_data:
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"growth_engine_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    else:
        st.info("No history yet. Generate some content!")
    
    st.divider()
    st.caption("Built with ❤️ by Shweta Mishra")

# --- 6. MAIN INTERFACE ---

st.title("🚀 Personal Branding AI Architect")
st.markdown("Build your audience on **LinkedIn** & **Twitter** without the spam.")

# Build voice instruction
voice_instructions = {
    "Default": "",
    "Professional & Formal": "Use a professional, formal tone suitable for corporate audiences.",
    "Casual & Conversational": "Use a casual, friendly, conversational tone like talking to a friend.",
    "Humorous & Witty": "Use humor, wit, and clever wordplay to engage readers.",
    "Inspirational & Motivational": "Use an inspiring, motivational tone that uplifts and encourages.",
    "Technical & Analytical": "Use a technical, data-driven tone with precise language.",
    "Custom": st.session_state.get('custom_voice', '')
}
voice_instruction = voice_instructions.get(selected_voice, "")

# Create Tabs for different workflows
tab1, tab2, tab3, tab4 = st.tabs(["✍️ Viral Post Generator", "🎣 Hook Smith", "🔍 Profile Auditor", "🏷️ Hashtag Generator"])

# === TAB 1: VIRAL POST GENERATOR ===
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        topic = st.text_area("What do you want to post about?", height=150, placeholder="e.g., I learned Python in 30 days...", key="post_topic")
        tone = st.selectbox("Select Tone", [
            "Storytelling (Hero's Journey)",
            "Contrarian (Hot Take)",
            "Educational (How-to)",
            "Professional Update",
            "Personal Reflection",
            "Listicle/Tips"
        ], key="post_tone")
        
        include_hashtags = st.checkbox("Include relevant hashtags", value=True)
        
        if st.button("Generate Posts", type="primary", key="gen_posts"):
            if topic and topic.strip():
                hashtag_req = "Include 3-5 relevant hashtags at the end." if include_hashtags else "Do not include hashtags."
                
                system_prompt = f"""
                You are a top-tier ghostwriter for Silicon Valley founders.
                Role: Take the user's raw idea and write two distinct posts.
                
                Input Idea: {topic}
                Selected Tone: {tone}
                {voice_instruction}

                Requirements:
                1. LINKEDIN POST: Use short paragraphs. Focus on value. No emojis in the first line. Maximum 3000 characters.
                2. TWITTER THREAD: Write a hook + 3 body tweets + conclusion. Each tweet must be under 280 characters. Label each tweet clearly.
                
                {hashtag_req}
                
                Output format:
                ### LINKEDIN
                [Content]
                ### TWITTER
                [Content]
                """
                
                generated_text = generate_content(system_prompt)
                if generated_text:
                    st.session_state['generated_post'] = generated_text
                    save_to_history('Post', generated_text, {'topic': topic, 'tone': tone})
                    st.success("✅ Posts generated successfully!")
                else:
                    st.error("Failed to generate posts. Please try again.")
            else:
                st.warning("Please enter a topic first.")

    with col2:
        st.subheader("Output")
        if st.session_state['generated_post']:
            linkedin_content = extract_section(st.session_state['generated_post'], 'LINKEDIN')
            twitter_content = extract_section(st.session_state['generated_post'], 'TWITTER')
            
            # LinkedIn section
            st.markdown("#### LinkedIn Post")
            linkedin_div_id = "linkedin_content"
            st.markdown(f'<div id="{linkedin_div_id}">{linkedin_content}</div>', unsafe_allow_html=True)
            
            col_li1, col_li2 = st.columns(2)
            with col_li1:
                twitter_url = create_linkedin_link(linkedin_content)
                st.markdown(f"[🔗 Open LinkedIn Composer]({twitter_url})", unsafe_allow_html=True)
            with col_li2:
                st.code(linkedin_content, language="markdown")
                if st.button("📋 Copy LinkedIn Post", key="copy_li"):
                    st.session_state['copy_buffer'] = linkedin_content
                    st.success("Copied! (Use Ctrl+V to paste)")
            
            st.divider()
            
            # Twitter section
            st.markdown("#### Twitter Thread")
            twitter_div_id = "twitter_content"
            st.markdown(f'<div id="{twitter_div_id}">{twitter_content}</div>', unsafe_allow_html=True)
            
            col_tw1, col_tw2 = st.columns(2)
            with col_tw1:
                twitter_url = create_twitter_link(twitter_content[:280])
                st.markdown(f"[🔗 Post to X/Twitter]({twitter_url})", unsafe_allow_html=True)
            with col_tw2:
                st.code(twitter_content, language="markdown")
                if st.button("📋 Copy Twitter Thread", key="copy_tw"):
                    st.session_state['copy_buffer'] = twitter_content
                    st.success("Copied! (Use Ctrl+V to paste)")
            
        else:
            st.info("Generated posts will appear here. Enter a topic and click 'Generate Posts'.")

# === TAB 2: HOOK SMITH ===
with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        st.markdown("### The Hook is 80% of the Post")
        boring_hook = st.text_input("Enter your current (boring) opening line:", placeholder="I wrote a new app today.", key="hook_input")
        
        num_hooks = st.slider("Number of hooks to generate", 3, 10, 5)
        
        if st.button("Rewrite Hooks", type="primary", key="gen_hooks"):
            if boring_hook and boring_hook.strip():
                hook_prompt = f"""
                Act as a viral marketing expert. Rewrite the following sentence into {num_hooks} different 'Hook' styles.
                Input: "{boring_hook}"
                {voice_instruction}
                
                Provide diverse styles including:
                - The Negative Bias ("Why X is a mistake")
                - The 'How-To' Promise ("How to X in Y steps")
                - The Insider Secret ("What nobody tells you about X")
                - The Data/Number ("I saved $50k by...")
                - The Direct Question ("Are you still doing X?")
                - The Story Opener ("Last year, I...")
                - The Bold Claim ("Most people are wrong about X")
                
                Number each hook and give it a style name.
                """
                hooks = generate_content(hook_prompt)
                if hooks:
                    st.session_state['generated_hooks'] = hooks
                    save_to_history('Hook', hooks, {'original': boring_hook})
                    st.success("✅ Hooks generated!")
                else:
                    st.error("Failed to generate hooks.")
            else:
                st.warning("Please enter an opening line first.")

    with col2:
        st.subheader("Output")
        if st.session_state['generated_hooks']:
            hooks_div_id = "hooks_content"
            st.markdown(f'<div id="{hooks_div_id}">{st.session_state["generated_hooks"]}</div>', unsafe_allow_html=True)
            
            st.divider()
            st.code(st.session_state['generated_hooks'], language="markdown")
            
            if st.button("📋 Copy All Hooks", key="copy_hooks"):
                st.session_state['copy_buffer'] = st.session_state['generated_hooks']
                st.success("Copied!")
        else:
            st.info("Generated hooks will appear here.")

# === TAB 3: PROFILE AUDITOR ===
with tab3:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        st.markdown("### Roast My Bio")
        current_bio = st.text_area("Paste your current LinkedIn/Twitter Bio:", height=100, key="audit_bio")
        target_audience = st.text_input("Who is your target audience?", placeholder="e.g. Recruiters, Founders, Developers", key="audit_audience")
        platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Both"], key="audit_platform")
        
        if st.button("Audit Profile", type="primary", key="gen_audit"):
            if current_bio and current_bio.strip():
                audit_prompt = f"""
                Act as a Senior Personal Brand Consultant. Analyze this bio.
                
                Bio: "{current_bio}"
                Target Audience: "{target_audience}"
                Platform: {platform}
                {voice_instruction}
                
                Provide:
                1. Score out of 10 (with brief justification)
                2. List 3 specific weaknesses (e.g., "Too vague", "Buzzwords", "Missing CTA")
                3. List 3 specific strengths
                4. Write 2 improved versions:
                   - Professional version
                   - Conversational version
                5. Suggest 1-2 keywords to add for SEO
                """
                audit = generate_content(audit_prompt)
                if audit:
                    st.session_state['generated_audit'] = audit
                    save_to_history('Audit', audit, {'bio': current_bio[:50], 'audience': target_audience})
                    st.success("✅ Profile audited!")
                else:
                    st.error("Failed to audit profile.")
            else:
                st.warning("Please paste your bio first.")

    with col2:
        st.subheader("Output")
        if st.session_state['generated_audit']:
            audit_div_id = "audit_content"
            st.markdown(f'<div id="{audit_div_id}">{st.session_state["generated_audit"]}</div>', unsafe_allow_html=True)
            
            st.divider()
            st.code(st.session_state['generated_audit'], language="markdown")
            
            if st.button("📋 Copy Audit Results", key="copy_audit"):
                st.session_state['copy_buffer'] = st.session_state['generated_audit']
                st.success("Copied!")
        else:
            st.info("Audit results will appear here.")

# === TAB 4: HASHTAG GENERATOR ===
with tab4:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        st.markdown("### 🏷️ AI Hashtag Generator")
        hashtag_topic = st.text_area("What is your post about?", height=100, placeholder="e.g., Artificial intelligence in healthcare, remote work productivity...", key="hashtag_topic")
        platform_ht = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "All Platforms"], key="hashtag_platform")
        num_hashtags = st.slider("Number of hashtags", 5, 30, 15)
        
        if st.button("Generate Hashtags", type="primary", key="gen_hashtags"):
            if hashtag_topic and hashtag_topic.strip():
                hashtag_prompt = f"""
                Act as a social media SEO expert. Generate {num_hashtags} highly relevant hashtags for the following topic.
                
                Topic: {hashtag_topic}
                Platform: {platform_ht}
                
                Requirements:
                1. Mix of popular (1M+ posts) and niche (10K-500K posts) hashtags
                2. Platform-appropriate (LinkedIn uses fewer, more professional tags; Twitter uses 2-3; Instagram uses more)
                3. Include some trending hashtags if relevant
                4. Group them by:
                   - High competition (broad reach)
                   - Medium competition (balanced)
                   - Low competition (targeted)
                
                Format as a simple list with brief explanations.
                """
                hashtags = generate_content(hashtag_prompt)
                if hashtags:
                    st.session_state['generated_hashtags'] = hashtags
                    save_to_history('Hashtag', hashtags, {'topic': hashtag_topic, 'platform': platform_ht})
                    st.success("✅ Hashtags generated!")
                else:
                    st.error("Failed to generate hashtags.")
            else:
                st.warning("Please enter a topic first.")

    with col2:
        st.subheader("Output")
        if st.session_state['generated_hashtags']:
            hashtags_div_id = "hashtags_content"
            st.markdown(f'<div id="{hashtags_div_id}">{st.session_state["generated_hashtags"]}</div>', unsafe_allow_html=True)
            
            st.divider()
            st.code(st.session_state['generated_hashtags'], language="markdown")
            
            if st.button("📋 Copy Hashtags", key="copy_hashtags"):
                st.session_state['copy_buffer'] = st.session_state['generated_hashtags']
                st.success("Copied!")
        else:
            st.info("Generated hashtags will appear here.")
