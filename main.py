import telebot
import pdfplumber
from io import BytesIO
from get_questions import get_questions
from keep_alive import keep_alive
import time
from fpdf import FPDF

class QuizBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.TOPIC = None
        self.NUM_QUESTIONS = None
        self.DIFF = None


    def send_pdf(self, chat_id, questions):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add the title
        pdf.cell(200, 10, txt="Generated Quiz", ln=True, align='C')
        pdf.ln(10)

        # Iterate over questions to render them in the PDF
        for i, (q_num, q_data) in enumerate(questions.items(), start=1):
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, f"{i}. {q_data['text']}", ln=True)  # Question text
            pdf.set_font("Arial", size=12)

            # Render each option
            for opt, ans in q_data["options"].items():
                # Highlight the correct answer in green
                if opt == q_data["answer"]:  # Assuming `correct` contains the correct option key
                    pdf.set_text_color(0, 128, 0)  # Green color
                else:
                    pdf.set_text_color(0, 0, 0)  # Black color
                
                pdf.cell(0, 10, f"   {opt}. {ans}", ln=True)

            pdf.ln(5)

        # Write PDF content to a BytesIO object
        output = BytesIO()
        pdf_data = pdf.output(dest='S').encode('latin1', 'ignore')  # Add 'ignore' to safely handle characters
        output.write(pdf_data)
        output.seek(0)  # Move the cursor to the beginning of the BytesIO object

        # Sending the document via Telegram bot with a proper filename
        self.bot.send_document(
            chat_id,
            output,
            visible_file_name="MyQuiz.pdf"
        )




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
            app_button = telebot.types.InlineKeyboardButton("التطبيق📱", 
                                                            url="https://www.mediafire.com/file/qqu7v8v6ufjh43o/RefOo+Quiz+V1.0.apk/file")
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
            

        @self.bot.callback_query_handler(func=lambda call: call.data in ["5", "10", "20", "40", "60", "80"])
        def select_num_questions(call):
            self.NUM_QUESTIONS = call.data
            self.get_difficulty_level(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data in ["easy", "medium", "hard",'mixed'])
        def select_difficulty_level(call):
            self.DIFF = call.data
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
        markup.row_width = 3  # Adjust to display 3 buttons per row
        markup.add(
            telebot.types.InlineKeyboardButton("5", callback_data="5"),
            telebot.types.InlineKeyboardButton("10", callback_data="10"),
            telebot.types.InlineKeyboardButton("20", callback_data="20"),
            telebot.types.InlineKeyboardButton("40", callback_data="40"),
            telebot.types.InlineKeyboardButton("60", callback_data="60"),
            telebot.types.InlineKeyboardButton("80", callback_data="80")
        )
        # Send the message with the buttons
        sent_message = self.bot.send_message(
            message.chat.id, 
            "*اختار عدد الأسئلة التي تحتاجها* 😌\n\n"
            "يتم تحديد العدد بناءً على حجم المحتوى وصعوبة الأسئلة. ",
            reply_markup=markup, 
            parse_mode='Markdown'
        )


    def get_difficulty_level(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 3  # Set the number of buttons per row to 3
        markup.add(
            telebot.types.InlineKeyboardButton("سهل😌", callback_data="easy"),
            telebot.types.InlineKeyboardButton("متوسط🤕", callback_data="medium"),
            telebot.types.InlineKeyboardButton("صعب😩", callback_data="hard")
        )
        # Add the "ميكس" button in a new row
        markup.add(
            telebot.types.InlineKeyboardButton("ميكس💀", callback_data="mixed")
        )
        
        self.bot.delete_message(message.chat.id, message.message_id)
        
        # Send the message with the buttons
        self.bot.send_message(
            message.chat.id, 
            "اختار مستوى الصعوبة 🏋️‍♂️",  # Added an emoji that represents difficulty (weightlifting)
            reply_markup=markup, 
            parse_mode="Markdown"
        )

        
        
    def create_quiz(self, message):
        self.bot.delete_message(message.chat.id, message.message_id)
        wait_message = self.bot.send_message(
            message.chat.id, 
            "*جارٍ إنشاء الأسئلة* 🫣\n\n"
            "🔹 تأكد من مراجعة الأسئلة بعد الإنشاء.\n"
            "🔹 قد يستغرق الأمر بعض الوقت، يرجى الانتظار.",
            parse_mode='Markdown')        
        loading_animation = self.bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIU1GYOk5jWvCvtykd7TZkeiFFZRdUYAAIjAAMoD2oUJ1El54wgpAY0BA")
        
        def send_error_message():
            self.bot.delete_message(message.chat.id, wait_message.message_id)
            self.bot.delete_message(message.chat.id, loading_animation.message_id)
            self.bot.send_message(message.chat.id, "حصلت مشكلة أثناء إنشاء الأسئلة. حاول تاني لو سمحت.")
        
        if self.DIFF == "mixed":
            for difficulty in ["easy", "medium", "hard"]:
                num_questions_per_level = int(self.NUM_QUESTIONS) // 3
                parsed_data = get_questions(difficulty, num_questions_per_level, self.TOPIC)
                
                if not isinstance(parsed_data, dict):
                    send_error_message()
                    return
                
                try:
                    self.bot.delete_message(message.chat.id, wait_message.message_id)
                    self.bot.delete_message(message.chat.id, loading_animation.message_id)
                except:
                    pass
                
                diff_levels = {
                    "easy": "سهل",
                    "medium": "متوسط",
                    "hard": "صعب"
                }
                diff_level = diff_levels.get(difficulty)
                self.bot.send_message(message.chat.id, f"أسئلة بمستوى صعوبة *{diff_level}*🎉", parse_mode='Markdown')
                
                for question_number, question_data in parsed_data.items():
                    try:
                        question_text = question_data["text"]
                        options = question_data["options"]
                        correct_answer = question_data["answer"]
                    except KeyError:
                        continue
                    
                    options_list = [f"{key}. {value}" for key, value in options.items()]
                    
                    if any(len(option) > 100 for option in options_list):
                        continue
                    
                    poll_message = self.bot.send_poll(
                        chat_id=message.chat.id,
                        question=question_text,
                        options=options_list,
                        is_anonymous=True,
                        type="quiz",
                        correct_option_id=list(options.keys()).index(correct_answer),
                        open_period=0,
                        protect_content=False
                    )
        else:
            parsed_data = get_questions(self.DIFF, self.NUM_QUESTIONS, self.TOPIC)
            
            if not isinstance(parsed_data, dict):
                send_error_message()
                return
            
            self.bot.delete_message(message.chat.id, wait_message.message_id)
            self.bot.delete_message(message.chat.id, loading_animation.message_id)
            
            try:
                for question_number, question_data in parsed_data.items():
                    try:
                        question_text = question_data["text"]
                        options = question_data["options"]
                        correct_answer = question_data["answer"]
                    except KeyError:
                        print(question_data)
                        continue
                    
                    options_list = [f"{key}. {value}" for key, value in options.items()]
                    
                    if any(len(option) > 100 for option in options_list):
                        continue
                    
                    poll_message = self.bot.send_poll(
                        chat_id=message.chat.id,
                        question=question_text,
                        options=options_list,
                        is_anonymous=True,
                        type="quiz",
                        correct_option_id=list(options.keys()).index(correct_answer),
                        open_period=0,
                        protect_content=False
                    )
            except Exception as e:
                print(f"An error occurred: {e}")
        self.send_pdf(message.chat.id, parsed_data)
        feedback_message = self.bot.send_message(message.chat.id,"شكراً لاستخدام البوت! ممكن تقيم الاختبار؟\nتقييمك هيساعدنا نحسن و نطور البوت😃",reply_markup=self.get_feedback_markup())
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
        user_details = f"مستخدم جديد بدأ يستخدم البوت:\n\nاسم المستخدم: @{username}\nالاسم الأول: {first_name}\nالاسم الأخير: {last_name}\nالرقم التعريفي: {user_id}"
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

