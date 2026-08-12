"""Componentes visuais do aplicativo."""

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from banco import buscar_produto, carregar_produtos, listar_sugestoes


AZUL = (0.06, 0.36, 0.70, 1)
AZUL_CLARO = (0.12, 0.55, 0.94, 1)
BRANCO = (1, 1, 1, 1)
PRETO = (0.03, 0.05, 0.10, 1)


class FundoGradiente(BoxLayout):
    """Layout com um fundo vertical em degradê azul-escuro/preto."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        textura = Texture.create(size=(1, 2), colorfmt="rgba")
        textura.blit_buffer(
            bytes((8, 18, 42, 255, 16, 94, 176, 255)), colorfmt="rgba", bufferfmt="ubyte"
        )
        textura.mag_filter = "linear"
        textura.min_filter = "linear"

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.fundo = Rectangle(texture=textura, pos=self.pos, size=self.size)

        self.bind(pos=self._atualizar_fundo, size=self._atualizar_fundo)

    def _atualizar_fundo(self, *_args):
        self.fundo.pos = self.pos
        self.fundo.size = self.size


class TelaProdutos(FundoGradiente):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(24), spacing=dp(12), **kwargs)
        Window.clearcolor = PRETO
        self.produtos = carregar_produtos()

        self.add_widget(
            Label(
                text="CONSULTA DE PRODUTOS",
                color=BRANCO,
                bold=True,
                font_size="24sp",
                size_hint_y=None,
                height=dp(38),
            )
        )
        self.add_widget(
            Label(
                text="Digite o nome para ver sugestões ou informe o CPD.",
                color=(0.78, 0.87, 1, 1),
                font_size="15sp",
                size_hint_y=None,
                height=dp(26),
            )
        )

        self.input_busca = TextInput(
            hint_text="Pesquisar produto ou CPD",
            multiline=False,
            size_hint_y=None,
            height=dp(52),
            font_size="18sp",
            padding=(dp(14), dp(14)),
            background_normal="",
            background_active="",
            background_color=BRANCO,
            foreground_color=PRETO,
            hint_text_color=(0.35, 0.40, 0.48, 1),
            cursor_color=AZUL,
        )
        self.input_busca.bind(text=self.atualizar_sugestoes, on_text_validate=self.buscar_por_enter)
        self.add_widget(self.input_busca)

        self.lista_sugestoes = GridLayout(cols=1, spacing=dp(4), size_hint_y=None)
        self.lista_sugestoes.bind(minimum_height=self.lista_sugestoes.setter("height"))

        self.area_sugestoes = ScrollView(size_hint_y=None, height=0, do_scroll_x=False)
        self.area_sugestoes.add_widget(self.lista_sugestoes)
        self.add_widget(self.area_sugestoes)

        self.resultado = Label(
            markup=True,
            text="[color=#BFD9FF]Selecione uma sugestão para consultar o produto.[/color]",
            font_size="20sp",
            color=BRANCO,
            halign="center",
            valign="middle",
        )
        self.resultado.bind(size=self.atualizar_texto)
        self.add_widget(self.resultado)

        botao_pesquisar = Button(
            text="PESQUISAR",
            size_hint_y=None,
            height=dp(48),
            bold=True,
            font_size="16sp",
            background_normal="",
            background_color=AZUL_CLARO,
            color=BRANCO,
        )
        botao_pesquisar.bind(on_release=self.buscar_por_enter)
        self.add_widget(botao_pesquisar)
        botao_sair = Button(
            text="SAIR",
            size_hint_y=None,
            height=dp(48),
            bold=True,
            font_size="16sp",
            background_normal="",
            background_color=AZUL,
            color=BRANCO,
        )
        botao_sair.bind(on_release=self.sair)
        self.add_widget(botao_sair)

    def atualizar_sugestoes(self, _campo, texto):
        sugestoes = listar_sugestoes(self.produtos, texto)
        self.lista_sugestoes.clear_widgets()

        if not sugestoes:
            self.area_sugestoes.height = 0
            return

        for produto in sugestoes:
            botao = Button(
                text=produto["nome"].upper(),
                size_hint_y=None,
                height=dp(44),
                halign="left",
                text_size=(None, None),
                padding=(dp(14), 0),
                background_normal="",
                background_color=(0.08, 0.18, 0.34, 1),
                color=BRANCO,
            )
            botao.bind(on_release=lambda _botao, item=produto: self.selecionar_produto(item))
            self.lista_sugestoes.add_widget(botao)

        self.area_sugestoes.height = min(dp(180), len(sugestoes) * dp(48))

    def selecionar_produto(self, produto):
        self.input_busca.text = produto["nome"]
        self.lista_sugestoes.clear_widgets()
        self.area_sugestoes.height = 0
        self.mostrar_produto(produto)

    def buscar_por_enter(self, *_args):
        produto = buscar_produto(self.produtos, self.input_busca.text)
        self.lista_sugestoes.clear_widgets()
        self.area_sugestoes.height = 0

        if produto is None:
            self.resultado.text = "[color=#FFB4B4]Produto não encontrado.[/color]"
            return

        self.mostrar_produto(produto)

    def mostrar_produto(self, produto):
        self.resultado.text = (
            f"[b]Produto:[/b] {produto['nome'].upper()}\n\n"
            f"[b]Classe:[/b]\n"
            f"[color=#63B3FF][size=30]{produto['classe']}[/size][/color]"
        )

    @staticmethod
    def atualizar_texto(instance, _valor):
        instance.text_size = instance.size

    @staticmethod
    def sair(*_args):
        App.get_running_app().stop()
