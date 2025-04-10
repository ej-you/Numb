from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class MyApp(App):
    def build(self):
        self.label = Label(text="Привет, Android!")
        button = Button(text="Нажми меня")
        button.bind(on_press=self.update_label)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def update_label(self, instance):
        self.label.text = "Текст изменен!"


if __name__ == "__main__":
    MyApp().run()
