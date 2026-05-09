import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Research PDF Downloader", page_icon="📚", layout="wide")

# Custom CSS to match your clean NICU style
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📂 Research Reference Retriever")
st.write("Paste your DOIs or Paper URLs below to fetch the PDFs.")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    scihub_mirror = st.text_input("Sci-Hub Mirror", value="https://sci-hub.se")
    st.info("If the mirror stops working, update it here.")

# Input Area
references = st.text_area("Enter References (one per line):", height=200, placeholder="e.g. 10.1038/nature14539")

if st.button("Start Batch Processing"):
    if not references:
        st.warning("Please enter at least one reference.")
    else:
        ref_list = [r.strip() for r in references.split('\n') if r.strip()]
        
        for ref in ref_list:
            cols = st.columns([3, 1])
            with cols[0]:
                st.write(f"🔍 Searching for: `{ref}`")
            
            try:
                # Scraper Logic
                url = f"{scihub_mirror}/{ref}"
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Find the PDF link in the Sci-Hub iframe or embed
                pdf_element = soup.find("iframe") or soup.find("embed")
                
                if pdf_element:
                    pdf_url = pdf_element.get("src")
                    if not pdf_url.startswith("http"):
                        pdf_url = "https:" + pdf_url if pdf_url.startswith("//") else f"{scihub_mirror}{pdf_url}"
                    
                    with cols[1]:
                        st.link_button("Download PDF", pdf_url)
                    st.success(f"Found match for {ref}")
                else:
                    with cols[1]:
                        st.error("Not Found")
            
            except Exception as e:
                st.error(f"Error: {e}")
            
            time.sleep(1) # Small delay to prevent IP blocks
