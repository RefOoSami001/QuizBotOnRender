import telebot
import requests
from bs4 import BeautifulSoup
import json
import re
from keep_alive import keep_alive
import random
# Replace with your bot token
TELEGRAM_BOT_TOKEN = "6893223743:AAGreuO7BRrhRcaOj8CSUKvZG1AQk-C048E"

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
def send_user_details(chat_id, user):
    first_name = user.first_name
    last_name = user.last_name
    user_id = user.id
    username = user.username
    user_details = f"اسم المستخدم: @{username}\nالاسم الأول: {first_name}\nالاسم الأخير: {last_name}\nالرقم التعريفي: {user_id}"
    bot.send_message(chat_id, user_details)
def extract_quiz_data(quiz_url):
    """Extract quiz data from the HTML DOM of the quiz page."""
    try:
        # Fetch the quiz page
        response = requests.get(f"https://reooquizbot.onrender.com/quiz/{quiz_url}")
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag containing the quiz data
        script_tag = soup.find('script', string=lambda x: x and 'const questions = JSON.parse' in x)
        if not script_tag:
            raise ValueError("Quiz data not found in the HTML.")

        # Extract the JSON string from the script tag
        script_content = script_tag.string

        # Use regex to extract the JSON array
        json_match = re.search(r'JSON\.parse\(\'([^\']+)\'\)', script_content)
        if not json_match:
            raise ValueError("Failed to extract JSON data from the script tag.")

        json_data = json_match.group(1)

        # Parse the JSON data
        quiz_data = json.loads(json_data)
        return quiz_data

    except Exception as e:
        print(f"Error extracting quiz data: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send a welcome message when the user starts the bot."""
    # Create a button with the website link
    markup = telebot.types.InlineKeyboardMarkup()
    website_button = telebot.types.InlineKeyboardButton(
        text="زيارة الموقع 🌍",
        url="https://reooquizbot.onrender.com/"
    )
        # Create a button to share contact
    contact_button = telebot.types.InlineKeyboardButton(
        text="محتاج مساعدة؟🫡",
        url="https://t.me/RefOoSami"
    )
    
    # Add buttons to the markup
    markup.add(website_button, contact_button)

    # Send the welcome message with the button
    bot.reply_to(
        message,
        "مرحبًا بك في بوت RefOo Quiz Maker! 🎉\n\n"
        "أرسل  معرف الاختبار للبدء في انشاء الاختبار.\n"
        "اذا تم تحويلك من الموقع سيكون معرف الاختبار بالفعل تم نسخة قم باللصق مباشرة",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_quiz_link(message):
    """Handle the quiz link sent by the user."""
    quiz_url = message.text.strip()

    # Send a "processing" message
    processing_message = bot.reply_to(
        message,
        "⏳ جاري معالجة طلبك... الرجاء الانتظار."
    )

    try:
        # Extract quiz data from the HTML DOM
        quiz_data = extract_quiz_data(quiz_url)

        if not quiz_data:
            # Update the processing message with an error
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=processing_message.message_id,
                text="❌ فشل في استرداد بيانات الاختبار. يرجى التحقق من معرف الاختبار والمحاولة مرة أخرى."
            )
            return

        # Delete the processing message
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=processing_message.message_id
        )

        # Send each question as a poll
        for question in quiz_data:
            question_text = question['questionText']
            options = question['answerOptions']
            correct_answer = question['correctAnswer']

            # Shuffle the options and get the new index of the correct answer
            shuffled_options = options.copy()
            random.shuffle(shuffled_options)
            correct_option_id = shuffled_options.index(correct_answer)

            try:
                # Send the poll
                bot.send_poll(
                    chat_id=message.chat.id,
                    question=question_text,
                    options=shuffled_options,
                    type="quiz",
                    correct_option_id=correct_option_id,
                    is_anonymous=True,
                    explanation=f"{question.get('explanation', '')}-RefOo🥱"
                )
            except Exception as e:
                print(f"Error sending poll: {e}")

        # Send a "thank you" message
        markup = telebot.types.InlineKeyboardMarkup()
        website_button = telebot.types.InlineKeyboardButton(
            text="زيارة الموقع 🌍",
            url="https://reooquizbot.onrender.com/"
        )
        markup.add(website_button)
        bot.reply_to(
            message,
            "شكرًا لاستخدامك RefOo Quiz Maker! 🎉\n"
            "إذا كنت ترغب في إنشاء اختبارات جديدة، قم بزيارة موقعنا:\n",
            reply_markup=markup
        )
        send_user_details(854578633, message.from_user)

    except Exception as e:
        # Update the processing message with the error
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_message.message_id,
            text=f"❌ حدث خطأ أثناء معالجة طلبك: {str(e)}"
        )
if __name__ == "__main__":
    keep_alive()
    
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"An error occurred: {e}")
  
