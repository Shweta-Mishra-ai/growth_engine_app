# 🚀 Growth Engine AI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20AI-Gemini%202.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered "Content Velocity Engine" designed to accelerate organic growth on LinkedIn, X (Twitter), and Instagram without using spam bots.**

---

## 📖 Overview

**Growth Engine AI** is a Human-in-the-Loop (HITL) application that leverages the **Google Gemini 2.0 Flash LLM** to eliminate writer's block and optimize content for social media algorithms. 

Unlike automation tools that risk account bans, this app focuses on **content creation and strategy**. It uses "Intent-based" posting, allowing you to generate high-quality drafts and post them directly to social platforms with a single click, keeping your account 100% safe.

### 🌟 Key Features

* **✍️ Viral Post Generator:**
    * Takes raw ideas/notes and transforms them into two formats simultaneously:
        * **LinkedIn:** Professional, story-driven, formatted for readability.
        * **Twitter/X:** Thread-style format (Hook + Value + Conclusion) under 280 chars.
    * Direct "Post to" links for each platform.
    * One-click copy to clipboard.

* **🎣 Hook Smith (A/B Tester):**
    * Analyzes your opening line and rewrites it using viral psychological frameworks.
    * Customizable number of hooks (3-10).
    * *Goal:* Increase "Stop Scroll" rate.

* **🔍 Profile Auditor:**
    * Acts as a Senior Personal Brand Consultant.
    * Grades your bio (0-10), identifies weaknesses/strengths, and suggests SEO-optimized improvements.
    * Platform-specific optimization (LinkedIn, Twitter/X, or Both).

* **🏷️ Hashtag Generator (NEW):**
    * AI-powered hashtag suggestions based on your topic.
    * Platform-optimized (LinkedIn, Twitter/X, Instagram).
    * Categorized by competition level (High/Medium/Low).
    * Mix of trending and niche hashtags.

### 🆕 NEW Features (v2.0)

* **Brand Voice Customization** - Choose from 7 preset voices or create your own custom brand voice
* **Content History** - Automatically saves all generated content with search and filter
* **Export History** - Download your content history as JSON for backup
* **Copy to Clipboard** - One-click copy for all generated content
* **Platform-Specific Links** - Working "Post to" links for LinkedIn and Twitter/X
* **Session State Management** - No more data leaking between tabs
* **Improved Error Handling** - Graceful API error recovery and input validation
* **Configurable Temperature** - Fine-tune AI creativity

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Rapid UI Development)
* **LLM Engine:** [Google Gemini API](https://ai.google.dev/) (Model: `gemini-2.0-flash`)
* **Authentication:** Streamlit Secrets Management (Secure API Key handling)
* **Posting Mechanism:** Web Intent URLs (No paid platform APIs required)

---

## 📂 Repository Structure

```text
growth_engine_app/
├── app.py                  # Main application logic and UI
├── requirements.txt        # Python dependencies
├── .gitignore              # Security rules (prevents uploading keys)
├── README.md               # Project documentation
└── .streamlit/             # Configuration folder
   ├── secrets.toml        # (Local) Stores your API Key (DO NOT COMMIT)
   └── secrets.toml.example # Template for API key setup

```

## 🚀 Installation & Local Setup

Follow these steps to run the app on your own machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Shweta-Mishra-ai/growth_engine_app.git
cd growth_engine_app
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

You need a free API key from Google.

1. Get your key here: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a folder named `.streamlit` in the root directory.
3. Create a file named `secrets.toml` inside that folder.
4. Add the following line:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "AIzaSy...[PASTE YOUR KEY HERE]"
```

Or use the provided template:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Then edit `secrets.toml` with your actual API key.

### 5. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Cloud)

Deploying this app for public use is free and takes less than 2 minutes.

1. **Push to GitHub:** Ensure your code (excluding `.streamlit/secrets.toml`) is on GitHub.
2. **Streamlit Cloud:** Log in to [share.streamlit.io](https://share.streamlit.io).
3. **New App:** Click "New App" and select your repository.
4. **Add Secrets (Crucial):**
   - Before clicking "Deploy", click on **Advanced Settings**.
   - Go to the **Secrets** field.
   - Paste your API key in the TOML format:
   ```toml
   GOOGLE_API_KEY = "AIzaSy...[PASTE YOUR KEY HERE]"
   ```
5. **Deploy:** Click the **Deploy** button.

---

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'google'` | Run `pip install -r requirements.txt` again. Ensure you are in the correct virtual environment. |
| `API Key not found` | Check that your `.streamlit/secrets.toml` file exists and is spelled correctly. If on Cloud, check the "Secrets" settings in the dashboard. |
| `Quota Exceeded` | The Gemini Free tier has limits (~60 requests/minute). Wait a minute and try again. |
| `Content not appearing` | Check browser console for errors. Try refreshing the page. |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See LICENSE for more information.

---

Built with ❤️ by Shweta Mishra
