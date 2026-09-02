from pathlib import Path
import re

file = Path("index.html")
html = file.read_text(encoding="utf-8")

# -----------------------------
# Islamic HTML section
# -----------------------------
section = r'''
<section id="islamic" class="section">
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
  <p>সম্পূর্ণ ৯৯টি নাম</p>
</div>

<div class="menu-card" onclick="showIslamic('ayat')">
  <div class="icon">📜</div>
  <h3>আয়াতুল কুরসি</h3>
  <p>আরবি ও অনুবাদ</p>
</div>

<div class="menu-card" onclick="showIslamic('surah')">
  <div class="icon">📖</div>
  <h3>সূরা সমূহ</h3>
  <p>১১৪টি সূরা</p>
</div>

<div class="menu-card" onclick="showIslamic('namaz')">
  <div class="icon">🧎</div>
  <h3>নামাজ শেখা</h3>
  <p>ধাপে ধাপে</p>
</div>

<div class="menu-card" onclick="showIslamic('dua')">
  <div class="icon">📿</div>
  <h3>যিকির ও দোয়া</h3>
  <p>প্রয়োজনীয় যিকির</p>
</div>

</div>

<div id="islamicContent"></div>

</div>
</section>
'''

# Replace Islamic section only
pattern = r'<section id="islamic" class="section">.*?</section>'
html, count = re.subn(pattern, section, html, count=1, flags=re.S)

if count != 1:
    print("ERROR: Islamic section পাওয়া যায়নি")
    raise SystemExit(1)

# -----------------------------
# JavaScript
# -----------------------------
script = r'''
<script id="taskmoon-islamic">

const ALLAH_NAMES = [
"আর-রহমান — পরম দয়ালু",
"আর-রহীম — পরম করুণাময়",
"আল-মালিক — সর্বময় অধিপতি",
"আল-কুদ্দুস — অতি পবিত্র",
"আস-সালাম — শান্তির উৎস",
"আল-মু'মিন — নিরাপত্তাদানকারী",
"আল-মুহাইমিন — রক্ষাকর্তা",
"আল-আজীয — পরাক্রমশালী",
"আল-জাব্বার — মহাপরাক্রমশালী",
"আল-মুতাকাব্বির — মহিমান্বিত",
"আল-খালিক — সৃষ্টিকর্তা",
"আল-বারী — সৃষ্টিকারী",
"আল-মুসাওয়ির — আকৃতিদানকারী",
"আল-গাফফার — অতিশয় ক্ষমাশীল",
"আল-কাহহার — পরাক্রমশালী",
"আল-ওয়াহহাব — মহাদাতা",
"আর-রাযযাক — রিযিকদাতা",
"আল-ফাত্তাহ — বিজয়দাতা",
"আল-আলীম — সর্বজ্ঞ",
"আল-কাবিদ — সংকোচনকারী",
"আল-বাসিত — প্রশস্তকারী",
"আল-খাফিদ — অবনতকারী",
"আর-রাফি — উন্নতকারী",
"আল-মু'ইয — সম্মানদাতা",
"আল-মুযিল — অপমানকারী",
"আস-সামী — সর্বশ্রোতা",
"আল-বাসীর — সর্বদ্রষ্টা",
"আল-হাকাম — বিচারক",
"আল-আদল — ন্যায়বিচারক",
"আল-লতীফ — সূক্ষ্মদর্শী",
"আল-খবীর — সর্বজ্ঞাত",
"আল-হালীম — পরম সহনশীল",
"আল-আযীম — মহান",
"আল-গফুর — ক্ষমাশীল",
"আশ-শাকুর — কৃতজ্ঞতার প্রতিদানদাতা",
"আল-আলী — সর্বোচ্চ",
"আল-কাবীর — সর্বশ্রেষ্ঠ",
"আল-হাফীয — সংরক্ষণকারী",
"আল-মুকীত — রিযিকদাতা",
"আল-হাসীব — হিসাব গ্রহণকারী",
"আল-জালীল — মহিমান্বিত",
"আল-কারীম — পরম দাতা",
"আর-রকীব — পর্যবেক্ষক",
"আল-মুজীব — দোয়া কবুলকারী",
"আل-ওয়াসি — সর্বব্যাপী",
"আল-হাকীম — প্রজ্ঞাময়",
"আল-ওয়াদুদ — প্রেমময়",
"আল-মাজীদ — মহিমান্বিত",
"আল-বাসিত — প্রশস্তকারী",
"আশ-শাহীদ — সাক্ষী",
"আল-হক — পরম সত্য",
"আল-ওয়াকীল — কর্মবিধায়ক",
"আল-কাওয়ী — শক্তিশালী",
"আল-মাতীন — সুদৃঢ়",
"আল-ওয়ালীয় — অভিভাবক",
"আল-হামীদ — প্রশংসিত",
"আল-মুহসী — হিসাবকারী",
"আল-মুবদি — সূচনাকারী",
"আল-মুঈদ — পুনরায় সৃষ্টিকারী",
"আল-মুহয়ী — জীবনদাতা",
"আল-মুমীত — মৃত্যুদাতা",
"আল-হাই — চিরঞ্জীব",
"আল-কাইয়ূম — সবকিছুর ধারক",
"আল-ওয়াজিদ — সর্বপ্রাপ্ত",
"আল-মাজিদ — মহিমান্বিত",
"আল-ওয়াহিদ — এক",
"আল-আহাদ — অদ্বিতীয়",
"আস-সামাদ — অমুখাপেক্ষী",
"আল-কাদির — সর্বশক্তিমান",
"আল-মুকতাদির — সর্বক্ষমতাবান",
"আল-মুকাদ্দিম — অগ্রসরকারী",
"আল-মুয়াখখির — পিছিয়ে দানকারী",
"আল-আউয়াল — প্রথম",
"আল-আখির — শেষ",
"আয-যাহির — প্রকাশ্য",
"আল-বাতিন — অপ্রকাশ্য",
"আল-ওয়ালী — অভিভাবক",
"আল-মুতাআলী — সর্বোচ্চ",
"আল-বার — কল্যাণময়",
"আত-তাওয়াব — তওবা কবুলকারী",
"আল-মুনতাকিম — প্রতিশোধ গ্রহণকারী",
"আল-আফুও — ক্ষমাকারী",
"আর-রউফ — পরম স্নেহশীল",
"মালিকুল-মুলক — রাজ্যের মালিক",
"যুল-জালালি ওয়াল-ইকরাম — মহিমা ও সম্মানের অধিকারী",
"আল-মুকসিত — ন্যায়পরায়ণ",
"আল-জামি — একত্রকারী",
"আল-গনী — অমুখাপেক্ষী",
"আল-মুগনী — অভাবমুক্তকারী",
"আল-মানি — প্রতিরোধকারী",
"আদ-দার — ক্ষতির ক্ষমতাধারী",
"আন-নাফি — উপকারকারী",
"আন-নূর — আলো",
"আল-হাদী — পথপ্রদর্শক",
"আল-বাদী — অনুপম স্রষ্টা",
"আল-বাকী — চিরস্থায়ী",
"আল-ওয়ারিস — উত্তরাধিকারী",
"আর-রশীদ — সঠিক পথপ্রদর্শক",
"আস-সবুর — পরম ধৈর্যশীল"
];

function islamicBox(){
  return document.getElementById("islamicContent");
}

async function showIslamic(type){

  const box = islamicBox();

  if(!box) return;

  if(type === "prayer"){

    box.innerHTML = `
      <div class="title">
        <h2>🕐 নামাজের সময়সূচি</h2>
      </div>

      <div class="card">
        <p>📍 আপনার location permission দিন।</p>
        <p>তারপর আজকের সময় automatic দেখাবে।</p>
      </div>

      <div id="prayerTimes"></div>
    `;

    if(!navigator.geolocation){
      document.getElementById("prayerTimes").innerHTML =
      `<div class="card"><p>Location support পাওয়া যায়নি।</p></div>`;
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async position => {

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        const now = new Date();

        const day = String(now.getDate()).padStart(2,"0");
        const month = String(now.getMonth()+1).padStart(2,"0");
        const year = now.getFullYear();

        try{

          const url =
          `https://api.aladhan.com/v1/timings/${day}-${month}-${year}?latitude=${lat}&longitude=${lon}&method=1`;

          const response = await fetch(url);
          const json = await response.json();

          if(json.code !== 200){
            throw new Error("Prayer API error");
          }

          const t = json.data.timings;

          document.getElementById("prayerTimes").innerHTML = `
            <div class="prayer">
              <span>ফজর 😇</span>
              <strong>${t.Fajr}</strong>
            </div>

            <div class="prayer">
              <span>যোহর 😇</span>
              <strong>${t.Dhuhr}</strong>
            </div>

            <div class="prayer">
              <span>আছর 😇</span>
              <strong>${t.Asr}</strong>
            </div>

            <div class="prayer">
              <span>মাগরিব 😇</span>
              <strong>${t.Maghrib}</strong>
            </div>

            <div class="prayer">
              <span>এশা 😇</span>
              <strong>${t.Isha}</strong>
            </div>
          `;

        }catch(error){

          document.getElementById("prayerTimes").innerHTML =
          `<div class="card">
             <p>নামাজের সময় লোড করা যায়নি।</p>
             <p>Internet connection পরীক্ষা করুন।</p>
           </div>`;

        }

      },

      () => {

        document.getElementById("prayerTimes").innerHTML =
        `<div class="card">
           <p>📍 Location permission Allow করুন।</p>
         </div>`;

      }
    );

    return;
  }

  if(type === "names"){

    box.innerHTML = `
      <div class="title">
        <h2>99️⃣ আল্লাহর ৯৯ নাম</h2>
      </div>

      <div id="allahNames"></div>
    `;

    const list = document.getElementById("allahNames");

    ALLAH_NAMES.forEach((name,index) => {

      const item = document.createElement("div");

      item.className = "card";

      item.innerHTML =
      `<h3>${index+1}. ${name}</h3>`;

      list.appendChild(item);

    });

    return;
  }

  if(type === "ayat"){

    box.innerHTML = `
      <div class="title">
        <h2>📜 আয়াতুল কুরসি</h2>
      </div>

      <div class="card">

        <div class="arabic">
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ
        </div>

        <p>
          আল্লাহ, তিনি ছাড়া কোনো সত্য উপাস্য নেই।
          তিনি চিরঞ্জীব, সমস্ত সৃষ্টির ধারক।
        </p>

        <p>
          পূর্ণ আয়াতটি নির্ভরযোগ্য Quran source থেকে পড়ার জন্য
          নিচের বাটন ব্যবহার করুন।
        </p>

        <button class="btn"
        onclick="window.open('https://quran.com/2/255','_blank')">
          📖 পূর্ণ আয়াত দেখুন
        </button>

      </div>
    `;

    return;
  }

  if(type === "surah"){

    box.innerHTML = `
      <div class="title">
        <h2>📖 সূরা সমূহ</h2>
        <span>১১৪টি</span>
      </div>

      <div id="surahList">
        <div class="card">
          <p>সূরার তালিকা লোড হচ্ছে...</p>
        </div>
      </div>
    `;

    try{

      const response =
      await fetch("https://api.alquran.cloud/v1/surah");

      const json = await response.json();

      if(json.code !== 200){
        throw new Error("Surah API error");
      }

      const list = document.getElementById("surahList");

      list.innerHTML = "";

      json.data.forEach(surah => {

        const item = document.createElement("div");

        item.className = "card";

        item.innerHTML = `
          <div class="task-top">
            <h3>${surah.number}. ${surah.name}</h3>
            <span>${surah.numberOfAyahs} আয়াত</span>
          </div>

          <p>${surah.englishName}</p>

          <button class="btn"
          onclick="openSurah(${surah.number})">
            📖 পড়ুন
          </button>
        `;

        list.appendChild(item);

      });

    }catch(error){

      document.getElementById("surahList").innerHTML =
      `<div class="card">
        <p>সূরার তালিকা লোড করা যায়নি।</p>
      </div>`;

    }

    return;
  }

  if(type === "namaz"){

    box.innerHTML = `
      <div class="title">
        <h2>🧎 নামাজ শেখার নিয়ম</h2>
      </div>

      <div class="card">
        <h3>১️⃣ অজু</h3>
        <p>নামাজের আগে শরিয়তসম্মতভাবে অজু করতে হবে।</p>
      </div>

      <div class="card">
        <h3>২️⃣ কিবলামুখী হওয়া</h3>
        <p>কিবলার দিকে মুখ করে দাঁড়াতে হবে।</p>
      </div>

      <div class="card">
        <h3>৩️⃣ নিয়ত</h3>
        <p>মনে নির্দিষ্ট নামাজের নিয়ত করতে হবে।</p>
      </div>

      <div class="card">
        <h3>৪️⃣ তাকবিরে তাহরিমা</h3>
        <p>আল্লাহু আকবার বলে নামাজ শুরু করতে হবে।</p>
      </div>

      <div class="card">
        <h3>৫️⃣ কিয়াম</h3>
        <p>দাঁড়িয়ে কিরাআত পড়তে হবে।</p>
      </div>

      <div class="card">
        <h3>৬️⃣ রুকু</h3>
        <p>রুকু করতে হবে এবং তাসবিহ পড়তে হবে।</p>
      </div>

      <div class="card">
        <h3>৭️⃣ সিজদা</h3>
        <p>সঠিক নিয়মে দুই সিজদা করতে হবে।</p>
      </div>

      <div class="card">
        <h3>৮️⃣ শেষ বৈঠক</h3>
        <p>শেষ বৈঠকে তাশাহহুদ, দরুদ ও দোয়া পড়তে হবে।</p>
      </div>

      <div class="card">
        <h3>৯️⃣ সালাম</h3>
        <p>ডানে ও বামে সালাম দিয়ে নামাজ শেষ করতে হবে।</p>
      </div>
    `;

    return;
  }

  if(type === "dua"){

    box.innerHTML = `
      <div class="title">
        <h2>📿 যিকির ও দোয়া</h2>
      </div>

      <div class="card">
        <h3>سُبْحَانَ اللَّهِ</h3>
        <p>সুবহানাল্লাহ — আল্লাহ পবিত্র।</p>
      </div>

      <div class="card">
        <h3>الْحَمْدُ لِلَّهِ</h3>
        <p>আলহামদুলিল্লাহ — সমস্ত প্রশংসা আল্লাহর।</p>
      </div>

      <div class="card">
        <h3>اللَّهُ أَكْبَرُ</h3>
        <p>আল্লাহু আকবার — আল্লাহ সর্বশ্রেষ্ঠ।</p>
      </div>

      <div class="card">
        <h3>أَسْتَغْفِرُ اللَّهَ</h3>
        <p>আস্তাগফিরুল্লাহ — আমি আল্লাহর কাছে ক্ষমা চাই।</p>
      </div>

      <div class="card">
        <h3>لَا إِلٰهَ إِلَّا اللَّهُ</h3>
        <p>আল্লাহ ছাড়া কোনো সত্য উপাস্য নেই।</p>
      </div>

      <div class="card">
        <h3>দরুদ শরিফ</h3>
        <p>নবী ﷺ-এর প্রতি দরুদ পাঠের অভ্যাস করুন।</p>
      </div>
    `;

    return;
  }
}

async function openSurah(number){

  const box = islamicBox();

  box.innerHTML = `
    <div class="title">
      <h2>📖 সূরা</h2>
    </div>

    <div class="card">
      <p>সূরা লোড হচ্ছে...</p>
    </div>
  `;

  try{

    const response =
    await fetch(
      `https://api.alquran.cloud/v1/surah/${number}/quran-uthmani-quran-academy`
    );

    const json = await response.json();

    if(json.code !== 200){
      throw new Error("Quran API error");
    }

    const surah = json.data;

    let content = `
      <div class="title">
        <h2>${surah.name}</h2>
      </div>
    `;

    surah.ayahs.forEach(ayah => {

      content += `
        <div class="card">

          <div class="arabic">
            ${ayah.text}
          </div>

          <p>
            আয়াত ${ayah.numberInSurah}
          </p>

        </div>
      `;

    });

    box.innerHTML = content;

  }catch(error){

    box.innerHTML = `
      <div class="card">
        <p>সূরা লোড করা যায়নি। Internet connection পরীক্ষা করুন।</p>
      </div>
    `;

  }
}

</script>
'''

# Remove an old TaskMoon Islamic script if present
html = re.sub(
    r'<script id="taskmoon-islamic">.*?</script>',
    '',
    html,
    flags=re.S
)

# Put new Islamic JS before </body>
html = html.replace("</body>", script + "\n</body>", 1)

file.write_text(html, encoding="utf-8")

print("COMPLETE ISLAMIC SECTION ADDED")
