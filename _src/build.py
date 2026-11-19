#!/usr/bin/env python3
"""Genera la web (ES y EN) a partir de este archivo.
Uso: python3 _src/build.py   (desde la raíz del repositorio)
     python3 _src/build.py CARPETA --preview   (versión de prueba: enlaces relativos, borradores visibles)
Edita los datos de abajo (CERTS, PROJECTS, textos) y vuelve a ejecutarlo.
El correo de contacto se lee de _src/mail.txt.
"""
import base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
_args = [a for a in sys.argv[1:] if not a.startswith("--")]
PREVIEW = "--preview" in sys.argv
OUT = _args[0] if _args else ROOT
BASE = "https://candelavazquezfontal.github.io"
LASTMOD = "2026-11-17"
CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
MAIL = open(os.path.join(HERE, "mail.txt"), encoding="utf-8").read().strip()
MAIL_ENC = base64.b64encode(MAIL[::-1].encode()).decode()   # el correo no aparece en claro en el HTML (anti-spam)

def e(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- páginas
# clave -> (ruta ES, ruta EN)
PAGES = {
    "home":  ("", "en/"),
    "path":  ("trayectoria/", "en/experience/"),
    "proj":  ("proyectos/", "en/projects/"),
    "cert":  ("certificaciones/", "en/certifications/"),
    "more":  ("mas-alla-del-cv/", "en/beyond-the-cv/"),
    "contact": ("contacto/", "en/contact/"),
}
ORDER = ["home", "path", "proj", "cert", "more", "contact"]
CV_FILE = {"es": "cv/Candela-Vazquez-Fontal-CV-ES.pdf", "en": "cv/Candela-Vazquez-Fontal-CV-EN.pdf"}
CUR = {"path": ""}   # página que se está escribiendo (para enlaces relativos en la versión de prueba)

def url(key, lang): return BASE + "/" + PAGES[key][0 if lang == "es" else 1]

def asset(p):  # archivo del sitio (css, pdf, imagen)
    if PREVIEW:
        return os.path.relpath(p, CUR["path"] or ".").replace(os.sep, "/")
    return "/" + p

def href(key, lang):  # enlace a otra página del sitio
    target = PAGES[key][0 if lang == "es" else 1]
    if PREVIEW:
        return os.path.relpath(target + "index.html", CUR["path"] or ".").replace(os.sep, "/")
    return "/" + target

# ---------------------------------------------------------------- textos de interfaz
UI = {
 "es": {
  "lang": "es", "locale": "es_ES", "other_locale": "en_GB", "label": "ES",
  "brand": "C. Vázquez Fontal",
  "nav": {"home": "Inicio", "path": "Trayectoria", "proj": "Proyectos", "cert": "Certificaciones", "more": "Más allá del CV", "contact": "Contacto"},
  "nav_aria": "Secciones", "lang_aria": "Idioma",
  "site_name": "Candela Vázquez Fontal",
  "titles": {
    "home": "Candela Vázquez Fontal · Ingeniería en Organización Industrial",
    "path": "Trayectoria · Candela Vázquez Fontal",
    "proj": "Proyectos · Candela Vázquez Fontal",
    "cert": "Certificaciones · Candela Vázquez Fontal",
    "more": "Más allá del CV · Candela Vázquez Fontal",
    "contact": "Contacto · Candela Vázquez Fontal"},
  "descs": {
    "home": "Web personal de Candela Vázquez Fontal, estudiante de Ingeniería en Organización Industrial en Deusto y en prácticas de consultoría de transformación digital en IDOM. Trayectoria, proyectos y certificaciones.",
    "path": "Experiencia, formación, reconocimientos y vida universitaria de Candela Vázquez Fontal: IDOM, Universidad de Deusto, LSE, CBS y Universidad de Oviedo.",
    "proj": "Proyectos de Candela Vázquez Fontal: simulación de colas en macro-tiendas de Zara, modelo de negocio de EcoPlay y monografía del Bachillerato Internacional.",
    "cert": "Certificaciones de Candela Vázquez Fontal en datos e IA, gestión de proyectos, operaciones, idiomas (Cambridge C2) y más, con enlace a cada certificado.",
    "more": "Lo que no cabe en un CV: ballet, la experiencia en UWC Atlantic College, de Gijón a Bilbao y las ideas que estoy construyendo.",
    "contact": "Contacto de Candela Vázquez Fontal: LinkedIn, correo electrónico y CV en PDF."},
  "og_desc": "Operaciones, logística y análisis de datos. Trayectoria, proyectos y certificaciones.",
  "og_alt": "Candela Vázquez Fontal, Ingeniería en Organización Industrial. Operaciones, logística y datos.",
  "footer": "Candela Vázquez Fontal · 2026",
 },
 "en": {
  "lang": "en", "locale": "en_GB", "other_locale": "es_ES", "label": "EN",
  "brand": "C. Vázquez Fontal",
  "nav": {"home": "Home", "path": "Experience", "proj": "Projects", "cert": "Certifications", "more": "Beyond the CV", "contact": "Contact"},
  "nav_aria": "Sections", "lang_aria": "Language",
  "site_name": "Candela Vázquez Fontal",
  "titles": {
    "home": "Candela Vázquez Fontal · Industrial Organisation Engineering",
    "path": "Experience · Candela Vázquez Fontal",
    "proj": "Projects · Candela Vázquez Fontal",
    "cert": "Certifications · Candela Vázquez Fontal",
    "more": "Beyond the CV · Candela Vázquez Fontal",
    "contact": "Contact · Candela Vázquez Fontal"},
  "descs": {
    "home": "Personal website of Candela Vázquez Fontal, Industrial Organisation Engineering student at Deusto and digital transformation consulting intern at IDOM. Experience, projects and certifications.",
    "path": "Experience, education, honours and university life of Candela Vázquez Fontal: IDOM, University of Deusto, LSE, CBS and University of Oviedo.",
    "proj": "Projects by Candela Vázquez Fontal: queueing simulation for Zara mega-stores, the EcoPlay business model and the International Baccalaureate extended essay.",
    "cert": "Certifications of Candela Vázquez Fontal in data and AI, project management, operations, languages (Cambridge C2) and more, with a link to each certificate.",
    "more": "What doesn't fit on a CV: ballet, the UWC Atlantic College experience, from Gijón to Bilbao and the ideas I'm building.",
    "contact": "Contact Candela Vázquez Fontal: LinkedIn, email and CV as PDF."},
  "og_desc": "Operations, logistics and data analysis. Experience, projects and certifications.",
  "og_alt": "Candela Vázquez Fontal, Industrial Organisation Engineering. Operations, logistics and data.",
  "footer": "Candela Vázquez Fontal · 2026",
 },
}

# ---------------------------------------------------------------- contenido: inicio
HOME = {
 "es": {
  "kicker": "Ingeniería en Organización Industrial · Universidad de Deusto",
  "lead": "Quiero ayudar a las empresas a hacer lo mismo con menos recursos. Me formo en operaciones, logística y análisis de datos, y hago prácticas de consultoría de transformación digital en IDOM.",
  "cta1": "Ver proyectos", "cta2": "Certificaciones", "cta3": "Descargar CV (PDF)",
  "label_title": "Albarán · Ref. CVF-2026", "label_aria": "Datos rápidos",
  "dl": [("Origen", "Gijón → Bilbao"),
         ("Ahora", "Prácticas de consultoría de transformación digital en IDOM"),
         ("Destino", "Optimización de operaciones y logística"),
         ("Idiomas", "ES nativo · EN C2 (CPE) · DE A1 → A2"),
         ("Grado", "Hasta 2027")],
  "about": ["Enfoco los estudios, el trabajo y los idiomas como proyectos a largo plazo. Leo mucho, planifico con detalle y trabajo mejor con problemas e información real.",
            "Estudio Ingeniería en Organización Industrial en Deusto y hago la formación dual en IDOM, en un proyecto de consultoría SAP para un cliente industrial. En verano de 2026 cursé microeconomía en LSE y macroeconomía en CBS.",
            "Me interesan sobre todo los almacenes, el inventario y los costes, y las pequeñas empresas que casi nunca tienen herramientas hechas a su medida."],
  "areas_t": "Áreas de interés",
  "areas": ["Logística y almacenes", "Operaciones", "Optimización", "Gestión de costes", "Análisis de datos", "IA aplicada"],
  "tools_t": "Herramientas",
  "tools": ["Power BI", "SAP (QM)", "Jira", "Notion", "Microsoft 365"],
  "seek_t": "Lo que busco",
  "seek": "Quiero dedicarme a optimizar los recursos de una empresa para que haga lo mismo con menos, con un enfoque más sostenible. Me interesan la logística y las operaciones apoyadas en datos y en transformación digital.",
  "seek_chips": ["Operaciones y logística", "Análisis de datos", "Transformación digital", "Mejora de procesos"],
  "doors": [("path", "Trayectoria", "4 matrículas de honor", "Experiencia y formación →"),
            ("proj", "Proyectos", "{n} proyectos", "Abrir cada uno →"),
            ("cert", "Certificaciones", "{n} certificaciones", "Filtrar y ver insignias →"),
            ("more", "Más allá del CV", "Ballet, UWC y más", "Conocerme mejor →")],
 },
 "en": {
  "kicker": "Industrial Organisation Engineering · University of Deusto",
  "lead": "I want to help companies do the same with fewer resources. I'm training in operations, logistics and data analysis, and I'm doing a digital transformation consulting internship at IDOM.",
  "cta1": "See projects", "cta2": "Certifications", "cta3": "Download CV (PDF)",
  "label_title": "Waybill · Ref. CVF-2026", "label_aria": "Quick facts",
  "dl": [("Origin", "Gijón → Bilbao"),
         ("Now", "Digital transformation consulting internship at IDOM"),
         ("Destination", "Optimising operations and logistics"),
         ("Languages", "Spanish native · English C2 (CPE) · German A1 → A2"),
         ("Degree", "Until 2027")],
  "about": ["I approach my studies, work and languages as long-term projects. I read a lot, plan in detail, and work best with real problems and real information.",
            "I study Industrial Organisation Engineering at Deusto and do the dual programme at IDOM, on an SAP consulting project for an industrial client. In summer 2026 I took microeconomics at LSE and macroeconomics at CBS.",
            "I'm especially interested in warehouses, inventory and costs, and in small businesses that rarely have tools made to measure."],
  "areas_t": "Areas of interest",
  "areas": ["Logistics and warehouses", "Operations", "Optimisation", "Cost management", "Data analysis", "Applied AI"],
  "tools_t": "Tools",
  "tools": ["Power BI", "SAP (QM)", "Jira", "Notion", "Microsoft 365"],
  "seek_t": "What I'm looking for",
  "seek": "I want to optimise a company's resources so it does the same with less, with a more sustainable approach. I'm interested in logistics and operations supported by data and digital transformation.",
  "seek_chips": ["Operations and logistics", "Data analysis", "Digital transformation", "Process improvement"],
  "doors": [("path", "Experience", "4 Matrícula de Honor grades", "Experience and education →"),
            ("proj", "Projects", "{n} projects", "Open each one →"),
            ("cert", "Certifications", "{n} certifications", "Filter and see badges →"),
            ("more", "Beyond the CV", "Ballet, UWC and more", "Get to know me →")],
 },
}

# ---------------------------------------------------------------- contenido: trayectoria
# Cada elemento: (fecha, titulo, organización, descripción, viñetas, chips)
PATH = {
 "es": {
  "h": "Trayectoria", "mono": "Experiencia · formación · reconocimientos",
  "sections": [
   ("Experiencia", [
     ("Sep 2026 – hoy", "Becaria en consultoría de transformación digital", "IDOM Consulting, Engineering, Architecture · Bilbao",
      "Prácticas de formación dual en un proyecto de consultoría SAP para un cliente industrial del sector Oil & Gas.",
      ["Soporte y evolución del módulo de calidad de SAP (QM): pruebas y documentación de nuevos campos de ensayo de calidad y conversiones de unidades, y traslado de errores reproducibles al desarrollador.",
       "Apoyo en el despliegue en una nueva sede internacional.",
       "Detección de mejoras de proceso."], []),
     ("Jul – Ago 2025", "Auxiliar administrativo", "Arminza asesores · Gijón",
      "Contabilidad de varias empresas y particulares con software de asesoría y Excel. Presentación de modelos a Hacienda y cuentas anuales.", [], []),
     ("Jul – Ago 2024", "Auxiliar administrativo", "Idoneea (antes Disashop) · A Coruña",
      "Prevención de riesgos laborales y tareas básicas de contabilidad.", [], []),
     ("Oct – Dic 2021", "Profesora de ballet", "Academia Paso a Dos · Gijón", "", [], []),
   ]),
   ("Formación", [
     ("Sep 2025 – 2027", "Grado en Ingeniería en Organización Industrial (bilingüe)", "Universidad de Deusto", "", [],
      ["Optimización y Simulación", "Logística", "Production Management", "Integrated Production Systems",
       "Procesos y Gestión de la Calidad", "Oficina de Gestión de Proyectos", "Ingeniería del Producto", "Inglés"]),
     ("Ago 2026", "Summer School: Introductory Microeconomics", "The London School of Economics and Political Science (LSE)", "", [],
      ["Microeconomía", "Economía", "Inglés"]),
     ("Jun – Jul 2026", "Summer School: Principles of Macroeconomics", "Copenhagen Business School (CBS)", "", [],
      ["Macroeconomía", "Economía", "Inglés"]),
     ("Sep 2023 – Jun 2025", "Grado en Ingeniería en Organización Industrial (bilingüe)", "Universidad de Oviedo",
      "Dos primeros cursos, antes del traslado a Deusto para hacer la formación dual.", [],
      ["Strength of Materials", "Graphic Expression", "Statistics", "Inglés"]),
     ("Sep 2021 – Jul 2023", "Bachillerato Internacional y Bachillerato de Ciencias", "RIES Jovellanos · Gijón", "", [],
      ["Español A: Literatura (NS)", "Física (NS)", "Matemáticas: Análisis (NS)", "Inglés B (NM)", "Filosofía (NM)", "Química (NM)", "Monografía", "Teoría del Conocimiento"]),
   ]),
   ("Reconocimientos", [
     ("Jun 2026", "Matrícula de honor en Optimización y Simulación", "Universidad de Deusto", "", [], []),
     ("Ene 2026", "Matrícula de honor en Ingeniería del Producto", "Universidad de Deusto", "", [], []),
     ("Ene 2025", "Matrícula de honor en Strength of Materials", "Universidad de Oviedo", "", [], []),
     ("May 2024", "Matrícula de honor en Graphic Expression", "Universidad de Oviedo", "", [], []),
   ]),
   ("Vida universitaria", [
     ("Feb 2026 – hoy", "Deusto Consulting Club", "Junior · División Operations and Supply Chain (desde oct. 2026) · División Digital, Tech & AI (desde nov. 2026)", "", [], []),
     ("Oct 2025 – Jun 2026", "UNIC Student Ambassador", "UNIC, European University of Cities in Post-Industrial Transition",
      "Embajadora estudiantil de la alianza UNIC en Deusto. Colaboré en la UNIC Conference (Bilbao, nov. 2025) guiando a los asistentes en el registro y las salas, y en el UNIC Day (mar. 2026) dinamizando una actividad interactiva para atraer a estudiantes a la alianza. Participé en la red de Student Ambassadors de las universidades UNIC y propuse mejoras como control de asistencia, encuentros presenciales y más visibilidad de la alianza.", [], []),
     ("Oct – Nov 2025", "Deusto START I", "Deusto Emprende · programa de emprendimiento",
      "El proyecto que desarrollamos durante el curso es PAUSA, un concepto de app móvil freemium que ayuda a jóvenes profesionales (20-35 años) a reducir el uso del móvil y a gestionar su tiempo de forma más consciente.",
      ["Desarrollé la idea en equipo: definición del problema, estudio de mercado, propuesta de valor y Business Model Canvas, donde me centré en segmentos de clientes, propuesta de valor, actividades clave, canales y socios.",
       "Diseñé el modelo de negocio: app base gratuita con paquetes de asesoramiento especializado y un plan de marketing basado en influencers de estilo de vida.",
       "Presenté el proyecto en un pitch final."], []),
     ("Sep 2025 – Ene 2026", "Big Buddy y Programa Tandem", "Universidad de Deusto",
      "Actividades interculturales con estudiantes internacionales e intercambio de idiomas.", [], []),
   ]),
  ],
 },
 "en": {
  "h": "Experience", "mono": "Experience · education · honours",
  "sections": [
   ("Experience", [
     ("Sep 2026 – present", "Digital Transformation Consulting Intern", "IDOM Consulting, Engineering, Architecture · Bilbao",
      "Dual-training internship on an SAP consulting project for an industrial client in the Oil & Gas sector.",
      ["Support and evolution of the SAP quality module (QM): testing and documenting new quality-inspection fields and unit conversions, and passing reproducible errors to the developer.",
       "Support for the rollout at a new international site.",
       "Identifying process improvements."], []),
     ("Jul – Aug 2025", "Administrative Assistant", "Arminza asesores · Gijón",
      "Accounting for several companies and individuals using accountancy software and Excel. Filing tax returns and annual accounts.", [], []),
     ("Jul – Aug 2024", "Administrative Assistant", "Idoneea (formerly Disashop) · A Coruña",
      "Occupational risk prevention and basic accounting tasks.", [], []),
     ("Oct – Dec 2021", "Ballet teacher", "Paso a Dos academy · Gijón", "", [], []),
   ]),
   ("Education", [
     ("Sep 2025 – 2027", "Bachelor's degree in Industrial Organisation Engineering (bilingual)", "University of Deusto", "", [],
      ["Optimization and Simulation", "Logistics", "Production Management", "Integrated Production Systems",
       "Quality Processes and Management", "Project Management Office", "Product Engineering", "English"]),
     ("Aug 2026", "Summer School: Introductory Microeconomics", "The London School of Economics and Political Science (LSE)", "", [],
      ["Microeconomics", "Economics", "English"]),
     ("Jun – Jul 2026", "Summer School: Principles of Macroeconomics", "Copenhagen Business School (CBS)", "", [],
      ["Macroeconomics", "Economics", "English"]),
     ("Sep 2023 – Jun 2025", "Bachelor's degree in Industrial Organisation Engineering (bilingual)", "University of Oviedo",
      "First two years, before transferring to Deusto for the dual programme.", [],
      ["Strength of Materials", "Graphic Expression", "Statistics", "English"]),
     ("Sep 2021 – Jul 2023", "International Baccalaureate and Science Bachillerato", "RIES Jovellanos · Gijón", "", [],
      ["Spanish A: Literature (HL)", "Physics (HL)", "Mathematics: Analysis (HL)", "English B (SL)", "Philosophy (SL)", "Chemistry (SL)", "Extended essay", "Theory of Knowledge"]),
   ]),
   ("Honours", [
     ("Jun 2026", "Matrícula de Honor in Optimization and Simulation", "University of Deusto", "", [], []),
     ("Jan 2026", "Matrícula de Honor in Product Engineering", "University of Deusto", "", [], []),
     ("Jan 2025", "Matrícula de Honor in Strength of Materials", "University of Oviedo", "", [], []),
     ("May 2024", "Matrícula de Honor in Graphic Expression", "University of Oviedo", "", [], []),
   ]),
   ("University life", [
     ("Feb 2026 – present", "Deusto Consulting Club", "Junior · Operations and Supply Chain division (since Oct 2026) · Digital, Tech & AI division (since Nov 2026)", "", [], []),
     ("Oct 2025 – Jun 2026", "UNIC Student Ambassador", "UNIC, European University of Cities in Post-Industrial Transition",
      "UNIC Student Ambassador at Deusto. Supported the UNIC Conference in Bilbao (Nov 2025) by guiding participants through registration and sessions, and ran an interactive game at UNIC Day (Mar 2026) to raise student interest in the alliance. Took part in the UNIC Student Ambassadors network and proposed improvements such as attendance tracking, in-person ambassador meetings and greater visibility of the alliance.", [], []),
     ("Oct – Nov 2025", "Deusto START I", "Deusto Emprende · entrepreneurship programme",
      "The project we developed during the programme is PAUSA, a freemium mobile app concept that helps young professionals (aged 20–35) cut down on phone use and manage their time more consciously.",
      ["Developed the idea as a team: problem definition, market study, value proposition and Business Model Canvas, where I focused on customer segments, value proposition, key activities, channels and partners.",
       "Designed the business model: a free base app with specialist advice packages and a marketing plan based on lifestyle influencers.",
       "Presented the project in a final pitch."], []),
     ("Sep 2025 – Jan 2026", "Big Buddy and Tandem Programme", "University of Deusto",
      "Intercultural activities with international students and language exchange.", [], []),
   ]),
  ],
 },
}

# ---------------------------------------------------------------- proyectos
PROJECTS = [
 {"id": "PRJ-004", "short": {"es": "reZZ", "en": "reZZ"}, "honor": False, "areas": ["digital", "pm"],
  "link": "https://rezz-app.pages.dev",
  "es": {"t": "reZZ: app de recetas para iPhone y Mac",
         "meta": "Proyecto personal · oct. – nov. 2026 · en marcha",
         "ctx": "Quería guardar mis recetas en un solo sitio, adaptarlas a lo que tengo en la despensa y guardar recetas de Instagram sin copiarlas a mano.",
         "how": "Diseñé y puse en marcha una app web instalable (PWA) que funciona sin conexión y se sincroniza entre el iPhone y el Mac.",
         "res": ["App publicada y en uso diario, sin coste: alojamiento en Cloudflare Pages y datos en Supabase.",
                 "Cada receta original se conserva intacta y las variantes quedan encima, con su historial.",
                 "Despensa y lista de la compra conectadas con las recetas; un Atajo de iPhone guarda reels de Instagram como receta."],
         "tools": ["Diseño de producto", "PWA", "Supabase", "Cloudflare Pages"], "role": "Proyecto individual: idea, diseño y pruebas.",
         "link": "Abrir la app"},
  "en": {"t": "reZZ: a recipe app for iPhone and Mac",
         "meta": "Personal project · Oct – Nov 2026 · ongoing",
         "ctx": "I wanted my recipes in one place, adapted to what I have in the pantry, and to save Instagram recipes without copying them by hand.",
         "how": "Designed and launched an installable web app (PWA) that works offline and syncs between iPhone and Mac.",
         "res": ["App live and in daily use at no cost: hosted on Cloudflare Pages with data in Supabase.",
                 "Each original recipe is kept intact, with variants layered on top and their history.",
                 "Pantry and shopping list linked to recipes; an iPhone Shortcut saves Instagram reels as recipes."],
         "tools": ["Product design", "PWA", "Supabase", "Cloudflare Pages"], "role": "Individual project: idea, design and testing.",
         "link": "Open the app"}},
 {"id": "PRJ-001", "short": {"es": "Zara", "en": "Zara"}, "honor": True, "areas": ["opt", "log", "data"],
  "es": {"t": "Colas y simulación: macro-tiendas de Zara",
         "meta": "Optimización y Simulación · Deusto · feb. – may. 2026 · proyecto en grupo (3 personas)",
         "ctx": "Trabajo de la asignatura sobre el proceso de recogida y preparación de pedidos online de las macro-tiendas de Zara.",
         "how": "Modelo del proceso como una cola de varios servidores, comparando una única macro-tienda con cinco tiendas distribuidas, y simulación de un año de operación (777.780 pedidos).",
         "res": ["Sistema saturado en la franja de 16:00 a 21:00 en ambos escenarios y sin capacidad para recuperar la cola (−795 y −390 pedidos al día).",
                 "Simulación de un año: 62,58 % de pedidos servidos y 290.030 ventas perdidas, todas en la franja nocturna.",
                 "Propuesta: avisar a los clientes de los retrasos, limitar la cola de pedidos online y añadir capacidad por la tarde y por la noche."],
         "tools": ["Teoría de colas", "Simulación"], "role": "Proyecto en grupo de 3 personas."},
  "en": {"t": "Queueing and Simulation: Zara mega-stores",
         "meta": "Optimization and Simulation · Deusto · Feb – May 2026 · group project (3 people)",
         "ctx": "Course project on the online-order pickup and packing process of Zara mega-stores.",
         "how": "Modelled the process as a multi-server queue, comparing a single mega-store with five distributed stores, and simulated a full year of operation (777,780 orders).",
         "res": ["System saturated in the 16:00–21:00 slot in both scenarios and unable to recover its backlog (−795 and −390 orders/day).",
                 "One-year simulation: 62.58% of orders served and 290,030 lost sales, all in the overnight slot.",
                 "Proposal: notify customers of delays, cap the online order queue and add afternoon and night capacity."],
         "tools": ["Queueing theory", "Simulation"], "role": "Group project, 3 people."}},
 {"id": "PRJ-002", "short": {"es": "EcoPlay", "en": "EcoPlay"}, "honor": True, "areas": ["cost", "biz"],
  "es": {"t": "EcoPlay: suscripción circular de juguetes",
         "meta": "Ingeniería del Producto · Deusto · sept. 2025 – ene. 2026 · proyecto en grupo (3 personas)",
         "ctx": "Modelo de negocio de un servicio de suscripción de juguetes reacondicionados.",
         "how": "Business Model Canvas y Value Proposition Canvas, modelo económico y diseño de una validación con 7 hipótesis críticas y 4 entrevistas a clientes.",
         "res": ["Punto de equilibrio en 411 suscriptores mensuales activos y beneficio neto objetivo de 25.000 € en el tercer año.",
                 "Coste variable de 13 € por cliente y planes de 19,90 €, 25,90 € y 34,90 € al mes.",
                 "Validación: el 80 % entendió el concepto y preguntó por los plazos de entrega, sin motivo para cambiar de rumbo."],
         "tools": ["Business Model Canvas", "Value Proposition Canvas", "Análisis de costes", "Entrevistas"], "role": "Proyecto en grupo de 3 personas."},
  "en": {"t": "EcoPlay: circular toy subscription",
         "meta": "Product Engineering · Deusto · Sep 2025 – Jan 2026 · group project (3 people)",
         "ctx": "Business model for a subscription service of refurbished toys.",
         "how": "Business Model Canvas and Value Proposition Canvas, economic model, and a validation test with 7 critical hypotheses and 4 customer interviews.",
         "res": ["Break-even at 411 active monthly subscribers and a €25,000 net profit target in year 3.",
                 "€13 variable cost per customer and plans at €19.90, €25.90 and €34.90 a month.",
                 "Validation: 80% understood the concept and asked about delivery times, with no reason found to pivot."],
         "tools": ["Business Model Canvas", "Value Proposition Canvas", "Cost analysis", "Interviews"], "role": "Group project, 3 people."}},
 {"id": "PRJ-003", "short": {"es": "Monografía", "en": "Extended essay"}, "honor": False, "areas": [],
  "es": {"t": "Monografía del Bachillerato Internacional",
         "meta": "Literatura castellana e inglesa · ene. 2022 – mar. 2023",
         "ctx": "La monografía es el trabajo de fin del Bachillerato Internacional: una investigación propia sobre un tema elegido por el alumno.",
         "how": "Investigación guiada y redacción académica sobre literatura castellana e inglesa, elegida por mi interés en la lectura.",
         "res": ["Monografía entregada y evaluada."],
         "tools": ["Investigación", "Planificación de proyectos", "Redacción académica"], "role": "Trabajo individual."},
  "en": {"t": "International Baccalaureate Extended Essay",
         "meta": "Spanish and English literature · Jan 2022 – Mar 2023",
         "ctx": "The extended essay is the capstone of the IB Diploma: independent research on a topic chosen by the student.",
         "how": "Guided research and academic writing on Spanish and English literature, chosen out of my interest in reading.",
         "res": ["Extended essay submitted and assessed."],
         "tools": ["Research", "Project planning", "Academic writing"], "role": "Individual work."}},
]
AREAS = [("digital", {"es": "Producto digital", "en": "Digital product"}),
         ("opt", {"es": "Optimización", "en": "Optimisation"}),
         ("log", {"es": "Logística", "en": "Logistics"}),
         ("data", {"es": "Datos", "en": "Data"}),
         ("cost", {"es": "Costes", "en": "Costs"}),
         ("pm", {"es": "Gestión de proyectos", "en": "Project management"}),
         ("biz", {"es": "Negocio", "en": "Business"})]
PROJ_UI = {
 "es": {"h": "Proyectos", "mono": "Abre cada uno para ampliar", "area": "Área", "all": "Todas",
        "count": "{a} de {b} proyectos", "honor": "Asignatura con matrícula de honor", "problem": "Problema",
        "done": "Qué se hizo", "role": "Mi parte", "res": "Resultados", "tools": "Herramientas y métodos",
        "areas": "Áreas", "area_aria": "Área del proyecto"},
 "en": {"h": "Projects", "mono": "Open each one to expand", "area": "Area", "all": "All",
        "count": "{a} of {b} projects", "honor": "Course with Matrícula de Honor", "problem": "Problem",
        "done": "What was done", "role": "My part", "res": "Results", "tools": "Tools and methods",
        "areas": "Areas", "area_aria": "Project area"},
}

# ---------------------------------------------------------------- certificaciones
LL = "https://www.linkedin.com/learning/certificates/"
CR = "https://www.credly.com/badges/"
SJ = "https://verify.skilljar.com/c/"
CATS = [("data", {"es": "Datos e IA", "en": "Data and AI"}),
        ("ops", {"es": "Operaciones y finanzas", "en": "Operations and finance"}),
        ("pm", {"es": "Gestión de proyectos", "en": "Project management"}),
        ("prod", {"es": "Productividad y habilidades", "en": "Productivity and skills"}),
        ("lang", {"es": "Idiomas", "en": "Languages"}),
        ("ballet", {"es": "Ballet", "en": "Ballet"})]
# (título en, título es o None, emisor, cat, fecha, url, id, pdf, "badge" o None)
CERTS = [
 ("Notion Advanced Badge", None, "Notion", "prod", "2026-03", SJ + "xu6fxgkbqdtj", None, None, None),
 ("Notion Workflows Badge", None, "Notion", "prod", "2026-03", SJ + "t9p6pafir5xa", None, None, None),
 ("Notion Essentials Badge", None, "Notion", "prod", "2026-03", SJ + "k6drqh7ybahc", None, None, None),
 ("Project Management Fundamentals", None, "IBM", "pm", "2025-11", CR + "fda90fd6-bf41-454a-a05c-a5a7dce7dfeb", None, None, "badge"),
 ("Project Management and Agile Fundamentals", None, "Santander Open Academy", "pm", "2025-09", None, "OA-2025-0924001763036", "certificados/project-management-and-agile-fundamentals.pdf", None),
 ("Leading in a Digital World", None, "IE University", "prod", "2025-09", None, "OA-2025-0922001750874", "certificados/leading-in-a-digital-world.pdf", None),
 ("Introduction to Generative AI", None, "MIT Professional Education", "data", "2025-09", None, "OA-2025-0922001750362", "certificados/introduction-to-generative-ai.pdf", None),
 ("C2 Proficiency (CPE)", None, "Cambridge English", "lang", "2025-07", None, None, "certificados/c2-proficiency-cambridge.pdf", None),
 ("Managing Multiple Projects", None, "LinkedIn Learning", "pm", "2025-07", LL + "6d967894c8d602e24c68b66d6d60f02e17e83166a874dbd9c2fe51df52e58ff1", None, None, None),
 ("AI for Administrative Roles: Streamline Tasks and Boost Productivity", None, "LinkedIn Learning", "data", "2025-07", LL + "2f2649018ba1a5fd018c0eee74096a909efea05e823dc9b5ac042890fc282127", None, None, None),
 ("Using Microsoft Teams and Outlook Together: Maximizing Productivity", None, "LinkedIn Learning", "prod", "2025-07", LL + "802a17363575a44039c5802fdb3ab9493e353a2b3156d9a123fb1d1b1a5739ee", None, None, None),
 ("Outlook: Efficient Email Management", None, "LinkedIn Learning", "prod", "2025-07", LL + "361cea6c955319cbfad60c8e697ef9124948472aed5e21b45fbc0017d85ae766", None, None, None),
 ("Business Analysis: Essential Tools and Techniques", None, "LinkedIn Learning", "data", "2025-07", LL + "e4cb9fd79dfc14a808d413f85f2076626b413cfc9ea497fbaac9ca6db66af848", None, None, None),
 ("The Role of Business Analysis in Data Analytics", None, "LinkedIn Learning", "data", "2025-07", LL + "a967b50a1b112452a21be6a401eed408db7bc0bb62fa1ed11132eece9193b944", None, None, None),
 ("Financial Accounting Part 2", None, "LinkedIn Learning", "ops", "2025-07", LL + "8d37386fbaf039bccbbcba031050771baf6fbf5534b9651e667726b146fdd1d6", None, None, None),
 ("Excel Supply Chain Analysis: Solving Inventory Problems", None, "LinkedIn Learning", "ops", "2025-07", LL + "43a9916b4a7e85bf1a4c3a263fa0da773255f57f9168afb816fe2332063998b9", None, None, None),
 ("Financial Accounting Part 1", None, "LinkedIn Learning", "ops", "2025-07", LL + "3f714be15bfcfa3c3023316436246532507650f180e9d23c22f99b8f1a5d9ddb", None, None, None),
 ("Financial Accounting Foundations", None, "LinkedIn Learning", "ops", "2025-07", LL + "050ba2d8f70a2633acee2c65d782d4b4dfdb503516910c3ce6a30464afbd777a", None, None, None),
 ("Data Fundamentals", None, "IBM", "data", "2025-07", CR + "e8f19719-776a-4687-b844-7bce2758eecb", None, None, "badge"),
 ("Introduction to Data Science", "Introducción a la Ciencia de Datos", "IE University", "data", "2025-06", None, "OA-2025-0628001296627", "certificados/introduccion-ciencia-de-datos.pdf", None),
 ("Google: Artificial Intelligence and Productivity", None, "Google", "data", "2025-06", None, "OA-2025-0624001278542", None, None),
 ("Project management with Jira", "Gestión de proyectos con Jira", "LinkedIn Learning", "pm", "2025-06", LL + "5924d9c8bdc2583e0664523a1dc770c6446726e1429bb750f072e7c7d2a5989b", None, None, None),
 ("Working in a Digital World: Professional Skills", None, "IBM", "prod", "2025-06", CR + "b61aba8e-ad4b-45a9-aefc-69a7f2bf5ebf", None, None, "badge"),
 ("Atlantic Masters Experience", None, "UWC Atlantic College", "prod", "2025-06", None, None, None, None),
 ("Power BI", None, "Santander Open Academy", "data", "2024-08", None, "OA-2024-0819000507633", "certificados/power-bi.pdf", None),
 ("Explore Emerging Tech", None, "IBM", "data", "2024-08", CR + "cb5fa4d7-588a-404c-93de-69f75b5592be", None, None, "badge"),
 ("Online Digital Marketing course TalentUO (50 h)", "Curso online en Marketing Digital TalentUO (50 h)", "Universidad de Oviedo", "ops", "2024-06", None, None, None, None),
 ("C1 Advanced (CAE)", None, "Cambridge English", "lang", "2024-06", None, None, None, None),
 ("Ballet: Intermediate", None, "Royal Academy of Dance", "ballet", "2024-06", None, None, None, None),
 ("Professional Development", None, "IMFAHE", "prod", "2024-01", None, None, "certificados/professional-development-imfahe.pdf", None),
 ("Typing speed (249 wpm)", "Mecanografía (249 ppm)", "Cursomeca", "prod", "2023-10", None, None, "certificados/mecanografia-cursomeca.pdf", None),
 ("Ballet: Intermediate Foundation", None, "Royal Academy of Dance", "ballet", "2023-06", None, None, None, None),
 ("Ballet: Grade 8", None, "Royal Academy of Dance", "ballet", "2021-12", None, None, None, None),
 ("Ballet: Grade 7", None, "Royal Academy of Dance", "ballet", "2019-08", None, None, None, None),
 ("Ballet: Grade 6", None, "Royal Academy of Dance", "ballet", "2018-09", None, None, None, None),
 ("Ballet: Grade 1", None, "Royal Academy of Dance", "ballet", "2014-07", None, None, None, None),
]
MES = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
       "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
CERT_UI = {
 "es": {"h": "Certificaciones", "mono": "Las más recientes, arriba", "all": "Todas", "org_all": "Todos los emisores",
        "search": "Buscar un curso", "orgs_aria": "Emisor", "cats_aria": "Categorías",
        "count": "{a} de {b} · {c} con certificado enlazado", "none": "Ningún curso coincide con esos filtros.", "year_all": "Todos los años", "year_aria": "Año",
        "view": "Ver certificado", "pdf": "Ver certificado (PDF)", "badge": "Ver insignia", "id": "ID"},
 "en": {"h": "Certifications", "mono": "Most recent first", "all": "All", "org_all": "All issuers",
        "search": "Search a course", "orgs_aria": "Issuer", "cats_aria": "Categories",
        "count": "{a} of {b} · {c} with a linked certificate", "none": "No course matches those filters.", "year_all": "All years", "year_aria": "Year",
        "view": "View certificate", "pdf": "View certificate (PDF)", "badge": "View badge", "id": "ID"},
}

CONTACT = {
 "es": {"h": "Contacto", "mono": "Escríbeme",
        "p": "Estoy abierta a conversaciones sobre operaciones, logística y proyectos de mejora con datos.",
        "copy": "Copiar correo", "copied": "Correo copiado", "select": "Selecciona y copia", "mail": "Correo:",
        "nojs": "Activa JavaScript para ver el correo o escríbeme por LinkedIn.", "cv_t": "CV en PDF", "cv_es": "CV en español", "cv_en": "CV en inglés"},
 "en": {"h": "Contact", "mono": "Get in touch",
        "p": "I'm open to conversations about operations, logistics and data-driven improvement projects.",
        "copy": "Copy email", "copied": "Email copied", "select": "Select and copy", "mail": "Email:",
        "nojs": "Turn on JavaScript to see the email, or message me on LinkedIn.", "cv_t": "CV as PDF", "cv_es": "CV in Spanish", "cv_en": "CV in English"},
}

# ---------------------------------------------------------------- contenido: más allá del CV
# Cada bloque: (título, [párrafos], borrador o None). Los borradores solo se ven en la versión de prueba.
# Libros: (título, autor, por qué). Los que empiezan por "[" son ejemplos y no se publican.
MORE = {
 "es": {
  "h": "Más allá del CV", "mono": "Lo que no cabe en una página",
  "intro": "El CV dice qué he hecho. Aquí cuento algo de cómo lo hago y de lo que me gusta fuera del grado.",
  "photo_alt": "Candela Vázquez Fontal",
  "blocks": [
   ("Cómo trabajo",
    ["Enfoco los estudios, el trabajo y los idiomas como proyectos a largo plazo. Leo vorazmente, planifico obsesivamente y trabajo mejor cuando hay un problema real y datos reales de por medio."],
    "Falta un ejemplo concreto tuyo: un día en que planificar con detalle te salvó un trabajo o una entrega. Cuéntame cuál y lo redacto."),
   ("Ballet",
    ["Bailé ballet durante quince años, de enero de 2009 a junio de 2024, con el método de la Royal Academy of Dance, y me examiné hasta el nivel Intermediate. En 2021 di clases en la academia Paso a Dos, en Gijón. Quince años de ballet me enseñaron constancia y disciplina."],
    None),
   ("Salir de la zona de confort",
    ["En junio de 2025 participé en la Atlantic Masters Experience, en el UWC Atlantic College. Conocí a personas de entornos muy distintos al mío y me cuestioné cómo pensamos y cómo eso nos limita.",
     "Hicimos espeleología (caving) y escalada, algo que me aterraba. Gracias a ello establecimos vínculos mucho más fuertes."],
    None),
   ("De Gijón a Bilbao",
    ["Hice el Bachillerato Internacional en Gijón y dos años de carrera en Oviedo. Me cambié a Deusto esperando poder hacer la formación dual en cuarto y estar en una comunidad universitaria más activa. Allí participo en el Consulting Club, fui embajadora de UNIC y colaboré en el programa Big Buddy y Tandem con estudiantes internacionales.",
     "Este cambio también ha sido positivo fuera de lo académico y lo profesional: he tenido un crecimiento personal exponencial que no habría alcanzado de otra forma."],
    None),
   ("Lo que leo",
    ["Leo mucho, y por eso elegí la literatura para mi monografía del Bachillerato Internacional."],
    "Aquí van de tres a cinco libros con el motivo en una línea. Sustituye los de ejemplo por los tuyos: solo se publican los que no empiezan por corchete."),
   ("Ideas en construcción",
    ["Me gustaría construir un ERP sencillo y a medida para microempresas y autónomos, que casi nunca tienen herramientas pensadas para ellos: el software que existe suele ser caro y trae módulos que no necesitan. Todavía es una idea. Cuando tenga algo funcionando, lo enseñaré aquí.",
     "En la asignatura Oficina de Gestión de Proyectos de Deusto diseñé y planifiqué el anteproyecto de esa idea: una aplicación de escritorio que digitaliza el ciclo comercial de una microempresa, con inventario y stock automático, trazabilidad entre albaranes y facturas, facturación emitida y recibida con estado de cobro, exportación a PDF y un panel con alertas de vencimientos, para una sola persona sin perfil técnico. El documento recoge objetivos con criterios de aceptación medibles, diez hitos, requisitos, plan de documentación y de comunicaciones, matriz RACI, gestión de riesgos, planificación en MS Project y presupuesto. Está sin construir."],
    "He leído el anteproyecto (74 páginas) y redacté esto solo con lo que dice. Revisa que el nivel de detalle te convence y si quieres que cite alguna cifra, como los criterios de aceptación."),
  ],
  "books_t": "Libros que recomiendo",
  "books": [("[Título del libro 1]", "[Autor/a]", "[Una línea sobre por qué te marcó]"),
            ("[Título del libro 2]", "[Autor/a]", "[Una línea sobre por qué te marcó]"),
            ("[Título del libro 3]", "[Autor/a]", "[Una línea sobre por qué te marcó]")],
  "now_t": "Ahora",
  "now": ["Alemán: A1 → A2.",
          "SAP QM, en el proyecto de consultoría de IDOM.",
          "Consulting Club: divisiones de Operations and Supply Chain y de Digital, Tech & AI."],
  "now_draft": "Añade lo que estés leyendo o aprendiendo ahora si quieres.",
  "draft_label": "Borrador · solo en la versión de prueba",
 },
 "en": {
  "h": "Beyond the CV", "mono": "What doesn't fit on one page",
  "intro": "The CV says what I've done. Here I share a little of how I do it and what I enjoy outside my degree.",
  "photo_alt": "Candela Vázquez Fontal",
  "blocks": [
   ("How I work",
    ["I approach my studies, work and languages as long-term projects. I read voraciously, plan obsessively, and work best when there is a real problem and real data involved."],
    "A concrete example of yours is missing: a day when detailed planning saved a piece of work or a deadline. Tell me which and I'll write it."),
   ("Ballet",
    ["I danced ballet for fifteen years, from January 2009 to June 2024, following the Royal Academy of Dance method, and took exams up to Intermediate level. In 2021 I taught at the Paso a Dos academy in Gijón. Fifteen years of ballet taught me consistency and discipline."],
    None),
   ("Stepping out of my comfort zone",
    ["In June 2025 I took part in the Atlantic Masters Experience at UWC Atlantic College. I met people from very different backgrounds and questioned how we think and how that limits us.",
     "We went caving and climbing, which terrified me. Because of it we built much stronger bonds."],
    None),
   ("From Gijón to Bilbao",
    ["I did the International Baccalaureate in Gijón and two years of my degree in Oviedo. I moved to Deusto hoping to do the dual programme in my fourth year and to join a more active university community. There I take part in the Consulting Club, was a UNIC ambassador and helped with the Big Buddy and Tandem programme for international students.",
     "The move has also been positive beyond academics and work: I've had exponential personal growth that I couldn't have reached any other way."],
    None),
   ("What I read",
    ["I read a lot, which is why I chose literature for my International Baccalaureate extended essay."],
    "Three to five books with the reason in one line go here. Replace the examples with yours: only titles that don't start with a bracket are published."),
   ("Ideas in the making",
    ["I'd like to build a simple, made-to-measure ERP for micro-businesses and freelancers, who rarely have tools designed for them: the software that exists is usually expensive and full of modules they don't need. It is still an idea. When I have something working, I'll show it here.",
     "In the Project Management Office course at Deusto I designed and planned the draft project for that idea: a desktop application that digitises a micro-business's commercial cycle, with inventory and automatic stock, traceability between delivery notes and invoices, issued and received invoicing with payment status, PDF export and a dashboard with due-date alerts, for a single non-technical user. The document covers objectives with measurable acceptance criteria, ten milestones, requirements, documentation and communication plans, a RACI matrix, risk management, an MS Project schedule and a budget. It has not been built."],
    "I've read the 74-page draft project and wrote this using only what it says. Check the level of detail works for you and whether you want any figures quoted, such as the acceptance criteria."),
  ],
  "books_t": "Books I recommend",
  "books": [("[Book title 1]", "[Author]", "[One line on why it stayed with you]"),
            ("[Book title 2]", "[Author]", "[One line on why it stayed with you]"),
            ("[Book title 3]", "[Author]", "[One line on why it stayed with you]")],
  "now_t": "Right now",
  "now": ["German: A1 → A2.",
          "SAP QM, on the IDOM consulting project.",
          "Consulting Club: Operations and Supply Chain and Digital, Tech & AI divisions."],
  "now_draft": "Add what you're reading or learning right now if you like.",
  "draft_label": "Draft · preview only",
 },
}
LINKEDIN = "https://www.linkedin.com/in/candela-vazquez-fontal"
GITHUB = "https://github.com/candelavazquezfontal"
LI_ICON = '''<svg class="li" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'''
H1 = 'style="font-size:clamp(32px,6vw,54px);font-weight:800;letter-spacing:-.02em;line-height:1"'

# ---------------------------------------------------------------- plantillas
def slug(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def sectlinks(items):  # texto a la derecha del título, con cada parte enlazada a su sección
    return '<span class="mono sect">' + " · ".join(f'<a href="#{i}">{e(t)}</a>' for i, t in items) + "</span>"

PMO_LINK = {"Oficina de Gestión de Proyectos": ("more", "ideas-en-construccion"),
            "Project Management Office": ("more", "ideas-in-the-making")}

def ul_chips_link(items, lang):
    out = []
    for i in items:
        if i in PMO_LINK:
            k, anchor = PMO_LINK[i]
            out.append(f'<li><a href="{href(k, lang)}#{anchor}">{e(i)}</a></li>')
        else:
            out.append(f"<li>{e(i)}</li>")
    return '<ul class="chips">' + "".join(out) + "</ul>"

def ul_chips(items):
    return '<ul class="chips">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

def jsonld(lang):
    desc = {"es": "Estudiante de Ingeniería en Organización Industrial en la Universidad de Deusto y en prácticas de consultoría de transformación digital en IDOM.",
            "en": "Industrial Organisation Engineering student at the University of Deusto and digital transformation consulting intern at IDOM."}[lang]
    job = {"es": "Estudiante de Ingeniería en Organización Industrial", "en": "Industrial Organisation Engineering student"}[lang]
    know = {"es": ["Logística", "Operaciones", "Optimización", "Gestión de costes", "Análisis de datos"],
            "en": ["Logistics", "Operations", "Optimisation", "Cost management", "Data analysis"]}[lang]
    d = {"@context": "https://schema.org", "@type": "ProfilePage", "inLanguage": lang,
         "mainEntity": {"@type": "Person", "name": "Candela Vázquez Fontal", "givenName": "Candela",
                        "familyName": "Vázquez Fontal", "url": url("home", lang), "image": BASE + "/og-image.png",
                        "jobTitle": job, "description": desc,
                        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad de Deusto"},
                                     {"@type": "CollegeOrUniversity", "name": "Universidad de Oviedo"}],
                        "worksFor": {"@type": "Organization", "name": "IDOM"},
                        "knowsLanguage": ["es", "en", "de"], "knowsAbout": know,
                        "sameAs": [LINKEDIN, GITHUB]}}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))

def head(lang, key):
    u = UI[lang]
    t, d = u["titles"][key], u["descs"][key]
    od = u["og_desc"] if key == "home" else d
    parts = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{e(t)}</title>",
        f'<meta name="description" content="{e(d)}">',
        *([] if key == "home" else ['<meta name="robots" content="noindex,follow">']),
        '<meta name="author" content="Candela Vázquez Fontal">',
        f'<link rel="canonical" href="{url(key, lang)}">',
        f'<link rel="alternate" hreflang="es" href="{url(key, "es")}">',
        f'<link rel="alternate" hreflang="en" href="{url(key, "en")}">',
        f'<link rel="alternate" hreflang="x-default" href="{url(key, "es")}">',
        f'<meta property="og:type" content="{"profile" if key == "home" else "website"}">',
        f'<meta property="og:locale" content="{u["locale"]}">',
        f'<meta property="og:locale:alternate" content="{u["other_locale"]}">',
        f'<meta property="og:site_name" content="{e(u["site_name"])}">',
        f'<meta property="og:title" content="{e(t)}">',
        f'<meta property="og:description" content="{e(od)}">',
        f'<meta property="og:url" content="{url(key, lang)}">',
        f'<meta property="og:image" content="{BASE}/og-image.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(u["og_alt"])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(t)}">',
        f'<meta name="twitter:description" content="{e(od)}">',
        f'<meta name="twitter:image" content="{BASE}/og-image.png">',
    ]
    if key == "home":
        parts += ['<meta property="profile:first_name" content="Candela">',
                  '<meta property="profile:last_name" content="Vázquez Fontal">',
                  f'<script type="application/ld+json">{jsonld(lang)}</script>']
    parts += [
        '<style>html{-webkit-text-size-adjust:100%}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>',
    ]
    if PREVIEW:
        parts += ['<link rel="preconnect" href="https://fonts.googleapis.com">',
                  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
                  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">']
    else:
        parts += [f'<link rel="preload" href="/fonts/BricolageGrotesque-800-normal-latin.woff2" as="font" type="font/woff2" crossorigin>',
                  '<link rel="stylesheet" href="/fonts/fonts.css">']
    parts += [
        f"<style>\n{CSS}\n</style>",
    ]
    return "\n".join(parts)

def nav(lang, key):
    u = UI[lang]
    cur = ' aria-current="page"'
    items = "".join(
        f'<li><a href="{href(k, lang)}"{cur if k == key else ""}>{e(u["nav"][k])}</a></li>' for k in ORDER)
    sw = (f'<div class="langsw" role="group" aria-label="{u["lang_aria"]}">'
          + "".join(
              (f'<span aria-current="true" lang="{l}">{UI[l]["label"]}</span>' if l == lang else
               f'<a href="{href(key, l)}" hreflang="{l}" lang="{l}" data-setlang="{l}">{UI[l]["label"]}</a>')
              for l in ("es", "en")) + "</div>")
    return (f'<nav aria-label="{u["nav_aria"]}"><div class="wrap">'
            f'<a href="{href("home", lang)}" style="text-decoration:none;color:inherit"><b>{e(u["brand"])}</b></a>'
            f'<div class="navr"><ul>{items}</ul>{sw}</div></div></nav>')

def footer(lang):
    return (f'<div class="wrap"><footer><span>{e(UI[lang]["footer"])}</span>'
            f'<a class="lilink" href="{LINKEDIN}" target="_blank" rel="noopener">{LI_ICON}LinkedIn</a></footer></div>')

def page(lang, key, body, script=""):
    remember = ('try{document.querySelectorAll("[data-setlang]").forEach(function(a){'
                'a.addEventListener("click",function(){localStorage.setItem("lang",a.dataset.setlang)})})}catch(_){}\n')
    return (f'<!doctype html>\n<html lang="{lang}">\n<head>\n{head(lang, key)}\n</head>\n<body>\n'
            f'{nav(lang, key)}\n<main class="wrap">\n{body}\n</main>\n{footer(lang)}\n'
            f'<script>\n{remember}{script}</script>\n</body>\n</html>\n')

# ---------------------------------------------------------------- cuerpos
def body_home(lang):
    h = HOME[lang]
    dl = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in h["dl"])
    about = "".join(f"<p>{e(p)}</p>" for p in h["about"])
    doors = ""
    for k, mono, big, go in h["doors"]:
        n = len(PROJECTS) if k == "proj" else len(CERTS)
        doors += (f'<a href="{href(k, lang)}"><span class="mono">{e(mono)}</span>'
                  f'<b>{e(big.format(n=n))}</b><span class="go">{e(go)}</span></a>')
    return f'''<section class="view" id="v-inicio">
  <div class="hero">
    <div>
      <p class="mono">{e(h["kicker"])}</p>
      <h1 style="margin-top:14px">Candela<br>Vázquez <span>Fontal</span></h1>
      <p class="lead">{e(h["lead"])}</p>
      <div class="cta">
        <a class="btn" href="{href("proj", lang)}">{e(h["cta1"])}</a>
        <a class="btn ghost" href="{href("cert", lang)}">{e(h["cta2"])}</a>
        <a class="btn ghost" href="{asset(CV_FILE[lang])}">{e(h["cta3"])}</a>
      </div>
    </div>
    <aside class="label" aria-label="{e(h["label_aria"])}">
      <span class="mono">{e(h["label_title"])}</span>
      <dl>{dl}</dl>
    </aside>
  </div>

  <div class="about" id="sobre-mi">
    <div>{about}</div>
    <div class="side">
      <div><p class="mono">{e(h["areas_t"])}</p>{ul_chips(h["areas"])}</div>
      <div><p class="mono">{e(h["tools_t"])}</p>{ul_chips(h["tools"])}</div>
    </div>
  </div>

  <div class="seek" id="lo-que-busco">
    <p class="mono">{e(h["seek_t"])}</p>
    <p>{e(h["seek"])}</p>
    {ul_chips(h["seek_chips"])}
  </div>

  <div class="doors" id="explorar">{doors}</div>
</section>'''

def body_path(lang):
    c = PATH[lang]
    out = [f'<section class="view" id="v-trayectoria">\n  <div class="view-head"><h1 {H1}>{e(c["h"])}</h1>{sectlinks([(slug(t), t) for t, _ in c["sections"]])}</div>']
    for title, rows in c["sections"]:
        out.append(f'  <h2 class="sub" id="{slug(title)}">{e(title)}</h2>\n  <ol class="tl">')
        for date, t, org, desc, pts, chips in rows:
            inner = f'<h4>{e(t)}</h4><span class="org">{e(org)}</span>'
            if desc: inner += f"<p>{e(desc)}</p>"
            if pts: inner += '<ul class="pts">' + "".join(f"<li>{e(p)}</li>" for p in pts) + "</ul>"
            if chips: inner += ul_chips_link(chips, lang)
            out.append(f'    <li><span class="mono">{e(date)}</span><div>{inner}</div></li>')
        out.append("  </ol>")
    out.append("</section>")
    return "\n".join(out)

def body_proj(lang):
    ui = PROJ_UI[lang]
    area_name = {k: v[lang] for k, v in AREAS}
    used = [(k, v[lang]) for k, v in AREAS if any(k in p["areas"] for p in PROJECTS)]
    chips = f'<button type="button" class="chip" data-f="all" aria-pressed="true">{e(ui["all"])}<span>{len(PROJECTS)}</span></button>'
    for k, n in used:
        cnt = sum(1 for p in PROJECTS if k in p["areas"])
        chips += f'<button type="button" class="chip" data-f="{k}" aria-pressed="false">{e(n)}<span>{cnt}</span></button>'
    items = ""
    for p in PROJECTS:
        c = p[lang]
        blk = ""
        if p["honor"]: blk += f'<div class="wide"><span class="honor">{e(ui["honor"])}</span></div>'
        blk += f'<div class="wide"><h4>{e(ui["problem"])}</h4><p>{e(c["ctx"])}</p></div>'
        blk += f'<div class="wide"><h4>{e(ui["done"])}</h4><p>{e(c["how"])}</p></div>'
        blk += f'<div class="wide"><h4>{e(ui["role"])}</h4><p>{e(c["role"])}</p></div>'
        blk += f'<div class="wide"><h4>{e(ui["res"])}</h4><ul>' + "".join(f"<li>{e(x)}</li>" for x in c["res"]) + "</ul></div>"
        blk += f'<div><h4>{e(ui["tools"])}</h4><div class="tags">' + "".join(f"<span>{e(x)}</span>" for x in c["tools"]) + "</div></div>"
        if p.get("link"):
            blk += f'<div class="wide"><p><a href="{e(p["link"])}" target="_blank" rel="noopener">{e(c["link"])} ↗</a></p></div>'
        if p["areas"]:
            blk += f'<div><h4>{e(ui["areas"])}</h4><div class="tags">' + "".join(f"<span>{e(area_name[a])}</span>" for a in p["areas"]) + "</div></div>"
        items += (f'<details class="proj" id="{p["id"].lower()}" data-areas="{" ".join(p["areas"])}"><summary>'
                  f'<span class="mono">{p["id"]}</span><div><h2 style="font-size:20px;font-weight:700">{e(c["t"])}</h2>'
                  f'<div class="meta">{e(c["meta"])}</div></div><span class="plus" aria-hidden="true">+</span></summary>'
                  f'<div class="proj-body"><span></span><div class="in">{blk}</div></div></details>\n')
    body = f'''<section class="view" id="v-proyectos">
  <div class="view-head"><h1 {H1}>{e(ui["h"])}</h1>{sectlinks([(p["id"].lower(), p["short"][lang]) for p in PROJECTS])}</div>
  <div class="tools" id="proj-area" role="group" aria-label="{e(ui["area_aria"])}"><span class="mono lab">{e(ui["area"])}</span>{chips}</div>
  <span class="mono count" id="proj-count" aria-live="polite"></span>
  <div id="proj-list">
{items}  </div>
</section>'''
    js = '''(function(){
  var T=%s,N=%d;
  var chips=document.querySelectorAll("#proj-area .chip"),items=document.querySelectorAll("details.proj"),cnt=document.getElementById("proj-count");
  function apply(f){var n=0;items.forEach(function(d){var ok=f==="all"||(d.dataset.areas||"").split(" ").indexOf(f)>-1;d.hidden=!ok;if(ok)n++});
    chips.forEach(function(c){c.setAttribute("aria-pressed",c.dataset.f===f)});cnt.textContent=T.replace("{a}",n).replace("{b}",N)}
  chips.forEach(function(c){c.onclick=function(){apply(c.dataset.f)}});apply("all");
  function openHash(){if(location.hash){var t=document.querySelector(location.hash);if(t&&t.tagName==="DETAILS"){t.hidden=false;t.open=true;t.scrollIntoView()}}}
  window.addEventListener("hashchange",openHash);openHash();
})();
''' % (json.dumps(ui["count"]), len(PROJECTS))
    return body, js

def fecha(d, lang):
    y, m = d.split("-")
    return MES[lang][int(m) - 1] + " " + y

def body_cert(lang):
    ui = CERT_UI[lang]
    catname = {k: v[lang] for k, v in CATS}
    rows = sorted(enumerate(CERTS), key=lambda x: (-int(x[1][4].replace("-", "")), x[0]))
    cat_chips = f'<button type="button" class="chip" data-f="all" aria-pressed="true">{e(ui["all"])}<span>{len(CERTS)}</span></button>'
    for k, v in CATS:
        cnt = sum(1 for c in CERTS if c[3] == k)
        cat_chips += f'<button type="button" class="chip" data-f="{k}" aria-pressed="false">{e(v[lang])}<span>{cnt}</span></button>'
    orgs = sorted({c[2] for c in CERTS}, key=lambda s: s.lower())
    org_opts = f'<option value="">{e(ui["org_all"])}</option>' + "".join(f"<option>{e(o)}</option>" for o in orgs)
    years = sorted({c[4][:4] for c in CERTS}, reverse=True)
    year_opts = f'<option value="">{e(ui["year_all"])}</option>' + "".join(f"<option>{y}</option>" for y in years)
    out = ""
    for _, c in rows:
        title = c[0] if (lang == "en" or not c[1]) else c[1]
        if c[5]:
            lab = ui["badge"] if c[8] == "badge" else ui["view"]
            go = f'<a href="{e(c[5])}" target="_blank" rel="noopener">{e(lab)}</a>'
        elif c[7]:
            go = f'<a href="{e(asset(c[7]))}" target="_blank" rel="noopener">{e(ui["pdf"])}</a>'
        elif c[6]:
            go = f'<span class="id">{e(ui["id"])} {e(c[6])}</span>'
        else:
            go = ""
        q = (c[0] + " " + (c[1] or "") + " " + c[2]).lower()
        out += (f'<div class="row" data-cat="{c[3]}" data-org="{e(c[2])}" data-year="{c[4][:4]}" data-q="{e(q)}">'
                f'<span class="mono">{fecha(c[4], lang)}</span><div><h3>{e(title)}</h3>'
                f'<div class="meta">{e(c[2])} · {e(catname[c[3]])}</div></div><span class="go">{go}</span></div>\n')
    body = f'''<section class="view" id="v-certificaciones">
  <div class="view-head"><h1 {H1}>{e(ui["h"])}</h1><span class="mono">{e(ui["mono"])}</span></div>
  <div class="tools" id="cert-filters" role="group" aria-label="{e(ui["cats_aria"])}">{cat_chips}</div>
  <div class="tools">
    <select class="field" id="cert-org" aria-label="{e(ui["orgs_aria"])}">{org_opts}</select>
    <select class="field" id="cert-year" aria-label="{e(ui["year_aria"])}">{year_opts}</select>
    <input class="field" id="cert-q" type="search" placeholder="{e(ui["search"])}" aria-label="{e(ui["search"])}">
  </div>
  <span class="mono count" id="cert-count" aria-live="polite"></span>
  <div class="rows" id="cert-rows">
{out}  </div>
  <p class="empty" id="cert-none" hidden>{e(ui["none"])}</p>
</section>'''
    js = '''(function(){
  var T=%s,N=%d;
  var rows=[].slice.call(document.querySelectorAll("#cert-rows .row")),chips=document.querySelectorAll("#cert-filters .chip");
  var org=document.getElementById("cert-org"),yr=document.getElementById("cert-year"),q=document.getElementById("cert-q"),cnt=document.getElementById("cert-count"),none=document.getElementById("cert-none");
  var cat="all";
  function norm(s){return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"")}
  function apply(){var qq=norm(q.value.trim()),o=org.value,n=0,l=0;
    rows.forEach(function(r){var ok=(cat==="all"||r.dataset.cat===cat)&&(!o||r.dataset.org===o)&&(!yr.value||r.dataset.year===yr.value)&&(!qq||norm(r.dataset.q).indexOf(qq)>-1);
      r.hidden=!ok;if(ok){n++;if(r.querySelector("a"))l++}});
    none.hidden=n>0;cnt.textContent=T.replace("{a}",n).replace("{b}",N).replace("{c}",l)}
  chips.forEach(function(c){c.onclick=function(){cat=c.dataset.f;chips.forEach(function(x){x.setAttribute("aria-pressed",x===c)});apply()}});
  org.onchange=apply;yr.onchange=apply;q.oninput=apply;apply();
})();
''' % (json.dumps(ui["count"]), len(CERTS))
    return body, js


def body_more(lang):
    c = MORE[lang]
    def draft(t):
        if not (PREVIEW and t): return ""
        return f'<p class="draft"><b>{e(c["draft_label"])}</b>{e(t)}</p>'
    rows = ""
    for title, paras, dr in c["blocks"]:
        if title in ("Lo que leo", "What I read") and not [b for b in c["books"] if not b[0].startswith("[")]:
            continue
        inner = "".join(f"<p>{e(p)}</p>" for p in paras) + draft(dr)
        if title in ("Lo que leo", "What I read"):
            books = [b for b in c["books"] if PREVIEW or not b[0].startswith("[")]
            if books:
                inner += f'<h5 class="mini">{e(c["books_t"])}</h5><ul class="books">' + "".join(
                    f'<li><b>{e(t)}</b> <span>{e(a)}</span><br>{e(w)}</li>' for t, a, w in books) + "</ul>"
        rows += f'<li id="{slug(title)}"><span class="mono">{e(title)}</span><div>{inner}</div></li>\n'
    return f'''<section class="view" id="v-mas-alla">
  <div class="view-head"><h1 {H1}>{e(c["h"])}</h1>{sectlinks([(slug(b[0]), b[0]) for b in c["blocks"] if not (b[0] in ("Lo que leo", "What I read") and not [x for x in c["books"] if not x[0].startswith("[")])])}</div>
  <div class="beyond">
    <img src="{asset("img/candela-2.jpg")}" alt="{e(c["photo_alt"])}" width="140" height="140">
    <p class="lead2">{e(c["intro"])}</p>
  </div>
  <ol class="tl">
{rows}  </ol>
</section>'''

def body_contact(lang):
    ui = CONTACT[lang]
    body = f'''<section class="view" id="v-contacto">
  <div class="view-head"><h1 {H1}>{e(ui["h"])}</h1>{sectlinks([("escribeme", ui["mono"]), ("cv", ui["cv_t"])])}</div>
  <p id="escribeme" style="margin:0 0 18px;max-width:56ch">{e(ui["p"])}</p>
  <div class="cta" style="margin-top:0">
    <button class="btn" id="copy-mail" type="button">{e(ui["copy"])}</button>
    <a class="btn ghost lilink" href="{LINKEDIN}" target="_blank" rel="noopener">{LI_ICON}LinkedIn</a>
  </div>
  <p style="margin:14px 0 0">{e(ui["mail"])} <span id="mail" data-e="{MAIL_ENC}" style="user-select:all"></span><noscript>{e(ui["nojs"])}</noscript></p>
  <h2 class="sub" id="cv" style="font-size:20px;margin:34px 0 10px">{e(ui["cv_t"])}</h2>
  <div class="cta" style="margin-top:0">
    <a class="btn ghost" href="{asset(CV_FILE["es"])}" target="_blank" rel="noopener">{e(ui["cv_es"])}</a>
    <a class="btn ghost" href="{asset(CV_FILE["en"])}" target="_blank" rel="noopener">{e(ui["cv_en"])}</a>
  </div>
</section>'''
    js = '''(function(){var m=document.getElementById("mail");m.textContent=atob(m.dataset.e).split("").reverse().join("")})();
document.getElementById("copy-mail").onclick=async function(ev){
  var b=ev.currentTarget,txt=document.getElementById("mail").textContent;
  try{await navigator.clipboard.writeText(txt);b.textContent=%s}
  catch(_){var r=document.createRange();r.selectNodeContents(document.getElementById("mail"));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent=%s}
  setTimeout(function(){b.textContent=%s},2200);
};
''' % (json.dumps(ui["copied"]), json.dumps(ui["select"]), json.dumps(ui["copy"]))
    return body, js

# enlaces antiguos con # (versión de una sola página) -> páginas nuevas; recuerda el idioma elegido
LEGACY = '''(function(){var m={"#trayectoria":"/trayectoria/","#proyectos":"/proyectos/","#certificaciones":"/certificaciones/","#contacto":"/contacto/"};
if(m[location.hash]){location.replace(m[location.hash]);return}
try{if(!location.hash&&!document.referrer.startsWith(location.origin)&&localStorage.getItem("lang")==="en")location.replace("/en/")}catch(_){}})();
'''

# ---------------------------------------------------------------- escritura
def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("escrito", path)

def build():
    for lang in ("es", "en"):
        for key in ORDER:
            rel = PAGES[key][0 if lang == "es" else 1] + "index.html"
            CUR["path"] = os.path.dirname(rel)
            script = ""
            if key == "home":
                body = body_home(lang)
                script = LEGACY if (lang == "es" and not PREVIEW) else ""
            elif key == "more": body = body_more(lang)
            elif key == "path": body = body_path(lang)
            elif key == "proj": body, script = body_proj(lang)
            elif key == "cert": body, script = body_cert(lang)
            else: body, script = body_contact(lang)
            write(rel, page(lang, key, body, script))
    urls = []
    for key in ORDER:
        if key != "home": continue   # solo la portada se indexa; las secciones llevan noindex
        for lang in ("es", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(key, l)}"/>' for l in ("es", "en"))
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(key, "es")}"/>'
            pr = "1.0" if key == "home" else "0.8"
            urls.append(f"  <url><loc>{url(key, lang)}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority>{alts}</url>")
    if PREVIEW: return
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")

if __name__ == "__main__":
    build()
