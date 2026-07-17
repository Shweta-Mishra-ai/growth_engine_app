def build_graphic_prompt(content: str, platform: str, style: str = "Modern Illustration") -> str:
    return f"""You are a professional social media graphic designer and art director.
Analyze the following post content and create a highly detailed, professional image generation prompt.

POST CONTENT:
{content}

PLATFORM:
{platform}

ART STYLE SPECIFIED:
{style}

Create a single text-to-image prompt that will generate a stunning, visually engaging graphic representing this post's topic.
The prompt must describe:
1. Subject & Composition (what is in the scene, camera angle, layout)
2. Colors & Mood (vibrant, dark editorial, high contrast, warm/cool palette)
3. Specific style details (e.g., if "Modern Illustration": clean vectors, minimalist flat design, isometric perspective, tech corporate style; if "Photorealistic": sharp focus, cinematic lighting, shot on 85mm lens, realistic textures; if "Professional 3D Render": smooth clay renders, soft shadows, vibrant lighting)
4. NO text in the image (specify: "clean background, textless, no typos, no letters, no words")

Output ONLY the final image generation prompt. Zero introduction, zero explanation, just the prompt itself. Make it extremely specific and descriptive."""
