# coding: utf-8
from sympy import solve, sympify, symbols, simplify
from mpmath import *
import random
import sys
import re

REPLACE_DIGITS = {
    'ноль':'0', 'один':'1', 'два':'2', 'три':'3', 'четыре':'4', 'пять':'5', 'шесть':'6', 'восемь':'8', 'семь':'7', 'девять':'9', 'десять':'10',
    'одиннадцать':'11', 'двенадцать':'12', 'тринадцать':'13', 'четырнадцать':'14', 'пятнадцать':'15', 'шестнадцать':'16', 
    'семнадцать':'17', 'восемнадцать':'18', 'девятнадцать':'19',
    'х':'x', 'у':'y'
}

REPLACE_IN = {
    'уравнение':'',
    'икс':'x', 'игрек':'y', 
    'плюс':'+', 'минус':'-', 
    'умножить':'*',
    '×':'*',
    '−':'-',
    '–':'-',
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
    'корень':'sqrt',
    ' факториал':'!',
    'из':'',
    'на':'',
    'модуль':'abs',
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
# варианты произношений скобок
REPLACE_BRACE = {
    'открывается':'открыть',
    'закрывается':'закрыть',
    'открываем':'открыть',
    'закрываем':'закрыть',
    'открылась':'открыть',
    'закрылась':'закрыть',
    'открылось':'открыть',
    'закрылось':'закрыть',
    'открылись':'открыть',
    'закрылись':'закрыть',
    'открылся':'открыть',
    'закрылся':'закрыть',
    'открыли':'открыть',
    'закрыли':'закрыть',
    'открыта':'открыть',
    'закрыта':'закрыть',
    'открыто':'открыть',
    'закрыто':'закрыть',
    'открыл':'открыть',
    'закрыл':'закрыть',
    'скобки':'скобка',
    'скобку':'скобка',
    'скобочка':'скобка',
    'скобочки':'скобка',
    'скобочку':'скобка',
    'скобу':'скобка',
    'открыть скобка':'(',
    'закрыть скобка':')',
    'скобка открыть':'(',
    'скобка закрыть':')',
    'левая скобка':'(',
    'правая скобка':')',
}

ERRORS = {
    0:['Нет ошибок'],
    1:['Уравнение должно содержать переменную x или y','В вашем уравнении нет неизвестной'],
    2:['Уравнение должно содержать только одну переменную x или y', 'В вашем уравнении больше одной неизвестной'],
    3:['Уравнение может содержать только один знак равенства', 'В вашем уравнении несколько знаков равенства'],
    4:['В уравнении непарные скобки', 'Число отрывающихся скобок не равно числу закрывающихся'],
    5:['В выражении есть русские буквы'],
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
    '-':' минус ',
    'acos':'арккосинус',
    'asin':'арксинус',
    'cos':'косинус',
    'sin':'синус',
    'cot':'котангенс',
    'tan':'тангенс',
    'log':'логарифм',
    'exp':'экспонента',
    'abs':'модуль',
    'x':'икс',
    'y':'игрек',
    'pi':'пи',
    'E':'е',
    'I':'число и',
    '\(':' открыть скобку ',
    '\)':' закрыть скобку ',
    '\n':' - - ',
}

HELP_TEXTS = {
    'реши':['5x+12=7', 'cos(y)=sin(y)'],
    'вычисли':['0.5(0.76-0.06)', '2^5*sqrt(16)'],
    'упрости':['(2x-3y)(3y-2x)-12xy'],
}
# Проверка на int
def is_number_int(s):
    try:
        int(s)
        return int(s) == s
    except (TypeError, ValueError):
        return False

# Основной класс обработки алгебраического выражения        
class Processing:
    def __init__(self, equation):
        # определяем что делать по первому слову в команде
        parts = equation.split(' ', 1)
        self.first_word = parts[0]
        self.equation = parts[1] if len(parts) > 1 else ''
               
    # Главный обработчик
    def process(self):
        # Первичная подготовка текста запроса
        # Замена слов в тексте на переменные и цифры
        self.equation = self.find_replace_multi(self.equation, REPLACE_DIGITS, True)
        self.equation = self.find_replace_multi(self.equation, REPLACE_BRACE)
        self.equation = self.find_replace_multi(self.equation, REPLACE_IN)
        # ставим скобки если остались
        self.brace_placement()
        # добавляем умножение
        self.equation = re.sub(r'(\d+\)?)\s*([a-z(])' , r'\1*\2', self.equation)
        self.equation = re.sub(r'\)\s*\(', r')*(', self.equation)

        # проверка русского текста
        if self.check_russian():
            self.answer = random.choice(ERRORS[5])
            return

        if self.first_word in ['реши', 'решить']:
            self._solve()
        elif self.first_word in ['вычисли', 'вычислить']:
            self._calculate()
        elif self.first_word in ['упрости', 'упростить']:
            self._simplify()
        else: 
            self.answer = False

    # Функция для решения уравнения
    def _solve(self):
        # Проверка на ошибки
        err = 0
        # проверка равенства 
        if self.check_equality() > 1:
            err = 3
        # проверка соответствия скобок
        if not self.check_pairing():
            err = 4
        # проверка числа перемнных  
        var_num = self.check_unknown()
        if var_num == 0:
            err = 1
        if var_num == 2:
            err = 2
        # сообщаем об ошибке
        if 0 != err:
            self.answer = random.choice(ERRORS[err])

        if self.check_equality() == 1:
            self.move()
        # пытаемся решить
        # print(self.equation)
        try:
            x, y = symbols('x,y')
            solution = solve(self.equation, dict=True)
        except NotImplementedError:
            self.answer = 'Такие уравнения я пока решать не умею'
        except Exception:
            self.answer = 'Ошибка в уравнении'
        else:
            if not solution:
                self.answer = 'Нет решений'
            else:
                res = []
                for sol in solution:
                    for key, value in sol.items():
                        # проверка если слишком длинный ответ, вычисляем
                        if len(str(value)) > 50:
                            ans = Processing('вычисли '+str(value))
                            ans._calculate()
                            res.append(str(key) + '=' + str(ans.answer))
                        else:
                            # Округляем если целое
                            if is_number_int(value):
                                value = int(value)
                            res.append(str(key) + '=' + str(value))
                self.answer = 'Ответ %s' % (' или '.join(res))


    # Функция вычисления выражения
    def _calculate(self):
        # проверка равенства 
        if self.check_equality() > 0:
            self.answer = 'Уравнения я могу решать а не вычислять'
        else:    
            try:
                self.answer = sympify(self.equation).evalf(4)
            except Exception:
                self.answer = 'Ошибка в выражении'
            # Округляем если целое
            if is_number_int(self.answer):
                self.answer = int(self.answer)

    # Функция упрощения выражения
    def _simplify(self):
        # проверка равенства 
        if self.check_equality() > 0:
            self.answer = 'Уравнения я могу решать а не упрощать'
        else:    
            try:
                self.answer = simplify(self.equation)
            except Exception:
                self.answer = 'Ошибка в выражении'

    # Функция замены по словарю 
    def find_replace_multi(self, string, dictionary, use_word = False):
        for item in dictionary.keys():
            if use_word:
                string = re.sub(r'\b{}\b'.format(item), r'{}'.format(dictionary[item]), string)
            else:
                string = re.sub(item, dictionary[item], string)

        return str(string)

    # Расстановка скобок без вложенности
    def brace_placement(self, is_left=True):
        if 'скобка' in self.equation:
            brace = '(' if is_left else ')'
            self.equation = self.equation.replace('скобка', brace, 1).strip()
            self.brace_placement(not is_left)

    # перенос в одну часть (приравнивание к 0)
    def move(self):
        parts = self.equation.split('=')
        self.equation = parts[0].strip() + '-(' + parts[1].strip() + ')'

    # Определение наличия русских букв
    def check_russian(self):
        match = re.search(r'[а-яА-ЯёЁ]', self.equation)
        return bool(match)
    # Определение числа вхождений равенства
    def check_equality(self):
        return self.equation.count("=")
    # Проверка парности скобок
    def check_pairing(self):
        return self.equation.count('(') == self.equation.count(')')
    # Проверка наличия неизвестной x или y
    def check_unknown(self):
        # проверка наличия x
        x_in = 'x' in self.equation
        # проверка наличия y
        y_in = 'y' in self.equation
        # сразу оба
        if x_in and y_in:
            return 2
        # нет ни x ни y
        if not (x_in or y_in): 
            return 0
        # есть одна неизвестная
        return 1

             
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
    user_command = req.command.lower().replace('спроси знайка ответит', '').strip()
    # Подготавливаем класс обработчик
    process = Processing(user_command)
    # данные о исходном сообщении
    user_message = req.original.lower().strip()
    # ответ на некорректный запрос
    default_answer = 'Я понимаю фразы начинающиеся с ключевых слов: ' + ', '.join(HELP_TEXTS) + \
    ', дополненные алгебраическим выражением.\n'

    if not process.first_word:
        user_answer = 'Привет!\nЯ могу решать уравнения с одной неизвестной x или y,'+ \
        ' вычислять или упрощать выражения.\nПриступим?'
        res.set_text(user_answer)
        res.set_tts(process.find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
        
    # ответ яндекс боту
    if user_message == 'ping':
        res.set_text('pong')
        user_storage['to_log'] = False
        return res, user_storage

    # если похвалили
    if process.first_word in [
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
    if process.first_word == 'пример':
        s = user_command.split(' ', 2)
        if len(s) == 1 or s[1] not in HELP_TEXTS:
            user_answer = "Укажите ключевое слово для примера: "+', '.join(HELP_TEXTS)
        else:
            user_answer = s[1]+' '+' или '.join(HELP_TEXTS[s[1]])

        res.set_text(user_answer)
        res.set_tts(process.find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage    
    
    if process.first_word in [
        'хватит',
        'стоп',
        'пока'
    ]:
        # Пользователь закончил, прощаемся.
        res.set_text('Приходите ещё, порешаем!')
        res.end()
        return res, user_storage
    # Обрабатываем другие запросы
    process.process()
    
    # Если ошибка попробуем с исходным сообщением
    if isinstance(process.answer, str) and process.answer.startswith('Ошибка'):
        process = Processing(user_message)
        process.process()

    user_answer = str(process.answer if process.answer else default_answer)

    res.set_text(user_answer)
    res.set_tts(process.find_replace_multi(user_answer, REPLACE_TTS))
    res.set_buttons(user_storage['suggests'])

    return res, user_storage


if __name__ == '__main__':
    equation = ' '.join(sys.argv[1:])
    res = Processing(equation)
    res.process()
    user_answer = str(res.answer if res.answer else 'default_answer')
    print(user_answer)
  
