import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Body na kružnici", layout="wide")

# 🪪 Informace o aplikaci v bočním panelu
with st.sidebar:
    st.header("O aplikaci")
    st.markdown("""
    **Body na kružnici**  
    Tato aplikace vykresluje body rovnoměrně rozmístěné po kružnici na základě zadaných parametrů.

    **Použité technologie:**  
    - Python  
    - Streamlit  
    - Matplotlib  
    - FPDF

    **Autor:** Microsoft Copilot  
    **Kontakt:** [copilot.microsoft.com](https://copilot.microsoft.com)
    """)

# 📥 Vstupní parametry
st.title("Body na kružnici s exportem do PDF")

col1, col2 = st.columns(2)
with col1:
    center_x = st.number_input("Střed X [m]", value=0.0)
    radius = st.number_input("Poloměr [m]", value=10.0)
    num_points = st.number_input("Počet bodů", min_value=1, value=12)
with col2:
    center_y = st.number_input("Střed Y [m]", value=0.0)
    color = st.color_picker("Barva bodů", "#FF0000")

# 🧮 Výpočet souřadnic
angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
x_points = center_x + radius * np.cos(angles)
y_points = center_y + radius * np.sin(angles)

# 🎨 Vykreslení grafu
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(x_points, y_points, color=color, s=100)
ax.set_aspect('equal')
ax.set_xlim(center_x - radius - 5, center_x + radius + 5)
ax.set_ylim(center_y - radius - 5, center_y + radius + 5)
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_title("Rozmístění bodů na kružnici")
ax.grid(True)

st.pyplot(fig)

# 📤 Export do PDF
if st.button("Exportovat do PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Body na kružnici – Výstupní zpráva", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Střed: ({center_x} m, {center_y} m)", ln=True)
        pdf.cell(200, 10, txt=f"Poloměr: {radius} m", ln=True)
        pdf.cell(200, 10, txt=f"Počet bodů: {num_points}", ln=True)
        pdf.cell(200, 10, txt=f"Barva bodů: {color}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Autor: Microsoft Copilot", ln=True)
        pdf.cell(200, 10, txt="Kontakt: https://copilot.microsoft.com", ln=True)
        pdf.image(tmpfile.name, x=10, y=80, w=180)

        pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(pdf_output.name)

        with open(pdf_output.name, "rb") as f:
            st.download_button("Stáhnout PDF", f, file_name="kruznice_vystup.pdf", mime="application/pdf")

        os.unlink(tmpfile.name)
        os.unlink(pdf_output.name)