# app.py - SafeLabel Streamlit App (Multi-tab, PyTesseract, Groq LLM)
import streamlit as st
import json
import os
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import requests
import pytesseract
from PIL import Image
import cv2

# ---------------------- CONFIG ----------------------
load_dotenv()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
api_key = GROQ_API_KEY
DATA_DIR = "data"
PRODUCT_INGREDIENTS_JSON = os.path.join(DATA_DIR, "product_ingredients.json")
INGREDIENTS_INFO_JSON = os.path.join(DATA_DIR, "ingredients_info.json")
MODEL_OPTIONS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b", "gemma-7b-it"]

@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@st.cache_resource
def setup_faiss_index(product_data):
    if not product_data:
        return None, None, []
    model = SentenceTransformer("all-MiniLM-L6-v2")
    names = list(product_data.keys())
    embeddings = model.encode(names)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return model, index, names

class SafeLabelController:
    def __init__(self, model_name):
        self.model_name = model_name
        self.product_data = load_json(PRODUCT_INGREDIENTS_JSON)
        self.embedding_model, self.faiss_index, self.product_names = setup_faiss_index(self.product_data)

    def search_db(self, query, top_k=3):
        if self.faiss_index is None:
            return []
        query_vector = self.embedding_model.encode([query])
        D, I = self.faiss_index.search(query_vector, top_k)
        return [self.product_names[i] for i in I[0] if i < len(self.product_names)]

    def duckduckgo_lookup(self, query):
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            return results[0]['body'][:500] if results else "No info found."

    def run_llm(self, prompt):
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are an expert in food safety and ingredient analysis."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 300
        }
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"API Error: {e}"

    def extract_keywords(self, user_query):
        prompt = f"""Extract keywords or product names from the user query: '{user_query}'. List them comma-separated."""
        response = self.run_llm(prompt)
        return [kw.strip() for kw in response.split(',') if kw.strip()]

    def build_final_prompt(self, user_query, retrieved_info):
        return f"""User Query: '{user_query}'\n\nProduct Info:\n{retrieved_info}\n\nGive a short, helpful and relevant answer (max 120 words)."""

# ---------------------- STREAMLIT UI ----------------------
def main():
    st.set_page_config(page_title="SafeLabel", page_icon="🛡️", layout="wide")
    selected_tab = st.sidebar.radio("🔍 Navigation", ["Database Viewer", "Chat Interface"])
    selected_model = st.sidebar.selectbox("LLM Model", MODEL_OPTIONS)
    controller = SafeLabelController(selected_model)
    st.sidebar.markdown(f"📦 Products in DB: **{len(controller.product_data)}**")

    if selected_tab == "Database Viewer":
        st.title("📄 Product & Ingredients Database")
        if controller.product_data:
            df = pd.DataFrame([{"Product": k, "Ingredients": ", ".join(v)} for k, v in controller.product_data.items()])
            st.dataframe(df)
        else:
            st.info("Database is empty.")

    elif selected_tab == "Chat Interface":
        st.title("💬 SafeLabel Chat Interface")
        uploaded_img = st.file_uploader("Upload Label Image (Optional)", type=["jpg", "png", "jpeg"])
        ocr_text = ""

        if uploaded_img:
            img = Image.open(uploaded_img)
            gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            ocr_text = pytesseract.image_to_string(gray)
            st.image(img, caption="Uploaded Image", use_column_width=True)
            st.text_area("OCR Extracted Text", ocr_text, height=120)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if query := st.chat_input("Ask about food products, ingredients, or upload image..."):
            user_combined = query + (". " + ocr_text if ocr_text else "")
            st.session_state.messages.append({"role": "user", "content": query})

            with st.chat_message("user"):
                st.markdown(query)

            # Step 1: Extract keywords
            keywords = controller.extract_keywords(user_combined)
            matched = []
            for kw in keywords:
                found = controller.search_db(kw)
                for f in found:
                    ing = ", ".join(controller.product_data.get(f, []))
                    matched.append(f"{f}: {ing}")

            # Step 2: Fallback to DDG
            if not matched:
                search_query = controller.run_llm(f"Generate a search engine query for: {', '.join(keywords)}")
                info = controller.duckduckgo_lookup(search_query)
            else:
                info = "\n".join(matched)

            # Step 3: Final response
            # Step 3: Final response
            final_prompt = controller.build_final_prompt(user_combined, info)  # <-- Fix here
            with st.chat_message("assistant"):
                with st.spinner("Analyzing ingredients..."):
                    response = controller.run_llm(final_prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
