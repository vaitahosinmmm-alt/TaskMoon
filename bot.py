import telebot
from telebot import types
import sqlite3

# ==============================
# 🔐 BOT CONFIG
# ==============================

BOT_TOKEN = "8965586086:AAHmNMQQlo8pAIu7zcZ2Byys0zha_boed90"
ADMIN_ID = 7346014474

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
DB = "taskmoon.db"


# ==============================
# DATABASE
# ==============================

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    conn = connect()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            reward REAL DEFAULT 0,
            status TEXT DEFAULT 'active'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            user_id INTEGER,
            proof TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            method TEXT,
            account TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)

    conn.commit()
    conn.close()


setup_database()


# ==============================
# USER
# ==============================

def add_user(user):
    conn = connect()

    conn.execute(
        "INSERT OR IGNORE INTO users(user_id, username) VALUES (?, ?)",
        (user.id, user.username or "")
    )

    conn.commit()
    conn.close()


def main_menu():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "🚀 Open TaskMoon App",
            web_app=types.WebAppInfo(
                url="https://vaitahosinmmm-alt.github.io/TaskMoon/"
            )
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📋 Tasks",
            callback_data="tasks"
        ),
        types.InlineKeyboardButton(
            "💰 Wallet",
            callback_data="wallet"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "👥 Refer",
            callback_data="refer"
        ),
        types.InlineKeyboardButton(
            "💸 Withdraw",
            callback_data="withdraw"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📜 History",
            callback_data="history"
        ),
        types.InlineKeyboardButton(
            "ℹ️ Help",
            callback_data="help"
        )
    )

    return keyboard


# ==============================
# START
# ==============================

@bot.message_handler(commands=["start"])
def start(message):

    add_user(message.from_user)

    bot.send_message(
        message.chat.id,
        "🌙 <b>Welcome to TaskMoon!</b>\n\n"
        "🎯 কাজ সম্পন্ন করুন\n"
        "💰 Reward Earn করুন\n"
        "💸 Balance Withdraw করুন\n\n"
        "নিচের Menu থেকে একটি অপশন নির্বাচন করুন।",
        reply_markup=main_menu()
    )


# ==============================
# TASK LIST
# ==============================

@bot.message_handler(func=lambda message: message.text == "📋 Tasks")
def show_tasks(message):

    add_user(message.from_user)

    conn = connect()

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE status='active' ORDER BY id DESC"
    ).fetchall()

    conn.close()

    if not tasks:
        bot.send_message(
            message.chat.id,
            "📭 <b>এই মুহূর্তে কোনো Task নেই।</b>"
        )
        return

    for task in tasks:

        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                "📤 Submit Proof",
                callback_data=f"submit_{task['id']}"
            )
        )

        text = (
            f"🌙 <b>{task['title']}</b>\n\n"
            f"📝 {task['description']}\n\n"
            f"💰 Reward: <b>{task['reward']}</b>"
        )

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard
        )


# ==============================
# SUBMIT PROOF
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("submit_")
)
def submit_start(call):

    task_id = int(call.data.split("_")[1])

    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id,
        "📤 <b>Task Proof পাঠান</b>\n\n"
        "আপনার কাজের Screenshot অথবা Text পাঠান।"
    )

    bot.register_next_step_handler(
        msg,
        save_proof,
        task_id
    )


def save_proof(message, task_id):

    add_user(message.from_user)

    if message.content_type == "photo":
        proof = message.photo[-1].file_id
    else:
        proof = message.text or "Proof"

    conn = connect()

    conn.execute(
        """
        INSERT INTO submissions(task_id, user_id, proof)
        VALUES (?, ?, ?)
        """,
        (
            task_id,
            message.from_user.id,
            proof
        )
    )

    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        "✅ <b>Proof Submitted!</b>\n\n"
        "Admin review করার পর Reward যোগ হবে।",
        reply_markup=main_menu()
    )

    bot.send_message(
        ADMIN_ID,
        "📨 <b>New Task Proof</b>\n\n"
        f"👤 User ID: <code>{message.from_user.id}</code>\n"
        f"🎯 Task ID: <code>{task_id}</code>"
    )


# ==============================
# WALLET
# ==============================

@bot.message_handler(func=lambda message: message.text == "💰 Wallet")
def wallet(message):

    add_user(message.from_user)

    conn = connect()

    user = conn.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.from_user.id,)
    ).fetchone()

    conn.close()

    balance = user["balance"] if user else 0

    bot.send_message(
        message.chat.id,
        "💰 <b>TaskMoon Wallet</b>\n\n"
        f"💎 Balance: <b>{balance:.2f}</b>"
    )


# ==============================
# REFERRAL
# ==============================

@bot.message_handler(func=lambda message: message.text == "👥 Refer")
def referral(message):

    add_user(message.from_user)

    me = bot.get_me()

    link = (
        f"https://t.me/{me.username}"
        f"?start=ref_{message.from_user.id}"
    )

    bot.send_message(
        message.chat.id,
        "👥 <b>Referral System</b>\n\n"
        "🔗 আপনার Referral Link:\n\n"
        f"<code>{link}</code>"
    )


# ==============================
# WITHDRAW
# ==============================

@bot.message_handler(func=lambda message: message.text == "💸 Withdraw")
def withdraw(message):

    add_user(message.from_user)

    conn = connect()

    user = conn.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.from_user.id,)
    ).fetchone()

    conn.close()

    balance = user["balance"] if user else 0

    if balance <= 0:

        bot.send_message(
            message.chat.id,
            "❌ <b>আপনার Wallet-এ কোনো Balance নেই।</b>"
        )

        return

    msg = bot.send_message(
        message.chat.id,
        f"💰 আপনার Balance: <b>{balance:.2f}</b>\n\n"
        "💸 কত টাকা Withdraw করতে চান?"
    )

    bot.register_next_step_handler(
        msg,
        withdraw_amount
    )


def withdraw_amount(message):

    try:
        amount = float(message.text)

    except:

        bot.send_message(
            message.chat.id,
            "❌ সঠিক Amount লিখুন।"
        )

        return

    conn = connect()

    user = conn.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.from_user.id,)
    ).fetchone()

    if not user or amount <= 0 or amount > user["balance"]:

        conn.close()

        bot.send_message(
            message.chat.id,
            "❌ আপনার Balance যথেষ্ট নেই।"
        )

        return

    conn.close()

    msg = bot.send_message(
        message.chat.id,
        "💳 Payment Method লিখুন:\n\n"
        "যেমন: bKash / Nagad / USDT"
    )

    bot.register_next_step_handler(
        msg,
        withdraw_method,
        amount
    )


def withdraw_method(message, amount):

    method = message.text

    msg = bot.send_message(
        message.chat.id,
        "📱 আপনার Payment Number / Address পাঠান।"
    )

    bot.register_next_step_handler(
        msg,
        withdraw_account,
        amount,
        method
    )


def withdraw_account(message, amount, method):

    account = message.text

    conn = connect()

    conn.execute(
        """
        INSERT INTO withdrawals(
            user_id,
            amount,
            method,
            account
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            message.from_user.id,
            amount,
            method,
            account
        )
    )

    conn.execute(
        "UPDATE users SET balance=balance-? WHERE user_id=?",
        (
            amount,
            message.from_user.id
        )
    )

    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        "✅ <b>Withdrawal Request Submitted!</b>\n\n"
        "Admin review করবেন।",
        reply_markup=main_menu()
    )

    bot.send_message(
        ADMIN_ID,
        "💸 <b>New Withdrawal Request</b>\n\n"
        f"👤 User: <code>{message.from_user.id}</code>\n"
        f"💰 Amount: <b>{amount}</b>\n"
        f"💳 Method: <b>{method}</b>\n"
        f"📱 Account: <code>{account}</code>"
    )


# ==============================
# HISTORY
# ==============================

@bot.message_handler(func=lambda message: message.text == "📜 History")
def history(message):

    conn = connect()

    submissions = conn.execute(
        """
        SELECT * FROM submissions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
        """,
        (message.from_user.id,)
    ).fetchall()

    withdrawals = conn.execute(
        """
        SELECT * FROM withdrawals
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
        """,
        (message.from_user.id,)
    ).fetchall()

    conn.close()

    text = "📜 <b>TaskMoon History</b>\n\n"

    text += "🎯 <b>Tasks</b>\n"

    if submissions:

        for item in submissions:

            text += (
                f"#{item['id']} — "
                f"{item['status']}\n"
            )

    else:

        text += "No task history.\n"

    text += "\n💸 <b>Withdrawals</b>\n"

    if withdrawals:

        for item in withdrawals:

            text += (
                f"#{item['id']} — "
                f"{item['amount']} — "
                f"{item['status']}\n"
            )

    else:

        text += "No withdrawal history."

    bot.send_message(
        message.chat.id,
        text
    )


# ==============================
# HELP
# ==============================

@bot.message_handler(func=lambda message: message.text == "ℹ️ Help")
def help_menu(message):

    bot.send_message(
        message.chat.id,
        "🌙 <b>TaskMoon Help</b>\n\n"
        "📋 Tasks — Available Task দেখুন\n"
        "💰 Wallet — Balance দেখুন\n"
        "👥 Refer — Referral Link\n"
        "💸 Withdraw — Withdrawal Request\n"
        "📜 History — আপনার History"
    )


# ==============================
# ADMIN PANEL
# ==============================

@bot.message_handler(commands=["admin"])
def admin_panel(message):

    if message.from_user.id != ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "❌ আপনি Admin নন।"
        )

        return

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "➕ Add Task",
            callback_data="admin_add"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📨 Pending Proof",
            callback_data="admin_proof"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "💸 Withdrawals",
            callback_data="admin_withdraw"
        )
    )

    bot.send_message(
        message.chat.id,
        "👨‍💻 <b>TaskMoon Admin Panel</b>\n\n"
        "নিচের অপশন নির্বাচন করুন।",
        reply_markup=keyboard
    )


# ==============================
# ADD TASK
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data == "admin_add"
)
def admin_add(call):

    if call.from_user.id != ADMIN_ID:
        return

    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        ADMIN_ID,
        "➕ Task Title লিখুন:"
    )

    bot.register_next_step_handler(
        msg,
        add_title
    )


def add_title(message):

    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(
        ADMIN_ID,
        "📝 Task Description লিখুন:"
    )

    bot.register_next_step_handler(
        msg,
        add_description,
        message.text
    )


def add_description(message, title):

    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(
        ADMIN_ID,
        "💰 Reward কত হবে?\n\n"
        "উদাহরণ: 10"
    )

    bot.register_next_step_handler(
        msg,
        add_reward,
        title,
        message.text
    )


def add_reward(message, title, description):

    if message.from_user.id != ADMIN_ID:
        return

    try:

        reward = float(message.text)

    except:

        bot.send_message(
            ADMIN_ID,
            "❌ Reward সংখ্যা হতে হবে।"
        )

        return

    conn = connect()

    conn.execute(
        """
        INSERT INTO tasks(
            title,
            description,
            reward
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            description,
            reward
        )
    )

    conn.commit()
    conn.close()

    bot.send_message(
        ADMIN_ID,
        "✅ <b>Task Added Successfully!</b>"
    )


# ==============================
# PENDING PROOFS
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data == "admin_proof"
)
def pending_proofs(call):

    if call.from_user.id != ADMIN_ID:
        return

    bot.answer_callback_query(call.id)

    conn = connect()

    rows = conn.execute(
        """
        SELECT * FROM submissions
        WHERE status='pending'
        ORDER BY id ASC
        """
    ).fetchall()

    conn.close()

    if not rows:

        bot.send_message(
            ADMIN_ID,
            "📭 No pending proofs."
        )

        return

    for row in rows:

        keyboard = types.InlineKeyboardMarkup()

        keyboard.row(
            types.InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{row['id']}"
            ),
            types.InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{row['id']}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            "📨 <b>Pending Proof</b>\n\n"
            f"🆔 Submission: <code>{row['id']}</code>\n"
            f"👤 User: <code>{row['user_id']}</code>\n"
            f"🎯 Task: <code>{row['task_id']}</code>\n\n"
            f"📄 Proof:\n<code>{row['proof']}</code>",
            reply_markup=keyboard
        )


# ==============================
# APPROVE
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("approve_")
)
def approve(call):

    if call.from_user.id != ADMIN_ID:
        return

    submission_id = int(
        call.data.split("_")[1]
    )

    conn = connect()

    row = conn.execute(
        """
        SELECT submissions.*, tasks.reward
        FROM submissions
        JOIN tasks
        ON submissions.task_id=tasks.id
        WHERE submissions.id=?
        AND submissions.status='pending'
        """,
        (submission_id,)
    ).fetchone()

    if not row:

        conn.close()

        bot.answer_callback_query(
            call.id,
            "Already processed."
        )

        return

    conn.execute(
        """
        UPDATE submissions
        SET status='approved'
        WHERE id=?
        """,
        (submission_id,)
    )

    conn.execute(
        """
        UPDATE users
        SET balance=balance+?
        WHERE user_id=?
        """,
        (
            row["reward"],
            row["user_id"]
        )
    )

    conn.commit()
    conn.close()

    bot.answer_callback_query(
        call.id,
        "Approved!"
    )

    bot.send_message(
        row["user_id"],
        "🎉 <b>Task Approved!</b>\n\n"
        f"💰 Reward Added: <b>{row['reward']}</b>"
    )

    bot.edit_message_reply_markup(
        ADMIN_ID,
        call.message.message_id,
        reply_markup=None
    )


# ==============================
# REJECT
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("reject_")
)
def reject(call):

    if call.from_user.id != ADMIN_ID:
        return

    submission_id = int(
        call.data.split("_")[1]
    )

    conn = connect()

    row = conn.execute(
        """
        SELECT * FROM submissions
        WHERE id=?
        AND status='pending'
        """,
        (submission_id,)
    ).fetchone()

    if not row:

        conn.close()

        bot.answer_callback_query(
            call.id,
            "Already processed."
        )

        return

    conn.execute(
        """
        UPDATE submissions
        SET status='rejected'
        WHERE id=?
        """,
        (submission_id,)
    )

    conn.commit()
    conn.close()

    bot.answer_callback_query(
        call.id,
        "Rejected!"
    )

    bot.send_message(
        row["user_id"],
        "❌ <b>Your Task Proof was rejected.</b>"
    )

    bot.edit_message_reply_markup(
        ADMIN_ID,
        call.message.message_id,
        reply_markup=None
    )


# ==============================
# ADMIN WITHDRAWALS
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data == "admin_withdraw"
)
def admin_withdraw(call):

    if call.from_user.id != ADMIN_ID:
        return

    bot.answer_callback_query(call.id)

    conn = connect()

    rows = conn.execute(
        """
        SELECT * FROM withdrawals
        WHERE status='pending'
        ORDER BY id ASC
        """
    ).fetchall()

    conn.close()

    if not rows:

        bot.send_message(
            ADMIN_ID,
            "📭 No pending withdrawals."
        )

        return

    for row in rows:

        keyboard = types.InlineKeyboardMarkup()

        keyboard.row(
            types.InlineKeyboardButton(
                "✅ Paid",
                callback_data=f"paid_{row['id']}"
            ),
            types.InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"wreject_{row['id']}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            "💸 <b>Withdrawal Request</b>\n\n"
            f"🆔 ID: <code>{row['id']}</code>\n"
            f"👤 User: <code>{row['user_id']}</code>\n"
            f"💰 Amount: <b>{row['amount']}</b>\n"
            f"💳 Method: <b>{row['method']}</b>\n"
            f"📱 Account: <code>{row['account']}</code>",
            reply_markup=keyboard
        )


# ==============================
# PAID
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("paid_")
)
def paid(call):

    if call.from_user.id != ADMIN_ID:
        return

    withdrawal_id = int(
        call.data.split("_")[1]
    )

    conn = connect()

    row = conn.execute(
        """
        SELECT * FROM withdrawals
        WHERE id=?
        AND status='pending'
        """,
        (withdrawal_id,)
    ).fetchone()

    if not row:

        conn.close()

        bot.answer_callback_query(
            call.id,
            "Already processed."
        )

        return

    conn.execute(
        """
        UPDATE withdrawals
        SET status='paid'
        WHERE id=?
        """,
        (withdrawal_id,)
    )

    conn.commit()
    conn.close()

    bot.answer_callback_query(
        call.id,
        "Marked as Paid!"
    )

    bot.send_message(
        row["user_id"],
        f"✅ <b>Withdrawal Paid!</b>\n\n"
        f"💰 Amount: <b>{row['amount']}</b>"
    )

    bot.edit_message_reply_markup(
        ADMIN_ID,
        call.message.message_id,
        reply_markup=None
    )


# ==============================
# WITHDRAW REJECT
# ==============================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("wreject_")
)
def withdraw_reject(call):

    if call.from_user.id != ADMIN_ID:
        return

    withdrawal_id = int(
        call.data.split("_")[1]
    )

    conn = connect()

    row = conn.execute(
        """
        SELECT * FROM withdrawals
        WHERE id=?
        AND status='pending'
        """,
        (withdrawal_id,)
    ).fetchone()

    if not row:

        conn.close()

        bot.answer_callback_query(
            call.id,
            "Already processed."
        )

        return

    conn.execute(
        """
        UPDATE users
        SET balance=balance+?
        WHERE user_id=?
        """,
        (
            row["amount"],
            row["user_id"]
        )
    )

    conn.execute(
        """
        UPDATE withdrawals
        SET status='rejected'
        WHERE id=?
        """,
        (withdrawal_id,)
    )

    conn.commit()
    conn.close()

    bot.answer_callback_query(
        call.id,
        "Rejected!"
    )

    bot.send_message(
        row["user_id"],
        f"❌ <b>Withdrawal Rejected</b>\n\n"
        f"💰 {row['amount']} আপনার Wallet-এ ফেরত দেওয়া হয়েছে।"
    )

    bot.edit_message_reply_markup(
        ADMIN_ID,
        call.message.message_id,
        reply_markup=None
    )


# ==============================
# START BOT
# ==============================

print("🌙 TaskMoon Bot is running...")

bot.infinity_polling(
    skip_pending=True
)
