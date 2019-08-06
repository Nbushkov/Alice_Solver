# coding: utf-8
from __future__ import division
from sympy import *
from mpmath  import *
import random
import sys
import re
# словарь замен числительных
REPLACE_DIGITS = {
    'ноль':'0', 'один':'1', 'два':'2', 'три':'3', 'четыре':'4', 'пять':'5', 'шесть':'6', 'восемь':'8', 'семь':'7', 'девять':'9', 'десять':'10',
    'одиннадцать':'11', 'двенадцать':'12', 'тринадцать':'13', 'четырнадцать':'14', 'пятнадцать':'15', 'шестнадцать':'16', 
    'семнадцать':'17', 'восемнадцать':'18', 'девятнадцать':'19', 
    'единице':'1',
    'двойке':'2',
    'тройке':'3',
    'четверке':'4',
    'пятерке':'5',
    'шестерке':'6',
    'семерке':'7',
    'восьмерке':'8',
    'девятке':'9',
    'десятке':'10',
    'единица':'1',
    'двойка':'2',
    'тройка':'3',
    'четверка':'4',
    'пятерка':'5',
    'шестерка':'6',
    'семерка':'7',
    'восьмерка':'8',
    'девятка':'9',
    'десятка':'10',
    'двадцать':'20',
    'тридцать':'30',
    'сорок':'40',
    'пятьдесят':'50',
    'шестьдесят':'60',
    'семьдесят':'70',
    'восемьдесят':'80',
    'девяносто':'90',
    'сто':'100',
    'сотня':'100',
    'полтора':'1.5*',
    'полторы':'1.5*',
    'нуль':'0',
    'нулю':'0', 'одному':'1', 'двум':'2', 'трем':'3', 'четырем':'4', 'трём':'3', 'четырём':'4', 'пяти':'5', 'шести':'6', 'восьми':'8', 'семи':'7', 'девяти':'9', 'десяти':'10',
    'одного':'1', 'двух':'2', 'трех':'3', 'четырех':'4','трёх':'3', 'четырёх':'4',
    'тысяч':'*1000',
    'миллионов':'*10**6',
    'миллиардов':'*10**9',
    'биллионов':'*10**9',
    'триллионов':'*10**12',
    'квадриллионов':'*10**15',
    'квинтиллионов':'*10**18',
    'секстиллионов':'*10**21',
    'сиксилионов':'*10**21',
    'сиксиллионов':'*10**21',
    'септиллионов':'*10**24',
    'октиллионов':'*10**27',
    'нониллионов':'*10**30',
    'дециллионов':'*10**33',
    'миллиарда':'*10**9',
    'биллиона':'*10**9',
    'триллиона':'*10**12',
    'квадриллиона':'*10**15',
    'квинтиллиона':'*10**18',
    'секстиллиона':'*10**21',
    'сиксилиона':'*10**21',
    'сиксиллиона':'*10**21',
    'септиллиона':'*10**24',
    'октиллиона':'*10**27',
    'нониллиона':'*10**30',
    'дециллиона':'*10**33',
    'миллиард':'10**9',
    'биллион':'10**9',
    'триллион':'10**12',
    'квадриллион':'10**15',
    'квинтиллион':'10**18',
    'секстиллион':'10**21',
    'триллиард':'10**21',
    'сиксилион':'10**21',
    'сиксиллион':'10**21',
    'септиллион':'10**24',
    'октиллион':'10**27',
    'нониллион':'10**30',
    'дециллион':'10**33',
    'дважды':'2*',
    'трижды':'3*',
    'четырежды':'4*',
    'икса':'x', 'игрека':'y', 
    'икс':'x', 'игрек':'y', 
    'игрик':'y', 
    'х':'x', 'у':'y', 
    'зет':'z', 'зед':'z', 'зэт':'z', 'зэд':'z', 
    'число пи':'pi',
    'число е':'E', 
    'число и':'I',
    'пи':'pi',
    'е':'E', 
    'бесконечность':'oo', 
}
# словарь замен 
REPLACE_ACTIONS = {   
    'плюс':'+', 'минус':'-', 
    'добавить':'+',  
    'прибавить':'+',  
    'отнять':'-', 
    'вычесть':'-', 
    'помноженное':'*',
    'помножить':'*',
    'умноженное':'*',
    'умножили':'*',
    'умножить':'*',
    'умножаем':'*',
    'умножим':'*',
    'умножь':'*',
    '×':'*',
    '−':'-',
    '–':'-',   
    'разделить':'/',
    'поделить':'/',
    'поделили':'/',
    'поделенное':'/',
    'деленное':'/',
    'делить':'/',
    'разделим':'/',
    'разделили':'/',
    'раздели':'/',
    'делим':'/',
    '÷':'/',
    ':':'/',
    'xy':'x*y',
    'yx':'y*x',
    'x y':'x*y',
    'y x':'y*x',
    'равняется':'=',
    'получается':'=',
    'равно':'=',
    'равен':'=',
    'равняет':'=',
    ' в квадрате':'**2',
    'квадрате':'**2',
    ' в кубе':'**3',
    'кубе':'**3',
    ' квадрат':'**2',
    ' куб':'**3',
    ' во второй':'**2',
    ' в третьей':'**3',
    ' в четвертой':'**4',
    ' в пятой':'**5',   
    ' в шестой':'**6',   
    ' в седьмой':'**7',   
    ' в восьмой':'**8',   
    ' в девятой':'**9',   
    ' в десятой':'**10',   
    ' в степени':'**',
    ' факториал':'!',
}
# словарь замен функций
REPLACE_FUNCTIONS = {
    'квадратный корень':'sqrt',
    'корень':'sqrt',
    'модуль':'abs',
    'арккосинус':'acos',
    'арксинус':'asin',
    'арккотангенс':'acot',
    'арктангенс':'atan',
    'косинус':'cos',
    'синус':'sin',
    'котангенс':'cot',
    'тангенс':'tan',
    'экспонента':'exp',
    'експонента':'exp',
    'логарифм':'log',
    'производная':'diff',
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
    'скобках':'скобка',
    'скобки':'скобка',
    'скобке':'скобка',
    'скобку':'скобка',
    'скобочка':'скобка',
    'скобочки':'скобка',
    'скобочку':'скобка',
    'скобу':'скобка',
    'скобка открыть':'(',
    'скобка закрыть':')',
    'открыть скобка':'(',
    'закрыть скобка':')',
    'левая скобка':'(',
    'правая скобка':')',
}
# словарь ошибок
ERRORS = {
    0:['Нет ошибок'],
    1:['Нет выражения','Необходимо ввести выражение', 'Укажите выражение'],
    2:['Уравнение должно содержать только одну переменную x,y или z', 'В вашем уравнении больше одной неизвестной'],
    3:['Уравнение может содержать только один знак равенства', 'В вашем уравнении несколько знаков равенства'],
    4:['В уравнении непарные скобки', 'Число отрывающихся скобок не равно числу закрывающихся'],
    5:['Уравнение должно содержать переменную x,y или z.', 'Похоже в вашем уравнении нет неизвестной', 'Я могу решать уравнения с x,y или z. Попробуйте перефразировать'],
    6:['Уравнение можно только решить, а не упростить или разложить'],
}
# словарь озвучки результата
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
    'LambertW':'W-функция Ламберта',
    'x':'икс',
    'y':'игрек',
    'pi':'пи',
    'E':'е',
    'I':'число И',
    '\(':' открыть скобку ',
    '\)':' закрыть скобку ',
    'oo': 'бесконечность', 
    'inf': 'бесконечность', 
    'nan': 'Результат неопределен',
    '\n':' - - ',
}
# словарь больших чисел
REPLACE_LARGE_TTS = {
    '1000000000000000000000000000000000': 'дециллион',
    '1000000000000000000000000000000': 'нониллион',
    '1000000000000000000000000000': 'октиллион',
    '1000000000000000000000000': 'септиллион',
    '1000000000000000000000': 'секстиллион',
    '1000000000000000000': 'квинтиллион',
    '1000000000000000': 'квадриллион',
    '1000000000000': 'триллион',
    '1000000000': 'миллиард',
}
# словарь примеров
HELP_TEXTS = {
    'реши':['5x+12=7', 'Я могу решать уравнения с одной неизвестной x,y или z.\n' +\
            'Для этого скажите команду Реши и продиктуйте уравнение или введите с клавиатуры.'],
    'вычисли':['2^5*sqrt(16)', 'Я могу вычислять числовое значение выражения без переменных, для этого скажите команду Вычисли и продиктуйте выражение.'],
    'упрости':['(2x-3y)(3y-2x)-12xy', 'Я могу упрощать алгебраические выражения, для этого скажите команду Упрости и продиктуйте выражение.'],
    'разложи':['x**2 + 4xy + 4y**2', 'Я могу раскладывать на множители алгебраические выражения, для этого скажите команду Разложи и продиктуйте выражение.'],
}
# лишие слова, междометия
UNNECESSARY_WORDS = ['давай', 'на', 'ну', 'а', 'и', 'из', 'от']
# Команды решения
COMMAND_SOLV = ['реши', 'решить',  'решите', 'решение']
# Команды упрощения
COMMAND_SIMPL = ['упрости', 'упростить', 'упростите', 'ну прости', 'прости', 'опусти', 'сократи']
# Команды вычисления
COMMAND_CALC = ['вычисли', 'вычислить', 'сколько', 'найди']
# Команды разложения на множители
COMMAND_FACT = ['разложи', 'разложить', 'разложение']
# ответ на некорректный запрос
DEFAULT_ANSWER = ['У меня нет ответа.', 'Я просто работаю с выражениями.', 'Этого я не понимаю.', 'Я не по этой части.', 'Я понимаю определенные команды.']
# побуждающая прибавка к тексту
DEFAULT_ENDING = 'Назовите команду или скажите Помощь.'
# точность (число знаков) для округления
CALC_PRECISION = 4

'''
Общие функции 
'''
# Классическое Округление (чтоб не было лишних нулей)
def rd(x, prec=50):
    if not isinstance(x, Float):
        return x
    if x.equals(0):
        return 0
    x = x.round(prec)
    return str(x).rstrip('0').rstrip('.')

# Функция замены по словарю 
def find_replace_multi(string, dictionary, use_word = False):
    for item in dictionary.keys():
        if use_word:
            pattern = r'\b({})\b'.format(item)
            string = re.sub(pattern, r'{}'.format(dictionary[item]), string)
        else:
            string = re.sub(item, dictionary[item], string)

    return str(string)

# исходное выражение выбросим лишние слова
def clear_str(string):
    for item in UNNECESSARY_WORDS:
        string = re.sub(r'\b{}\b'.format(item), '', string)
    return string.strip()
# Вставка математиченской функции в строку
def insert_function(fpattern, fname, string):
    start = string.find(fpattern)
    if start == -1:
        return string
    pat_len = len(fpattern)
    nam_len = len(fname)
    index1 = start + pat_len
    # делаем замену в зависимости от наличия скобки
    sko = re.search(r"\S", string[index1:])
    if sko is not None and '(' == sko.group():
        string = string.replace(fpattern, fname, 1)
    else:
        string = string.replace(fpattern, fname+'(', 1)
        index2 = start + nam_len + 1
        # ищем позицию для закрытия скобки
        # первый непробельный и первый значимый (не знаки действий) символ
        nonspace = re.search(r"\S", string[index2:])
        datastart = re.search(r"[^-+*/\s]", string[index2:])       
        if datastart is not None:
            # убираем лишние пробелы после открывающей скобки
            index_nonspace = index2 + nonspace.start()
            string = string[:index2] + string[index_nonspace:]
            index3 = index2 + datastart.start() - nonspace.start()
        else:
            index3 = len(string)
        # первый пробел после непробельного или конец строки
        space = re.search(r"[\s=]", string[index3:])
        end = len(string) if space is None else index3 + space.start()
        string = string[:end] + ')' + string[end:]
    # если паттерн есть еще, повторяем
    if fpattern in string:
        string = insert_function(fpattern, fname, string)

    return string

'''
Основной класс обработки алгебраического выражения      
'''
class Processing:
    def __init__(self, equation):
        # выделяем первое слово в команде
        parts = equation.split(' ', 1)
        self.first_word = parts[0]
        # исходное выражение
        self.equation = equation
        # код ошибки
        self.error = 0
        # тип задачи
        self.task = 'unknown'

    # Главный обработчик
    def process(self):
        self._prepare()
        print(self.equation)
        if self.task == 'solve':
            self._solve()
        elif self.task == 'calculate':
            self._calculate()
        elif self.task == 'simplify':
            self._simplify()
        elif self.task == 'factorize':
            self._factorize()           

    # Предварительная подготовка выражения
    def _prepare(self):
        self.error = 0
        # дефолтный ответ на непонятный запрос
        self.answer = False
        # Замена слов в тексте на переменные и цифры
        self.equation = find_replace_multi(self.equation, REPLACE_DIGITS, True)
        self.equation = find_replace_multi(self.equation, REPLACE_BRACE)
        self.equation = find_replace_multi(self.equation, REPLACE_ACTIONS)
        # замена запятых в числах на точки
        self.equation = re.sub(r'(\d),(\d)', r'\1.\2', self.equation)
        # обработка составного числа с дробной частью (со словом целых)
        self.equation = re.sub(r'(\d+\)?) целых ([\d/]+)' , r'(\1+\2)', self.equation)
        # обработка в степени с числовым показателем
        self.equation = re.sub(r'в (\d+\)?) степени' , r'**\1', self.equation)
        # ставим скобки если остались
        self.brace_placement()  
        # ставим функции, если есть
        for func in REPLACE_FUNCTIONS.keys():
            self.equation = insert_function(func, REPLACE_FUNCTIONS[func], self.equation)
        # Заменяем i на I для корректной обработки мнимой единицы
        self.equation = re.sub(r"\bi\b","I", self.equation)
        # Заменяем e на E для корректной обработки числа e
        self.equation = re.sub(r"\be\b","E", self.equation)
        # базовые проверки
        # проверка соответствия скобок
        if not self.check_pairing():
            self.error = 4
        # проверка знаков равенства 
        eqn = self.check_equality()
        if eqn > 1:
            self.error = 3   
        
        # определяем тип задачи
        if any(c in self.equation for c in COMMAND_SOLV) or eqn == 1:
            self.task = 'solve'
        if any(c in self.equation for c in COMMAND_SIMPL):
            self.task = 'simplify'
        if any(c in self.equation for c in COMMAND_CALC):
            self.task = 'calculate'
        if any(c in self.equation for c in COMMAND_FACT):
            self.task = 'factorize'
        # Определяем число русских слов в выражении, для предположения что это задача
        if len(re.findall(r'[а-яё]+', self.equation, re.I)) > 7:
            self.answer = 'Похоже на условие задачи, я работаю только с алгебраическими выражениями.'
            self.task = 'unknown'
            return
        # убираем оставшийся русский текст
        self.equation = re.sub('[а-яА-ЯёЁ,]', '', self.equation).strip()
        # если ничего не осталось то дефолтный ответ
        if self.equation == '':
            return
        # убираем пробелы между числами
        self.equation = re.sub('(?<=\d)\s+(?=\d)', '', self.equation)
        # добавляем умножение после чисел
        self.equation = re.sub(r'(\d+\)?)\s*([a-z(])' , r'\1*\2', self.equation)
        # перед скобкой
        self.equation = re.sub(r'([x,y,z])\s*\(', r'\1*(', self.equation)
        # между скобками
        self.equation = re.sub(r'\)\s*\(', r')*(', self.equation)
        # после скобки
        self.equation = re.sub(r'\)\s*([x,y,z,\d]){1}', r')*\1', self.equation)
        # убираем лишние плюсы и равенства (по краям)
        self.equation = self.equation.strip('+= */').rstrip('-')
        # если неясно, смотрим по переменным
        if self.task == 'unknown':
            var_num = self.check_unknown()
            if var_num == 1:
                self.task = 'solve'
            elif var_num == 0:
                self.task = 'calculate'
            elif self.equation != '':
                self.task = 'simplify'
        
    # Функция для решения уравнения
    def _solve(self):
        eqn = self.check_equality()    
        # проверка числа перемнных  
        var_num = self.check_unknown()
        if var_num > 1:
            self.error = 2 
        if var_num == 0 and eqn == 1:
            self.error = 5
        # Проверка на ошибки
        if self.check_errors():
            return
        # если переменных нет, и нет равенства пытаемся вычислить
        if var_num == 0 and eqn == 0:
            self._calculate()
            return
        # переносим все в левую часть (приравниваем к 0)
        if eqn == 1:
            self.move()
        # пытаемся решить       
        try:
            x, y, z = symbols('x y z')
            # сначала упростим чтоб не нагромождать
            self.equation = simplify(self.equation)
            # проверка на вырождение уравнения
            if self.equation.equals(0):
                self.answer = 'Ответ любое число'
                return
            solution = solve(self.equation, dict=True)
        except NotImplementedError:
            self.answer = 'Такие уравнения я пока решать не умею'
        except Exception:
            self.answer = 'Ошибка в уравнении: ' + self.equation
        else:
            if not solution:
                self.answer = 'Нет решений'
            else:

                res = []
                for sol in solution:
                    for key, value in sol.items():
                        # проверка если слишком длинный ответ, вычисляем
                        if len(str(value)) > 40 or 'CRootOf' in str(value):
                            value = value.evalf(CALC_PRECISION)
                        # Округляем
                        value = rd(value, CALC_PRECISION)
                        res.append(str(key) + '=' + str(value))
                self.answer = 'Ответ %s' % (' или '.join(res))

    # Функция вычисления выражения
    def _calculate(self, prec=50):
        # Проверка на ошибки
        if self.check_errors():
            return
        # проверка наличия равенства или переменной
        if self.check_equality() == 1:
            self._solve()
        else:    
            try:
                self.answer = simplify(self.equation).evalf(prec)
                # Округляем
                if prec == 50:
                    prec = 10
                self.answer = rd(self.answer, prec)
            except Exception:
                self.answer = 'Ошибка в выражении: ' + self.equation

    # Функция упрощения выражения
    def _simplify(self):
        # проверка равенства 
        if self.check_equality() == 1:
            self.error = 6
        # Проверка на ошибки
        if self.check_errors():
            return 
        try:
            self.equation = simplify(self.equation)
            # дополнительно пробуем разложить на множители
            self.answer = factor(self.equation)
            # Округляем
            self.answer = rd(self.answer, CALC_PRECISION)
        except Exception:
            self.answer = 'Ошибка в выражении: ' + self.equation

    # Функция разложения на множители
    def _factorize(self):
        # проверка равенства 
        if self.check_equality() == 1:
            self.error = 6
        # Проверка на ошибки
        if self.check_errors():
            return  
        try:
            self.answer = factor(self.equation)
        except Exception:
            self.answer = 'Ошибка в выражении: ' + self.equation

    # Расстановка скобок без вложенности
    def brace_placement(self):
        start = self.equation.find('скобка')
        if start > -1:
            # определяем тип скобки исходя из имеющихся
            is_left = bool(self.equation[:start].count('(') <= self.equation[:start].count(')'))
            brace = '(' if is_left else ')'
            self.equation = self.equation.replace('скобка', brace, 1).strip()
            self.brace_placement()

    # перенос в одну часть (приравнивание к 0)
    def move(self):
        parts = self.equation.split('=')
        self.equation = parts[0].strip() + '-(' + parts[1].strip() + ')'
    # Определение числа вхождений равенства
    def check_equality(self):
        return self.equation.count('=')
    # Проверка парности скобок
    def check_pairing(self):
        return self.equation.count('(') == self.equation.count(')')
    # Проверка наличия неизвестной x,y или z
    def check_unknown(self):
        # проверка наличия x
        x_in = 'x' in self.equation
        # проверка наличия y
        y_in = 'y' in self.equation
        # проверка наличия z
        z_in = 'z' in self.equation
        return int(x_in) + int(y_in) + int(z_in)
    # Проверка наличия ошибок
    def check_errors(self):
        # проверка на наличие выражения
        if self.equation == '':
            self.error = 1 
        # Проверка на ошибки
        if bool(self.error):
            self.answer = random.choice(ERRORS[self.error])
            return True
        # ошибок нет    
        return False

             
# Функция для непосредственной обработки диалога.
def handle_dialog(req, res, user_storage):
    if req.is_new_session or user_storage is None:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        user_storage = {
            'user_id': req.user_id,
            'suggests': [
            {'title': 'Помощь', 'hide': True},
            {
                "title": "Сайт",
                "url": "https://gdeze.ru",
                "hide": True
            },
            {
                "title": "Оценить",
                "url": "https://dialogs.yandex.ru/store/skills/48b31fb4-areshkin-pomozhet-reshit-i-podschi",
                "hide": True
            }],
            "to_log": True
        }

    # Флаг добавления в логи
    user_storage['to_log'] = True
    # данные о команде, убираем лишнее
    user_command = req.command.lower().replace('спроси знайка ответит', '').strip()
    # исходное выражение выбросим лишние слова
    user_command = clear_str(user_command)
    # Подготавливаем класс обработчик
    process = Processing(user_command)
    # данные о исходном сообщении
    user_message = req.original.lower().strip()
    user_message = clear_str(user_message)
    # токены
    user_tokens = req.tokens

    if not process.first_word or process.first_word in [
        'запусти',
        'включи',
    ]: 
        user_answer = 'Привет!\nЯ помогаю решать уравнения и примеры по алгебре.\n'+\
        'Чтобы узнать подробнее скажите Помощь.'
        res.set_text(user_answer)
        res.set_tts(find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
        
    # ответ яндекс боту
    if user_message == 'ping':
        res.set_text('pong')
        user_storage['to_log'] = False
        return res, user_storage
    # ответ почему
    if user_message == 'почему':
        res.set_text('По правилам алгебры. Я вычисляю результат, а не рассказываю как решать.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # ответ нет
    if user_message == 'нет':
        res.set_text('На нет и суда нет. '+DEFAULT_ENDING)
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # ответ на слово команда
    if user_message == 'команда' or user_message == 'команду':
        res.set_text('Я понимаю команды: ' + ', '.join(HELP_TEXTS) + '. Для помощи по командам скажите помощь и имя команды.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # Знакомство
    if 'как' in user_tokens and 'зовут' in user_tokens:
        res.set_text('Меня зовут Знайка. И я люблю считать.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # Просьба вернуть Алису
    if 'алиса' in user_tokens:
        res.set_text('Я не Алиса. Чтобы закончить скажите выйти или стоп.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # Просьба вернуть Марусю
    if 'маруся' in user_tokens:
        res.set_text('Я не Маруся. Чтобы закончить скажите выйти или стоп.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # переход по ссылке
    if process.first_word in [
        'сайт',
        'оценить',
    ]:
        # отвечаем аналогично
        res.set_text('Открываю ссылку')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # если похвалили
    if any(i in user_tokens for i in [
        'верно',
        'хорошо',
        'офигеть',
        'красавчик',
        'молодец',
        'спасибо',
    ]):
        # Благодарим пользователя
        res.set_text('Спасибо, я стараюсь!')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # если не согласны
    if any(i in user_tokens for i in [
        'неправильно',
        'неверный',
        'неверно',
        'ошибка',
    ]):
        # предлагаем повторить
        res.set_text('Возможно я не расслышал, попробуйте повторить.')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # всяко разное
    if process.first_word in [
        'привет',
        'ладно',
        'здрасте',
        'пожалуйста',
        'да',
    ]:
        # отвечаем аналогично
        res.set_text('Ну '+process.first_word)
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
# ответ на ругательства
    if req.danger:
        res.set_text('Давайте не будем ругаться!')
        res.set_buttons(user_storage['suggests'])
        return res, user_storage
    # помощь юзеру и примеры
    if process.first_word in [
        'помощь',
        'помочь',
        'помоги',
    ]:
        s = user_command.split(' ', 2)
        if len(s) == 1:
            user_answer = 'Я умею решать уравнения с одной неизвестной x,y или z, упрощать и вычислять алгебраические выражения.\n'+\
            'Я понимаю команды: ' + ', '.join(HELP_TEXTS) + ', дополненные алгебраическим выражением.\n'+ \
            'Для помощи по командам скажите помощь и имя команды.\n'+ \
            'Для помощи по вводу выражений со скобками скажите помощь скобки.\n'+ \
            'Для помощи по математическим функциям скажите помощь функции.\n'+ \
            'Чтобы закончить скажите выйти или стоп.'
        elif s[1] in HELP_TEXTS:
            user_answer = HELP_TEXTS[s[1]][1]+'\nНапример: '+ s[1] +' '+HELP_TEXTS[s[1]][0]
        elif s[1] in [
            'скобки',
            'скобка',
            'скобке',
            'скобку'
        ]:
            user_answer = 'Если в вашем выражении нет вложенных скобок, то при голосовом вводе любой скобки можно просто говорить скобка.\n'+\
            'Если скобки вложенные то нужно говорить открыть скобку и закрыть скобку соответственно.'
        elif s[1] in [
            'функции',
            'функция',
            'функций',
        ]:
            user_answer = 'Я понимаю тригонометрические функции, а также, корень, логарифм и экспонента.'
        else:
            user_answer = 'Уточните помощь по какому разделу вас интересует.\n'+\
            'Для помощи по командам скажите помощь и имя команды.\n'+ \
            'Для помощи по вводу выражений со скобками скажите помощь скобки.\n'+ \
            'Для помощи по математическим функциям скажите помощь функции.'

        res.set_text(user_answer)
        res.set_tts(find_replace_multi(user_answer, REPLACE_TTS))
        res.set_buttons(user_storage['suggests'])
        return res, user_storage    
    
    if process.first_word in [
        'выйти',
        'стоп',
        'хватит',
        'пока'
    ]:
        # Пользователь закончил, прощаемся.
        res.set_text('Приходите ещё, порешаем!')
        res.end()
        return res, user_storage

    # Обрабатываем основные запросы
    process.process()
    
    # Если ошибка попробуем с исходным сообщением
    if isinstance(process.answer, str) and process.answer.startswith('Ошибка') and len(user_message) > 1:
        process = Processing(user_message)
        process.process()

    user_answer = str(random.choice(DEFAULT_ANSWER)+' '+DEFAULT_ENDING if process.answer is False else process.answer)

    res.set_text(user_answer)
    # озвучка результата
    tts = find_replace_multi(user_answer, REPLACE_TTS)
    tts = find_replace_multi(tts, REPLACE_LARGE_TTS, True)
    res.set_tts(tts)
    res.set_buttons(user_storage['suggests'])

    return res, user_storage


if __name__ == '__main__':
    equation = ' '.join(sys.argv[1:])
    equation = clear_str(equation)
    res = Processing(equation)
    res.process()
    if bool(res.error):
        res.answer = random.choice(ERRORS[res.error])
    user_answer = str(random.choice(DEFAULT_ANSWER) if res.answer is False else res.answer)
    tts = find_replace_multi(user_answer, REPLACE_TTS)
    tts = find_replace_multi(tts, REPLACE_LARGE_TTS, True)
    print(user_answer)
    print(tts)
  