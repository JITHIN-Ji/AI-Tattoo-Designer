🎨 Custom AI Tattoo Designer
Turn your tattoo vision into stunning visual art using Google Gemini AI and a beautifully styled Streamlit interface. This app allows users to generate tattoo reference designs by selecting styles, themes, placements, colors, and aesthetic preferences.

🔥 Features
🎯 Style Selector – Choose from 8 professional tattoo styles (e.g., Minimalist, Realistic, Watercolor).

💡 Prompt-based Design – Enter themes like dragon, rose, phoenix, etc.

🎨 Color Picker – Customize primary ink color.

🧍 Placement Control – Pick common body areas like Forearm, Back, Wrist.

✨ Advanced Options – Add ribbons, dotwork, shading, or control background style.

⚡ Quick Mode – Input your own prompt and generate instantly.

📥 High-Quality Image Download – Save designs locally in .png format.

💅 Beautiful Custom UI – Full dark-themed professional interface with animation and gradients.


🧰 Technologies Used
Streamlit – UI framework

Google Gemini AI – Image generation (via google.generativeai)

Python Pillow (PIL) – Image processing

WebColors – Convert hex color to color name

Custom CSS for fully responsive and styled interface

⚙️ Setup Instructions
🔑 1. Get Google Gemini API Key
Go to Google AI Studio

Click Get API Key and copy it.

📁 2. Add .streamlit/secrets.toml
In your project root, create:

bash
Copy
Edit
.streamlit/secrets.toml
Paste the following:

toml
Copy
Edit
[google]
api_key = "your-google-ai-api-key"
▶️ 3. Run the App
bash
Copy
Edit
pip install -r requirements.txt
streamlit run app.py
Replace app.py with your actual filename if different.

📦 requirements.txt (example)
txt
Copy
Edit
streamlit
google-generativeai
Pillow
webcolors
📌 Example Prompts
Regular Mode:
Style: Geometric

Theme: Wolf

Color: #000000

Placement: Forearm

Vibe: Fierce

Quick Mode:
"Realistic lion tattoo for chest in black ink with flowing mane and tribal background."

💡 Pro Tips
Use Quick Mode for speed and full control.

The more specific your prompt, the better the result.

This tool is best used as a reference for real tattoo artists.

Color names are automatically extracted from the hex color code for realism.
