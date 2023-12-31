import customtkinter as ctk
import json
from pages import pages_names
from pages import sport_text
from PIL import Image
import sys
import os

# Функция которая позволяет найти путь к файлам внутри единого exe файла
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Класс контейнера для страницы куда будут помещться все страницы
class PageContainer(ctk.CTkFrame):
    def __init__(self, master, page_select_callback):
        super().__init__(master)

        self.page_button_var = ctk.StringVar()
        self.page_select_callback = page_select_callback

        self.configure(fg_color='#242424')

        self.page_buttons = ctk.CTkSegmentedButton(
            self,
            values=[name.title() for name in pages_names],
            font=('Arial', 37),
            height=60,
            variable=self.page_button_var,
            command=self.select_page
        )
        self.page_buttons.pack(
            side=ctk.BOTTOM,
            pady=(40, 0)
        )
    #Метод для выбора страницы 
    def select_page(self, *args):
        selected_page_name = self.page_button_var.get()
        self.page_select_callback(pages_names[selected_page_name.lower()])

#Класс для создания начального окна
class WelcomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.page_name = 'welcome'
        self.configure(fg_color='#242424')
        self.show_widgets()
    #Текст и шрифт внутри окна
    def show_widgets(self):
        self.welcome_label = ctk.CTkLabel(
            self,
            text='Добро пожаловать',
            font=('Arial', 50)
        )
        self.welcome_label.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.45)

        self.welcome_text = ctk.CTkLabel(
            self,
            text='Выберите пункт меню',
            font=('Arial', 27)
        )
        self.welcome_text.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.525
        )

#Класс для раздела пользователь в котором будет имя фамилия рост вес 
class UserPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.page_name = 'user'
        self.configure(fg_color='#242424')
        self.show_widgets()
    #Метод для показа видежетов
    def show_widgets(self):
        self.form = ctk.CTkFrame(
            self,
            width=500,
        )
        self.form.propagate(False)
        self.form.pack(
            expand=True,
            fill=ctk.Y
        )

        width = 300
        placeholder_color = '#6b6b6b'
        font = ('Arial', 30)

        self.name = ctk.CTkEntry(
            self.form,
            placeholder_text='Имя',
            placeholder_text_color=placeholder_color,
            width=width,
            font=font
        )
        self.surname = ctk.CTkEntry(
            self.form,
            placeholder_text='Фамилия',
            placeholder_text_color=placeholder_color,
            width=width,
            font=font,
        )
        self.height = ctk.CTkEntry(
            self.form,
            placeholder_text='Рост',
            placeholder_text_color=placeholder_color,
            width=width,
            font=font
        )
        self.weight = ctk.CTkEntry(
            self.form,
            placeholder_text='Вес',
            placeholder_text_color=placeholder_color,
            width=width,
            font=font
        )
        #Пакуем все вызванные виджеты через переборку
        for widget in (self.name, self.surname, self.height, self.weight):
            widget.pack(
                pady=(40, 0)
            )

        self.vars = {
            'name': self.name,
            'surname': self.surname,
            'height': self.height,
            'weight': self.weight
        }

        self.bmi_var = ctk.StringVar()

        self.your_bmi = ctk.CTkLabel(
            self.form,
            font=('Arial', 30),
            text='Ваш ИМТ'
        )
        self.your_bmi.pack(
            pady=(50, 0)
        )
        self.bmi = ctk.CTkLabel(
            self.form,
            font=('Arial', 40),
            textvariable=self.bmi_var,
            wraplength=350
        )
        self.bmi.pack(
            pady=(10, 0)
        )
    #Выйти со страницы
    def leave(self, callback):
        callback(self)
        for var in self.vars.values():
            var.delete(0, ctk.END)
    #Войти в страницу пользователя 
    def enter(self, callback):
        callback(self)
        self.get_bmi(self.weight.get(), self.height.get())
#По таблице можно рассчитать ИМТ тела
    def get_bmi(self, weight, height):
        if not weight or not height:
            return

        bmi = float(weight) / ((float(height) / 100) ** 2)

        bmi_table = {
            (0, 16): 'Выраженный дефицит массы',
            (16, 18.49): 'Недостаточная масса тела',
            (18.5, 25): 'Норма',
            (25, 30): 'Избыточная масса тела',
            (30, 35): 'Ожирение 1-й степени',
            (35, 40): 'Ожирение 2-й степени',
            (40, float('inf')): 'Ожирение 3-й степени'
        }

        bmi_colors = ('#6699cc', '#339966', '#33cc66',
                      '#00cc00', '#ff6600', '#ff3300',
                      '#ff0000')

        for i, ((lower_limit, upper_limit), value) in enumerate(bmi_table.items()):
            if lower_limit <= bmi < upper_limit:
                self.bmi_var.set(value)
                self.bmi.configure(
                    text_color=bmi_colors[i]
                )

#Создания класса для раздела Спорт
class SportPage(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.read_callback = callback
        self.page_name = 'sport'
        self.configure(fg_color='#242424')
        self.show_widgets()
    #Для показа Виджетов для Спорта
    def show_widgets(self):
        #Импортируем из папки image с помощью resourse_path 
        jogging = Image.open(resource_path('images/jogging.jpg'))
        cycling = Image.open(resource_path('images/cycling.jpg'))
        brisk_walking = Image.open(resource_path('images/brisk_walking.jpg'))
        swimming = Image.open(resource_path('images/swimming.jpg'))

        jogging_ratio = jogging.width / jogging.height
        cycling_ratio = cycling.width / cycling.height
        brisk_walking_ratio = brisk_walking.width / brisk_walking.height
        swimming_ratio = swimming.width / swimming.height
        
        #Размер фотки 
        image_height = 1100

        #Подсчет для каждого вида спорта
        self.sports = ('Бег', 'Езда на велосипеде', 'Быстрая ходьба', 'Плавание')
        self.sport_images = (
            ctk.CTkImage(jogging, size=(int(image_height * jogging_ratio), image_height)),
            ctk.CTkImage(cycling, size=(int(image_height * cycling_ratio), image_height)),
            ctk.CTkImage(brisk_walking, size=(int(image_height * brisk_walking_ratio), image_height)),
            ctk.CTkImage(swimming, size=(int(image_height * swimming_ratio), image_height))
        )
        self.sport_questions = (
            'Сколько вы пробежали?', 'Сколько вы проехали?', 'Сколько вы прошли?',
            'Сколько вы проплыли?'
        )

        self.selected_sport = 0

        self.sport_frame = ctk.CTkFrame(
            self,
            fg_color='#242424'
        )

        self.sport_frame.pack(
            expand=True,
            fill=ctk.BOTH,
            pady=(0, 40)
        )

        self.sport_image = ctk.CTkLabel(
            self.sport_frame,
            image=self.sport_images[self.selected_sport],
            text=''
        )
        self.sport_image.place(
            anchor=ctk.CENTER,
            relx=0.2,
            rely=0.4
        )

        self.form_frame = ctk.CTkFrame(
            self.sport_frame,
            fg_color='#242424',
            width=600,
            corner_radius=0
        )
        self.form_frame.pack(
            side=ctk.RIGHT,
            fill=ctk.Y
        )

        self.question = ctk.CTkLabel(
            self.form_frame,
            font=('Arial', 20),
            text=self.sport_questions[self.selected_sport]
        )
        self.question.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.3
        )

        self.distance_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text='Дистанция',
            font=('Arial', 30),
            width=300
        )
        self.distance_entry.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.4
        )
        self.distance_entry.bind(
            '<KeyPress-Return>',
            self.calculate_calories
        )

        self.meteres = ctk.CTkLabel(
            self.form_frame,
            font=('Arial', 30),
            text='метров'
        )
        self.meteres.place(
            anchor=ctk.CENTER,
            relx=0.84,
            rely=0.4
        )

        self.calculate_button = ctk.CTkButton(
            self.form_frame,
            font=('Arial', 25),
            text='Посчитать калории',
            command=self.calculate_calories
        )
        self.calculate_button.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.5
        )

        self.calculated_calories = ctk.CTkLabel(
            self.form_frame,
            font=('Arial', 30),
            text=''
        )
        self.calculated_calories.place(
            anchor=ctk.CENTER,
            relx=0.5,
            rely=0.75
        )

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color='#242424'
        )
        self.buttons_frame.pack()

        self.left_button = ctk.CTkButton(
            self.buttons_frame,
            width=50,
            font=('Arial', 40),
            text='◀',
            command=self.cycle_left
        )
        self.left_button.pack(
            side=ctk.LEFT,
            padx=(0, 20)
        )

        self.sport_name = ctk.CTkLabel(
            self.buttons_frame,
            font=('Arial', 40)
        )
        self.sport_name.pack(
            side=ctk.LEFT
        )

        self.right_button = ctk.CTkButton(
            self.buttons_frame,
            width=50,
            font=('Arial', 40),
            text='▶',
            command=self.cycle_right
        )
        self.right_button.pack(
            side=ctk.LEFT,
            padx=(20, 0)
        )

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )
    #Кнопка для перехода влево при этом происходит -1
    def cycle_left(self, *args):
        if not self.selected_sport:
            self.selected_sport = len(self.sports) - 1
        else:
            self.selected_sport -= 1

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )
        self.sport_image.configure(
            image=self.sport_images[self.selected_sport]
        )
        self.question.configure(
            text=self.sport_questions[self.selected_sport]
        )
    #Кнопка для перехода вправо при этом происходит +1
    def cycle_right(self, *args):
        if self.selected_sport == len(self.sports) - 1:
            self.selected_sport = 0
        else:
            self.selected_sport += 1

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )
        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )
        self.sport_image.configure(
            image=self.sport_images[self.selected_sport]
        )
        self.question.configure(
            text=self.sport_questions[self.selected_sport]
        )
    #Для каждого вида спорта идет свой подсчет
    def calculate_calories(self, *args):
        coeffs = (0.9, 0.5, 0.7, 0.5)

        distance = self.distance_entry.get()
        weight = self.read_callback()
        #Задаем переменную с формулой
        calories = coeffs[self.selected_sport] * int(weight) * (int(distance) / 1000)
        #показ калорий
        string = f'Соженно калорий: {int(calories)}'

        self.calculated_calories.configure(
            text=string
        )

#Класс раздела Руководство
class GuidePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.page_name = 'guide'
        self.configure(fg_color='#242424')
        self.show_widgets()
    #Создание метода для показа виджетов в окне
    def show_widgets(self):
        self.sports = ('Бег', 'Езда на велосипеде', 'Быстрая ходьба', 'Плавание')
        self.selected_sport = 0

        self.text_frame = ctk.CTkFrame(
            self,
            fg_color='#242424',
        )

        self.text_frame.pack(
            expand=True,
            fill=ctk.BOTH,
            pady=(0, 40)
        )

        self.text_state = ctk.NORMAL
        self.text = ctk.CTkTextbox(
            self.text_frame,
            fg_color='#242424',
            font=('Arial', 17),
            wrap=ctk.WORD
        )
        self.text.insert(0.0, sport_text.texts[self.selected_sport])
        self.switch_text()

        self.text.pack(
            expand=True,
            fill=ctk.BOTH
        )

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color='#242424'
        )
        self.buttons_frame.pack()

        self.left_button = ctk.CTkButton(
            self.buttons_frame,
            width=50,
            font=('Arial', 40),
            text='◀',
            command=self.cycle_left
        )
        self.left_button.pack(
            side=ctk.LEFT,
            padx=(0, 20)
        )

        self.sport_name = ctk.CTkLabel(
            self.buttons_frame,
            font=('Arial', 40)
        )
        self.sport_name.pack(
            side=ctk.LEFT
        )

        self.right_button = ctk.CTkButton(
            self.buttons_frame,
            width=50,
            font=('Arial', 40),
            text='▶',
            command=self.cycle_right
        )
        self.right_button.pack(
            side=ctk.LEFT,
            padx=(20, 0)
        )

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )
    #Сменить текст при смене физической активности 
    def switch_text(self):
        if self.text_state == ctk.DISABLED:
            self.text_state = ctk.NORMAL
        else:
            self.text_state = ctk.DISABLED

        self.text.configure(
            state=self.text_state
        )
    #Создание кнопки влево для перехода на след окно
    def cycle_left(self, *args):
        self.switch_text()
        self.text.delete(0.0, ctk.END)

        if not self.selected_sport:
            self.selected_sport = len(self.sports) - 1
        else:
            self.selected_sport -= 1

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )

        self.text.insert(0.0, sport_text.texts[self.selected_sport])
        self.switch_text()
    #сокздание кнопки вправо
    def cycle_right(self, *args):
        self.switch_text()
        self.text.delete(0.0, ctk.END)

        if self.selected_sport == len(self.sports) - 1:
            self.selected_sport = 0
        else:
            self.selected_sport += 1

        self.sport_name.configure(
            text=self.sports[self.selected_sport]
        )

        self.text.insert(0.0, sport_text.texts[self.selected_sport])
        self.switch_text()
