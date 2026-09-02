from pathlib import Path
import re

file = Path("index.html")
html = file.read_text(encoding="utf-8")

# Task section
task_section = r'''
<section id="tasks" class="section">
<div class="container">

<div class="title">
  <h2>📋 Task Center</h2>
  <span>🪙</span>
</div>

<div class="card task-balance">
  <h3>🪙 Your Coins</h3>
  <div id="taskCoinBalance">0 Coins</div>
  <p>Task complete করে coins earn করুন।</p>
</div>

<div id="taskList"></div>

</div>
</section>
'''

# Existing task section থাকলে replace, না থাকলে Islamic-এর আগে add
pattern = r'<section[^>]*id=["\']tasks["\'][^>]*>.*?</section>'
html, count = re.subn(pattern, task_section, html, count=1, flags=re.S)

if count == 0:
    marker = '<section id="islamic"'
    pos = html.find(marker)

    if pos != -1:
        html = html[:pos] + task_section + "\n" + html[pos:]
    else:
        html = html.replace("</body>", task_section + "\n</body>", 1)

# Task JavaScript
task_script = r'''
<script id="taskmoon-tasks">

const TASKS = [
  {
    id: 1,
    title: "📢 Telegram Channel Join",
    description: "নির্দিষ্ট Telegram channel-এ join করুন।",
    reward: 50,
    link: "https://t.me/"
  },
  {
    id: 2,
    title: "📣 Telegram Group Join",
    description: "নির্দিষ্ট Telegram group-এ join করুন।",
    reward: 75,
    link: "https://t.me/"
  },
  {
    id: 3,
    title: "⭐ Daily Task",
    description: "আজকের task সম্পূর্ণ করুন।",
    reward: 100,
    link: "#"
  }
];

let completedTasks =
  JSON.parse(localStorage.getItem("taskmoon_completed_tasks") || "[]");

let taskCoins =
  Number(localStorage.getItem("taskmoon_task_coins") || 0);

function saveTaskData(){

  localStorage.setItem(
    "taskmoon_completed_tasks",
    JSON.stringify(completedTasks)
  );

  localStorage.setItem(
    "taskmoon_task_coins",
    String(taskCoins)
  );

}

function updateTaskBalance(){

  const balance =
    document.getElementById("taskCoinBalance");

  if(balance){
    balance.textContent =
      taskCoins + " Coins";
  }

}

function renderTasks(){

  const list =
    document.getElementById("taskList");

  if(!list) return;

  list.innerHTML = "";

  TASKS.forEach(task => {

    const completed =
      completedTasks.includes(task.id);

    const card =
      document.createElement("div");

    card.className = "card";

    card.innerHTML = `
      <div class="task-top">

        <div>
          <h3>${task.title}</h3>
          <p>${task.description}</p>
        </div>

        <span class="reward">
          +${task.reward} 🪙
        </span>

      </div>

      ${
        completed

        ? `
          <button class="btn" disabled>
            ✅ Completed
          </button>
        `

        : `
          <button
            class="btn"
            onclick="startTask(${task.id})">
            🚀 Start Task
          </button>

          <button
            class="btn"
            id="complete-${task.id}"
            style="display:none"
            onclick="completeTask(${task.id})">
            ✅ Complete Task
          </button>
        `
      }

    `;

    list.appendChild(card);

  });

  updateTaskBalance();

}

function startTask(id){

  alert("Coming Soon Dear ❤️🌙");
  return;

  const task =
    TASKS.find(item => item.id === id);

  if(!task) return;

  if(task.link && task.link !== "#"){

    window.open(task.link, "_blank");

  }

  const button =
    document.getElementById("complete-" + id);

  if(button){

    button.style.display = "block";

    button.textContent =
      "✅ কাজ শেষ হলে এখানে চাপুন";

  }

}

function completeTask(id){

  if(completedTasks.includes(id)){

    alert("এই task-এর reward আগেই নেওয়া হয়েছে।");

    return;

  }

  const task =
    TASKS.find(item => item.id === id);

  if(!task) return;

  completedTasks.push(id);

  taskCoins += task.reward;

  saveTaskData();

  renderTasks();

  alert(
    "🎉 Task Complete! +" +
    task.reward +
    " Coins"
  );

}

document.addEventListener(
  "DOMContentLoaded",
  renderTasks
);

</script>
'''

# Remove previous task script if it exists
html = re.sub(
    r'<script id="taskmoon-tasks">.*?</script>',
    '',
    html,
    flags=re.S
)

html = html.replace(
    "</body>",
    task_script + "\n</body>",
    1
)

file.write_text(html, encoding="utf-8")

print("TASK SYSTEM ADDED SUCCESSFULLY")
