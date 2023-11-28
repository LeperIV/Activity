import customtkinter as ctk
import pages
import json
import pathlib
from pprint import pprint
from pages import (PageContainer, WelcomePage, SportPage, GuidePage, UserPage)
import sys
import os

#Создание пути для сохранение базы данных, все наши
#сохраненные данные будут конвертироваться в файл json
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Создание базового окна customtkinter на основе tkinter
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('1024x768')
        self.title('Activity App')
        self.resizable(False, False)
        self.configure(bg='#242424', fg_color='#242424')

        self.pages = pages.pages_dict

        self.page_container = PageContainer(self, self.select_page)
        self.page_container.pack(
            expand=True,
            fill=ctk.BOTH,
            padx=40,
            pady=40
        )
        pages_classes = (
            SportPage(self.page_container, self.read_weight),
            GuidePage(self.page_container),
            UserPage(self.page_container)
        )

        self.welcome_page = WelcomePage(self.page_container)
        self.welcome_page.pack(
            expand=True,
            fill=ctk.BOTH
        )
        self.welcome_page.show_widgets()

        self.selected_page = self.welcome_page

        for page_name, page_class in zip(pages.pages_names.values(), pages_classes):
            if page_class:
                self.pages[page_name] = page_class
    #Метод выбора страницы
    def select_page(self, page_name):
        if self.selected_page.page_name == 'user':
            self.selected_page.leave(self.update_data)

        self.selected_page.forget()

        page = self.pages.get(page_name, None)
        if page:
            page.pack(
                expand=True,
                fill=ctk.BOTH
            )

            if page_name == 'user':
                page.enter(self.read_data)

            self.selected_page = page
        else:
            self.selected_page = self.welcome_page
    #Метод для чтения данных
    def read_data(self, page):
        data_path = 'data.json'
        if not pathlib.Path(data_path).exists():
            self.create_data()
        with open(data_path, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)

            for entry_name, entry_var in page.vars.items():
                if data.get(entry_name, None):
                    entry_var.insert(0, data[entry_name])
    #Метод для чтения созданной json файла
    def read_weight(self):
        data_path = 'data.json'
        with open(data_path, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)

        return data['weight']
    #Обновление файла json при изменении
    def update_data(self, page):
        # data_path = resource_path('data.json')
        data_path = 'data.json'
        if not pathlib.Path(data_path).exists():
            self.create_data()
        with open(data_path, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)

            for entry_name, entry_var in page.vars.items():
                data[entry_name] = entry_var.get()

        with open(data_path, 'w', encoding='utf-8') as data_file:
            json.dump(data, data_file)
    #Созданиее базы данных при переходе в раздел Профиль
    def create_data(self):
        # data_path = resource_path('data.json')
        data_path = 'data.json'
        with open(data_path, 'w', encoding='utf-8') as data_file:
            json.dump({}, data_file)

    def launch(self):
        self.mainloop()
