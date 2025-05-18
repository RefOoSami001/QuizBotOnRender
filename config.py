import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not found, using environment variables directly")

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '6982141096:AAFpEspslCkO0KWNbONnmWjUU_87jib__g8')

# Admin chat ID for notifications
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '854578633'))

# Minimum text length required for generating questions
MIN_TEXT_LENGTH = int(os.getenv('MIN_TEXT_LENGTH', '30'))

# Difficulty Levels
DIFFICULTY_LEVELS = {
    'en': {
        'easy': '🟢 Easy',
        'medium': '🟡 Medium',
        'hard': '🔴 Hard',
        'all': '🌈 All Levels'
    },
    'ar': {
        'easy': '🟢 سهل',
        'medium': '🟡 متوسط',
        'hard': '🔴 صعب',
        'all': '🌈 جميع المستويات'
    }
}

# Difficulty Emojis
DIFFICULTY_EMOJIS = {
    'EASY': '🟢',
    'MEDIUM': '🟡',
    'HARD': '🔴',
    'UNKNOWN': '⚪'
}

# Question Count Options
QUESTION_COUNTS = {
    'en': {
        '5': '5 Questions',
        '10': '10 Questions',
        '15': '15 Questions',
        '20': '20 Questions',
        '25': '25 Questions',
        '30': '30 Questions',
        '40': '40 Questions'
    },
    'ar': {
        '5': '5 أسئلة',
        '10': '10 أسئلة',
        '15': '15 سؤال',
        '20': '20 سؤال',
        '25': '25 سؤال',
        '30': '30 سؤال',
        '40': '40 سؤال'
    }
}

# Message Templates
MESSAGES = {
    'en': {
        'welcome': (
            "👋 *Welcome to the MCQ Generator Bot!*\n\n"
            "🎓 I can help you generate multiple-choice questions from your study materials.\n\n"
            "✨ *Features:*\n"
            "• Generate questions from text\n"
            "• Generate questions from PDF files\n"
            "• Interactive quiz format\n"
            "• Detailed explanations\n\n"
            "Please choose an option below:"
        ),
        'help': (
            "❓ *Help & Tips*\n\n"
            "📝 *How to use the bot:*\n"
            "1. Choose 'Create MCQ Questions'\n"
            "2. Select input method (Text/PDF)\n"
            "3. Send your material\n"
            "4. Get your questions!\n\n"
            "💡 *Tips for best results:*\n"
            "• Use clear, well-structured text\n"
            "• For PDFs, select relevant pages\n"
            "• Try different difficulty levels\n"
            "• Keep text length reasonable\n\n"
            "❓ *Common questions:*\n"
            "• *Q:* How many questions will I get?\n"
            "• *A:* Usually 10-20 questions per submission\n\n"
            "• *Q:* Can I get questions in different languages?\n"
            "• *A:* Currently supports English only\n\n"
            "Need more help? Contact the developer!"
        ),
        'contact': (
            "📧 *Contact Information*\n\n"
            "Feel free to reach out if you have any questions or suggestions!\n\n"
            "📧 Email: raafatsami101@gmail.com\n"
            "📱 Telegram: @RefOoSami\n"
            "📞 Whatsapp: +201011508719\n"
        ),
        'model_selection': (
            "🤖 *Select AI Model*\n\n"
            "Choose which AI model to use for generating questions:\n\n"
            "• *Model 1*: Standard model with explanations\n"
            "• *Model 2*: Advanced model with customizable question count\n\n"
            "💡 *Tip:* Model 2 is better for generating specific number of questions"
        ),
        'question_count': (
            "📊 *Select Number of Questions*\n\n"
            "Choose how many questions you want to generate:\n\n"
            "💡 *Tip:* More questions may take longer to generate"
        ),
        'select_language': (
            "🌐 *Select Your Language*\n\n"
            "Please choose your preferred language:"
        ),
        'language_changed': (
            "✅ Language set to English"
        ),
        'input_method': (
            "📝 *Choose Input Method*\n\n"
            "How would you like to send your study material?\n\n"
            "• 📄 *Text*: Send your material as plain text\n"
            "• 📚 *PDF*: Upload a PDF file and select pages\n\n"
            "💡 *Tip:* Text input is faster, while PDFs are better for formatted content."
        ),
        'send_text': (
            "📝 *Send Your Text*\n\n"
            "Please send your study material as text.\n"
            "I'll analyze it and generate multiple-choice questions.\n\n"
            "💡 *Tip:* Your text should be at least 30 characters long for better results."
        ),
        'text_too_short': (
            "❌ *Text Too Short*\n\n"
            "The text you provided is too short to generate meaningful questions.\n"
            "Please send a longer text (at least 30 characters)."
        ),
        'send_pdf': (
            "📚 *Send Your PDF*\n\n"
            "Please send your PDF file.\n"
            "After receiving the file, I'll ask you to specify which pages to analyze.\n\n"
            "💡 *Tip:* Make sure your PDF is readable and not password-protected."
        ),
        'processing_pdf': "⏳ Processing your PDF file...",
        'pdf_processed': (
            "✅ PDF processed successfully!\n\n"
            "📚 The document has *{0}* pages.\n\n"
            "Please send the page range in the format:\n"
            "`start-end` (e.g., `1-5`)\n\n"
            "💡 *Tip:* You can analyze the entire document by sending `1-{0}`"
        ),
        'extracting_text': "⏳ Extracting text from PDF pages...",
        'text_extracted': "✅ Text extracted successfully!\n\n⏳ Generating questions...",
        'analyzing_text': "⏳ Analyzing your text and generating questions...",
        'no_questions': (
            "❌ No questions could be generated from the provided material.\n\n"
            "Try:\n"
            "• Using different material\n"
            "• Selecting a different difficulty level\n"
            "• Making the text more detailed"
        ),
        'questions_generated': "✅ Generated {0} questions!\n\n📝 Sending questions...",
        'question_header': "📝 Question {0}/{1}\n\n{2}",
        'completion': (
            "🎉 *Questions Generated Successfully!*\n\n"
            "📊 *Summary:*\n"
            "• Total Questions: {0}\n"
            "• Questions Sent: {1}\n"
            "• Questions Skipped: {2}\n\n"
            "💡 *Tips:*\n"
            "• Try different materials for varied questions\n"
            "• Use the help menu for more tips\n"
            "• Share your feedback with the developer"
        ),
        'feedback_request': (
            "📝 *How was your experience?*\n\n"
            "Please rate the quality of the generated questions:"
        ),
        'feedback_thanks': (
            "🙏 *Thank you for your feedback!*\n\n"
            "Your input helps us improve the service."
        ),
        'feedback_comment': (
            "💬 *Additional Comments*\n\n"
            "If you'd like to share more detailed feedback, please send a message. Or tap Skip if you're done."
        ),
        'feedback_skip': "⏭️ Skip",
        'feedback_excellent': "⭐⭐⭐⭐⭐ Excellent",
        'feedback_good': "⭐⭐⭐⭐ Good",
        'feedback_average': "⭐⭐⭐ Average",
        'feedback_poor': "⭐⭐ Poor",
        'feedback_very_poor': "⭐ Very Poor",
        'invalid_pdf': "❌ Please send a PDF file.",
        'pdf_error': "❌ Error processing PDF: {0}\n\nPlease try again with a different file.",
        'invalid_range': "❌ Invalid page range. Please send the range in the format `start-end` (e.g., `1-5`).",
        'error': (
            "❌ *An error occurred*\n\n"
            "Error details: `{0}`\n\n"
            "Please try again or contact the developer if the problem persists."
        ),
        'returning_to_menu': "🔙 Returning to main menu...",
        'main_menu': "🔙 *Main Menu*\n\nPlease select an option:",
        'create_mcq': "📝 Create MCQ Questions",
        'contact_dev': "👨‍💻 Contact Developer",
        'help_btn': "❓ Help & Tips",
        'model1': "🤖 AI Model 1",
        'model2': "🤖 AI Model 2",
        'back_main': "🔙 Back to Main Menu",
        'back': "🔙 Back",
        'text_btn': "📄 Send Text",
        'pdf_btn': "📚 Send PDF"
    },
    'ar': {
        'welcome': (
            "👋 *مرحبا بك في بوت توليد أسئلة الاختيار من متعدد!*\n\n"
            "🎓 يمكنني مساعدتك في توليد أسئلة اختيار من متعدد من المواد الدراسية الخاصة بك.\n\n"
            "✨ *الميزات:*\n"
            "• توليد أسئلة من النص\n"
            "• توليد أسئلة من ملفات PDF\n"
            "• تنسيق اختبار تفاعلي\n"
            "• شروحات مفصلة\n\n"
            "الرجاء اختيار أحد الخيارات أدناه:"
        ),
        'help': (
            "❓ *المساعدة والنصائح*\n\n"
            "📝 *كيفية استخدام البوت:*\n"
            "1. اختر 'إنشاء أسئلة اختيار من متعدد'\n"
            "2. حدد طريقة الإدخال (نص/PDF)\n"
            "3. أرسل المادة الخاصة بك\n"
            "4. احصل على أسئلتك!\n\n"
            "💡 *نصائح للحصول على أفضل النتائج:*\n"
            "• استخدم نصًا واضحًا ومنظمًا جيدًا\n"
            "• بالنسبة لملفات PDF، حدد الصفحات ذات الصلة\n"
            "• جرب مستويات صعوبة مختلفة\n"
            "• احتفظ بطول نص معقول\n\n"
            "❓ *الأسئلة الشائعة:*\n"
            "• *س:* كم عدد الأسئلة التي سأحصل عليها؟\n"
            "• *ج:* عادة 10-20 سؤالًا لكل تقديم\n\n"
            "• *س:* هل يمكنني الحصول على أسئلة بلغات مختلفة؟\n"
            "• *ج:* يدعم حاليًا اللغة الإنجليزية فقط\n\n"
            "هل تحتاج إلى مزيد من المساعدة؟ اتصل بالمطور!"
        ),
        'contact': (
            "📧 *معلومات الاتصال*\n\n"
            "لا تتردد في التواصل إذا كان لديك أي أسئلة أو اقتراحات!\n\n"
            "📧 Email: raafatsami101@gmail.com\n"
            "📱 Telegram: @RefOoSami\n"
            "📞 Whatsapp: +201011508719\n"
        ),
        'model_selection': (
            "🤖 *اختر نموذج الذكاء الاصطناعي*\n\n"
            "اختر نموذج الذكاء الاصطناعي الذي ترغب في استخدامه لتوليد الأسئلة:\n\n"
            "• *النموذج 1*: نموذج قياسي مع شروحات\n"
            "• *النموذج 2*: نموذج متقدم مع عدد أسئلة قابل للتخصيص\n\n"
            "💡 *نصيحة:* النموذج 2 أفضل لتوليد عدد محدد من الأسئلة"
        ),
        'question_count': (
            "📊 *حدد عدد الأسئلة*\n\n"
            "اختر عدد الأسئلة التي ترغب في توليدها:\n\n"
            "💡 *نصيحة:* قد يستغرق عدد أكبر من الأسئلة وقتًا أطول للتوليد"
        ),
        'select_language': (
            "🌐 *اختر لغتك*\n\n"
            "الرجاء اختيار اللغة المفضلة لديك:"
        ),
        'language_changed': (
            "✅ تم تغيير اللغة إلى العربية"
        ),
        'input_method': (
            "📝 *اختر طريقة الإدخال*\n\n"
            "كيف ترغب في إرسال المادة الدراسية الخاصة بك؟\n\n"
            "• 📄 *نص*: أرسل المادة كنص عادي\n"
            "• 📚 *PDF*: قم بتحميل ملف PDF وتحديد الصفحات\n\n"
            "💡 *نصيحة:* إدخال النص أسرع، بينما ملفات PDF أفضل للمحتوى المنسق."
        ),
        'send_text': (
            "📝 *أرسل النص الخاص بك*\n\n"
            "الرجاء إرسال المادة الدراسية كنص.\n"
            "سأقوم بتحليلها وتوليد أسئلة اختيار من متعدد.\n\n"
            "💡 *نصيحة:* يجب أن يكون النص 30 حرفًا على الأقل للحصول على نتائج أفضل."
        ),
        'text_too_short': (
            "❌ *النص قصير جدًا*\n\n"
            "النص الذي قدمته قصير جدًا لتوليد أسئلة ذات مغزى.\n"
            "الرجاء إرسال نص أطول (30 حرفًا على الأقل)."
        ),
        'send_pdf': (
            "📚 *أرسل ملف PDF الخاص بك*\n\n"
            "الرجاء إرسال ملف PDF الخاص بك.\n"
            "بعد استلام الملف، سأطلب منك تحديد الصفحات التي تريد تحليلها.\n\n"
            "💡 *نصيحة:* تأكد من أن ملف PDF قابل للقراءة وغير محمي بكلمة مرور."
        ),
        'processing_pdf': "⏳ معالجة ملف PDF الخاص بك...",
        'pdf_processed': (
            "✅ تمت معالجة ملف PDF بنجاح!\n\n"
            "📚 يحتوي المستند على *{0}* صفحة.\n\n"
            "الرجاء إرسال نطاق الصفحات بالتنسيق:\n"
            "`البداية-النهاية` (مثال: `1-5`)\n\n"
            "💡 *نصيحة:* يمكنك تحليل المستند بأكمله بإرسال `1-{0}`"
        ),
        'extracting_text': "⏳ استخراج النص من صفحات PDF...",
        'text_extracted': "✅ تم استخراج النص بنجاح!\n\n⏳ توليد الأسئلة...",
        'analyzing_text': "⏳ تحليل النص الخاص بك وتوليد الأسئلة...",
        'no_questions': (
            "❌ لا يمكن توليد أسئلة من المادة المقدمة.\n\n"
            "حاول:\n"
            "• استخدام مادة مختلفة\n"
            "• اختيار مستوى صعوبة مختلف\n"
            "• جعل النص أكثر تفصيلاً"
        ),
        'questions_generated': "✅ تم توليد {0} سؤال!\n\n📝 جاري إرسال الأسئلة...",
        'question_header': "📝 سؤال {0}/{1}\n\n{2}",
        'completion': (
            "🎉 *تم توليد الأسئلة بنجاح!*\n\n"
            "📊 *ملخص:*\n"
            "• إجمالي الأسئلة: {0}\n"
            "• الأسئلة المرسلة: {1}\n"
            "• الأسئلة التي تم تخطيها: {2}\n\n"
            "💡 *نصائح:*\n"
            "• جرب مواد مختلفة للحصول على أسئلة متنوعة\n"
            "• استخدم قائمة المساعدة للمزيد من النصائح\n"
            "• شارك ملاحظاتك مع المطور"
        ),
        'feedback_request': (
            "📝 *كيف كانت تجربتك؟*\n\n"
            "يرجى تقييم جودة الأسئلة التي تم إنشاؤها:"
        ),
        'feedback_thanks': (
            "🙏 *شكرًا لك على ملاحظاتك!*\n\n"
            "مساهمتك تساعدنا في تحسين الخدمة."
        ),
        'feedback_comment': (
            "💬 *تعليقات إضافية*\n\n"
            "إذا كنت ترغب في مشاركة ملاحظات أكثر تفصيلاً، يرجى إرسال رسالة. أو اضغط على تخطي إذا كنت قد انتهيت."
        ),
        'feedback_skip': "⏭️ تخطي",
        'feedback_excellent': "⭐⭐⭐⭐⭐ ممتاز",
        'feedback_good': "⭐⭐⭐⭐ جيد",
        'feedback_average': "⭐⭐⭐ متوسط",
        'feedback_poor': "⭐⭐ ضعيف",
        'feedback_very_poor': "⭐ ضعيف جدًا",
        'invalid_pdf': "❌ الرجاء إرسال ملف PDF.",
        'pdf_error': "❌ خطأ في معالجة ملف PDF: {0}\n\nالرجاء المحاولة مرة أخرى باستخدام ملف مختلف.",
        'invalid_range': "❌ نطاق صفحات غير صالح. الرجاء إرسال النطاق بالتنسيق `البداية-النهاية` (مثال: `1-5`).",
        'error': (
            "❌ *حدث خطأ*\n\n"
            "تفاصيل الخطأ: `{0}`\n\n"
            "الرجاء المحاولة مرة أخرى أو الاتصال بالمطور إذا استمرت المشكلة."
        ),
        'returning_to_menu': "🔙 العودة إلى القائمة الرئيسية...",
        'main_menu': "🔙 *القائمة الرئيسية*\n\nالرجاء الاختيار من الازرار التالية:",
        'create_mcq': "📝 إنشاء أسئلة اختيار من متعدد",
        'contact_dev': "👨‍💻 اتصل بالمطور",
        'help_btn': "❓ المساعدة والنصائح",
        'model1': "🤖 نموذج الذكاء الاصطناعي 1",
        'model2': "🤖 نموذج الذكاء الاصطناعي 2",
        'back_main': "🔙 العودة إلى القائمة الرئيسية",
        'back': "🔙 رجوع",
        'text_btn': "📄 إرسال نص",
        'pdf_btn': "📚 إرسال PDF"
    }
} 