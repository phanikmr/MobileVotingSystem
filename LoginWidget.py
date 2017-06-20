from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
import time


class LoginWidget(GridLayout):
    def __init__(self, **kwargs):
        self.loginSuccess = False
        super(LoginWidget, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 3
        self.add_widget(Label(text="User Name"))
        self.username = TextInput(multiline=True)
        self.add_widget(self.username)
        self.add_widget(Label(text="Password"))
        self.password = TextInput(multiline=True, password=True)
        self.add_widget(self.password)
        self.login = Button(text="Login")
        self.add_widget(self.login)
        self.cancel = Button(text="Cancel")
        self.add_widget(self.cancel)
        self.login.bind(on_press=self.login_callback)
        self.cancel.bind(on_press=self.cancel_callback)
        self.btn = Button(text='Wrong UserName or Password')
        self.popup = Popup(title='Attention..!!!', content=self.btn, auto_dismiss=True)
        self.btn.background_color = [0, 0, 0, 0]
        self.btn.bind(on_release=self.popup.dismiss)
        Window.size = (300, 100)

    def login_callback(self, instance):
        f = open("data\username.txt", "r")
        username = f.read()
        f.close()
        f = open("data\password.txt", "r")
        password = f.read()
        f.close()
        if username == self.username.text and password == self.password.text:
            self.loginSuccess = True
            time.sleep(0.5)
            App.get_running_app().stop()
        else:
            self.popup.open()
            self.password.text = ""

    def cancel_callback(self, instance):
        self.loginSuccess = False
        time.sleep(0.5)
        App.get_running_app().stop()


class AdminLogin(App):
    def build(self):
        return LoginWidget()


if __name__ == "__main__":
    AdminLogin().run()
