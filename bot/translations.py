TRANSLATIONS = {
    'russian': {
        # ============ ОБЩИЕ ============
        'choose_language': '🌍 Выберите язык:',
        'send_phone': '📱 Отправить номер телефона',
        'phone_request': '📱 *Пожалуйста, отправьте ваш номер телефона*\n\nНажмите кнопку ниже, чтобы поделиться номером:',
        'phone_error': '❌ Пожалуйста, используйте кнопку "Отправить номер телефона"',
        'phone_saved': '✅ Номер телефона сохранен!',
        'greeting': '👋 Здравствуйте!\n\nЯ HR-бот помощник по поиску работы.\n\n❓ *Как Вас зовут?*',
        'enter_name': '❓ *Как Вас зовут?*\n\nВведите ваше имя:',
        'name_error': '❌ Имя должно содержать только буквы и пробелы.',
        'name_short': '❌ Имя слишком короткое (минимум 2 буквы).',
        'choose_from_buttons': '⚠️ Пожалуйста, выберите из кнопок ниже 👇',
        'skip': '⏭ Пропустить',
        'error': '❌ Произошла ошибка. Попробуйте ещё раз.',
        'yes': '✅ Да',
        'no': '❌ Нет',

        # ============ ДОКУМЕНТ ============
        'doc_question': '📄 *Какой у вас документ?*\n\nВыберите из кнопок ниже:',
        'doc_visa': '🛂 Виза',
        'doc_id': '🪪 Теудат зеут / ID',
        'doc_other': '📋 Другое',

        # ============ ВИЗА ============
        'visa_question': '🛂 *Какая у вас виза?*\n\nВыберите из кнопок ниже:',
        'visa_other': '📋 Другое',
        'visa_b1': 'B/1',
        'visa_b2': 'B/2',
        'visa_a5': 'A/5',
        'visa_a2': 'A/2',
        'visa_refugee': '🟠 Refugee visa / Виза беженца',
        'visa_blue_paper': '🔵 Blue paper / Синяя бумага',

        # ============ ВАКАНСИИ ============
        'vacancies_found': '📋 *Доступные вакансии для вашей визы:*\n\n{vacancies}',
        'no_vacancies': '🚫 *На данный момент у нас нет подходящих вакансий с вашей визой.*',
        'no_vacancies_at_all': '🚫 *В системе пока нет вакансий для вашей визы.*',

        # ============ СМЕНА ВИЗЫ ============
        'change_visa_question': '🔄 *Хотите рассмотреть смену типа визы?*',
        'visa_change_requested': '✅ *Спасибо! С вами свяжется менеджер.*',
        'visa_change_declined': '✅ *Хорошо! Когда изменится ваша ситуация — вы сможете выбрать работу.*',

        # ============ ГРУППА ============
        'group_message': '💬 *Присоединитесь к нашей группе вакансий.*\nЗдесь публикуются все доступные предложения.\nКогда изменится ваша ситуация — вы сможете выбрать работу.\n\n🔗 {group_link}',

        # ============ ГЛАВНОЕ МЕНЮ ============
        'vacancies_btn': '📋 Вакансии',
        'help_btn': 'ℹ️ Помощь',
        'admin_btn': '🔧 Админ-панель',
        'help_text': '🤖 *HR-бот*\n\n/start - начать анкету\n/admin - админ-панель (только для админов)\n/help - помощь',

        # ============ АДМИН-ПАНЕЛЬ ============
        'admin_panel': '🔧 *Админ-панель*\n\n📊 Выберите действие:',
        'admin_candidates': '👤 Кандидаты',
        'admin_vacancies': '📋 Вакансии',
        'admin_add': '➕ Добавить',
        'admin_edit': '✏️ Редактировать',
        'admin_delete': '🗑 Удалить',
        'admin_requests': '📊 Заявки',
        'admin_close': '❌ Закрыть',
        'admin_access_denied': '⛔ Доступ запрещен!',

        # ============ АДМИН - КАНДИДАТЫ ============
        'admin_candidates_list': '📋 *Список кандидатов:*\n\n{candidates}',
        'admin_no_candidates': '📭 Нет зарегистрированных кандидатов',

        # ============ АДМИН - ВАКАНСИИ ============
        'admin_vacancies_list': '📋 *Список вакансий:*\n\n{vacancies}',
        'admin_no_vacancies': '📭 Нет активных вакансий',

        # ============ АДМИН - ДОБАВЛЕНИЕ ============
        'admin_add_title': '✏️ Введите название вакансии:',
        'admin_add_description': '✏️ Введите описание вакансии:',
        'admin_add_photo': '📸 Отправьте фото для вакансии (или нажмите "Пропустить"):',
        'admin_add_visa': '✏️ Введите тип визы (B/1, B/2, A/5, A/2, Refugee, Blue Paper, Other):',
        'admin_add_success': '✅ Вакансия добавлена! ID: {vacancy_id}',

        # ============ АДМИН - УДАЛЕНИЕ ============
        'admin_delete_ask_id': '🗑 Введите ID вакансии для удаления:',
        'admin_delete_success': '✅ Вакансия удалена!',
        'admin_delete_not_found': '❌ Вакансия с таким ID не найдена',

        # ============ АДМИН - РЕДАКТИРОВАНИЕ ============
        'admin_edit_ask_id': '✏️ Введите ID вакансии для редактирования:',
        'admin_edit_not_found': '❌ Вакансия с таким ID не найдена',
        'admin_edit_title': '✏️ Введите новое название (или нажмите "Пропустить"):',
        'admin_edit_description': '✏️ Введите новое описание (или нажмите "Пропустить"):',
        'admin_edit_photo': '📸 Отправьте новое фото (или нажмите "Пропустить"):',
        'admin_edit_visa': '✏️ Введите новый тип визы (или нажмите "Пропустить"):',
        'admin_edit_success': '✅ Вакансия обновлена!',

        # ============ АДМИН - ЗАЯВКИ ============
        'admin_requests_list': '📊 *Заявки на смену визы:*\n\n{requests}',
        'admin_no_requests': '📭 Нет новых заявок',

        # ============ АДМИН - ЗАКРЫТИЕ ============
        'admin_closed': '❌ Админ-панель закрыта'
    },

    'english': {
        # ============ GENERAL ============
        'choose_language': '🌍 Choose language:',
        'send_phone': '📱 Send phone number',
        'phone_request': '📱 *Please send your phone number*\n\nClick the button below to share your number:',
        'phone_error': '❌ Please use the "Send phone number" button',
        'phone_saved': '✅ Phone number saved!',
        'greeting': '👋 Hello!\n\nI am an HR bot assistant for job search.\n\n❓ *What is your name?*',
        'enter_name': '❓ *What is your name?*\n\nEnter your name:',
        'name_error': '❌ Name must contain only letters and spaces.',
        'name_short': '❌ Name is too short (minimum 2 letters).',
        'choose_from_buttons': '⚠️ Please choose from the buttons below 👇',
        'skip': '⏭ Skip',
        'error': '❌ An error occurred. Please try again.',
        'yes': '✅ Yes',
        'no': '❌ No',

        # ============ DOCUMENT ============
        'doc_question': '📄 *What document do you have?*\n\nChoose from the buttons below:',
        'doc_visa': '🛂 Visa',
        'doc_id': '🪪 Teudat Zehut / ID',
        'doc_other': '📋 Other',

        # ============ VISA ============
        'visa_question': '🛂 *What visa do you have?*\n\nChoose from the buttons below:',
        'visa_other': '📋 Other',
        'visa_b1': 'B/1',
        'visa_b2': 'B/2',
        'visa_a5': 'A/5',
        'visa_a2': 'A/2',
        'visa_refugee': '🟠 Refugee visa',
        'visa_blue_paper': '🔵 Blue paper',

        # ============ VACANCIES ============
        'vacancies_found': '📋 *Available vacancies for your visa:*\n\n{vacancies}',
        'no_vacancies': '🚫 *At the moment we have no suitable vacancies with your visa.*',
        'no_vacancies_at_all': '🚫 *There are no vacancies for your visa in the system yet.*',

        # ============ CHANGE VISA ============
        'change_visa_question': '🔄 *Do you want to consider changing your visa type?*',
        'visa_change_requested': '✅ *Thank you! A manager will contact you.*',
        'visa_change_declined': '✅ *Okay! When your situation changes, you can choose a job.*',

        # ============ GROUP ============
        'group_message': '💬 *Join our vacancy group.*\nAll available offers are published here.\nWhen your situation changes, you can choose a job.\n\n🔗 {group_link}',

        # ============ MAIN MENU ============
        'vacancies_btn': '📋 Vacancies',
        'help_btn': 'ℹ️ Help',
        'admin_btn': '🔧 Admin Panel',
        'help_text': '🤖 *HR-bot*\n\n/start - start questionnaire\n/admin - admin panel (only for admins)\n/help - help',

        # ============ ADMIN PANEL ============
        'admin_panel': '🔧 *Admin Panel*\n\n📊 Choose an action:',
        'admin_candidates': '👤 Candidates',
        'admin_vacancies': '📋 Vacancies',
        'admin_add': '➕ Add',
        'admin_edit': '✏️ Edit',
        'admin_delete': '🗑 Delete',
        'admin_requests': '📊 Requests',
        'admin_close': '❌ Close',
        'admin_access_denied': '⛔ Access denied!',

        # ============ ADMIN - CANDIDATES ============
        'admin_candidates_list': '📋 *Candidates list:*\n\n{candidates}',
        'admin_no_candidates': '📭 No registered candidates',

        # ============ ADMIN - VACANCIES ============
        'admin_vacancies_list': '📋 *Vacancy list:*\n\n{vacancies}',
        'admin_no_vacancies': '📭 No active vacancies',

        # ============ ADMIN - ADD ============
        'admin_add_title': '✏️ Enter vacancy title:',
        'admin_add_description': '✏️ Enter vacancy description:',
        'admin_add_photo': '📸 Send photo for vacancy (or click "Skip"):',
        'admin_add_visa': '✏️ Enter visa type (B/1, B/2, A/5, A/2, Refugee, Blue Paper, Other):',
        'admin_add_success': '✅ Vacancy added! ID: {vacancy_id}',

        # ============ ADMIN - DELETE ============
        'admin_delete_ask_id': '🗑 Enter vacancy ID to delete:',
        'admin_delete_success': '✅ Vacancy deleted!',
        'admin_delete_not_found': '❌ Vacancy with this ID not found',

        # ============ ADMIN - EDIT ============
        'admin_edit_ask_id': '✏️ Enter vacancy ID to edit:',
        'admin_edit_not_found': '❌ Vacancy with this ID not found',
        'admin_edit_title': '✏️ Enter new title (or click "Skip"):',
        'admin_edit_description': '✏️ Enter new description (or click "Skip"):',
        'admin_edit_photo': '📸 Send new photo (or click "Skip"):',
        'admin_edit_visa': '✏️ Enter new visa type (or click "Skip"):',
        'admin_edit_success': '✅ Vacancy updated!',

        # ============ ADMIN - REQUESTS ============
        'admin_requests_list': '📊 *Visa change requests:*\n\n{requests}',
        'admin_no_requests': '📭 No new requests',

        # ============ ADMIN - CLOSE ============
        'admin_closed': '❌ Admin panel closed'
    },

    'hebrew': {
        # ============ כללי ============
        'choose_language': '🌍 בחר שפה:',
        'send_phone': '📱 שלח מספר טלפון',
        'phone_request': '📱 *אנא שלח את מספר הטלפון שלך*\n\nלחץ על הכפתור למטה כדי לשתף את המספר:',
        'phone_error': '❌ אנא השתמש בכפתור "שלח מספר טלפון"',
        'phone_saved': '✅ מספר הטלפון נשמר!',
        'greeting': '👋 שלום!\n\nאני בוט HR לעוזר בחיפוש עבודה.\n\n❓ *מה שמכם?*',
        'enter_name': '❓ *מה שמכם?*\n\nהזינו את שמכם:',
        'name_error': '❌ השם חייב להכיל רק אותיות ורווחים.',
        'name_short': '❌ השם קצר מדי (לפחות 2 אותיות).',
        'choose_from_buttons': '⚠️ אנא בחרו מהכפתורים למטה 👇',
        'skip': '⏭ דלג',
        'error': '❌ אירעה שגיאה. אנא נסו שוב.',
        'yes': '✅ כן',
        'no': '❌ לא',

        # ============ מסמך ============
        'doc_question': '📄 *איזה מסמך יש לכם?*\n\nבחרו מהכפתורים למטה:',
        'doc_visa': '🛂 ויזה',
        'doc_id': '🪪 תעודת זהות / ID',
        'doc_other': '📋 אחר',

        # ============ ויזה ============
        'visa_question': '🛂 *איזו ויזה יש לכם?*\n\nבחרו מהכפתורים למטה:',
        'visa_other': '📋 אחר',
        'visa_b1': 'B/1',
        'visa_b2': 'B/2',
        'visa_a5': 'A/5',
        'visa_a2': 'A/2',
        'visa_refugee': '🟠 ויזת פליט',
        'visa_blue_paper': '🔵 נייר כחול',

        # ============ משרות ============
        'vacancies_found': '📋 *משרות זמינות לויזה שלכם:*\n\n{vacancies}',
        'no_vacancies': '🚫 *כרגע אין לנו משרות מתאימות עם הויזה שלכם.*',
        'no_vacancies_at_all': '🚫 *אין משרות לויזה שלכם במערכת כרגע.*',

        # ============ שינוי ויזה ============
        'change_visa_question': '🔄 *האם תרצו לשקול שינוי סוג ויזה?*',
        'visa_change_requested': '✅ *תודה! מנהל ייצור איתכם קשר.*',
        'visa_change_declined': '✅ *בסדר! כשהמצב שלכם ישתנה, תוכלו לבחור עבודה.*',

        # ============ קבוצה ============
        'group_message': '💬 *הצטרפו לקבוצת המשרות שלנו.*\nכאן מפרסמים את כל ההצעות הזמינות.\nכשהמצב שלכם ישתנה, תוכלו לבחור עבודה.\n\n🔗 {group_link}',

        # ============ תפריט ראשי ============
        'vacancies_btn': '📋 משרות',
        'help_btn': 'ℹ️ עזרה',
        'admin_btn': '🔧 לוח בקרה',
        'help_text': '🤖 *HR-בוט*\n\n/start - התחל שאלון\n/admin - לוח בקרה (רק למנהלים)\n/help - עזרה',

        # ============ לוח בקרה ============
        'admin_panel': '🔧 *לוח בקרה*\n\n📊 בחר פעולה:',
        'admin_candidates': '👤 מועמדים',
        'admin_vacancies': '📋 משרות',
        'admin_add': '➕ הוסף',
        'admin_edit': '✏️ ערוך',
        'admin_delete': '🗑 מחק',
        'admin_requests': '📊 בקשות',
        'admin_close': '❌ סגור',
        'admin_access_denied': '⛔ גישה נדחתה!',

        # ============ לוח בקרה - מועמדים ============
        'admin_candidates_list': '📋 *רשימת מועמדים:*\n\n{candidates}',
        'admin_no_candidates': '📭 אין מועמדים רשומים',

        # ============ לוח בקרה - משרות ============
        'admin_vacancies_list': '📋 *רשימת משרות:*\n\n{vacancies}',
        'admin_no_vacancies': '📭 אין משרות פעילות',

        # ============ לוח בקרה - הוספה ============
        'admin_add_title': '✏️ הזן כותרת משרה:',
        'admin_add_description': '✏️ הזן תיאור משרה:',
        'admin_add_photo': '📸 שלח תמונה למשרה (או לחץ "דלג"):',
        'admin_add_visa': '✏️ הזן סוג ויזה (B/1, B/2, A/5, A/2, Refugee, Blue Paper, Other):',
        'admin_add_success': '✅ המשרה נוספה! מזהה: {vacancy_id}',

        # ============ לוח בקרה - מחיקה ============
        'admin_delete_ask_id': '🗑 הזן מזהה משרה למחיקה:',
        'admin_delete_success': '✅ המשרה נמחקה!',
        'admin_delete_not_found': '❌ לא נמצאה משרה עם מזהה זה',

        # ============ לוח בקרה - עריכה ============
        'admin_edit_ask_id': '✏️ הזן מזהה משרה לעריכה:',
        'admin_edit_not_found': '❌ לא נמצאה משרה עם מזהה זה',
        'admin_edit_title': '✏️ הזן כותרת חדשה (או לחץ "דלג"):',
        'admin_edit_description': '✏️ הזן תיאור חדש (או לחץ "דלג"):',
        'admin_edit_photo': '📸 שלח תמונה חדשה (או לחץ "דלג"):',
        'admin_edit_visa': '✏️ הזן סוג ויזה חדש (או לחץ "דלג"):',
        'admin_edit_success': '✅ המשרה עודכנה!',

        # ============ לוח בקרה - בקשות ============
        'admin_requests_list': '📊 *בקשות לשינוי ויזה:*\n\n{requests}',
        'admin_no_requests': '📭 אין בקשות חדשות',

        # ============ לוח בקרה - סגירה ============
        'admin_closed': '❌ לוח הבקרה נסגר'
    }
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """Получить перевод по ключу"""
    text = TRANSLATIONS.get(lang, TRANSLATIONS['russian']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text