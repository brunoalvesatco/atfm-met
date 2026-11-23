"""Gera o index.html do portal (raiz do repositório) a partir de src/src.html.

Tailwind compilado e embutido, ícones Lucide inline, logos e QR Codes em data URL.
Uso (dentro de portal-src/):  npm install  &&  pip install qrcode pillow  &&  python3 build.py
Para atualizar ações, reuniões ou documentos, edite os blocos de dados no <script> de src/src.html.
"""
import base64, io, json, re, subprocess, sys
from pathlib import Path
import qrcode, qrcode.image.svg
from PIL import Image

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC, BUILD = ROOT / 'src', ROOT / '.build'
ICONS = ROOT / 'node_modules/lucide-static/icons'
BUILD.mkdir(exist_ok=True)
(REPO / 'qr').mkdir(exist_ok=True)

html = (SRC / 'src.html').read_text(encoding='utf-8')

# 1) CSS (Tailwind 3)
subprocess.run(['npx', 'tailwindcss', '-c', 'tailwind.config.js', '-i', 'input.css', '-o', '.build/app.css', '--minify'],
               cwd=ROOT, check=True, capture_output=True)
css = (BUILD / 'app.css').read_text(encoding='utf-8')

# 2) Ícones Lucide
def inner(name):
    svg = (ICONS / f'{name}.svg').read_text(encoding='utf-8')
    body = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
    return re.sub(r'\s*\n\s*', '', body).strip()

def svg(name, cls):
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner(name)}</svg>')

html = re.sub(r'\{\{ic:([a-z0-9-]+):"([^"]*)"\}\}', lambda m: svg(m.group(1), m.group(2)), html)
script = html[html.index('<script>\n/*'):]
names = sorted({t for t in re.findall(r'"([a-z0-9]+(?:-[a-z0-9]+)*)"', script) if (ICONS / f'{t}.svg').exists()})
html = html.replace('{{ICONS}}', json.dumps({n: inner(n) for n in names}, ensure_ascii=False))

# 3) Logos e favicon
def png64(path, size):
    im = Image.open(path).convert('RGBA'); im.thumbnail((size, size), Image.LANCZOS)
    bio = io.BytesIO(); im.save(bio, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(bio.getvalue()).decode()

html = (html.replace('{{LOGO_L}}', png64(SRC / 'img0_light.png', 144))
            .replace('{{LOGO_D}}', png64(SRC / 'img0.png', 144))
            .replace('{{FAV}}', png64(SRC / 'img0_light.png', 64)))

# 4) QR Codes (credenciamento e portal)
def qr_pair(url, file):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=1)
    q.add_data(url); q.make(fit=True)
    s = q.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string(encoding='unicode')
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'width="[^"]*" height="[^"]*"', '', s, count=1)
    q2 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=2)
    q2.add_data(url); q2.make(fit=True)
    img = q2.make_image(fill_color='#0f172a', back_color='white')
    img.save(REPO / 'qr' / file)
    bio = io.BytesIO(); img.save(bio, 'PNG')
    return {'url': url, 'svg': s, 'png': 'data:image/png;base64,' + base64.b64encode(bio.getvalue()).decode(), 'file': file}

QR = {'presenca': qr_pair('https://atfmmet.com.br/presenca.html', 'credenciamento.png'),
      'portal': qr_pair('https://atfmmet.com.br/', 'portal.png')}
QR['presenca']['file'] = 'QRCode_credenciamento_atfmmet.png'   # nome do arquivo baixado pelo botão do modal
QR['portal']['file'] = 'QRCode_portal_atfmmet.png'
html = html.replace('{{QRDATA}}', json.dumps(QR, ensure_ascii=False))

html = html.replace('{{CSS}}', css)
left = re.findall(r'\{\{[A-Za-z_:-]+', html)
if left:
    sys.exit(f'Placeholders sem substituir: {left[:5]}')
(REPO / 'index.html').write_text(html, encoding='utf-8')
print('index.html', len(html), 'bytes ·', len(names), 'ícones runtime · css', len(css))
