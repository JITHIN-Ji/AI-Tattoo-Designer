import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import webcolors

# --- Streamlit Page Config (MUST BE FIRST) ---
st.set_page_config(
    page_title="Custom AI Tattoo Designer", 
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Dark Theme CSS with Tattoo Elements
def inject_custom_css():
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Cinzel:wght@400;500;600&display=swap');
    
    /* Global styles - Professional Pure Black */
    .stApp {
        background: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
        min-height: 100vh;
        position: relative;
    }
    
    /* Subtle professional pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.02) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.02) 0%, transparent 50%),
            linear-gradient(45deg, transparent 49%, rgba(255, 255, 255, 0.005) 50%, transparent 51%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Main container - Professional black design */
    .main .block-container {
        background: rgba(10, 10, 10, 0.98);
        border-radius: 16px;
        padding: 3rem;
        margin-top: 1rem;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.8),
            0 0 100px rgba(255, 255, 255, 0.03),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
    }
    
    /* Header styling - Professional metallic */
    h1 {
        font-family: 'Orbitron', monospace !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #ffffff, #d1d5db, #9ca3af, #6b7280) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.1) !important;
        letter-spacing: 3px !important;
        position: relative !important;
    }
    
    /* Professional decorative elements */
    h1::before, h1::after {
        content: '▪';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        color: #ffffff;
        opacity: 0.8;
        animation: fadeInOut 3s ease-in-out infinite;
    }
    
    h1::before {
        left: -80px;
    }
    
    h1::after {
        right: -80px;
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    
    /* Subheaders - Professional clean */
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        color: #ffffff !important;
        margin: 2rem 0 1.5rem 0 !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.15) !important;
        padding-bottom: 0.8rem !important;
        text-shadow: none !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        color: #e5e7eb !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Info box styling - Dark theme */
    .stAlert > div {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(79, 70, 229, 0.1)) !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border-left: 4px solid #7c3aed !important;
        color: #c7d2fe !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.1) !important;
    }
    
    /* Form styling - Professional black */
    .stForm {
        background: rgba(0, 0, 0, 0.7) !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* Input styling - Clean black theme */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stTextArea > div > div {
        background: rgba(0, 0, 0, 0.6) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1) !important;
        background: rgba(0, 0, 0, 0.8) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Input text color */
    .stSelectbox input,
    .stTextInput input,
    .stTextArea textarea {
        color: #ffffff !important;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #374151, #4b5563, #6b7280) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 0.8rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4b5563, #6b7280, #9ca3af) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Form submit button - Professional accent */
    .stForm .stButton > button {
        background: linear-gradient(135deg, #1f2937, #374151, #4b5563) !important;
        color: #f0f0f0 !important; /* 👈 This ensures text is visible */
        font-size: 1.1rem !important;
        padding: 1rem 2.5rem !important;
        width: 100% !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    
    .stForm .stButton > button:hover {
        background: linear-gradient(135deg, #374151, #4b5563, #6b7280) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Color picker styling */
    .stColorPicker > div {
        background: rgba(30, 30, 40, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 30, 40, 0.6) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(20, 20, 30, 0.8) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-top: none !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Success/Error message styling */
    .stSuccess > div {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        border-left: 4px solid #22c55e !important;
        color: #86efac !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError > div {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        border-left: 4px solid #ef4444 !important;
        color: #fca5a5 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning > div {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        border-left: 4px solid #f59e0b !important;
        color: #fde68a !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Code block styling */
    .stCode {
        background: rgba(15, 15, 23, 0.9) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
        font-family: 'Inter', monospace !important;
        color: #e2e8f0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #7c3aed !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10b981, #34d399) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 
            0 4px 15px rgba(5, 150, 105, 0.3),
            0 0 20px rgba(5, 150, 105, 0.1) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #10b981, #059669, #047857) !important;
        transform: translateY(-2px) !important;
        box-shadow: 
            0 8px 25px rgba(5, 150, 105, 0.4),
            0 0 30px rgba(5, 150, 105, 0.2) !important;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #7c3aed, transparent) !important;
        margin: 3rem 0 !important;
    }
    
    /* Image styling */
    .stImage > img {
        border-radius: 16px !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 0 60px rgba(124, 58, 237, 0.2) !important;
        border: 2px solid rgba(124, 58, 237, 0.3) !important;
    }
    
    /* Labels - Clean professional */
    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    .stColorPicker label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: none !important;
    }
    
    /* Section headers - Professional clean */
    .section-header {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #ffffff !important;
        margin-bottom: 1.5rem !important;
        padding: 0.8rem 0 !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
        text-shadow: none !important;
    }
    
    /* Tattoo-inspired decorative elements */
    .tattoo-border {
        border: 2px solid;
        border-image: linear-gradient(45deg, #f59e0b, #7c3aed, #f59e0b) 1;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 30, 40, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7c3aed, #f59e0b);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f59e0b, #7c3aed);
    }
    </style>
    """, unsafe_allow_html=True)

# Convert HEX to name
def hex_to_color_name(hex_code):
    try:
        return webcolors.hex_to_name(hex_code)
    except:
        return "custom color"

def generate_image_from_prompt(prompt):
    try:
        # Use Streamlit secrets for API key (SECURE)
        client = genai.Client(api_key=st.secrets["google"]["api_key"])
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        image_path = None
        message_text = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                message_text = part.text
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image_path = "gemini_generated_image.png"
                image.save(image_path)
                return image_path, message_text
        
        return None, message_text or "No image data returned."
        
    except Exception as e:
        return None, f"Error: {e}"

# Enhanced tattoo-specific prompt generator
def create_tattoo_prompt(style, theme, color_name, placement, vibe):
    return f"""Create a professional {style.lower()} tattoo design of a {theme} in {color_name} ink. 
    This tattoo is designed for placement on the {placement.lower()} with a {vibe} aesthetic.
    
    Style specifications:
    - Clean, professional linework suitable for actual tattooing
    - {style} artistic style with appropriate line weights
    - High contrast and clear details
    - Proper tattoo composition and flow
    
    Please generate a high-quality tattoo design that a professional tattoo artist could use as reference."""

# Apply custom CSS
inject_custom_css()

st.markdown("""
<div style="text-align: center; margin-bottom: 3rem; position: relative;">
    <h1>CUSTOM AI TATTOO DESIGNER</h1>
    <div style="
        font-family: 'Inter', sans-serif; 
        font-size: 1.1rem; 
        color: #9ca3af; 
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 1px;
    ">
        Professional AI-Powered Tattoo Art Generation
    </div>
</div>
""", unsafe_allow_html=True)

st.info('🎨 "Transform your vision into ink-worthy art with cutting-edge AI technology"')

# Main form section
st.markdown("## Design Your Perfect Tattoo")

# Tattoo customization form
with st.form("tattoo_form"):
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="section-header">Style & Theme</div>', unsafe_allow_html=True)
        style = st.selectbox(
            "Tattoo Style", 
            ["Minimalist", "Traditional", "Neo-Traditional", "Geometric", "Realistic", "Watercolor", "Blackwork", "Fine Line"],
            help="Choose the artistic style for your tattoo"
        )
        theme = st.text_input(
            "Theme/Subject", 
            placeholder="e.g., dragon, rose, geometric pattern, phoenix",
            help="Describe what you want your tattoo to depict"
        )
        color = st.color_picker(
            "Primary Ink Color", 
            "#8FDF7B",
            help="Select the main color for your tattoo"
        )
    
    with col2:
        st.markdown('<div class="section-header">Placement & Details</div>', unsafe_allow_html=True)
        placement = st.selectbox(
            "Body Placement", 
            ["Forearm", "Upper Arm", "Shoulder", "Back", "Chest", "Neck", "Wrist", "Thigh", "Calf"],
            help="Where will this tattoo be placed on your body?"
        )
        vibe = st.selectbox(
            "Overall Vibe", 
            ["Bold", "Elegant", "Fierce", "Delicate", "Modern", "Classic", "Edgy", "Soft"],
            help="What feeling should your tattoo convey?"
        )
        size = st.selectbox(
            "Size", 
            ["Small (2-3 inches)", "Medium (4-6 inches)", "Large (7+ inches)"],
            help="Approximate size of the finished tattoo"
        )
    
    # Advanced options
    with st.expander("🎛 Advanced Customization Options"):
        col3, col4 = st.columns(2)
        with col3:
            custom_prompt = st.text_area(
                "Custom additions to prompt (optional)",
                placeholder="e.g., 'include flowing ribbons', 'add subtle shading', 'incorporate dotwork elements'",
                help="Add specific details or modifications to your design"
            )
        with col4:
            background_style = st.selectbox(
                "Background Style",
                ["Clean white background", "Show on skin", "Transparent background", "Minimal decorative elements"],
                help="How should the background be rendered?"
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Generate My Tattoo Design")

# Quick mode section
st.markdown("---")
st.markdown("## Quick Design Mode")
st.markdown("For experienced users who know exactly what they want")

col_quick1, col_quick2 = st.columns([3, 1])
with col_quick1:
    quick_prompt = st.text_input(
        "Direct prompt:", 
        placeholder="e.g., minimalist wolf tattoo for forearm, black ink, geometric style",
        label_visibility="collapsed"
    )
with col_quick2:
    quick_generate = st.button("Generate Now", use_container_width=True)

# Handle form submission
if submitted and theme:
    color_name = hex_to_color_name(color)
    
    # Create comprehensive tattoo prompt
    tattoo_prompt = create_tattoo_prompt(style, theme, color_name, placement, vibe.lower())
    
    # Add custom elements
    if custom_prompt:
        tattoo_prompt += f"\n\nAdditional requirements: {custom_prompt}"
    
    if background_style != "Clean white background":
        tattoo_prompt += f"\n\nBackground: {background_style}"
    
    st.markdown("## 📝 Generated Design Brief")
    with st.expander("View Complete Prompt", expanded=False):
        st.code(tattoo_prompt, language="text")
    
    with st.spinner("🎨 Our AI artist is creating your custom tattoo design..."):
        image_file, extra_text = generate_image_from_prompt(tattoo_prompt)
    
    if image_file:
        st.success("✅ Your professional tattoo design is ready!")
        
        # Display the generated image
        col_img1, col_img2, col_img3 = st.columns([1, 3, 1])
        with col_img2:
            st.image(image_file, caption=f"{style} {theme} tattoo design", use_container_width=True)
        
        if extra_text:
            st.markdown("## 🤖 AI Designer Notes")
            st.markdown(f"{extra_text}")
        
        # Download section
        st.markdown("## 📥 Download Your Design")
        with open(image_file, "rb") as file:
            st.download_button(
                label="💾 Download High-Quality Design",
                data=file.read(),
                file_name=f"tattoo_{theme.replace(' ', '')}{style.lower()}.png",
                mime="image/png",
                use_container_width=True
            )
    else:
        st.error(f"❌ Design generation failed")
        if extra_text:
            st.write(extra_text)

# Handle quick prompt
elif quick_generate and quick_prompt:
    enhanced_prompt = f"Professional tattoo design: {quick_prompt}. High quality, clean linework, suitable for actual tattooing."
    
    with st.spinner("🎨 Creating design from your prompt..."):
        image_file, extra_text = generate_image_from_prompt(enhanced_prompt)
    
    if image_file:
        st.success("✅ Quick design generated successfully!")
        
        col_quick_img1, col_quick_img2, col_quick_img3 = st.columns([1, 3, 1])
        with col_quick_img2:
            st.image(image_file, use_container_width=True)
        
        if extra_text:
            st.markdown(f"*AI Notes:* {extra_text}")
            
        # Quick download
        with open(image_file, "rb") as file:
            st.download_button(
                label="💾 Download Design",
                data=file.read(),
                file_name="quick_tattoo_design.png",
                mime="image/png"
            )
    else:
        st.error(f"❌ Generation failed: {extra_text}")

elif submitted and not theme:
    st.warning("⚠ Please enter a theme/subject for your tattoo design!")

# Setup instructions section
st.markdown("---")
with st.expander("🔧 Setup Instructions", expanded=False):
    st.markdown("""
    *To use this professional tattoo generator:*
    
    1. 🔑 Get your Google AI API key from [Google AI Studio](https://aistudio.google.com/)
    2. 📁 Create a .streamlit/secrets.toml file in your project directory
    3. 🔐 Add your API key securely:
    toml
    [google]
    api_key = "your-google-ai-api-key-here"
    
    
    *⚠ Security Notice:* Your API key is stored securely in Streamlit secrets and never exposed in the code.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #9ca3af;">
    <div style="font-family: 'Inter', serif; font-size: 1rem; margin-bottom: 1rem; color: #ffffff; font-weight: 600;">
        Professional AI Tattoo Artistry
    </div>
    <p><strong>Pro Tip:</strong> Be specific about style, placement, and aesthetic preferences for the best results.</p>
    <p>This AI-powered tool creates professional reference designs that tattoo artists can use and adapt.</p>
    <div style="margin-top: 1.5rem; font-style: italic; color: #6b7280;">
        "Every masterpiece begins with a vision"
    </div>
</div>
""", unsafe_allow_html=True)
