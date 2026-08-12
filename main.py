from kivy.app import App

from interface import TelaProdutos


class MeuApp(App):
    def build(self):
        return TelaProdutos()


if __name__ == "__main__":
    MeuApp().run()
