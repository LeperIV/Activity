from window import Window

# Основной класс приложения которая инициализирует окно
class App:
    def __init__(self):
        self.window = Window()
    # Pfgecr
    def run(self):
        self.window.launch()


if __name__ == '__main__':
    app = App()
    app.run()
