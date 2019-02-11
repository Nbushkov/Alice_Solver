# coding: utf-8
from sympy import solve, sympify, symbols, simplify
from mpmath import *
import random
import sys
import re

REPLACE_DIGITS = {
    'ноль':'0', 'один':'1', 'два':'2', 'три':'3', 'четыре':'4', 'пять':'5', 'шесть':'6', 'восемь':'8', 'семь':'7', 'девять':'9', 'десять':'10',
    'одиннадцать':'11', 'двенадцать':'12', 'тринадцать':'13', 'четырнадцать':'14', 'пятнадцать':'15', 'шестнадцать':'16', 
    'семнадцать':'17', 'восемнадцать':'18', 'девятнадцать':'19'
}

REPLACE_IN = {
    'икс':'x', 'игрек':'y', 
    'плюс':'+', 'минус':'-', 'умножить':'*',
    '−':'-',
    'делить':'/',
    'разделить':'/',
    '÷':'/',
    ':':'/',
    ',':'.',
    'xy':'x*y',
    'yx':'y*x',
    'равно':'=',
    'в квадрате':'**2',
    'в кубе':'**3',
    'квадрат':'**2',
    'куб':'**3',
    'в степени':'**',
    'степени':'**',
    'открыть скобку':'(',
    'закрыть скобку':')',
    'левая скобка':'(',
    'правая скобка':')',
    'корень':'sqrt',
    ' факториал':'!',
    'из':'',
    'на':'',
    'косинус':'cos',
    'синус':'sin',
    'котангенс':'cot',
    'тангенс':'tan',
    'экспонента':'exp',
    'експонента':'exp',
    'логарифм':'log',
    'число пи':'pi',
    'число е':'E', 
    'пи':'pi',
    'е':'E', 
}

ERRORS = {
    0:['Нет ошибок'],
    1:['Уравнение должно содержать переменную x или y','В вашем уравнении нет неизвестной'],
    2:['Уравнение должно содержать только одну переменную x или y', 'В вашем уравнении больше одной неизвестной'],
    3:['Уравнение может содержать только один знак равенства', 'В вашем уравнении несколько знаков равенства'],
    4:['В уравнении непарные скобки']
}

REPLACE_TTS = {
    'sqrt':' корень из ',
    '\*\*2':' в квадрате ',
    '\^2':' в квадрате ',
    '\*\*3':' в кубе ',
    '\^3':' в кубе ',
    '\*\*':' в степени ',
    '\^':' в степени ',
    '\*':' умножить на ',
    '-':'минус',
    'cos':'косинус',
    'sin':'синус',
    'cot':'котангенс',
    'tan':'тангенс',
    'log':'логарифм',
    'exp':'экспонента',
    'y':'игрек',
    'pi':'пи',
    'E':'е',
    'I':'мнимая единица',
    '\(':' открыть скобку ',
    '\)':' закрыть скобку ',
    '\n':' - - ',
}

HELP_TEXTS = {
    'реши':['5x+12=7', 'cos(y)=sin(y)'],
    'вычисли':['0.5(0.76-0.06)', '2^5*sqrt(16)'],
    'упрости':['(2x-3y)(3y-2x)-12xy'],
}
             
# Функция для непосредственной обработки диалога.
def handle_dialog(req, res, user_storage):
    if req.is_new_session:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        user_storage = {
            'user_id': req.user_id,
            'suggests': [
            {'title': 'Помощь', 'hide': True},
            {
                "title": "Решебник",
                "url": "https://gdeze.ru",
                "hide": True
            },
            {
                "title": "Оценить",
                "url": "https://dialogs.yandex.ru/store/skills/48b31fb4-areshkin-pomozhet-reshit-i-podschi",
                "hide": True
            }],
        }

    # Флаг добавления в логи
    user_storage['to_log'] = True
    # данные о команде, убираем лишнее
    user_command = req.command.lower().replace('спроси знайка ответить', '').replace('спроси знайка ответит', '').strip()
    # определяем что делать по первому слову в команде
    first_word = user_command.split(' ', 1)[0]
    # данные о исходном сообщении
    user_message = req.original.lower().strip()
    # ответ на некорректный запрос
    default_answer = 'Я понимаю фразы начинающиеся с ключевых слов: ' + ', '.join(HELP_TEXTS) + \
    ', дополненные алгебраическим выражением.\n'

    if not first_word:
        user_answer = 'Привет!\nЯ могу решать уравнения с одной неизвестной x или y,'+ \
        ' вычислять или упрощать выражения.\nПриступим?'
        res.set_text(user_answer)
        res.set_tts(find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
        
    # ответ яндекс боту
    if user_message == 'ping':
        res.set_text('pong')
        user_storage['to_log'] = False
        return res, user_storage

    # если похвалили
    if first_word in [
        'круто',
        'класс',
        'верно',
        'правильно',
        'молодец',
        'хорошо',
    ]:
        # Благодарим пользователя
        res.set_text('Спасибо, я стараюсь!')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage

    # помощь юзеру
    if user_message == 'помощь':
        res.set_text(default_answer+ \
            'Для примеров скажите: Пример и ключевое слово.\nЧтобы закончить скажите Хватит или стоп.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage

    # примеры
    if first_word == 'пример':
        s = user_command.split(' ', 2)
        if len(s) == 1 or s[1] not in HELP_TEXTS:
            user_answer = "Укажите ключевое слово для примера: "+', '.join(HELP_TEXTS)
        else:
            user_answer = s[1]+' '+' или '.join(HELP_TEXTS[s[1]])

        res.set_text(user_answer)
        res.set_tts(find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage    
    
    if first_word in [
        'хватит',
        'стоп',
        'пока'
    ]:
        # Пользователь закончил, прощаемся.
        res.set_text('Приходите ещё, порешаем!')
        res.end()
        return res, user_storage

    # Убираем первое слово из команды
    user_command = user_command.replace(first_word, '').strip()
    user_message = user_message.replace(first_word, '').strip()
    
    if first_word in ['реши', 'решить']:
        # Решаем уравнение
        user_command = user_command.replace('уравнение', '').strip()
        user_answer = handle_solve(user_command)
        # Если ошибка попробуем с исходным сообщением
        if user_answer.startswith('Ошибка'):
            user_message = user_message.replace('уравнение', '').strip()
            user_answer = handle_solve(user_message)

    elif first_word in ['вычисли', 'вычислить']:
        # Вычисляем
        user_answer = handle_calculate(user_command)
        # Если ошибка попробуем с исходным сообщением
        if user_answer.startswith('Ошибка'):
            user_answer = handle_calculate(user_message)

    elif first_word in ['упрости', 'упростить']:
        # Упрощаем
        user_answer = handle_simplify(user_command)
        # Если ошибка попробуем с исходным сообщением
        if user_answer.startswith('Ошибка'):
            user_answer = handle_simplify(user_message)
    else:
        user_answer = default_answer

    res.set_text(user_answer)
    res.set_tts(find_replace_multi(user_answer, REPLACE_TTS))
    res.set_buttons(user_storage['suggests'])

    return res, user_storage

# Функция для решения уравнения
def handle_solve(input_str):
    # Подготавливаем выражение
    equation = prepare_in(input_str)
    # Проверка на ошибки
    err = check(equation)
    if 0 != err:
        return random.choice(ERRORS[err])

    if equation.count("=") == 1:
        equation = move(equation)
    # пытаемся решить
    try:
        solution = peq(equation)
    except Exception:
        out_str = 'Ошибка в уравнении'
    else:
        if not solution:
            out_str = 'Нет решений'
        else:
            out_str = 'Ответ %s' % (answer(solution))

    return out_str

# Функция вычисления выражения
def handle_calculate(input_str):
    # Подготавливаем выражение
    equation = prepare_in(input_str)
    try:
        expr = sympify(equation)
        out_str = expr.evalf()
    except Exception:
        out_str = 'Ошибка в выражении'
    # Округляем если число
    if is_number_float(out_str):
        out_str = round(float(out_str), 3)

    return str(out_str)

# Функция упрощения выражения
def handle_simplify(input_str):
    # Подготавливаем выражение
    equation = prepare_in(input_str)
    try:
        out_str = simplify(equation)
    except Exception:
        out_str = 'Ошибка в выражении'

    return str(out_str)


# Функция замены по словарю 
def find_replace_multi(string, dictionary, use_word = False):
    for item in dictionary.keys():
        if use_word:
            string = re.sub(r'\b{}\b'.format(item), r'{}'.format(dictionary[item]), string)
        else:
            string = re.sub(item, dictionary[item], string)

    return str(string)

# Первичная подготовка текста запроса
def prepare_in(str_in):
    # Замена слов в тексте на переменные и цифры
    str_in = find_replace_multi(str_in, REPLACE_DIGITS, True)
    str_in = find_replace_multi(str_in, REPLACE_IN)
    # добавляем умножение
    str_in = re.sub(r'(\d+\)?)\s*([a-z(])' , r'\1*\2', str_in)
    str_in = re.sub('\)\s*\(', ')*(', str_in)

    return str_in

# перенос в одну часть (приравнивание к 0)
def move(str_in):
    parts = str_in.split('=')
    return parts[0].strip() + '-(' + parts[1].strip() + ')'

# Проверка корректности уравнения
def check(str_in):
    # проверка  числа вхождений равенства
    eq_num = str_in.count("=")
    if eq_num > 1:
        return 3
    # проверка соответствия скобок
    if str_in.count('(') != str_in.count(')'):
        return 4
    # проверка наличия x
    x_in = 'x' in str_in
    # проверка наличия y
    y_in = 'y' in str_in
    # сразу оба
    if x_in and y_in:
        return 2
    # нет ни x ни y
    if not (x_in or y_in): 
        return 1

    return 0

# Решатель уравнения s
def peq(s):
    x, y = symbols('x,y')
    return solve(s, dict=True)

# Подготовка ответа
def answer(an_list):
    return  ' или '.join(map(prepare_out, an_list)) 

def is_number_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Подготовка текста ответа
def prepare_out(an_dic):
    for key, value in an_dic.items():
        # проверка если слишком длинный ответ, вычисляем
        if len(str(value)) > 50:
            res = str(key) + '=' + handle_calculate(str(value)) 
        else:
            res = str(key) + '=' + str(value)  
    
    return res

if __name__ == '__main__':
    equation = ' '.join(sys.argv[1:])
    res = handle_solve(equation)
    print(res)
  
