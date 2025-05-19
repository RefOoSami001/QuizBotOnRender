import os
import telebot
from telebot import types
import pdfplumber
from keep_alive import keep_alive
from io import BytesIO
from api_service import MCQGeneratorAPI
from api_service2 import MCQGeneratorAPI2
from config import (
    BOT_TOKEN, DIFFICULTY_LEVELS, MESSAGES,
    QUESTION_COUNTS, MIN_TEXT_LENGTH, ADMIN_CHAT_ID
)
import threading
from concurrent.futures import ThreadPoolExecutor

# Initialize bot and API services with threading support
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
api_service1 = MCQGeneratorAPI()
api_service2 = MCQGeneratorAPI2()

# Store user states
user_states = {}
user_states_lock = threading.Lock()

# Store feedback data
user_feedback = {}
user_feedback_lock = threading.Lock()

# Thread pool for handling question generation
executor = ThreadPoolExecutor(max_workers=10)

def get_text(chat_id, text_key, *format_args):
    """Get text in user's language or default to English."""
    user_state = user_states.get(chat_id, {})
    lang = user_state.get('language', 'en')
    text = MESSAGES[lang].get(text_key, MESSAGES['en'].get(text_key, ""))
    if format_args:
        return text.format(*format_args)
    return text

def create_language_menu():
    """Create language selection menu."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    en_btn = types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
    ar_btn = types.InlineKeyboardButton('🇸🇦 العربية', callback_data='lang_ar')
    markup.add(en_btn, ar_btn)
    return markup

def create_main_menu(chat_id):
    """Create main menu with localized text."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    create_mcq_btn = types.InlineKeyboardButton(get_text(chat_id, 'create_mcq'), callback_data='create_mcq')
    contact_dev_btn = types.InlineKeyboardButton(get_text(chat_id, 'contact_dev'), callback_data='contact_dev')
    help_btn = types.InlineKeyboardButton(get_text(chat_id, 'help_btn'), callback_data='help')
    lang_btn = types.InlineKeyboardButton('🌐 Language/اللغة', callback_data='change_language')
    
    # Add first two buttons in one row, other buttons in second row
    markup.add(create_mcq_btn, contact_dev_btn)
    markup.add(help_btn, lang_btn)
    return markup

def create_model_selection_menu(chat_id):
    """Create model selection menu with localized text."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    model1_btn = types.InlineKeyboardButton(get_text(chat_id, 'model1'), callback_data='model_1')
    model2_btn = types.InlineKeyboardButton(get_text(chat_id, 'model2'), callback_data='model_2')
    back_btn = types.InlineKeyboardButton(get_text(chat_id, 'back_main'), callback_data='main_menu')
    
    # Add model buttons in one row, back button in second row
    markup.add(model1_btn, model2_btn)
    markup.add(back_btn)
    return markup

def create_question_count_menu(chat_id):
    """Create question count menu with localized text."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    lang = user_states.get(chat_id, {}).get('language', 'en')
    
    for count, text in QUESTION_COUNTS[lang].items():
        buttons.append(types.InlineKeyboardButton(text, callback_data=f'count_{count}'))
    
    # Add buttons two at a time
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    back_btn = types.InlineKeyboardButton(get_text(chat_id, 'back'), callback_data='create_mcq')
    markup.add(back_btn)
    return markup

def create_input_type_menu(chat_id):
    """Create input type menu with localized text."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    text_btn = types.InlineKeyboardButton(get_text(chat_id, 'text_btn'), callback_data='send_text')
    pdf_btn = types.InlineKeyboardButton(get_text(chat_id, 'pdf_btn'), callback_data='send_pdf')
    back_btn = types.InlineKeyboardButton(get_text(chat_id, 'back_main'), callback_data='main_menu')
    
    # Add first two buttons in one row, back button in second row
    markup.add(text_btn, pdf_btn)
    markup.add(back_btn)
    return markup

def create_difficulty_menu(chat_id):
    """Create difficulty menu with localized text."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    diff_buttons = []
    lang = user_states.get(chat_id, {}).get('language', 'en')
    
    for diff_key, diff_text in DIFFICULTY_LEVELS[lang].items():
        diff_buttons.append(types.InlineKeyboardButton(diff_text, callback_data=f'difficulty_{diff_key}'))
    
    # Add buttons two at a time
    for i in range(0, len(diff_buttons), 2):
        if i + 1 < len(diff_buttons):
            markup.add(diff_buttons[i], diff_buttons[i+1])
        else:
            markup.add(diff_buttons[i])
    
    back_btn = types.InlineKeyboardButton(get_text(chat_id, 'back'), callback_data='create_mcq')
    markup.add(back_btn)
    return markup

def create_feedback_menu(chat_id):
    """Create feedback menu with rating options."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    excellent_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_excellent'), callback_data='feedback_5')
    good_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_good'), callback_data='feedback_4')
    average_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_average'), callback_data='feedback_3')
    poor_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_poor'), callback_data='feedback_2')
    very_poor_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_very_poor'), callback_data='feedback_1')
    
    markup.add(excellent_btn, good_btn, average_btn, poor_btn, very_poor_btn)
    return markup

def create_comment_menu(chat_id):
    """Create menu for additional comment options."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    skip_btn = types.InlineKeyboardButton(get_text(chat_id, 'feedback_skip'), callback_data='feedback_skip')
    markup.add(skip_btn)
    return markup

def notify_admin(message, user=None):
    """Send notification to admin."""
    try:
        if user:
            # Format user information
            user_info = f"User ID: {user.id}\n"
            user_info += f"Username: @{user.username}\n" if user.username else "Username: None\n"
            user_info += f"First Name: {user.first_name}\n" if user.first_name else ""
            user_info += f"Last Name: {user.last_name}\n" if user.last_name else ""
            user_info += f"Language Code: {user.language_code}\n" if user.language_code else ""
            
            # Send user info to admin
            bot.send_message(
                ADMIN_CHAT_ID,
                f"🔔 Bot Notification\n\n{message}\n\nUser Information:\n{user_info}",
                parse_mode=None  # Disable Markdown parsing
            )
        else:
            # Send simple notification
            bot.send_message(
                ADMIN_CHAT_ID,
                f"🔔 Bot Notification\n\n{message}",
                parse_mode=None  # Disable Markdown parsing
            )
    except Exception as e:
        print(f"Failed to notify admin: {e}")

def get_or_create_user_state(chat_id, initial_state=None):
    """Thread-safe way to get or create user state"""
    with user_states_lock:
        if chat_id not in user_states:
            user_states[chat_id] = {'state': initial_state or 'main_menu', 'language': 'en'}
        return user_states[chat_id]

def update_user_state(chat_id, updates):
    """Thread-safe way to update user state"""
    with user_states_lock:
        if chat_id not in user_states:
            user_states[chat_id] = {'state': 'main_menu', 'language': 'en'}
        user_states[chat_id].update(updates)

@bot.message_handler(commands=['start'])
def start(message):
    # Notify admin about new user
    notify_admin("New user started the bot", message.from_user)
    
    # Initialize user state with default language
    if message.chat.id not in user_states:
        user_states[message.chat.id] = {'state': 'language_selection', 'language': 'en'}
        
        # Show language selection first
        bot.send_message(
            message.chat.id,
            "🌐 Please select your language / الرجاء اختيار لغتك",
            parse_mode='Markdown',
            reply_markup=create_language_menu()
        )
    else:
        # If user already has a state, show main menu
        user_states[message.chat.id]['state'] = 'main_menu'
        bot.send_message(
            message.chat.id,
            get_text(message.chat.id, 'welcome'),
            parse_mode='Markdown',
            reply_markup=create_main_menu(message.chat.id)
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_callback(call):
    lang = call.data.split('_')[1]
    # Update user's language preference
    if call.message.chat.id not in user_states:
        user_states[call.message.chat.id] = {'state': 'main_menu', 'language': lang}
    else:
        user_states[call.message.chat.id]['language'] = lang
        user_states[call.message.chat.id]['state'] = 'main_menu'
    
    # Send language confirmation message
    bot.edit_message_text(
        get_text(call.message.chat.id, 'language_changed'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    # Show main menu in selected language
    bot.send_message(
        call.message.chat.id,
        get_text(call.message.chat.id, 'welcome'),
        parse_mode='Markdown',
        reply_markup=create_main_menu(call.message.chat.id)
    )

@bot.callback_query_handler(func=lambda call: call.data == 'change_language')
def change_language_callback(call):
    bot.edit_message_text(
        get_text(call.message.chat.id, 'select_language'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_language_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_callback(call):
    bot.edit_message_text(
        get_text(call.message.chat.id, 'help'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_main_menu(call.message.chat.id)
    )

@bot.callback_query_handler(func=lambda call: call.data == 'contact_dev')
def contact_dev_callback(call):
    bot.edit_message_text(
        get_text(call.message.chat.id, 'contact'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'create_mcq')
def create_mcq_callback(call):
    # Initialize user state with empty dictionary
    update_user_state(call.message.chat.id, {'state': 'model_selection'})
    bot.edit_message_text(
        get_text(call.message.chat.id, 'model_selection'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_model_selection_menu(call.message.chat.id)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('model_'))
def model_selection_callback(call):
    model = call.data.split('_')[1]  # This will be '1' or '2'
    
    # Update state safely
    update_user_state(call.message.chat.id, {
        'state': 'question_count' if model == '2' else 'input_type',
        'model': model
    })
    
    if model == '2':
        bot.edit_message_text(
            get_text(call.message.chat.id, 'question_count'),
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=create_question_count_menu(call.message.chat.id)
        )
    else:
        bot.edit_message_text(
            get_text(call.message.chat.id, 'input_method'),
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=create_input_type_menu(call.message.chat.id)
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('count_'))
def question_count_callback(call):
    count = call.data.split('_')[1]
    update_user_state(call.message.chat.id, {
        'state': 'input_type',
        'question_count': int(count)
    })
    
    bot.edit_message_text(
        get_text(call.message.chat.id, 'input_method'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_input_type_menu(call.message.chat.id)
    )

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def back_to_main_callback(call):
    update_user_state(call.message.chat.id, {'state': 'main_menu'})
    bot.edit_message_text(
        get_text(call.message.chat.id, 'main_menu'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_main_menu(call.message.chat.id)
    )

@bot.callback_query_handler(func=lambda call: call.data == 'send_text')
def send_text_callback(call):
    # Preserve current state while updating
    current_state = user_states.get(call.message.chat.id, {})
    current_state['state'] = 'waiting_for_text'
    user_states[call.message.chat.id] = current_state
    
    bot.edit_message_text(
        get_text(call.message.chat.id, 'send_text'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'send_pdf')
def send_pdf_callback(call):
    # Preserve current state while updating
    current_state = user_states.get(call.message.chat.id, {})
    current_state['state'] = 'waiting_for_pdf'
    user_states[call.message.chat.id] = current_state
    
    bot.edit_message_text(
        get_text(call.message.chat.id, 'send_pdf'),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('difficulty_'))
def difficulty_callback(call):
    difficulty = call.data.split('_')[1]
    
    # Get current state and update
    current_state = user_states.get(call.message.chat.id, {})
    current_state['difficulty'] = difficulty
    user_states[call.message.chat.id] = current_state
    
    lang = current_state.get('language', 'en')
    difficulty_text = DIFFICULTY_LEVELS[lang][difficulty]
    bot.edit_message_text(
        f"{difficulty_text}\n\n{get_text(call.message.chat.id, 'send_text')}",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_state = user_states.get(message.chat.id, {})
    if user_state.get('state') != 'waiting_for_pdf':
        return

    if not message.document.file_name.endswith('.pdf'):
        bot.send_message(
            message.chat.id,
            get_text(message.chat.id, 'invalid_pdf')
        )
        return


    # Send processing message
    processing_msg = bot.send_message(
        message.chat.id,
        get_text(message.chat.id, 'processing_pdf')
    )

    try:
        # Download the PDF file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Use BytesIO instead of saving to disk
        pdf_bytes = BytesIO(downloaded_file)
        
        # Get number of pages
        with pdfplumber.open(pdf_bytes) as pdf:
            num_pages = len(pdf.pages)
        
        # Update state while preserving model selection
        new_state = {
            'state': 'waiting_for_page_range',
            'pdf_bytes': downloaded_file,  # Store PDF bytes in state
            'num_pages': num_pages
        }
        
        # Preserve important data from previous state
        for key in ['model', 'question_count', 'difficulty', 'language']:
            if key in user_state:
                new_state[key] = user_state[key]
        
        user_states[message.chat.id] = new_state
        
        # Update processing message
        bot.edit_message_text(
            get_text(message.chat.id, 'pdf_processed', num_pages, num_pages),
            message.chat.id,
            processing_msg.message_id,
            parse_mode='Markdown'
        )
        

        
    except Exception as e:
        bot.edit_message_text(
            get_text(message.chat.id, 'pdf_error', str(e)),
            message.chat.id,
            processing_msg.message_id
        )
        # Notify admin about the error
        notify_admin(f"Error processing PDF: {str(e)}")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_page_range')
def handle_page_range(message):
    user_state = user_states.get(message.chat.id, {})
    try:
        start_page, end_page = map(int, message.text.split('-'))
        if start_page < 1 or end_page > user_state['num_pages']:
            raise ValueError
        

        # Send processing message
        processing_msg = bot.send_message(
            message.chat.id,
            get_text(message.chat.id, 'extracting_text')
        )
        
        # Extract text from PDF using BytesIO
        pdf_bytes = user_state['pdf_bytes']
        text_content = ""
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page_num in range(start_page - 1, end_page):
                text_content += pdf.pages[page_num].extract_text() + "\n"
        
        # Check text length
        if len(text_content) < MIN_TEXT_LENGTH:
            bot.edit_message_text(
                get_text(message.chat.id, 'text_too_short'),
                message.chat.id,
                processing_msg.message_id,
                parse_mode='Markdown'
            )
            return
        
        # Update processing message
        bot.edit_message_text(
            get_text(message.chat.id, 'text_extracted'),
            message.chat.id,
            processing_msg.message_id
        )
        
        # Generate questions
        generate_questions(message.chat.id, text_content, processing_msg)
        
    except (ValueError, IndexError):
        bot.send_message(
            message.chat.id,
            get_text(message.chat.id, 'invalid_range'),
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_text')
def handle_text(message):
    # Check text length
    if len(message.text) < MIN_TEXT_LENGTH:
        bot.send_message(
            message.chat.id,
            get_text(message.chat.id, 'text_too_short'),
            parse_mode='Markdown'
        )
        return
    

    
    # Send processing message
    processing_msg = bot.send_message(
        message.chat.id,
        get_text(message.chat.id, 'analyzing_text')
    )
    
    # Generate questions asynchronously
    generate_questions_async(message.chat.id, message.text, processing_msg)

def generate_questions_async(chat_id, text, processing_msg=None):
    """Asynchronous wrapper for generate_questions"""
    def _generate():
        try:
            generate_questions(chat_id, text, processing_msg)
        except Exception as e:
            print(f"Error in generate_questions_async: {e}")
            
    # Submit the task to the thread pool
    executor.submit(_generate)

def generate_questions(chat_id, text, processing_msg=None):
    try:
        # Get the current user state thread-safely
        with user_states_lock:
            user_state = user_states.get(chat_id, {}).copy()
        
        # Get model and set default if not found
        model = user_state.get('model')
        
        # Default to model 1 if no model is specified
        if not model:
            model = '1'
        
        if model == '1':
            # Use original API service
            success, result = api_service1.generate_questions(text)
        else:
            # Use new API service with question count
            question_count = user_state.get('question_count', 10)
            success, result = api_service2.generate_questions(text, question_count)
        
        if success:
            questions = result
            difficulty = user_state.get('difficulty', 'all')
            
            # Filter questions by difficulty (only for model 1)
            if model == '1':
                questions = api_service1.filter_questions_by_difficulty(questions, difficulty)
            
            if not questions:
                bot.edit_message_text(
                    get_text(chat_id, 'no_questions'),
                    chat_id,
                    processing_msg.message_id,
                    parse_mode='Markdown'
                )
                return
            
            if processing_msg:
                bot.edit_message_text(
                    get_text(chat_id, 'questions_generated', len(questions)),
                    chat_id,
                    processing_msg.message_id
                )
            
            # Track skipped questions
            skipped_questions = 0
            
            # Send questions
            if model == '1':
                # Handle Model 1 format
                for i, question in enumerate(questions, 1):
                    if isinstance(question, dict):
                        question_text = question.get('question', '')
                        answers = question.get('answers', [])
                        
                        # Skip if question text is too long
                        if len(question_text) > 300:
                            skipped_questions += 1
                            continue
                        
                        # Filter out answers that are too long
                        valid_answers = []
                        for answer in answers:
                            answer_text = answer.get('answer', '')
                            if len(answer_text) <= 100:
                                valid_answers.append(answer)
                        
                        # Skip if we don't have enough valid answers
                        if len(valid_answers) < 2:
                            skipped_questions += 1
                            continue
                        
                        options = [answer.get('answer', '') for answer in valid_answers]
                        correct_option = next((i for i, ans in enumerate(valid_answers) if ans.get('isCorrect', False)), 0)
                        
                        # Get explanation
                        explanation = question.get('explanation', '')
                        if explanation and len(explanation) > 200:
                            explanation = explanation[:197] + "..."
                        
                        try:
                            bot.send_poll(
                                chat_id,
                                get_text(chat_id, 'question_header', i, len(questions), question_text),
                                options=options,
                                is_anonymous=True,
                                type='quiz',
                                correct_option_id=correct_option,
                                explanation=explanation
                            )
                        except Exception as e:
                            skipped_questions += 1
                            continue
            else:
                # Handle Model 2 format
                for i, question_data in questions.items():
                    if isinstance(question_data, dict):
                        question_text = question_data.get('text', '')
                        options_dict = question_data.get('options', {})
                        correct_answer = question_data.get('answer', '')
                        
                        # Skip if question text is too long
                        if len(question_text) > 300:
                            skipped_questions += 1
                            continue
                        
                        # Convert options dictionary to list and validate lengths
                        options = []
                        valid_options = True
                        for key, value in options_dict.items():
                            if len(value) > 100:
                                valid_options = False
                                break
                            options.append(value)
                        
                        if not valid_options or len(options) < 2:
                            skipped_questions += 1
                            continue
                        
                        # Find correct option index
                        if not correct_answer or not correct_answer.lower() in ['a', 'b', 'c', 'd']:
                            skipped_questions += 1
                            continue
                        correct_option = ord(correct_answer.lower()) - ord('a')
                        
                        try:
                            bot.send_poll(
                                chat_id,
                                get_text(chat_id, 'question_header', i, len(questions), question_text),
                                options=options,
                                is_anonymous=True,
                                type='quiz',
                                correct_option_id=correct_option
                            )
                        except Exception as e:
                            skipped_questions += 1
                            continue
            
            # Send completion message
            bot.send_message(
                chat_id,
                get_text(chat_id, 'completion', len(questions), len(questions) - skipped_questions, skipped_questions),
                parse_mode='Markdown'
            )
            
            # Notify admin about successful generation
            notify_admin(
                f"Questions generated successfully:\n"
                f"• Total: {len(questions)}\n"
                f"• Sent: {len(questions) - skipped_questions}\n"
                f"• Skipped: {skipped_questions}\n"
                f"• Model: {model}\n"
                f"• Difficulty: {difficulty}"
            )
            
            # Request feedback
            with user_states_lock:
                user_states[chat_id]['state'] = 'feedback'
            bot.send_message(
                chat_id,
                get_text(chat_id, 'feedback_request'),
                parse_mode='Markdown',
                reply_markup=create_feedback_menu(chat_id)
            )
            
        else:
            bot.send_message(chat_id, f"❌ {result}")
            notify_admin(f"Question generation failed: {result}")
        
    except Exception as e:
        bot.send_message(
            chat_id,
            get_text(chat_id, 'error', str(e)),
            parse_mode='Markdown'
        )
        
        # Notify admin about the error
        notify_admin(f"Error occurred during question generation: {str(e)}")
        
        # Preserve language when resetting state
        with user_states_lock:
            lang = user_states.get(chat_id, {}).get('language', 'en')
            user_states[chat_id] = {'state': 'main_menu', 'language': lang}
        
        bot.send_message(
            chat_id,
            get_text(chat_id, 'returning_to_menu'),
            reply_markup=create_main_menu(chat_id)
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('feedback_'))
def feedback_callback(call):
    feedback_value = call.data.split('_')[1]
    chat_id = call.message.chat.id
    
    if feedback_value in ['1', '2', '3', '4', '5']:
        # Store rating
        if chat_id not in user_feedback:
            user_feedback[chat_id] = {}
        
        user_feedback[chat_id]['rating'] = int(feedback_value)
        user_states[chat_id]['state'] = 'waiting_for_feedback_comment'
        
        # Thank the user and ask for additional comments in a single message
        bot.edit_message_text(
            get_text(chat_id, 'feedback_thanks') + "\n\n" + get_text(chat_id, 'feedback_comment'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=create_comment_menu(chat_id)
        )
        
        # Send rating to admin
        rating_text = "⭐" * int(feedback_value)
        notify_admin(f"User provided feedback: {rating_text} ({feedback_value}/5)", call.from_user)
        
    elif feedback_value == 'skip':
        # User skipped additional comments
        user_states[chat_id]['state'] = 'main_menu'
        
        # Show main menu
        bot.edit_message_text(
            get_text(chat_id, 'main_menu'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=create_main_menu(chat_id)
        )

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_feedback_comment')
def handle_feedback_comment(message):
    chat_id = message.chat.id
    
    # Store the comment
    if chat_id in user_feedback:
        user_feedback[chat_id]['comment'] = message.text
    
    # Send feedback to admin
    feedback_data = user_feedback.get(chat_id, {})
    rating = feedback_data.get('rating', 0)
    rating_text = "⭐" * rating if rating else "No rating"
    
    notify_admin(
        f"User provided feedback:\n"
        f"Rating: {rating_text} ({rating}/5)\n"
        f"Comment: {message.text}",
        message.from_user
    )
    
    # Thank the user and return to main menu
    user_states[chat_id]['state'] = 'main_menu'
    bot.send_message(
        chat_id,
        get_text(chat_id, 'feedback_thanks'),
        parse_mode='Markdown',
        reply_markup=create_main_menu(chat_id)
    )

if __name__ == '__main__':
    print("🤖 Bot is running...")
    keep_alive()
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot polling error: {e}")
            continue



