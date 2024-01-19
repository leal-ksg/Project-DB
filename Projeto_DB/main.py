from kivymd.tools.hotreload.app import MDApp
# from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.clock import mainthread
from kivy.metrics import dp

import threading
from time import sleep
import pyodbc

class Database():
    def __init__(self):
        connection_data = (
        "Driver={SQL Server};"
        "Server=MULCPDDT0515\SERVERPROJECTDB;"
        "Database=bancoprojeto;"
        )

        connection = pyodbc.connect(connection_data)

        self.cursor = connection.cursor()

    def select_data(self, query):
        result = self.cursor.execute(query).fetchall()
        self.cursor.commit()
        return result
    
    def insert_data(self, query):
        result = self.cursor.execute(query)
        self.cursor.commit()
        return result
    
class LoginScreen(Screen):

    def check_credentials(self):

        db = Database()
        query_result = db.select_data(f"select * from Users where name = '{self.ids.username.text}'")
        
        if query_result and query_result[0][9] == self.ids.password.text:
            return True
    
        return False

class SignUpScreen(Screen):

    dialog = None

    def on_pre_enter(self, *args):
        self.limpar_textfields()
        
    def limpar_textfields(self):
        for widget in self.walk():  # Percorre todos os widgets na tela
            if isinstance(widget, MDTextField):
                widget.text = ''

    def show_sign_up_alert(self, text):

        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ],
                radius=[20, 7, 20, 7] 
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.dialog = None
            
    def sign_up(self):

        db = Database()

        if (self.ids.name_sign_up.text and 
           self.ids.date_of_birth_sign_up.text and 
           self.ids.cpf_sign_up.text and 
           self.ids.rg_sign_up.text and 
           self.ids.office_sign_up.text and 
           self.ids.sex_sign_up.text and 
           self.ids.email_sign_up.text and 
           self.ids.phone_sign_up.text and
           self.ids.first_password_sign_up.text and
           self.ids.second_password_sign_up.text
           ):

            query_result = db.select_data(f"select * from Users where name = '{self.ids.name_sign_up.text}'")
            print(query_result)
            if not query_result:
                if self.ids.first_password_sign_up.text == self.ids.second_password_sign_up.text:
                    db.insert_data(f'''insert into Users(name, dob, cpf, rg, office, sex, email, phone, password) 
                                    values('{self.ids.name_sign_up.text}', 
                                   '{self.ids.date_of_birth_sign_up.text}',
                                   '{self.ids.cpf_sign_up.text}',
                                   '{self.ids.rg_sign_up.text}',
                                   '{self.ids.office_sign_up.text}',
                                   '{self.ids.sex_sign_up.text}',
                                   '{self.ids.email_sign_up.text}',
                                   '{self.ids.phone_sign_up.text}',
                                   '{self.ids.first_password_sign_up.text}')'''
                                )
                    print("Cadastro efetuado com sucesso.")
                    self.show_sign_up_alert(text="Cadastro efetuado com sucesso!")
                else:
                    print("A senhas não são iguais.")
                    self.show_sign_up_alert(text="A senhas não são iguais.")
            else:
                print("Esse cadastro já foi realizado previamente.")
                self.show_sign_up_alert(text="Esse cadastro já foi realizado previamente.")
        else:
            print("Todos os campos são obrigatórios.")
            self.show_sign_up_alert(text="Todos os campos são obrigatórios.")


class MenuScreen(Screen):
    pass

class UserManagementScreen(Screen):
    pass

class ReadUserScreen(Screen):
        def create_table(self):

            db = Database()
            data = db.select_data(query="select ID, name, dob, cpf, rg, office, sex, email, phone from Users")
            print(data)
            self.data_tables = MDDataTable(
                id="tabela",
                size_hint=(0.92, 0.8),
                pos_hint={"center_x":.5},
                pos=(self.x, 50),
                elevation=0,
                background_color=(0.51, 0.63, 0.48, 1),
                column_data=[
                    ("ID", dp(10)),
                    ("Nome", dp(55)),
                    ("Data Nasc", dp(30)),
                    ("CPF", dp(30)),
                    ("RG", dp(30)),
                    ("Cargo", dp(30)),
                    ("Sexo", dp(30)),
                    ("E-mail", dp(30)),
                    ("Telefone", dp(30)),
                ],
                row_data = [
                    tuple(str(value) if value is not None else '-' for value in row)
                    for row in data
                    ]
                )
            
            self.data_tables.bind(on_row_press=self.on_row_press)
            self.add_widget(self.data_tables)
        
        def on_row_press(self, *args):
            pass

        def on_enter(self, *args):
            self.create_table()

class DeleteUserScreen(Screen):

    def create_table_checkable(self):

        db = Database()
        data = db.select_data(query="select ID, name, dob, cpf, rg, office, sex, email, phone from Users")
        print(data)
        self.data_tables = MDDataTable(
            size_hint=(0.92, 0.8),
            pos_hint={"center_x":.5},
            pos=(self.x, 50),
            check=True,
            elevation=0,
            background_color=(0.51, 0.63, 0.48, 1),
            column_data=[
                ("ID", dp(30)),
                ("Nome", dp(60)),
                ("Data Nasc", dp(35)),
                ("CPF", dp(35)),
                ("RG", dp(35)),
                ("Cargo", dp(35)),
                ("Sexo", dp(35)),
                ("E-mail", dp(35)),
                ("Telefone", dp(35)),
            ],
            row_data = [
                tuple(str(value) if value is not None else '-' for value in row)
                for row in data
                ]
            )
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.add_widget(self.data_tables)
    
    def on_row_press(self, *args):
        pass
    
    def delete_rows_checked(self):

        checked = self.data_tables.get_row_checks()
        ids = []
        for data in checked:
            ids.append(data[0])
        
        print[ids]

    def on_enter(self, *args):
        self.create_table_checkable()

class App(MDApp):
    KV_FILES = ["app.kv"]
    DEBUG = True
    
    def build_app(self):

        self.theme_cls.material_style = "M3"

        Builder.load_file("app.kv")

        self.sm = ScreenManager()
        login_screen = LoginScreen(name="login")
        signup_screen = SignUpScreen(name="sign up")
        menu_screen = MenuScreen(name="menu")
        user_management_screen = UserManagementScreen(name="user_management")
        read_user_screen = ReadUserScreen(name="read_user")
        delete_user_screen = DeleteUserScreen(name="delete_user")

        self.sm.add_widget(login_screen)
        self.sm.add_widget(signup_screen)
        self.sm.add_widget(menu_screen)
        self.sm.add_widget(user_management_screen)
        self.sm.add_widget(read_user_screen)
        self.sm.add_widget(delete_user_screen)

        Window.size = (500, 500)
        Window.minimum_width = 500
        Window.minimum_height = 500
        Window.always_on_top = True

        login_screen.bind(on_pre_enter=self.set_window_size_login_screen)
        menu_screen.bind(on_pre_enter=self.set_window_size_menu_screen)
        signup_screen.bind(on_pre_enter=self.set_window_size_signup_screen)
        user_management_screen.bind(on_pre_enter=self.set_window_size_user_management_screen)
        read_user_screen.bind(on_pre_enter=self.set_window_size_read_user_screen)
        delete_user_screen.bind(on_pre_enter=self.set_window_size_delete_user_screen)

        self.login_screen = login_screen

        return self.sm
    
    def set_window_size_login_screen(self, *args):
        Window.size = (500, 500)  # Tamanho desejado para a tela de login
    
    def set_window_size_menu_screen(self, *args):
        Window.size = (500, 500)  # Tamanho desejado para a tela de menu
    
    def set_window_size_signup_screen(self, *args): 
        Window.size = (700, 500) # Tamanho desejado para a tela de cadastro de usuário
    
    def set_window_size_user_management_screen(self, *args): 
        Window.size = (500, 500) # Tamanho desejado para a tela de gestão de usuário

    def set_window_size_read_user_screen(self, *args): 
        Window.size = (1000, 700)
    
    def set_window_size_delete_user_screen(self, *args): 
        Window.size = (1000, 700)

    def login(self):
        if self.login_screen.check_credentials():
            self.go_to_menu_screen()    

    def go_to_menu_screen(self):
       self.sm.transition.direction = 'left'
       self.sm.current = 'menu'

    def go_to_sign_up_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'sign up'

    def go_to_login_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'login'

    def go_to_user_management_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'user_management'
    
    def go_to_read_user_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'read_user'
    
    def go_to_delete_user_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'delete_user'

    def return_to_menu_screen(self):
       self.sm.transition.direction = 'right'
       self.sm.current = 'menu'

    def return_to_sign_up_screen(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'sign up'

    def return_to_login_screen(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'login'

    def return_to_user_management_screen(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'user_management'
        

if __name__ == '__main__':
    App().run()