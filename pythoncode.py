import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to extract structured data from URL
def extract_structured_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')
        structured_data = soup.find_all('script', type='application/ld+json')

        if structured_data:
            extracted_data = ""
            for data in structured_data:
                if "schema.org" in data.text:
                    schema = data.text.strip()
                    if schema.startswith('{"@context"'):
                        schema = '<script type="application/ld+json">' + schema + '</script>'
                    extracted_data += schema + "\n\n"
            return extracted_data if extracted_data else "No structured data markup found on the page."
        else:
            return "No structured data markup found on the page."
    else:
        return "Failed to retrieve the webpage."

# Streamlit app title and description
st.title("JSON LD Structured Data Markup Code Extractor")
st.markdown("<p style='font-style: italic;'>This app allows you to extract JSON LD Structured Data Markup Code from URL. Created by <a href='https://www.linkedin.com/in/kunjal-chawhan/' target='_blank'>Kunjal Chawhan</a>. <a href='https://www.decodedigitalmarket.com' target='_blank'>More Apps & Scripts on my Website</a>.</p>", unsafe_allow_html=True)
# Input URL from the user
url_input = st.text_input("Enter the URL:", "https://www.example.com")

# Button to trigger extraction
if st.button("Extract Structured Data"):
    extracted_data = extract_structured_data(url_input)
    st.text_area("Extracted Code:", value=extracted_data, height=400, max_chars=None, key=None)
