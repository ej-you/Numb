# class DigitButton(Button):
#     hidden_value = ObjectProperty(None)  # Для хранения данных
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.background_normal = ""
#         self.background_color = [1, 1, 1, 1]
#
#
# # Создание кнопки
# btn = DigitButton(text=str(elem.get_value()))
# btn.hidden_value = elem.get_value()  # Сохраняем значение