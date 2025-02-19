import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Configuración de la API de Stable Diffusion Web UI
API_URL = "http://host.docker.internal:7860/sdapi/v1/txt2img"
MODEL_NAME = "legoworld_v20.safetensors [a522fbc64f]"

# Configurar la página
st.set_page_config(page_title="Generador de Imágenes LegoWorld", page_icon="🧱", layout="wide")

# Estilizar con CSS
st.markdown(
    """
    <style>
        .main { background-color: #eef5ff; }
        .stButton>button {
            background: linear-gradient(135deg, #ff5733 30%, #ff914d 100%);
            color: white;
            font-size: 20px;
            border-radius: 10px;
            padding: 10px 20px;
            transition: background 0.3s ease-in-out, color 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #e04d2a 30%, #ff7a36 100%);
            color: white;
        }
        .sidebar {
            background-color: #ffede0;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Título de la aplicación con estilo
st.markdown("""
<h1 style='text-align: center; color: #ff5733;'>🧱 Generador de Imágenes LegoWorld 🧱</h1>
<h3 style='text-align: center; color: #555;'>Crea increíbles imágenes al estilo LEGO con Stable Diffusion</h3>
""", unsafe_allow_html=True)

# Layout de dos columnas
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎨 Configuración del Prompt", unsafe_allow_html=True)
    
    # Contenedor eliminado para evitar el cuadro blanco innecesario
    category = st.selectbox("Selecciona una categoría:", ["Human", "Animal", "Object", "Scenery"])
    detail = st.text_input("Añade detalles:", "")
    num_images = st.slider("Número de imágenes:", min_value=1, max_value=5, value=1)
    
    prompt = f"{category}: {detail}" if detail else f"{category}"
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("🚀 Generar Imagen", use_container_width=True)

with col2:
    if generate:
        if prompt.strip():
            st.markdown("## ⏳ Generando imagen, por favor espera...")
            
            payload = {
                "prompt": prompt,
                "steps": 10,
                "cfg_scale": 7.5,
                "sampler_index": "Euler a",
                "n_iter": num_images,
                "width": 512,
                "height": 512,
                "seed": -1
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                images = result.get("images", [])
                st.markdown("### 🖼️ Imágenes generadas:")
                
                # Mostrar imágenes en filas con un máximo de 3 por fila
                cols = st.columns(min(num_images, 3))  # Ajusta el número de columnas dinámicamente
                for i, img_data in enumerate(images):
                    image = Image.open(BytesIO(base64.b64decode(img_data))).convert("RGB")  # Solución al warning
                    with cols[i % len(cols)]:
                        st.image(image, caption=f"Imagen {i+1}", use_container_width=True)
            else:
                st.error(f"❌ Error en la generación de imágenes: {response.status_code}")
        else:
            st.warning("⚠️ Por favor, introduce un prompt válido.")
