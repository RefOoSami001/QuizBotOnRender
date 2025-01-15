import telebot
import pdfplumber
from io import BytesIO
from keep_alive import keep_alive
import time
import random
from fpdf import FPDF
import json
def parse_quiz_text(quiz_text):
    import re
    
    # Remove any unnecessary parts (like title or any unwanted text)
    quiz_text = re.sub(r'#.*\n', '', quiz_text)  # Remove quiz title
    quiz_data = {}

    # Split the input into questions and options
    questions = re.findall(r'\*\*(\d+)\. (.*?)\*\*\s*(.*?)(?=\*\*|$)', quiz_text, re.DOTALL)

    for question in questions:
        question_number = question[0]
        question_text = question[1].strip()
        options_text = question[2].strip().splitlines()

        options = {}
        for option in options_text:
            match = re.match(r'([a-d])\)\s*(.*)', option.strip())  # Changed to use ')' instead of '.' 
            if match:
                options[match.group(1)] = match.group(2).strip()

        quiz_data[int(question_number)] = {
            "text": question_text,
            "options": options,
            "answer": ""  # Placeholder for the answer
        }

    # Extract the answer key section
    answer_key_section = re.search(r'Answers?:\s*(.*)', quiz_text, re.DOTALL)
    if answer_key_section:
        answer_key_text = answer_key_section.group(1).strip()
        answer_key_lines = answer_key_text.splitlines()

        for line in answer_key_lines:
            match = re.match(r'(\d+)\.\s*([a-d])', line.strip())
            if match:
                question_number = int(match.group(1))
                answer = match.group(2)
                if question_number in quiz_data:
                    quiz_data[question_number]["answer"] = answer

    return quiz_data

def get_questions(topic, num_questions):
    import requests
    import json
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://app.kangaroos.ai',
        'priority': 'u=1, i',
        'referer': 'https://app.kangaroos.ai/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    json_data = {
        'topic': topic,
        'education_level': '18+',
        'number_of_questions':num_questions,
    }

    response = requests.post('https://kangroos-ai-dqhgks3gba-uc.a.run.app/mcq', headers=headers, json=json_data)
    print(response.json()['output']['text'])
    parsed_data = parse_quiz_text(response.json()['output']['text'])

    # Convert the parsed data to JSON
    quiz_json = json.dumps(parsed_data, indent=4)
    data = quiz_json
    return data
class QuizBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.TOPIC = None
        self.NUM_QUESTIONS = None
        self.DIFF = None


    def send_pdf(self, chat_id, questions_data):
        try:
            # Create the PDF object
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Add the title (assuming you want to use a title, otherwise default to 'Generated Quiz')
            title = "Generated Quiz"
            pdf.cell(200, 10, txt=title, ln=True, align='C')
            pdf.ln(10)

            # Iterate over each question in the dictionary
            for i, (question_id, question_data) in enumerate(questions_data.items(), start=1):
                question_text = question_data.get('text', 'No question text provided')
                options = question_data.get('options', {})
                correct_answer_key = question_data.get('answer', '')

                # Shuffle the options to randomize their order
                options_list = [f"{key}) {value}" for key, value in options.items()]

                # Write the question
                pdf.set_font("Arial", style="B", size=12)
                pdf.cell(0, 10, f"{i}. {question_text}", ln=True)
                pdf.set_font("Arial", size=12)

                # Write the options
                correct_option_text = f"{correct_answer_key}) {options.get(correct_answer_key, '')}"
                for opt in options_list:
                    # Highlight the correct option
                    if opt == correct_option_text:
                        pdf.set_text_color(0, 128, 0)  # Green for correct answer
                        pdf.set_font("Arial", style="B", size=12)  # Bold for correct answer
                    else:
                        pdf.set_text_color(0, 0, 0)  # Black for other options
                        pdf.set_font("Arial", size=12)  # Regular font for other options

                    pdf.cell(0, 10, f"   - {opt}", ln=True)

                # Add explanation in bold (if exists, otherwise default message)
                pdf.set_text_color(50, 50, 50)  # Gray for explanations
                pdf.set_font("Arial", style="B", size=12)  # Bold font for explanation
                pdf.ln(5)  # Add space between questions

            # Write PDF content to a BytesIO object
            output = BytesIO()
            pdf_data = pdf.output(dest='S')  # No encoding necessary here
            output.write(pdf_data.encode('latin1'))  # Encode to latin1 which is compatible with FPDF
            output.seek(0)  # Move the cursor to the beginning of the BytesIO object

            # Sending the document via Telegram bot with a proper filename
            self.bot.send_document(
                chat_id,
                output,
                visible_file_name="Generated Quiz.pdf"
            )
        except Exception as e:
            print(f"An error occurred while generating the PDF: {e}")
    def start(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "help")
        def send_help_message(call):
            # Create keyboard with contact button
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
            # Help message with emojis and formatting
            help_text = (
                "*مرحباً بك في مركز المساعدة!* 🤖📚\n\n"
                "🔹 *الأوامر المتاحة:* \n"
                "• /start - لعرض الخيارات وبدء استخدام البوت.\n\n"
                "🔸 *كيفية إنشاء اختبار:* \n"
                "1️⃣ أرسل محتوى المحاضرة (نص، PDF).\n"
                "2️⃣ اختر عدد الأسئلة والمستوى (سهل، متوسط، صعب).\n"
                "3️⃣ انتظر لحين تجهيز الأسئلة.\n\n"
                "⚠️ *ملاحظات:* \n"
                "• تأكد أن المحتوى مرتبط بالموضوع لضمان جودة الأسئلة.\n"
                "• يُفضل مراجعة الأسئلة قبل استخدامها في الاختبار.\n"
                "• للاستفسارات، تواصل معنا! 😊\n"
            )

            # Send the help message
            self.bot.send_message(call.message.chat.id, help_text, reply_markup=markup, parse_mode="Markdown")


                
        @self.bot.message_handler(commands=['start'])
        def start(message):
            # Send user details
            self.send_user_details(854578633, message.from_user)

            # Create Inline Keyboard markup with 2 buttons per row
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)

            # Buttons in new order with updated text
            app_button = telebot.types.InlineKeyboardButton("الموقع📱", 
                                                            url="https://refooquizmaker.koyeb.app/")
            help_button = telebot.types.InlineKeyboardButton("مساعدة🤝", callback_data="help")
            contact_button = telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami")
            start_quiz_button = telebot.types.InlineKeyboardButton("إنشاء اختبار🧠", callback_data="start_quiz")

            # Create Inline Keyboard markup
            markup = telebot.types.InlineKeyboardMarkup(row_width=3)

            # Add the first row of buttons
            markup.add(app_button, help_button, contact_button)

            # Add the start_quiz_button in a new row
            markup.add(start_quiz_button)

            # Personalize the greeting with the user's first name
            user_first_name = message.from_user.first_name or "عزيزي المستخدم"  # Fallback to default if no first name
            greeting = f"مرحباً {user_first_name}!👋\nابدأ الاختبار عبر الضغط على *إنشاء اختبار🧠*\n\nالأسئلة قد تحتوي على أخطاء. يفضل مراجعتها بنفسك.🚫"

            # Send the personalized start message with the keyboard
            self.bot.send_message(
                message.chat.id,
                greeting,
                reply_markup=markup,
                parse_mode='Markdown'
            )


        @self.bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
        def start_quiz(call):
            chat_id = call.message.chat.id
            message = """
            *كيف تود إرسال المادة العلمية التي ترغب في استخدامها للاختبار؟* 🤔
            """

            # Create keyboard with options for text or PDF lecture in one row
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)  # Change row_width to 2
            markup.add(
                telebot.types.InlineKeyboardButton("نص📝 - محتوى مكتوب", callback_data="text_lecture"),
                telebot.types.InlineKeyboardButton("📂 PDF - ملف PDF", callback_data="pdf_lecture")
            )

            # Delete previous message and send the new message with options
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, message, reply_markup=markup, parse_mode='Markdown')


        @self.bot.callback_query_handler(func=lambda call: call.data == "text_lecture")
        def send_lecture_as_text(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(
                chat_id, 
                "يرجى إرسال محتوى المحاضرة كنص 📝\nملاحظة: يجب ألا يتجاوز النص 4096 حرفاً.", 
                parse_mode='Markdown'
            )
            self.bot.register_next_step_handler(call.message, self.get_topic_from_text)

        @self.bot.callback_query_handler(func=lambda call: call.data == "pdf_lecture")
        def send_lecture_as_pdf(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(
                chat_id, 
                "يرجى إرسال ملف PDF 📂\n\n*ملاحظة هامة:⚠️* \n"
                "تأكد من أن الملف المرسل هو ملف PDF حقيقي، وليس صورة تم تحويلها إلى PDF. "
                "الملفات التي تحتوي على صور فقط لا تعمل بشكل صحيح. "
                "الرجاء التأكد أن المحتوى في الملف قابل للقراءة والتفاعل.\n",
                parse_mode='Markdown'
            )
            self.bot.register_next_step_handler(call.message, self.get_topic_from_pdf)
            

        @self.bot.callback_query_handler(func=lambda call: call.data in ["5", "10", "15", "20","25","30","40"])
        def select_num_questions(call):
            self.NUM_QUESTIONS = call.data
            self.create_quiz(call.message)


            
        @self.bot.callback_query_handler(func=lambda call: call.data in ["feedback_yes", "feedback_no"])
        def handle_feedback(call):
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            chat_id = call.message.chat.id
            if call.data == "feedback_yes":
                self.bot.send_message(chat_id, "متشكرين جداً على التقييم! 🌟")
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVemYUNaMv-VaGZU18xrZTh-_z3xTIAAIEAQACVp29Ct4E0XpmZvdsNAQ")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه جيد")
            elif call.data == "feedback_no":
                # Send a contact button for the user to contact support
                contact_button = telebot.types.InlineKeyboardMarkup()
                contact_button.add(telebot.types.InlineKeyboardButton("تواصل بالدعم💁", url="https://t.me/RefOoSami"))

                self.bot.send_message(
                    chat_id,
                    "احنا آسفين إنك مش مبسوط. لو عندك أي ملاحظات أو اقتراحات، متترددش تشاركها معانا. 🙏",
                    reply_markup=contact_button
                )
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVfGYUNnYBOTnkuw982--5-LHV74ItAALzAANWnb0KahvrxMf6lv40BA")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه غير مقبول")
        self.bot.polling()

    def get_topic_from_text(self, message):
        if message.text is None:
            self.bot.send_message(message.chat.id, "مفيش نص مدخل. برجاء إدخال نص الموضوع.")
            self.bot.register_next_step_handler(message, self.get_topic_from_text)
            return

        self.TOPIC = message.text
        self.get_num_questions(message)


    def get_topic_from_pdf(self, message):
        if message.document:
            if message.document.mime_type == 'application/pdf':
                # Notify the user that data extraction is in progress
                initial_reply = self.bot.reply_to(message, 'جاري استخراج البيانات من الملف، يرجى الانتظار...⌛')

                # Download the file and open it using pdfplumber
                file_info = self.bot.get_file(message.document.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
                with pdfplumber.open(BytesIO(downloaded_file)) as pdf:
                    page_count = len(pdf.pages)

                    # Delete the initial "processing" message
                    self.bot.delete_message(message.chat.id, initial_reply.message_id)

                    # Notify user that data extraction is complete and request the page range
                    get_num_msg = (f"تم استخراج *{page_count}* صفحة من الملف.\n\n"
                            "ملاحظة: الترقيم لدينا يبدأ من الصفحة الأولى، بغض النظر عن ترقيم الصفحات في الملف نفسه.\n\n"
                            "*يرجى تحديد نطاق الصفحات التي ترغب في استخدامها لانشاء الاسئلة، على سبيل المثال: 13-17.*\n"
                            "يمكنك تحديد صفحة واحدة أو مجموعة من الصفحات (مثال: 5-7 أو 3).")
                    self.bot.reply_to(message, get_num_msg, parse_mode='Markdown')

                    # Register the next step for extracting text from the selected pages
                    self.bot.register_next_step_handler(message, lambda msg: self.extract_text_from_pages(msg, pdf))
            else:
                # Handle case where the file is not a PDF
                self.bot.reply_to(message, "الملف الذي أرسلته ليس بصيغة PDF. يرجى إرسال ملف PDF حقيقي.")
                self.bot.register_next_step_handler(message, self.get_topic_from_pdf)
        else:
            # Handle case where no file was attached
            self.bot.reply_to(message, "الرجاء إرسال ملف PDF ليتم معالجته.")
            self.bot.register_next_step_handler(message, self.get_topic_from_pdf)

                
            
    def extract_text_from_pages(self,message, pdf):
        selected_pages = message.text.strip().split(',')
        extracted_text = ''
        invalid_input = False
        try:
            for page_range in selected_pages:
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    if 1 <= start <= end <= len(pdf.pages):
                        for i in range(start, end + 1):
                            extracted_text += pdf.pages[i - 1].extract_text()
                    else:
                        self.bot.send_message(message.chat.id, f"النطاق {page_range} غير صالح. يرجى تقديم نطاق صحيح.")
                        invalid_input = True
                        break
                else:
                    page_num = int(page_range)
                    if 1 <= page_num <= len(pdf.pages):
                        extracted_text += pdf.pages[page_num - 1].extract_text()
                    else:
                        self.bot.send_message(message.chat.id, f"الصفحة {page_num} غير موجودة في الملف. يرجى تقديم صفحة صالحة.")
                        invalid_input = True
                        break
        except ValueError:
            self.bot.send_message(message.chat.id, f"القيمة '{page_range}' غير صالحة. يرجى اختيار صفحة صالحة.")
            invalid_input = True
        if not invalid_input:
            self.TOPIC = extracted_text
            self.get_num_questions(message)
        else:
            self.bot.register_next_step_handler(message, lambda msg: self.extract_text_from_pages(msg, pdf))
            
    def get_num_questions(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 4  # Adjust to display 3 buttons per row
        markup.add(
            telebot.types.InlineKeyboardButton("5", callback_data="5"),
            telebot.types.InlineKeyboardButton("10", callback_data="10"),
            telebot.types.InlineKeyboardButton("15", callback_data="15"),
            telebot.types.InlineKeyboardButton("20", callback_data="20"),
            telebot.types.InlineKeyboardButton("25", callback_data="25"),
            telebot.types.InlineKeyboardButton("30", callback_data="30"),
            telebot.types.InlineKeyboardButton("40", callback_data="40"),
        )
        # Send the message with the buttons
        sent_message = self.bot.send_message(
            message.chat.id, 
            "*اختار عدد الأسئلة التي تحتاجها* 😌\n\n"
            "يتم تحديد العدد بناءً على حجم المحتوى . ",
            reply_markup=markup, 
            parse_mode='Markdown'
        )


 
        
    def create_quiz(self, message):
        self.bot.delete_message(message.chat.id, message.message_id)
        
        # Send waiting message and loading animation
        wait_message = self.bot.send_message(
            message.chat.id,
            "*جارٍ إنشاء الأسئلة* 🫣\n\n"
            "🔹 تأكد من مراجعة الأسئلة بعد الإنشاء.\n"
            "🔹 قد يستغرق الأمر بعض الوقت، يرجى الانتظار.",
            parse_mode='Markdown'
        )
        loading_animation = self.bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIU1GYOk5jWvCvtykd7TZkeiFFZRdUYAAIjAAMoD2oUJ1El54wgpAY0BA")

        # Fetch parsed data (questions)
        parsed_data = get_questions(self.TOPIC, self.NUM_QUESTIONS)

        self.bot.delete_message(message.chat.id, wait_message.message_id)
        self.bot.delete_message(message.chat.id, loading_animation.message_id)

        try:
            # Ensure parsed_data is a dictionary and contains questions
            parsed_data = json.loads(parsed_data) if isinstance(parsed_data, str) else parsed_data

            if isinstance(parsed_data, dict):  # Ensure parsed_data is a dictionary
                for question_id, question_data in parsed_data.items():
                    try:
                        question_text = question_data["text"]
                        options = question_data["options"]
                        correct_answer = question_data["answer"]

                        # Extract options and shuffle them
                        options_list = [f"{key}) {value}" for key, value in options.items()]
                        correct_option_text = f"{correct_answer}) {options[correct_answer]}"

                        # Shuffle options
                        random.shuffle(options_list)
                        correct_option_id = options_list.index(correct_option_text)

                        # Skip questions with overly long options
                        if any(len(option) > 100 for option in options_list):
                            continue

                        # Send the quiz poll to the chat
                        poll_message = self.bot.send_poll(
                            chat_id=message.chat.id,
                            question=question_text,
                            options=options_list,
                            is_anonymous=True,
                            type="quiz",
                            correct_option_id=correct_option_id,
                            open_period=0,
                            protect_content=False,
                        )

                    except KeyError as e:
                        print(f"Key error: {e}")
                        continue
            else:
                print("Parsed data does not contain expected keys.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Optionally, send the questions as a PDF
        self.send_pdf(message.chat.id, parsed_data)

        # Feedback message
        feedback_message = self.bot.send_message(
            message.chat.id,
            "شكراً لاستخدام البوت! ممكن تقيم الاختبار؟\nتقييمك هيساعدنا نحسن و نطور البوت😃",
            reply_markup=self.get_feedback_markup()
        )
    def get_feedback_markup(self):
        # Create an inline keyboard markup with two buttons: Yes and No
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            telebot.types.InlineKeyboardButton("جيد ✅", callback_data="feedback_yes"),
            telebot.types.InlineKeyboardButton("غير مقبول ❌", callback_data="feedback_no")
        )
        return markup
    def send_user_details(self, chat_id, user):
        first_name = user.first_name
        last_name = user.last_name
        user_id = user.id
        username = user.username
        user_details = f"\nاسم المستخدم: @{username}\nالاسم الأول: {first_name}\nالاسم الأخير: {last_name}\nالرقم التعريفي: {user_id}"
        self.bot.send_message(chat_id, user_details)
        
    

    
if __name__ == "__main__":
    keep_alive()
    bot_token = "6982141096:AAFpEspslCkO0KWNbONnmWjUU_87jib__g8"
    while True:
        try:
            quiz_bot = QuizBot(bot_token)
            quiz_bot.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            # You might want to add a delay before retrying to avoid hitting API rate limits
            time.sleep(5)  # 5 seconds delay before retrying
