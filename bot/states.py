from aiogram.fsm.state import State, StatesGroup

class LanguageState(StatesGroup):
    choosing_language = State()

class SurveyState(StatesGroup):
    phone = State()
    name = State()
    document = State()          # <--- НОВЫЙ ВОПРОС
    visa = State()
    change_visa = State()
    add_vacancy_title = State()
    add_vacancy_description = State()
    add_vacancy_photo = State()
    add_vacancy_visa = State()
    delete_vacancy = State()
    edit_vacancy_id = State()
    edit_vacancy_title = State()
    edit_vacancy_description = State()
    edit_vacancy_photo = State()
    edit_vacancy_visa = State()