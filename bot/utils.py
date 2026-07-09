import re

def detect_language(text: str) -> str:
    if re.search('[а-яА-ЯёЁ]', text):
        return 'russian'
    if re.search('[\u0590-\u05FF]', text):
        return 'hebrew'
    if re.search('[a-zA-Z]', text):
        return 'english'
    return 'russian'

def format_vacancies(vacancies: list) -> str:
    if not vacancies:
        return ''
    
    text = ''
    for v in vacancies:
        text += f"*ID: {v['id']}*\n"
        text += f"📌 *{v['title']}*\n"
        text += f"{v['description']}\n"
        text += f"🛂 Виза: {v['visa_type']}\n\n"
    
    return text

def format_admin_vacancies(vacancies: list) -> str:
    if not vacancies:
        return ''
    
    text = ''
    for v in vacancies:
        text += f"ID: {v['id']} | {v['title']} | Виза: {v['visa_type']}\n"
    
    return text

def format_visa_requests(requests: list) -> str:
    if not requests:
        return ''
    
    text = ''
    for r in requests:
        text += f"ID: {r['id']} | {r.get('name', 'Без имени')} | {r['current_visa']}\n"
    
    return text

def format_candidates_list(users: list) -> str:
    """Форматировать список кандидатов для админа"""
    if not users:
        return ''
    
    text = ''
    for u in users:
        tg_id = u.get('tg_id', '')
        name = u.get('name', 'Без имени')
        phone = u.get('phone', 'Не указан')
        visa = u.get('visa_type', 'Не указана')
        lang = u.get('language', 'ru')
        created = u.get('created_at', '')
        
        text += (
            f"🆔 {tg_id}\n"
            f"👤 {name}\n"
            f"📞 {phone}\n"
            f"🛂 {visa}\n"
            f"🌍 {lang}\n"
            f"📅 {created[:10]}\n"
            f"{'-'*20}\n"
        )
    
    return text