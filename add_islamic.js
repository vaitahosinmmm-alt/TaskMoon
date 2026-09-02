const fs = require("fs");

const file = "index.html";
let html = fs.readFileSync(file, "utf8");

const start = html.indexOf('<section id="islamic"');
const end = html.indexOf('</section>', start);

if (start === -1 || end === -1) {
  console.log("Islamic section পাওয়া যায়নি");
  process.exit(1);
}

const section = `
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
<p>প্রয়োজনীয় যিকির</p>
</div>

</div>

<div id="islamicContent"></div>

</div>
</section>
`;

html = html.slice(0, start) + section + html.slice(end + 10);

const script = `
<script>
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
"আল-ওয়াসি — সর্বব্যাপী",
"আল-হাকীম — প্রজ্ঞাময়",
"আল-ওয়াদুদ — প্রেমময়",
"আল-মাজীদ — মহিমান্বিত",
"আল-বাইস — পুনরুত্থানকারী",
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

async function showIslamic(type){

const box = document.getElementById("islamicContent");

if(type === "prayer"){

box.innerHTML = \`
<div class="title"><h2>🕐 নামাজের সময়সূচি</h2></div>
<div class="note">📍 আপনার location অনুমতি দিলে আজকের সময় automatic দেখানো হবে।</div>
<br>
<div id="prayerTimes">
<div class="card"><p>সময় লোড হচ্ছে...</p></div>
</div>
\`;

if(!navigator.geolocation){
document.getElementById("prayerTimes").innerHTML =
'<div class="card"><p>আপনার browser location support করে না।</p></div>';
return;
}

navigator.geolocation.getCurrentPosition(async position => {

const lat = position.coords.latitude;
const lon = position.coords.longitude;

try{

const date = new Date();

const url =
\`https://api.aladhan.com/v1/timings/\${date.getDate()}-\${date.getMonth()+1}-\${date.getFullYear()}?latitude=\${lat}&longitude=\${lon}&method=1\`;

const response = await fetch(url);
const result = await response.json();

const t = result.data.timings;

document.getElementById("prayerTimes").innerHTML = \`
<div class="prayer"><span>ফজর 😇</span><span>\${t.Fajr}</span></div>
<div class="prayer"><span>যোহর 😇</span><span>\${t.Dhuhr}</span></div>
<div class="prayer"><span>আছর 😇</span><span>\${t.Asr}</span></div>
<div class="prayer"><span>মাগরিব 😇</span><span>\${t.Maghrib}</span></div>
<div class="prayer"><span>এশা 😇</span><span>\${t.Isha}</span></div>
\`;

}catch(error){

document.getElementById("prayerTimes").innerHTML =
'<div class="card"><p>নামাজের সময় লোড করা যায়নি। Internet connection পরীক্ষা করুন।</p></div>';

}

}, () => {

document.getElementById("prayerTimes").innerHTML =
'<div class="card"><p>📍 Prayer time দেখাতে location permission Allow করুন।</p></div>';

});

}

else if(type === "names"){

box.innerHTML = \`
<div class="title">
<h2>99️⃣ আল্লাহর ৯৯ নাম</h2>
</div>
<div id="namesList"></div>
\`;

const list = document.getElementById("namesList");

ALLAH_NAMES.forEach((name,index)=>{

const div = document.createElement("div");
div.className = "card";
div.innerHTML = \`<h3>\${index+1}. \${name}</h3>\`;

list.appendChild(div);

});

}

else if(type === "ayat"){

box.innerHTML = \`
<div class="title"><h2>📜 আয়াতুল কুরসি</h2></div>

<div class="card">

<div class="arabic">
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ
</div>

<p>
আল্লাহ, তিনি ছাড়া কোনো উপাস্য নেই। তিনি চিরঞ্জীব ও সমস্ত সৃষ্টির ধারক।
</p>

<div class="note">
পূর্ণ আয়াত ও নির্ভরযোগ্য অনুবাদ Quran API থেকে পরবর্তী আপডেটে যুক্ত করা হবে।
</div>

</div>
\`;

}

else if(type === "namaz"){

box.innerHTML = \`
<div class="title"><h2>🧎 নামাজ শেখার নিয়ম</h2></div>

<div class="card"><h3>১. অজু</h3><p>নামাজের আগে সঠিকভাবে অজু করতে হবে।</p></div>

<div class="card"><h3>২. কিবলামুখী হওয়া</h3><p>কিবলামুখী হয়ে নামাজের জন্য প্রস্তুত হতে হবে।</p></div>

<div class="card"><h3>৩. নিয়ত</h3><p>মনে নির্দিষ্ট নামাজের নিয়ত করতে হবে।</p></div>

<div class="card"><h3>৪. তাকবির</h3><p>আল্লাহু আকবার বলে নামাজ শুরু করতে হবে।</p></div>

<div class="card"><h3>৫. কিয়াম</h3><p>দাঁড়িয়ে কিরাআত পড়তে হবে।</p></div>

<div class="card"><h3>৬. রুকু</h3><p>রুকুতে গিয়ে আল্লাহর প্রশংসা করতে হবে।</p></div>

<div class="card"><h3>৭. সিজদা</h3><p>সিজদা করতে হবে এবং নিয়ম অনুযায়ী দুই সিজদা সম্পন্ন করতে হবে।</p></div>

<div class="card"><h3>৮. শেষ বৈঠক ও সালাম</h3><p>শেষ বৈঠকের পর ডানে ও বামে সালাম দিয়ে নামাজ শেষ করতে হবে।</p></div>
\`;

}

else if(type === "surah"){

box.innerHTML = \`
<div class="title">
<h2>📖 সূরা সমূহ</h2>
<span>১১৪টি</span>
</div>

<div class="card">
<p>সূরার সম্পূর্ণ তালিকা Quran API থেকে লোড হবে। নিচের তালিকায় চাপ দিলে নির্দিষ্ট সূরা পড়ার ব্যবস্থা করা যাবে।</p>
</div>

<div id="surahList">
<div class="card"><p>সূরার তালিকা লোড হচ্ছে...</p></div>
</div>
\`;

try{

const response =
await fetch("https://api.alquran.cloud/v1/surah");

const result = await response.json();

const list = document.getElementById("surahList");
list.innerHTML = "";

result.data.forEach(surah => {

const div = document.createElement("div");
div.className = "card";

div.innerHTML = \`
<div class="task-top">
<h3>\${surah.number}. \${surah.name}</h3>
<span class="reward">\${surah.numberOfAyahs} আয়াত</span>
</div>
<p>\${surah.englishName} — \${surah.englishNameTranslation}</p>
\`;

list.appendChild(div);

});

}catch(error){

document.getElementById("surahList").innerHTML =
'<div class="card"><p>সূরার তালিকা লোড করা যায়নি। Internet connection পরীক্ষা করুন।</p></div>';

}

}

else if(type === "dua"){

box.innerHTML = \`
<div class="title"><h2>📿 যিকির ও দোয়া</h2></div>

<div class="card">
<h3>সুবহানাল্লাহ</h3>
<p>আল্লাহ পবিত্র ও মহিমান্বিত।</p>
</div>

<div class="card">
<h3>আলহামদুলিল্লাহ</h3>
<p>সমস্ত প্রশংসা আল্লাহর জন্য।</p>
</div>

<div class="card">
<h3>আল্লাহু আকবার</h3>
<p>আল্লাহ সর্বশ্রেষ্ঠ।</p>
</div>

<div class="card">
<h3>আস্তাগফিরুল্লাহ</h3>
<p>আমি আল্লাহর কাছে ক্ষমা চাই।</p>
</div>

<div class="card">
<h3>লা ইলাহা ইল্লাল্লাহ</h3>
<p>আল্লাহ ছাড়া কোনো সত্য উপাস্য নেই।</p>
</div>

<div class="card">
<h3>সকাল-সন্ধ্যার যিকির</h3>
<p>নিয়মিত আল্লাহর স্মরণ, ইস্তিগফার ও দরুদ পাঠের অভ্যাস করুন।</p>
</div>
\`;

}

}
</script>
`;

const scriptStart = html.lastIndexOf("<script>");
const bodyEnd = html.lastIndexOf("</body>");

if(scriptStart !== -1 && bodyEnd !== -1){
html = html.slice(0, scriptStart) + script + html.slice(bodyEnd);
}

fs.writeFileSync(file, html, "utf8");

console.log("Complete Islamic section added.");
