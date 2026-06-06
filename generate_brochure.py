from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from io import BytesIO
from PIL import Image as PILImage, ImageDraw

# ─── Colores ───
PURPLE = "#8b5cf6"
PURPLE_D = "#7c3aed"
PURPLE_L = "#a78bfa"
PINK = "#ec4899"
CYAN = "#06b6d4"
GREEN = "#22c55e"
BG_DARK = "#0a0a12"
BG_CARD = "#111122"
BG_CARD2 = "#15152a"
TEXT_MAIN = "#e2e8f0"
TEXT_SEC = "#94a3b8"
TEXT_MUTED = "#64748b"
BORDER = "#1e1e3a"
WHITE = "#ffffff"

WIDTH, HEIGHT = A4
MARGIN = 20*mm
CW = WIDTH - 2*MARGIN

# ─── Estilos ───
styles = getSampleStyleSheet()
sty_title = ParagraphStyle("t1", fontSize=32, leading=38, textColor=HexColor(WHITE),
                           fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
sty_sub = ParagraphStyle("t2", fontSize=13, leading=18, textColor=HexColor(TEXT_SEC),
                         fontName="Helvetica", alignment=TA_CENTER, spaceAfter=6)
sty_h1 = ParagraphStyle("h1", fontSize=17, leading=21, textColor=HexColor(PURPLE_L),
                         fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=6)
sty_h2 = ParagraphStyle("h2", fontSize=12, leading=15, textColor=HexColor(WHITE),
                         fontName="Helvetica-Bold", spaceBefore=3, spaceAfter=3)
sty_body = ParagraphStyle("b1", fontSize=9.5, leading=14, textColor=HexColor(TEXT_SEC),
                          fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=4)
sty_small = ParagraphStyle("b2", parent=sty_body, fontSize=8.5, leading=12)
sty_footer = ParagraphStyle("f1", fontSize=7, leading=9, textColor=HexColor(TEXT_MUTED),
                            fontName="Helvetica", alignment=TA_CENTER)
sty_cta = ParagraphStyle("cta", fontSize=11, leading=14, textColor=HexColor(WHITE),
                         fontName="Helvetica-Bold", alignment=TA_CENTER)

def sp(h=6):
    return Spacer(1, h)

def accent_bar():
    d = Drawing(CW, 3)
    steps = 40
    seg = CW / steps
    colors = [PURPLE, PINK, CYAN]
    for i in range(steps):
        t = i / steps
        idx = min(int(t * 2), 2)
        lt = (t * 2) - idx
        c1 = colors[idx]
        c2 = colors[min(idx+1, 2)]
        r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
        r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
        r = int(r1*(1-lt)+r2*lt)
        g = int(g1*(1-lt)+g2*lt)
        b = int(b1*(1-lt)+b2*lt)
        d.add(Rect(i*seg, 0, seg+1, 3, fillColor=HexColor(f"#{r:02x}{g:02x}{b:02x}"), strokeColor=None))
    return d

def make_rounded_logo(path, size_mm=55):
    """Crea un logo con bordes redondeados usando PIL"""
    if not os.path.exists(path):
        return None
    img = PILImage.open(path).convert("RGBA")
    # Crear máscara redondeada
    mask = PILImage.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    r = int(img.width * 0.15)  # radio de 15%
    draw.rounded_rectangle([0, 0, img.width-1, img.height-1], radius=r, fill=255)
    # Aplicar máscara
    result = PILImage.new("RGBA", img.size, (0,0,0,0))
    result.paste(img, mask=mask)
    # Guardar en buffer
    buf = BytesIO()
    result.save(buf, format="PNG")
    buf.seek(0)
    return Image(buf, width=size_mm*mm, height=size_mm*mm)

def draw_bg(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(HexColor(BG_DARK))
    canvas_obj.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # Línea decorativa superior
    canvas_obj.setStrokeColor(HexColor(f"{PURPLE}20"))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(0, HEIGHT-1, WIDTH, HEIGHT-1)
    canvas_obj.restoreState()

def draw_page_num(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(HexColor(TEXT_MUTED))
    canvas_obj.drawCentredString(WIDTH/2, 12, f"GuLIN AI — Brochure — Pág. {doc.page}")
    canvas_obj.restoreState()

# ─── Construcción ───
out = os.path.join(os.path.dirname(__file__), "brochure_gulin.pdf")
logo_path = os.path.join(os.path.dirname(__file__), "GULIN_LOGO_3.jpeg")

doc = SimpleDocTemplate(out, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=16*mm, bottomMargin=18*mm,
    title="Brochure GuLIN AI", author="GuLIN AI")

S = []

# ============================================================
# PÁGINA 1 - PORTADA
# ============================================================
S.append(sp(35))

# Logo con bordes redondeados
logo_img = make_rounded_logo(logo_path, 60)
if logo_img:
    S.append(logo_img)
else:
    S.append(Image(logo_path, width=60*mm, height=60*mm))

S.append(sp(8))
S.append(Paragraph("GuLIN <font color='#8b5cf6'>IA</font>", sty_title))
S.append(Paragraph("Agente Inteligente Autónomo para TI Empresarial", sty_sub))
S.append(sp(6))
S.append(accent_bar())
S.append(sp(8))

S.append(Paragraph(
    "Detecta, diagnostica y mitiga incidentes de infraestructura "
    "<b>antes de que afecten a tus clientes</b>.",
    ParagraphStyle("desc", parent=sty_body, fontSize=11, leading=16,
                   textColor=HexColor(TEXT_SEC), alignment=TA_CENTER)
))
S.append(sp(22))

# ─── 4 métricas destacadas ───
metrics = [
    ("-40%", "MTTR", PURPLE),
    ("3x", "Velocidad", PINK),
    ("$50K+", "Ahorro/año", CYAN),
    ("99.9%", "SLA", GREEN),
]

m_data = []
for num, label, color in metrics:
    m_data.append([
        Paragraph(f"<font color='{color}' size='24'><b>{num}</b></font>",
                  ParagraphStyle("mn", fontSize=24, textColor=HexColor(color), alignment=TA_CENTER)),
        Paragraph(f"<b>{label}</b>",
                  ParagraphStyle("ml", fontSize=10, textColor=HexColor(WHITE), alignment=TA_CENTER)),
    ])

mt = Table(m_data, colWidths=[CW/4]*4)
mt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
S.append(mt)

S.append(sp(18))

# ─── Caja de propuesta de valor ───
val = Paragraph(
    "⚡ <b>Automatización Inteligente 24/7</b> — Correlaciona logs, métricas y trazas en tiempo real.<br/>"
    "🛡️ <b>Seguridad Enterprise</b> — SOC2, ISO 27001<br/>"
    "☁️ <b>Multicloud</b> — AWS, Azure, GCP, Jira, ServiceNow",
    ParagraphStyle("vb", fontSize=9.5, leading=15, textColor=HexColor(TEXT_SEC))
)
vt = Table([[val]], colWidths=[CW])
vt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD2)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(f"{PURPLE}30")),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
]))
S.append(vt)

S.append(sp(30))

# Contacto
ct = Table([[
    Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com",
              ParagraphStyle("ct", fontSize=8, textColor=HexColor(TEXT_MUTED), alignment=TA_CENTER))
]], colWidths=[CW])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
S.append(ct)

S.append(PageBreak())

# ============================================================
# PÁGINA 2 - PROBLEMA + SOLUCIÓN + CARACTERÍSTICAS
# ============================================================
S.append(Paragraph("El Problema", sty_h1))
S.append(Paragraph(
    "Las operaciones tradicionales de TI están al límite. Los ingenieros pasan el <b>60% de su tiempo</b> "
    "respondiendo a falsas alertas y apagando fuegos manualmente en lugar de construir valor.",
    sty_body
))
S.append(sp(4))

# Problemas
p_data = [
    [Paragraph("🔔", ParagraphStyle("pi", alignment=TA_CENTER, fontSize=14)),
     Paragraph("<b>Fatiga por Alertas</b>", ParagraphStyle("pt", fontSize=9.5, textColor=HexColor(WHITE))),
     Paragraph("Miles de notificaciones confusas al día. Imposible identificar qué es crítico antes de una caída.", sty_small)],
    [Paragraph("⏱️", ParagraphStyle("pi", alignment=TA_CENTER, fontSize=14)),
     Paragraph("<b>MTTR Elevado</b>", ParagraphStyle("pt", fontSize=9.5, textColor=HexColor(WHITE))),
     Paragraph("Horas de análisis de logs y llamadas de emergencia a las 3 a.m. con costosos tiempos muertos.", sty_small)],
    [Paragraph("☁️", ParagraphStyle("pi", alignment=TA_CENTER, fontSize=14)),
     Paragraph("<b>Costos Cloud</b>", ParagraphStyle("pt", fontSize=9.5, textColor=HexColor(WHITE))),
     Paragraph("Recursos sobre-dimensionados y licencias SaaS inactivas por falta de previsión inteligente.", sty_small)],
]
pt = Table(p_data, colWidths=[20, CW*0.28, CW*0.58])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD2)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('INNERGRID', (0,0), (-1,-1), 0.3, HexColor(BORDER)),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
S.append(pt)

S.append(sp(10))
S.append(accent_bar())
S.append(sp(6))

# Solución
S.append(Paragraph("Nuestra Solución", sty_h1))
S.append(Paragraph(
    "GuLIN es el <b>primer agente inteligente autónomo de TI</b> para empresas. Se integra de forma segura en tu stack "
    "tecnológico para diagnosticar anomalías, predecir problemas de infraestructura y mitigar incidentes "
    "de forma totalmente autónoma, <b>24/7</b>.",
    sty_body
))
S.append(sp(6))

# Características
S.append(Paragraph("Características Clave", sty_h1))

feats = [
    "🤖 <b>Diagnóstico Autónomo</b> — Correlaciona logs, métricas y trazas en tiempo real. Identifica causa raíz en segundos.",
    "🛡️ <b>Seguridad Enterprise</b> — Aislamiento absoluto. SOC2, ISO 27001. Tus datos nunca se usan para entrenar modelos públicos.",
    "☁️ <b>Multicloud</b> — AWS, Azure, GCP, Jira, ServiceNow. Conexión mediante APIs seguras OAuth 2.0.",
    "📊 <b>Optimización Costos</b> — Identifica recursos infrautilizados. Reduce hasta un 30% la factura cloud.",
    "🔔 <b>Alertas Inteligentes</b> — Filtra ruido y prioriza incidentes críticos con análisis contextual de impacto al negocio.",
    "⚡ <b>Automatización Segura</b> — Desde modo sugerencia hasta ejecución autónoma con permisos granulares.",
]

f_data = []
for f in feats:
    f_data.append([Paragraph(f, ParagraphStyle("fd", fontSize=8.5, leading=12, textColor=HexColor(TEXT_SEC)))])

ft = Table(f_data, colWidths=[CW])
ft.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD2)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
S.append(ft)

S.append(sp(10))
S.append(accent_bar())
S.append(sp(4))

# Roles
S.append(Paragraph("Casos de Uso por Rol", sty_h1))

roles = [
    "👨‍💻 <b>DevOps</b> — Pipelines CI/CD seguros, refactorización automatizada, despliegues sin intervención manual.",
    "🗄️ <b>DBAs</b> — Optimización de queries lentas, sugerencias de índices, monitoreo de cuellos de botella.",
    "🏗️ <b>Arquitectos</b> — Validación de arquitectura, detección de deuda técnica, generación de diagramas.",
    "🖥️ <b>SysAdmins</b> — Monitoreo proactivo, rotación de certificados, gestión de parches de seguridad.",
    "📈 <b>AIOps</b> — Correlación de alertas, reducción de falsos positivos, dashboards unificados.",
    "🏷️ <b>SAM</b> — Auditorías de licencias, detección de software no autorizado, optimización SaaS.",
]

r_data = []
for r in roles:
    r_data.append([Paragraph(r, ParagraphStyle("rd", fontSize=8.5, leading=12, textColor=HexColor(TEXT_SEC)))])

rt = Table(r_data, colWidths=[CW])
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD2)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
S.append(rt)

S.append(PageBreak())

# ============================================================
# PÁGINA 3 - IMPACTO + SEGURIDAD + CTA
# ============================================================
S.append(Paragraph("Impacto de Negocio", sty_h1))
S.append(sp(4))

# Impacto
imp_style = ParagraphStyle("is", fontSize=8.5, leading=12, textColor=HexColor(TEXT_SEC))
imp_val = ParagraphStyle("iv", fontSize=14, leading=17, textColor=HexColor(GREEN), fontName="Helvetica-Bold")

impact = [
    [Paragraph("<b>Métrica</b>", ParagraphStyle("ih", fontSize=9, textColor=HexColor(PURPLE_L), fontName="Helvetica-Bold")),
     Paragraph("<b>Resultado</b>", ParagraphStyle("ih", fontSize=9, textColor=HexColor(PURPLE_L), fontName="Helvetica-Bold")),
     Paragraph("<b>Descripción</b>", ParagraphStyle("ih", fontSize=9, textColor=HexColor(PURPLE_L), fontName="Helvetica-Bold"))],
    [Paragraph("MTTR", imp_style), Paragraph(f"<font color='{GREEN}'><b>-40%</b></font>", imp_val), Paragraph("Reducción del tiempo medio de resolución de incidentes críticos", imp_style)],
    [Paragraph("Velocidad Entrega", imp_style), Paragraph(f"<font color='{GREEN}'><b>3x</b></font>", imp_val), Paragraph("Aceleración en despliegues y resolución de impedimentos", imp_style)],
    [Paragraph("Costos Cloud", imp_style), Paragraph(f"<font color='{GREEN}'><b>-30%</b></font>", imp_val), Paragraph("Optimización de recursos y licencias SaaS", imp_style)],
    [Paragraph("Disponibilidad SLA", imp_style), Paragraph(f"<font color='{GREEN}'><b>99.9%</b></font>", imp_val), Paragraph("Disponibilidad garantizada con respuesta autónoma inmediata", imp_style)],
    [Paragraph("Productividad", imp_style), Paragraph(f"<font color='{GREEN}'><b>+60%</b></font>", imp_val), Paragraph("Más tiempo para construir valor en lugar de apagar fuegos", imp_style)],
    [Paragraph("ROI Inversión", imp_style), Paragraph(f"<font color='{GREEN}'><b>5x</b></font>", imp_val), Paragraph("Retorno sobre la inversión en el primer año de implementación", imp_style)],
]

it = Table(impact, colWidths=[CW*0.25, CW*0.17, CW*0.58])
it.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor("#1a1a30")),
    ('BACKGROUND', (0,1), (-1,-1), HexColor(BG_CARD)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
S.append(it)

S.append(sp(14))
S.append(accent_bar())
S.append(sp(6))

# Seguridad
S.append(Paragraph("Seguridad y Cumplimiento", sty_h1))

sec = [
    "🔐 <b>Control Humano</b> — Define permisos específicos. Desde sugerencias hasta ejecución automatizada.",
    "🛡️ <b>Nivel Enterprise</b> — Aislamiento absoluto. SOC2, ISO 27001. Datos nunca usados para entrenar modelos.",
    "🔗 <b>Integración Segura</b> — APIs OAuth 2.0 con tokens efímeros. AWS, Azure, GCP, Jira, ServiceNow.",
    "🔒 <b>Encriptación Total</b> — Tráfico TLS 1.3. Revocación de acceso en cualquier momento.",
]

s_data = []
for s in sec:
    s_data.append([Paragraph(s, ParagraphStyle("sd", fontSize=8.5, leading=12, textColor=HexColor(TEXT_SEC)))])

st = Table(s_data, colWidths=[CW])
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(BG_CARD2)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
S.append(st)

S.append(sp(18))
S.append(accent_bar())
S.append(sp(8))

# CTA
S.append(Paragraph(
    "Lleva la eficiencia de tu equipo de TI al siguiente nivel",
    ParagraphStyle("cta_t", parent=sty_title, fontSize=20, leading=24)
))
S.append(sp(4))
S.append(Paragraph(
    "Elimina la fatiga de alertas, asegura el tiempo de actividad y optimiza tus costos en nube "
    "con la primera solución TI autónoma.",
    ParagraphStyle("cta_sub", parent=sty_sub, fontSize=11, leading=15)
))
S.append(sp(12))

cta_t = Table([[Paragraph("<b>SOLICITAR DEMO →</b>", sty_cta)]], colWidths=[200])
cta_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(PURPLE)),
    ('BOX', (0,0), (-1,-1), 0, HexColor(PURPLE)),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 28),
    ('RIGHTPADDING', (0,0), (-1,-1), 28),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
S.append(cta_t)

S.append(sp(10))
S.append(Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com", sty_footer))
S.append(Paragraph("© 2026 GuLIN AI. Todos los derechos reservados.", sty_footer))

# ─── Generar ───
doc.build(S, onFirstPage=draw_bg, onLaterPages=lambda c,d: (draw_bg(c,d), draw_page_num(c,d)))
print(f"✅ Brochure PDF generado: {out}")
