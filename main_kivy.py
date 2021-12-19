from kivy.app import App
from kivy.uix.label import Label


class PyTrivia(App):

    def build(self):
        root_widget = Label(
            text='Welcome To PyTrivia!',
            font_size=70
        )
        return root_widget


PyTrivia().run()