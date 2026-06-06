"""
Genera el PDF del brochure corporativo GuLIN Enterprise
a partir del archivo brochure-pdf.html usando Playwright (Chromium).
"""
import os
from playwright.sync_api import sync_playwright

# Rutas
html_path = os.path.join(os.path.dirname(__file__), "brochure-pdf.html")
pdf_path = os.path.join(os.path.dirname(__file__), "brochure_gulin.pdf")

print(f"📄 Generando PDF desde: {html_path}")
print(f"📁 Destino: {pdf_path}")

# Convertir HTML a PDF con Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    
    # Esperar a que cargue todo
    page.wait_for_load_state("networkidle")
    
    # Generar PDF en orientación horizontal (landscape)
    page.pdf(
        path=pdf_path,
        format="A4",
        landscape=True,
        print_background=True,
        margin={
            "top": "0px",
            "bottom": "0px",
            "left": "0px",
            "right": "0px"
        }
    )
    
    browser.close()

print(f"✅ PDF generado exitosamente: {pdf_path}")
