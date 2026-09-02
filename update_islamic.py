from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

new_section = r'''<section id="islamic" class="section">
<div class="container">

<div class="title">
<h2>🕌 Islamic</h2>
<span>🌙</span>
</div>

<div class="menu-grid">

<div class="menu-card" onclick="showIslamic('prayer')">
<div class="icon">🕐</div>
<h3>নামাজের সময়সূচি</h3>
<p>আজকের ৫ ওয়াক্ত</p>
</div>

<div class="menu-card" onclick="showIslamic('names')">
<div class="icon">99️⃣</div>
<h3>আল্লাহর ৯৯ নাম</h3>
<p>সম্পূর্ণ তালিকা</p>
</div>

<div class="menu-card" onclick="showIslamic('ayat')">
<div class="icon">📜</div>
<h3>আয়াতুল কুরসি</h3>
<p>আরবি ও অর্থ</p>
</div>

<div class="menu-card" onclick="showIslamic('namaz')">
<div class="icon">🧎</div>
<h3>নামাজ শেখা</h3>
<p>ধাপে ধাপে</p>
</div>

<div class="menu-card" onclick="showIslamic('surah')">
<div class="icon">📖</div>
<h3>সূরা সমূহ</h3>
<p>১১৪টি সূরা</p>
</div>

<div class="menu-card" onclick="showIslamic('dua')">
<div class="icon">📿</div>
<h3>যিকির ও দোয়া</h3>
<p>প্রয়োজনীয় দোয়া</p>
</div>

</div>

<div id="islamicContent"></div>

</div>
</section>'''

pattern = r'<section id="islamic" class="section">.*?</section>'
new_html, count = re.subn(pattern, new_section, html, count=1, flags=re.S)

if count != 1:
    print("ERROR: Islamic section পাওয়া যায়নি। index.html পরিবর্তন করা হয়নি।")
    raise SystemExit(1)

p.write_text(new_html, encoding="utf-8")
print("Islamic section updated successfully.")
