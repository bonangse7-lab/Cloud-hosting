import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time

# ដាក់ Token របស់អ្នកនៅទីនេះ
BOT_TOKEN = '8458193379:AAHlW7YfHi6GuE_Qy6TucdbYsvJufPljDQg'
bot = telebot.TeleBot(BOT_TOKEN)

# មុខងារសម្រាប់បង្កើត Main Menu Buttons
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton('💰 Balance'), KeyboardButton('📊 Status Bot'))
    markup.row(KeyboardButton('🚀 Hosting Bot'), KeyboardButton('📦 Plan Bot'))
    markup.row(KeyboardButton('📞 Support'))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "សួស្តី! សូមស្វាគមន៍មកកាន់ Auto Hosting Bot 🚀\nសូមជ្រើសរើសជម្រើសណាមួយនៅខាងក្រោម៖"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# ចាប់យកការចុចលើ Main Menu
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == '💰 Balance':
        bot.send_message(chat_id, "💳 ទឹកប្រាក់របស់អ្នក (Balance): <b>$0.00</b>\nសូមបញ្ចូលប្រាក់ដើម្បីទិញ Host។", parse_mode='HTML')
        
    elif text == '📊 Status Bot':
        bot.send_message(chat_id, "📊 ស្ថានភាព (Status): 🟢 Online\n☁️ Server: Cloud Render")
        
    elif text == '📦 Plan Bot':
        plan_text = "<b>កញ្ចប់តម្លៃ Hosting (Plans):</b>\n\n• 1 host = 0.50$\n• 10 host = 8$"
        bot.send_message(chat_id, plan_text, parse_mode='HTML')
        
    elif text == '📞 Support':
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="ទាក់ទង Owner 👨‍💻", url="https://t.me/gito_kanxo")
        markup.add(btn)
        bot.send_message(chat_id, "ត្រូវការជំនួយឬមានចម្ងល់? សូមទាក់ទងទៅកាន់ Owner ផ្ទាល់៖", reply_markup=markup)
        
    elif text == '🚀 Hosting Bot':
        # សុំឱ្យ User បញ្ជូន File Zip
        msg = bot.send_message(chat_id, "📁 សូមបញ្ជូន File កូដរបស់អ្នកជាទម្រង់ <b>.zip</b> មកទីនេះ ដើម្បីដាក់ដំណើរការ (Run) លើ Cloud Render ☁️", parse_mode='HTML')
        # ប្តូរតំណាក់កាលទៅកាន់មុខងារទទួល File 
        bot.register_next_step_handler(msg, process_zip_upload)

# មុខងារសម្រាប់ត្រួតពិនិត្យ និងទទួល File .zip
def process_zip_upload(message):
    chat_id = message.chat.id
    
    # ពិនិត្យថាតើ User ពិតជាបានផ្ញើ File (Document) មកមែនឬអត់
    if message.content_type != 'document':
        bot.send_message(chat_id, "❌ អ្នកមិនបានបញ្ជូន File ទេ។ សូមចុច <b>🚀 Hosting Bot</b> ម្តងទៀត ហើយបញ្ជូន File .zip។", parse_mode='HTML')
        return

    doc = message.document
    
    # ពិនិត្យមើលកន្ទុយ File ថាជា .zip ដែរឬទេ
    if not doc.file_name.endswith('.zip'):
        bot.send_message(chat_id, "❌ File នេះមិនមែនជាទម្រង់ <b>.zip</b> ទេ។ សូមសាកល្បងម្តងទៀត។", parse_mode='HTML')
        return

    bot.send_message(chat_id, f"📥 កំពុងទទួល File <b>{doc.file_name}</b>...\nកំពុងបញ្ជូនទិន្នន័យទៅកាន់ Cloud Render... ⏳", parse_mode='HTML')
    
    # កន្លែងនេះអ្នកអាចសរសេរកូដទាញយក File ពិតៗដោយប្រើ bot.get_file() និង bot.download_file()
    # បន្ទាប់មកសរសេរ Script ដើម្បី Push ទៅ GitHub និង Trigger Render API
    
    # ផ្អាក 3 វិនាទី ដើម្បីធ្វើឱ្យដូចកំពុងដំណើរការ
    time.sleep(3)
    
    # ចាត់ទុកថាការ Hosting បរាជ័យ (Failed) ដូចដែលអ្នកបានស្នើសុំឱ្យបង្ហាញមូលហេតុ
    is_success = False 
    
    if is_success:
        bot.send_message(chat_id, "✅ ការ Hosting ទទួលបានជោគជ័យ! Bot របស់អ្នកកំពុងដំណើរការ។")
    else:
        # ប្រាប់ពីមូលហេតុដែល Failed
        error_reason = "ប្រព័ន្ធទាមទារការភ្ជាប់ទៅកាន់ GitHub Repository ជាមុនសិន។ Cloud Render មិនអាចអាន File .zip ដោយផ្ទាល់តាមរយៈ API បានទេ។"
        bot.send_message(chat_id, f"❌ ការ Hosting ទទួលបានបរាជ័យ (Failed)!\n\n⚠️ <b>មូលហេតុ:</b> {error_reason}", parse_mode='HTML')

# ដំណើរការ Bot ឱ្យនៅ Active រហូត
print("Bot is running...")
bot.infinity_polling()
