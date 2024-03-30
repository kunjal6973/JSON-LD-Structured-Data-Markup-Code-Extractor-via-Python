import requests
from bs4 import BeautifulSoup
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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
st.markdown("""
This app allows you to extract the JSON LD Structured Data Markup Code from a URL and visualize schema properties as a hub-and-spoke diagram.

Created by [John Smith](#)""")

# Input URL from the user
url_input = st.text_input("Enter the URL:", "https://www.example.com")

# Button to trigger extraction and visualization
if st.button("Extract Structured Data"):
    extracted_data = extract_structured_data(url_input)
    st.text_area("Extracted Code:", value=extracted_data, height=400, max_chars=None, key=None)

    # Visualization of schema properties as hub-and-spoke
    if extracted_data != "No structured data markup found on the page.":
        graph = nx.Graph()
        schema_lines = extracted_data.split("\n")
        for line in schema_lines:
            if line.startswith('{"@context"'):
                continue  # Skip @context line
            try:
                json_data = json.loads(line)
                if "@type" in json_data:
                    graph.add_node(json_data["@type"])
                    if "properties" in json_data:
                        for prop, val in json_data["properties"].items():
                            graph.add_edge(json_data["@type"], prop)
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines

        plt.figure(figsize=(10, 6))
        nx.draw(graph, with_labels=True, node_color='lightblue', font_weight='bold')
        plt.title("Schema Properties Visualization (Hub & Spoke)")
        st.pyplot()
