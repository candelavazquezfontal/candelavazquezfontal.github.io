# Web personal de Candela Vázquez Fontal

Sitio estático publicado con GitHub Pages, en español (raíz) e inglés (`/en/`).

- `index.html`, `trayectoria/`, `proyectos/`, `certificaciones/`, `contacto/`: versión en español.
- `en/`: versión en inglés (`experience/`, `projects/`, `certifications/`, `contact/`).
- `certificados/`: certificados en PDF enlazados desde la sección de certificaciones.
- `sitemap.xml`, `robots.txt`, `og-image.png`: indexación y vista previa al compartir el enlace.
- `_src/`: código que genera todas las páginas (GitHub Pages no lo publica).

## Cómo actualizarla

Los textos y los datos (certificaciones, proyectos, trayectoria) están en `_src/build.py`, en español e inglés.
Tras editarlos, desde la raíz del repositorio: `python3 _src/build.py`. Eso regenera todas las páginas y el sitemap.
Después, "Commit to main" y "Push origin" en GitHub Desktop.
