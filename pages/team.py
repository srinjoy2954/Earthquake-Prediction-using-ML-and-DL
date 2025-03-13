import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# ---- Streamlit Config ----
st.set_page_config(page_title="Our Team", layout="wide")

# ---- Default Placeholder Image ----
DEFAULT_IMAGE = "assets/default_image.png"  # Fallback image if profile image not found

# ---- Team Members Data ----
team_members = [
    {"name": "Brishti Ghosh", "role": "Team Lead", "image": "assets/Brishti Ghosh.jpg", "linkedin": "https://linkedin.com/in/brishti-ghosh"},
    {"name": "Anindya Dutta", "role": "Data Scientist", "image": "assets/Anindya Dutta.jpg", "linkedin": "https://linkedin.com/in/anindya-dutta"},
    {"name": "Soumojeet Dutta", "role": "ML Engineer", "image": "assets/Soumojeet Dutta.jpg", "linkedin": "https://linkedin.com/in/soumojeet-dutta"},
    {"name": "Srinjoy Roy", "role": "Research Analyst", "image": "assets/Srinjoy Roy.jpg", "linkedin": "https://linkedin.com/in/srinjoy-roy"},
    {"name": "Subham Mukherjee", "role": "Backend Developer", "image": "assets/Subham Mukherjee.jpg", "linkedin": "https://linkedin.com/in/subham-mukherjee"},
]

# ---- Convert Image to Base64 ----
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        with open(DEFAULT_IMAGE, "rb") as f:
            return base64.b64encode(f.read()).decode()

# ---- Page Title ----
st.title("👨‍💻 Meet Our Team")
st.markdown("### Passionate minds behind the AI/ML-based Earthquake Prediction Project.")
st.markdown("---")

# ---- Build the HTML for Horizontal Scrollable Cards ----
html_string = """
<style>
.horizontal-container {
    width: 100%;
    overflow-x: auto;
    white-space: nowrap;
    padding: 20px 0;
}
.card {
    display: inline-block;
    width: 240px;
    margin-right: 20px;
    vertical-align: top;
    background: #f8f9fa;
    padding: 10px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
.card img {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    border: 4px solid #4CAF50;
    margin-bottom: 15px;
    object-fit: cover;
}
.card h4 {
    margin-bottom: 5px;
    color: #333;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
.card p {
    color: #666;
    margin-bottom: 10px;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
}
.card a {
    display: inline-block;
    padding: 8px 16px;
    background-color: #0077b5;
    color: white;
    border-radius: 20px;
    text-decoration: none;
    font-size: 14px;
    font-family: 'Arial', sans-serif;
    transition: background-color 0.3s ease;
}
.card a:hover {
    background-color: #005f8e;
}
</style>
<div class="horizontal-container">
"""

for member in team_members:
    img_data = get_base64_image(member['image'])
    html_string += f"""
    <div class="card">
        <img src="data:image/jpeg;base64,{img_data}" alt="{member['name']}">
        <h4>{member['name']}</h4>
        <p>{member['role']}</p>
        <a href="{member['linkedin']}" target="_blank">🔗 LinkedIn</a>
    </div>
    """

html_string += "</div>"

# ---- Render the HTML using st.components.v1.html() ----
components.html(html_string, height=450)

# ---- Footer ----
st.markdown("---")
st.markdown("""
### 🤝 **Let's Collaborate!**
> We are open to collaborations and discussions. Reach out to us through LinkedIn!
""")
