import os
import re
import urllib.request

CSS_URL = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "fonts")
os.makedirs(FONTS_DIR, exist_ok=True)

req = urllib.request.Request(CSS_URL, headers={'User-Agent': USER_AGENT})
with urllib.request.urlopen(req) as response:
    css_content = response.read().decode('utf-8')

urls = re.findall(r'url\((https://[^)]+)\)', css_content)
for i, url in enumerate(urls):
    filename = url.split('/')[-1]
    filepath = os.path.join(FONTS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
    css_content = css_content.replace(url, f"../fonts/{filename}")

css_path = os.path.join(FONTS_DIR, "fonts.css")
with open(css_path, "w") as f:
    f.write(css_content)
print(f"Fonts CSS saved to {css_path}")
