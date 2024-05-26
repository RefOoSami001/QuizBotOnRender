import telebot
import pdfplumber
from io import BytesIO
from get_questions import get_questions
from keep_alive import keep_alive
class QuizBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.TOPIC = None
        self.NUM_QUESTIONS = None
        self.DIFF = None


    def start(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "help")
        def send_help_message(call):
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
            help_text = (
                "*مرحبًا بك في مركز المساعدة !* 🤖📚\n\n"
                "إليك الأوامر المتاحة:\n"
                "/start - يُستخدم لبدء استخدام البوت وعرض الخيارات المتاحة.\n"
                "/addpremium - يُستخدم لإضافة مستخدمين إلى الخطة المدفوعة، حيث يمكنهم الحصول على ميزات إضافية (مخصص للمشرفين).\n"
                "/removepremium - يُستخدم لإزالة مستخدمين من الخطة المدفوعة (مخصص للمشرفين).\n\n"
                "*لإنشاء اختبار، اتبع الخطوات التالية:*\n"
                "1. أرسل محتوى المحاضرة كنص أو ملف PDF أو صورة.\n"
                "2. اختر عدد الأسئلة التي تريد تضمينها في الاختبار.\n"
                "3. حدد مستوى الصعوبة المفضل للأسئلة (سهل، متوسط، أو صعب).\n"
                "4. انتظر حتى يقوم البوت بإنشاء أسئلة الاختبار استنادًا إلى ما قمت بتحديده.\n\n"
                "*ملاحظة:*\n"
                "- يُرجى التأكد من أن المحتوى المرسل يتعلق بموضوع محدد لضمان جودة الأسئلة المولدة.\n"
                "- يُنصح بالتحقق من الأسئلة المولدة قبل استخدامها في الاختبار، وذلك لضمان الدقة والصحة.\n"
                "- إذا كان لديك أي استفسارات أو تحتاج إلى مساعدة، فلا تتردد في التواصل! 😊\n"
            )
            self.bot.send_message(call.message.chat.id, help_text, reply_markup=markup,parse_mode="Markdown")

                
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.send_user_details(854578633, message.from_user)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row_width = 2

            # Add "إنشاء اختبار" button in one row
            markup.add(telebot.types.InlineKeyboardButton("إنشاء اختبار🧠", callback_data="start_quiz"))

            # Create a new row and add the other two buttons
            new_row = []
            new_row.append(telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
            new_row.append(telebot.types.InlineKeyboardButton("مساعدة🤝", callback_data="help"))
            markup.add(*new_row)

            disclaimer_message = (
                "يرجى ملاحظة أن الأسئلة المولدة قد تحتوي على أخطاء. هذا البوت يستخدم لمساعدتك في إعداد الأسئلة، "
                "وليس لتوليد الاختبارات بالكامل. ننصح بالتحقق من الأسئلة المولدة بنفسك، وجب التنويه.🚫"
            )

            self.bot.send_message(
                message.chat.id,
                f"أهلاً👋\nللبدء اضغط على *إنشاء اختبار🧠*\n\n{disclaimer_message}",
                reply_markup=markup,
                parse_mode='Markdown'
            )


        @self.bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
        def start_quiz(call):
            chat_id = call.message.chat.id
            message = """
                *مرحبًا👋\n\n كيف تفضل إرسال المادة العلمية؟ 🤔*
            """

            markup = telebot.types.InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(telebot.types.InlineKeyboardButton("نص📝", callback_data="text_lecture"),
                        telebot.types.InlineKeyboardButton("🗃️PDF", callback_data="pdf_lecture"))
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, message, reply_markup=markup,parse_mode='Markdown')

        @self.bot.callback_query_handler(func=lambda call: call.data == "text_lecture")
        def send_lecture_as_text(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, "برجاء ارسال محتوي المحاضرة في رسالة📝\n*يجب ارسال مادة علمية وليس عنوان لموضوع!*",parse_mode='Markdown')
            self.bot.register_next_step_handler(call.message, self.get_topic_from_text)

        @self.bot.callback_query_handler(func=lambda call: call.data == "pdf_lecture")
        def send_lecture_as_pdf(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, "برجاء ارسال ملف PDF🗃️\nيجب ان يكون الملف من نوع PDF لا نقبل صور محولة الي PDF.")
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
                self.bot.send_message(chat_id, "شكراً جزيلاً على التقييم! 🌟")
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVemYUNaMv-VaGZU18xrZTh-_z3xTIAAIEAQACVp29Ct4E0XpmZvdsNAQ")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه جيد")
            elif call.data == "feedback_no":
                # Send a contact button for the user to contact support
                contact_button = telebot.types.InlineKeyboardMarkup()
                contact_button.add(telebot.types.InlineKeyboardButton("تواصل بالدعم💁", url="https://t.me/RefOoSami"))

                self.bot.send_message(
                    chat_id,
                    "نأسف لسماع ذلك. إذا كان لديك أي ملاحظات أو اقتراحات، فلا تتردد في مشاركتها معنا. 🙏",
                    reply_markup=contact_button
                )
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVfGYUNnYBOTnkuw982--5-LHV74ItAALzAANWnb0KahvrxMf6lv40BA")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه غير مقبول")
        self.bot.polling()

    def get_topic_from_text(self, message):
        if message.text is None:
            self.bot.send_message(message.chat.id, "لم يتم إدخال نص. برجاء إدخال نص موضوع.")
            self.bot.register_next_step_handler(message, self.get_topic_from_text)
            return

        if len(message.text) < 60:  # Adjust the threshold as needed
            self.bot.send_message(message.chat.id, "المحتوى الذي أدخلته قصير جدًا. برجاء إدخال محتوى أطول.")
            self.bot.register_next_step_handler(message, self.get_topic_from_text)
            return

        self.TOPIC = message.text
        self.get_num_questions(message)


    def get_topic_from_pdf(self, message):
        if message.document:
            if message.document.mime_type == 'application/pdf':
                initial_reply = self.bot.reply_to(message, 'جاري استخراج البيانات برجاء الانتظار⌛')
                file_info = self.bot.get_file(message.document.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
                with pdfplumber.open(BytesIO(downloaded_file)) as pdf:
                    page_count = len(pdf.pages)
                    self.bot.delete_message(message.chat.id, initial_reply.message_id)
                    get_num_msg = (f"تم استخراج *{page_count}* صفحة من الملف. الترقيم بالنسبة لنا يبدء من الصفحة الاولي بغض النظر عن ترقيم الصفحات في الملف"
                                    "\n*يُرجى تحديد الصفحات المطلوبة، مثال: 17-13. *")
                    self.bot.reply_to(message, get_num_msg,parse_mode='Markdown')
                    self.bot.register_next_step_handler(message, lambda msg: self.extract_text_from_pages(msg, pdf))
            else:
                self.bot.reply_to(message, "الملف الذي قمت بإرساله ليس من نوع PDF. برجاء إرسال ملف PDF.")
                self.bot.register_next_step_handler(message, self.get_topic_from_pdf)
        else:
            self.bot.reply_to(message, "الرجاء إرسال ملف PDF.")
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
        markup.row_width = 2
        markup.add(
            telebot.types.InlineKeyboardButton("10", callback_data="10"),
            telebot.types.InlineKeyboardButton("5", callback_data="5"),
            telebot.types.InlineKeyboardButton("40 (Pro)🌟", callback_data="40"),
            telebot.types.InlineKeyboardButton("20 (Pro)🌟", callback_data="20"),
            telebot.types.InlineKeyboardButton("80 (Pro)🌟", callback_data="80"),
            telebot.types.InlineKeyboardButton("60 (Pro)🌟", callback_data="60")
        )
        # Send the message with the buttons
        sent_message = self.bot.send_message(message.chat.id, "*اختر عدد الأسئلة المطلوبة *😌\nقد يختلف عدد الاسئلة حسب كمية المحتوي وصعوبه الاسئلة", reply_markup=markup,parse_mode='Markdown')

    def get_difficulty_level(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            telebot.types.InlineKeyboardButton("متوسط🤕", callback_data="medium"),
            telebot.types.InlineKeyboardButton("سهل😌", callback_data="easy"),
            telebot.types.InlineKeyboardButton("ميكس💀", callback_data="mixed"),
            telebot.types.InlineKeyboardButton("صعب😩", callback_data="hard"),

        )
        self.bot.delete_message(message.chat.id, message.message_id)
        # Send the message with the buttons
        self.bot.send_message(message.chat.id, "اختر مستوي الصعوبه 🏋\nأنصح باختيار *ميكس* لإنشاء اسئلة بمستويات مختلفه🎉", reply_markup=markup,parse_mode="Markdown")
        
        
    def create_quiz(self, message):
        self.bot.delete_message(message.chat.id, message.message_id)
        wait_message = self.bot.send_message(message.chat.id, "*جارٍ إنشاء الأسئلة* 🫣\n🔹قد يختلف عدد الأسئلة اعتمادًا على المحتوى المقدم\n🔹برجاء مراجعة الاسئلة هناك نسبة خطأ!\n🔹برجاء الانتظار، قد يستغرق الأمر مدة تصل إلى *5* دقائق...", parse_mode='Markdown')
        loading_animation = self.bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIU1GYOk5jWvCvtykd7TZkeiFFZRdUYAAIjAAMoD2oUJ1El54wgpAY0BA")
        
        def send_error_message():
            self.bot.delete_message(message.chat.id, wait_message.message_id)
            self.bot.delete_message(message.chat.id, loading_animation.message_id)
            self.bot.send_message(message.chat.id, "حدث خطأ أثناء إنشاء الأسئلة. برجاء المحاولة مرة أخرى.")
        
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
                self.bot.send_message(message.chat.id, f"اسئلة ذات مستوي صعوبه *{diff_level}*🎉", parse_mode='Markdown')
                
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
        
        feedback_message = self.bot.send_message(
            message.chat.id,
            "شكراً لاستخدام البوت! هل يمكنك تقييم الاختبار؟\nيساعدنا تقييمك في تحسين وتطوير البوت😃",
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
        user_details = f"New user started ChatBot:\n\nUsername: @{username}\nFirst Name: {first_name}\nLast Name: {last_name}\nUser ID: {user_id}"
        self.bot.send_message(chat_id, user_details)
        
    
if __name__ == "__main__":
    bot_token = "6306869044:AAGh79xhZ4tOWNOPjk29r6uWvgPTg-Wyc2s"
    while True:
        try:
            keep_alive()
            quiz_bot = QuizBot(bot_token)
            quiz_bot.start()
        except:
            pass