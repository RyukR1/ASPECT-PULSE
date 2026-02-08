import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sys
import os

# --- Add project root to sys.path ---
# This is a common way to handle imports in a structured project.
# It allows us to import modules from other directories.
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
# ------------------------------------

# --- Import from our project modules ---
from nlp.preprocessing import get_sentences
from nlp.aspect_extractor import extract_aspect, ASPECT_KEYWORDS
from sentiment.sentiment_model import get_sentiment_pipeline, get_sentiment
# ---------------------------------------

# --- Caching Models ---
# Streamlit's cache decorator prevents reloading the heavy model every time
# the user interacts with the app.
@st.cache(allow_output_mutation=True)
def load_sentiment_model():
    return get_sentiment_pipeline()

# --- Main App Logic ---
def run_analysis(raw_text):
    """
    Runs the full NLP pipeline on a block of raw text.
    """
    sentences = get_sentences(raw_text)
    results = []
    
    sentiment_pipeline = load_sentiment_model()
    if not sentiment_pipeline:
        st.error("Failed to load sentiment model. Please check the logs.")
        return pd.DataFrame()

    for sentence in sentences:
        aspect = extract_aspect(sentence)
        if aspect != 'Unclassified':
            polarity = get_sentiment(sentence, sentiment_pipeline)
            results.append({
                'Sentence': sentence,
                'Aspect': aspect,
                'Polarity': polarity
            })
            
    return pd.DataFrame(results)

# --- Visualization Functions ---
def create_radar_chart(df1, df2, brand1_name, brand2_name):
    """Creates a competitive radar chart."""
    aspects = list(ASPECT_KEYWORDS.keys())
    
    # Calculate average polarity for each aspect
    avg_polarity1 = df1.groupby('Aspect')['Polarity'].mean().reindex(aspects, fill_value=0)
    avg_polarity2 = df2.groupby('Aspect')['Polarity'].mean().reindex(aspects, fill_value=0)
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_polarity1.values,
        theta=avg_polarity1.index,
        fill='toself',
        name=brand1_name
    ))
    fig.add_trace(go.Scatterpolar(
        r=avg_polarity2.values,
        theta=avg_polarity2.index,
        fill='toself',
        name=brand2_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-1, 1]
            )),
        showlegend=True,
        title="Competitive Aspect Comparison"
    )
    return fig

def create_word_cloud(df, aspect):
    """Generates a word cloud for negative sentences of a specific aspect."""
    text = ' '.join(df[(df['Aspect'] == aspect) & (df['Polarity'] < -0.5)]['Sentence'])
    
    if not text:
        return None
        
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🚀 Aspect-Pulse: Competitive Benchmarking Hub")

st.sidebar.header("Controls")
st.sidebar.info(
    "Paste raw text reviews for two different products into the text areas below. "
    "The app will analyze the feedback and generate a competitive comparison."
)

# Two text areas for Brand A and Brand B
col1, col2 = st.columns(2)

with col1:
    st.header("Brand A")
    brand_a_name = st.text_input("Enter Brand A Name (e.g., 'Samsung Galaxy')", "Brand A")
    text_a = st.text_area("Paste reviews for Brand A here:", height=300, key="text_a")

with col2:
    st.header("Brand B")
    brand_b_name = st.text_input("Enter Brand B Name (e.g., 'Apple iPhone')", "Brand B")
    text_b = st.text_area("Paste reviews for Brand B here:", height=300, key="text_b")

if st.sidebar.button("Analyze"):
    if not text_a or not text_b:
        st.sidebar.warning("Please paste reviews for both brands.")
    else:
        with st.spinner("Analyzing... This may take a moment."):
            df_a = run_analysis(text_a)
            df_b = run_analysis(text_b)

        if df_a.empty or df_b.empty:
            st.error("Analysis failed or no aspects were identified. Please try different text.")
        else:
            st.header("Analysis Results")
            
            # --- Radar Chart ---
            st.subheader("📊 Competitive Radar Chart")
            radar_fig = create_radar_chart(df_a, df_b, brand_a_name, brand_b_name)
            st.plotly_chart(radar_fig, use_container_width=True)
            
            st.markdown("---")
            
            # --- Pain-Point Word Clouds ---
            st.subheader("☁️ Pain-Point Word Clouds")
            st.write("These word clouds highlight common terms in strongly negative reviews for each aspect.")
            
            selected_aspect = st.selectbox("Select an aspect to view word clouds:", list(ASPECT_KEYWORDS.keys()))
            
            wc_col1, wc_col2 = st.columns(2)
            with wc_col1:
                st.write(f"**{brand_a_name} - Negative '{selected_aspect}' Cloud**")
                wc_fig_a = create_word_cloud(df_a, selected_aspect)
                if wc_fig_a:
                    st.pyplot(wc_fig_a)
                else:
                    st.info(f"No significant negative feedback found for '{selected_aspect}'.")

            with wc_col2:
                st.write(f"**{brand_b_name} - Negative '{selected_aspect}' Cloud**")
                wc_fig_b = create_word_cloud(df_b, selected_aspect)
                if wc_fig_b:
                    st.pyplot(wc_fig_b)
                else:
                    st.info(f"No significant negative feedback found for '{selected_aspect}'.")
            
            st.markdown("---")

            # --- Live Feed ---
            st.subheader("📜 Raw Data Feed")
            st.write("Here is the processed data used for the visualizations.")
            
            st.write(f"**{brand_a_name} - Processed Data**")
            st.dataframe(df_a)
            
            st.write(f"**{brand_b_name} - Processed Data**")
            st.dataframe(df_b)
