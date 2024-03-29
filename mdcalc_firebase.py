import io
import os
import threading

import firebase_admin
import numpy as np
import requests
from kivy.utils import platform
from firebase_admin import credentials, auth
from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCardSwipeLayerBox, MDCardSwipeFrontBox, MDCardSwipe
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogButtonContainer
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.icon_definitions import md_icons
from kivymd.uix.divider import MDDivider
from matplotlib import pyplot as plt
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from PIL import Image as PILImage
from pyrebase import pyrebase

from common_app import CommonApp
from emailverify import EmailListVerifyOne

from ConverterPackage import bucklc, boostlc, bckbstlc

from tf_response import buck_response, buckboost_response, boost_response

# Window.size = (dp(400), dp(700))
Config.set('graphics', 'width', dp(400))
Config.set('graphics', 'height', dp(700))
Config.set('graphics', 'dpi', 300)
Config.set('graphics', 'resizable', '1')

if not os.path.exists('converter_hist.npy'):
    hist = np.array([])
    np.save('converter_hist.npy', hist)

if not os.path.exists('user_record.npy'):
    user = np.array([{'user': None, 'email': None}])
    np.save('user_record.npy', user)


class MainScreen(MDScreen):
    name = StringProperty()


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen1(MDScreen):
    name = StringProperty()
    spinner_id = ObjectProperty()
    ip_vtg = ObjectProperty()
    op_vtg = ObjectProperty()
    op_resistance = ObjectProperty()
    freq = ObjectProperty()
    ip_rip_i = ObjectProperty()
    op_rip_v = ObjectProperty()
    label = ObjectProperty()


class BaseScreen2(MDScreen):
    name = StringProperty()
    card_list = ObjectProperty()


class LoginScreen(MDScreen):
    name = StringProperty()
    login_email = ObjectProperty()
    login_password = ObjectProperty()


class PasswordResetScreen(MDScreen):
    name = StringProperty()


class SwipeLayerBox(MDCardSwipeLayerBox):
    pass


class SwipeFrontBox(MDCardSwipeFrontBox):
    pass


class MyCardSwipe(MDCardSwipe):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        swipe_layer = SwipeLayerBox(radius=[20, 20, 20, 20])
        swipe_layer.add_widget(MDIcon(icon='delete', pos_hint={'center_y': .5}))
        self.add_widget(swipe_layer)

        swipe_front = SwipeFrontBox()
        swipe_front.add_widget(MDLabel(text=text,
                                       theme_text_color="Primary",
                                       halign="center"))
        self.add_widget(swipe_front)

    # Override the on_touch_down method to check if the touch is within the card
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        return False

    # Override the on_touch_move method to check if the touch is within the card
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_move(touch)
        return False


def label_text(param: object):
    duty_, output_current, ind_current, input_current, power_in, power_out, ind_cr, ind_, i_ripple, ind_cr_ripple, max_indcrnt, min_indcrnt, capacitor, esr = param

    text = f"Converter Parameters:\n  Duty Cycle = {duty_}\n" \
           f"  Power Input = {power_in}W\n  Power Output = {power_out}W\n" \
           f"  Output Current = {output_current}Amp\n  Inductor Current = {ind_current}Amp\n" \
           f"  Input Current = {input_current}Amp\n  Ripple Current = {i_ripple}Amp\n" \
           f"  Critical Inductance(Lcr) = {ind_cr}H\n  Inductance(L) as per calculated ripple current = {ind_}H\n" \
           f"  Ripple Current due to Lcr = {ind_cr_ripple}Amp\n  Maximum inductor ripple current = {max_indcrnt}Amp\n" \
           f"  Minimum inductor ripple current = {min_indcrnt}Amp\n  Output Capacitor = {capacitor}F\n" \
           f"  Capacitor ESR = {esr}Ohms"
    return text


def msg_dialog(icon: str, text_headline: str, text_main: str):
    MDDialog(
        MDDialogIcon(icon=icon),
        MDDialogHeadlineText(text=text_headline),
        MDDialogSupportingText(text=text_main)
    ).open()


def history(inputs: list, output: str):
    mode, vin, vo, ro, fsw, ip_ir, op_vr, ind_, capacitor, duty = inputs
    ip_str = f"Converter Mode = {mode}\n  Vin = {vin}V\n  Vo = {vo}V\n  Ro = {ro}Omh\n  Freq = {fsw}Hz\n  Irp = {ip_ir}A\n  Vrp = {op_vr}V\n\n"
    hist_text = ip_str + output
    # with open('converter_hist.npy', 'ab') as f:
    hist_ = np.load('converter_hist.npy', allow_pickle=True)
    sr_no = len(hist_) + 1
    hist_dict = {'no': sr_no, 'mode': mode, 'vin': vin, 'vo': vo, 'fsw': fsw, 'hist': hist_text, 'duty': duty,
                 'resistor': ro, 'inductor': ind_, 'capacitor': capacitor}
    hist_ = np.append(hist_, np.array(hist_dict))
    np.save('converter_hist.npy', hist_)


def is_connected():
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False


class MDCalc(MDApp, CommonApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_ = None
        self.image_widget = object
        self.sr_no = float
        self.dialog = None
        self.mode = str
        self.cap = float
        self.ind = float
        self.ro = float
        self.duty = float
        self.vin = str
        self.account_drop = None
        # self.login = None
        self.user = object
        self.screen_manager = MDScreenManager()
        self.label = str
        self.drop = None
        firebase_config = {
            'apiKey': "AIzaSyACRwxjYJzbNez8CN6zLMlGSdtK34YvStc",
            'authDomain': "convertercalc-be69f.firebaseapp.com",
            'databaseURL': 'https://convertercalc-be69f-default-rtdb.firebaseio.com/',
            'projectId': "convertercalc-be69f",
            'storageBucket': "convertercalc-be69f.appspot.com",
            'messagingSenderId': "414380692572",
            'appId': "1:414380692572:web:67ed4c7ffc2a162cdc0299",
            'measurementId': "G-YCJ75W4RDZ"
        }

        cred = credentials.Certificate('firebase_key.json')
        firebase_admin.initialize_app(cred, firebase_config)
        self.auth = auth
        firebase = pyrebase.initialize_app(firebase_config)
        self.pyrebase_auth = firebase.auth()

    def build(self):
        self.icon = 'assets/calc_logo1.png'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Skyblue'
        user_ = np.load('user_record.npy', allow_pickle=True)
        if user_[0]['user'] is None:
            self.screen_manager.add_widget(Builder.load_file('mdcalc_welcome.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_signup.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_login.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_main.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_plot.kv'))
        else:
            self.screen_manager.add_widget(Builder.load_file('mdcalc_main.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_plot.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_login.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_signup.kv'))
            self.screen_manager.add_widget(Builder.load_file('mdcalc_welcome.kv'))
        return self.screen_manager

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        if item_text == 'History':
            hist0 = np.load('converter_hist.npy', allow_pickle=True)
            if len(hist0) != 0:
                self.hist_layout(history_array=hist0)
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.current = item_text

    def create_account(self, username, email, password):
        try:
            if not is_connected():
                raise Exception("No internet connection")

            status = EmailListVerifyOne('nkxtjHv9DOCM4UfEaY1Wp', email)
            result = status.control()
            if result == 'ok':
                self.auth.create_user(uid=username, email=email, password=password)
                self.screen_manager.current = 'Login'
            else:
                msg_dialog(icon='alert', text_headline='INVALID EMAIL!',
                           text_main=f"Invalid email address. Please try again.\nError: {result}")
        except ValueError as e:
            print(e)
            msg_dialog(icon='alert', text_headline='VALUE ERROR!',
                       text_main=f"{e}")
        except auth.UidAlreadyExistsError as e:
            print(e)
            msg_dialog(icon='alert', text_headline='Username Already Exists!',
                       text_main=f"{e}\nUse another username.")
        except auth.EmailAlreadyExistsError as e:
            print(e)
            msg_dialog(icon='alert', text_headline='Email Already Exists!',
                       text_main=f"{e}\nUse another email.")
        except Exception:
            msg_dialog(icon='alert', text_headline='Connection Error!', text_main='No internet connection.')

    def login_user(self, email, password):
        user_ = np.load('user_record.npy', allow_pickle=True)
        try:
            if not is_connected():
                raise Exception("No internet connection")

            _user = self.auth.get_user_by_email(email)
            # print(self.user_.photo_url)
            response = requests.post(
                "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyACRwxjYJzbNez8CN6zLMlGSdtK34YvStc",
                data={
                    "email": email,
                    "password": password,
                    "returnSecureToken": True,
                },
            )
            response.raise_for_status()
            self.user = self.pyrebase_auth.sign_in_with_email_and_password(email, password)
            # print(self.user)
            self.screen_manager.current = "Main"
            self.screen_manager.get_screen('Login').login_screen_manager.get_screen('login').login_email.text = ''
            self.screen_manager.get_screen('Login').login_screen_manager.get_screen('login').login_password.text = ''
            user_[0]['user'] = _user
            user_[0]['email'] = email
            np.save('user_record.npy', user_)
        except ValueError as err:
            msg_dialog(icon='alert', text_headline='VALUE ERROR!',
                       text_main=f'{err}')
        except auth.UserNotFoundError as err:
            msg_dialog(icon='alert', text_headline='USER NOT FOUND!',
                       text_main=f'{err}')
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            error_data = http_err.response.json()
            error_message = error_data["error"]["message"]
            print(error_data)
            if error_message == "INVALID_LOGIN_CREDENTIALS":
                # Show an error dialog for invalid login credentials
                msg_dialog(icon='alert', text_headline='INVALID CREDENTIALS!',
                           text_main=f'Invalid login credentials. Please try again.\nError: {error_message}')
            elif error_message == "INVALID_EMAIL":
                # Show an error dialog for invalid login credentials
                msg_dialog(icon='alert', text_headline='INVALID EMAIL!',
                           text_main=f'Invalid email address. Please try again.\nError: {error_message}')
            elif error_message == "MISSING_PASSWORD":
                # Show an error dialog for invalid login credentials
                msg_dialog(icon='alert', text_headline='PASSWORD MISSING!',
                           text_main=f'Password field left empty. Please try again.\nError: {error_message}')
        except requests.exceptions.RequestException as err:
            # Handle other requests exceptions
            print(f"Error: {err}")
        except Exception:
            msg_dialog(icon='alert', text_headline='Connection Error!', text_main='No internet connection.')

    def drop_menu(self):
        mode_button = self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen('Calculator').spinner_id
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in ['Boost', 'Buck', 'BuckBoost']
        ]
        self.drop = MDDropdownMenu(caller=mode_button, items=menu_items)
        self.drop.open()

    def menu_callback(self, text_item):
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen(
            'Calculator').spinner_id.text.text = text_item
        self.drop.dismiss()

    # def appbar_drop(self):
    #     menu_btn = self.screen_manager.get_screen('Main').menu_btn
    #     menu = [{'text': 'Exit', 'on_release': self.app_exit}]
    #     menu_drop = MDDropdownMenu(caller=menu_btn, items=menu)
    #     menu_drop.open()
    #
    def app_exit(self):
        # os._exit(0)
        self.stop()

    # def topbar_dropdown(self):
    #     account_btn = self.screen_manager.get_screen('Main').account_btn
    #     menu = [{'text': 'Sign Out', 'on_release': self.account_signout},
    #             {'text': 'Delete Account', 'on_release': self.account_del}]
    #     self.account_drop = MDDropdownMenu(caller=account_btn, items=menu)
    #     self.account_drop.open()

    def nav_drawer(self):
        # _user = self.auth.get_user_by_email(self.email)
        user_ = np.load('user_record.npy', allow_pickle=True)
        if user_[0]['user'].photo_url is not None:
        #     self.screen_manager.get_screen('Main').nav_drawer.profile_img.source = 'https://picsum.photos/id/82/200/300/'
        # else:
            self.screen_manager.get_screen('Main').nav_drawer.profile_img.source = user_[0]['user'].photo_url
        self.screen_manager.get_screen('Main').nav_drawer.profile_uid.text = user_[0]['user'].uid

    def account_logout(self):
        user_ = np.load('user_record.npy', allow_pickle=True)
        hist_ = np.load('converter_hist.npy', allow_pickle=True)
        # print(self.user)
        self.user = None
        user_[0]['user'] = None
        hist_ = np.delete(hist_, slice(None))
        # self.account_drop.dismiss()
        np.save('converter_hist.npy', hist_)
        np.save('user_record.npy', user_)
        self.screen_manager.current = "Login"

    def account_del(self):
        user_ = np.load('user_record.npy', allow_pickle=True)
        self.auth.delete_user(uid=user_[0]['user'].uid)
        self.account_logout()
        self.screen_manager.current = "Welcome"

    def reset_password(self, email):
        try:
            if not is_connected():
                raise Exception("No internet connection")

            status = EmailListVerifyOne('nkxtjHv9DOCM4UfEaY1Wp', email)
            result = status.control()
            if result == 'ok':  # Check if the email is valid
                try:
                    self.auth.get_user_by_email(email)
                    self.pyrebase_auth.send_password_reset_email(email)  # Send a password reset email
                    msg_dialog(icon='check-decagram', text_headline='SUCCESS!',
                               text_main='A password reset email has been sent to your email address.')
                except requests.exceptions.HTTPError as http_err:
                    error_data = http_err.response.json()
                    error_message = error_data["error"]["message"]
                    if error_message == "USER_NOT_FOUND":
                        msg_dialog(icon='alert', text_headline='ERROR!', text_main='User not found. Please try again.')
                except auth.UserNotFoundError:
                    msg_dialog(icon='alert', text_headline='ALERT!',
                               text_main='User not found. Please try again.')
                except requests.exceptions.RequestException as err:
                    print(f"Error: {err}")
            else:
                msg_dialog(icon='alert', text_headline='ERROR!',
                           text_main=f'Invalid email address. Please try again.\nError: {result}')
        except Exception:
            msg_dialog(icon='alert', text_headline='Connection Error!', text_main='No internet connection.')

    def hist_layout(self, history_array: np.ndarray):
        card_list = self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen(
            'History').card_list
        card_list.clear_widgets()
        for t in history_array:
            card = MyCardSwipe(
                text=f"{t['no']}.  Mode:{t['mode']}  Vin:{t['vin']}V  Vo:{t['vo']}V  Ro:{t['resistor']}Ohms  Freq:{t['fsw']}Hertz",
                height=100,
                size_hint_y=None,
                on_swipe_complete=lambda instance,
                                         text=f"{t['no']}.  Mode:{t['mode']}  Vin:{t['vin']}V  Vo:{t['vo']}V  Ro:{t['resistor']}Ohms  Freq:{t['fsw']}Hertz": self.delete_card(
                    instance, text),
                type_swipe='auto',
                on_touch_up=lambda instance, touch,
                                   text=f"{t['no']}.  Mode:{t['mode']}  Vin:{t['vin']}V  Vo:{t['vo']}V  Ro:{t['resistor']}Ohms  Freq:{t['fsw']}Hertz": self.pop(
                    instance, touch, text) if instance.collide_point(*touch.pos) else None)
            card_list.add_widget(card)

    def delete_card(self, instance, text):
        hist_ = np.load('converter_hist.npy', allow_pickle=True)
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen(
            'History').card_list.remove_widget(instance)
        # Find the index where 'name' is 'text'
        index_to_delete = [i for i, entry in enumerate(hist_) if
                           f"{entry['no']}.  Mode:{entry['mode']}  Vin:{entry['vin']}V  Vo:{entry['vo']}V  Ro:{entry['resistor']}Ohms  Freq:{entry['fsw']}Hertz" == text]
        if index_to_delete:
            hist_ = np.delete(hist_, index_to_delete)
            for i in hist_[index_to_delete[0]:]:
                i['no'] -= 1
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen(
            'History').card_list.clear_widgets()
        self.hist_layout(history_array=hist_)
        np.save('converter_hist.npy', hist_)

    def pop(self, instance, touch, text):
        hist_ = np.load('converter_hist.npy', allow_pickle=True)
        for i in hist_:
            if text == f"{i['no']}.  Mode:{i['mode']}  Vin:{i['vin']}V  Vo:{i['vo']}V  Ro:{i['resistor']}Ohms  Freq:{i['fsw']}Hertz":
                self.sr_no = i['no']
                self.mode = i['mode']
                self.label = i['hist']
                self.vin = i['vin']
                self.duty = i['duty']
                self.ro = i['resistor']
                self.ind = i['inductor']
                self.cap = i['capacitor']
                break
        if self.mode == 'Boost':
            t, y, sys = boost_response(d=float(self.duty), vin=float(self.vin), resistor=float(self.ro),
                                       inductor=float(self.ind),
                                       capacitor=float(self.cap))
            y_ss = y[-1]
        elif self.mode == 'Buck':
            t, y, sys = buck_response(d=float(self.duty), vin=float(self.vin), resistor=float(self.ro),
                                      inductor=float(self.ind),
                                      capacitor=float(self.cap))
            y_ss = y[-1]
        else:
            t, y, sys = buckboost_response(d=float(self.duty), vin=float(self.vin), resistor=float(self.ro),
                                           inductor=float(self.ind), capacitor=float(self.cap))
            y_ss = y[-1]

        fig, ax = plt.subplots(dpi=300)
        ax.plot(t, y, label='Response')  # Plot steady-state response
        ax.plot(t, [y_ss] * len(t), label='Steady State Value')
        ax.set_xlabel('Time(sec)')
        ax.set_ylabel('Response')
        ax.set_title(f'Transient Response: Mode-{self.mode}, Vin-{self.vin}, D-{self.duty}')
        ax.text(t[-1], y_ss, f'Steady State Value: {y_ss:.2f}', ha='right', va='bottom')
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.grid()
        ax.legend()

        buf = io.BytesIO()

        fig.savefig(buf, format='png', dpi=300)

        buf.seek(0)

        # Convert the BytesIO object into a Kivy image
        image = CoreImage(buf, ext='png')

        # Create an Image widget to display the image
        self.image_widget = Image(texture=image.texture)

        self.dialog = MDDialog(MDDialogIcon(icon='history'), MDDialogSupportingText(text=self.label, halign='left'),
                               MDDialogButtonContainer(Widget(), MDButton(MDButtonText(text='Close', font_style='Body', role='small'), style='text',
                                                                          on_press=lambda x: self.dialog.dismiss()),
                                                       MDButton(MDButtonText(text='Plot', font_style='Body', role='small'), style='elevated',
                                                                on_press=lambda x: self.plot_response(
                                                                    image_widget=self.image_widget)),
                                                       MDButton(MDButtonText(text='Show TF', font_style='Body', role='small'),
                                                                style='elevated',
                                                                on_press=lambda x: msg_dialog(
                                                                    icon='information-variant-circle',
                                                                    text_headline='Transfer Function',
                                                                    text_main=f'H(s) = {sys}'))))
        self.dialog.open()

    def plot_response(self, image_widget: object):
        self.screen_manager.get_screen('Plot').add_widget(image_widget)
        self.dialog.dismiss()
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'Plot'

    def save_image(self):
        # Convert Kivy Image to PIL Image
        pil_image = PILImage.frombytes(mode="RGBA", size=self.image_widget.texture.size,
                                       data=self.image_widget.texture.pixels)

        if platform == 'android':
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            dir_ = primary_external_storage_path()
            download_folder = os.path.join(dir_, 'Download')
            file_path = os.path.join(download_folder, f"{self.sr_no}{self.mode}ResponseVin{self.vin}D{self.duty}.png")
        else:
            # Get the system's download folder path
            download_folder = os.path.expanduser("~") + "/Downloads/"
            # Define the file path
            file_path = os.path.join(download_folder, f"{self.sr_no}{self.mode}ResponseVin{self.vin}D{self.duty}.png")

        # Save the image
        pil_image.save(file_path)

        msg_dialog(icon='check-decagram', text_headline='Image Saved!',
                   text_main=f'Image saved successfully at {file_path}.')

    def delete_all(self):
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen('History').card_list.clear_widgets()
        hist_ = np.load('converter_hist.npy', allow_pickle=True)
        hist_ = np.delete(hist_, slice(None))
        np.save('converter_hist.npy', hist_)

    def calculate_process(self):
        main_widget = self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen('Calculator')

        mode = main_widget.spinner_id.text
        vin = main_widget.ip_vtg
        vo = main_widget.op_vtg
        ro = main_widget.op_resistance
        fsw = main_widget.freq
        ip_ir = main_widget.ip_rip_i
        op_vr = main_widget.op_rip_v
        op_label = main_widget.label

        try:
            if mode.text == "Boost":
                duty_ = boostlc.bst_duty_cycle(float(vo.text), float(vin.text))
                output_current = np.round(
                    np.divide(float(vo.text), float(ro.text)), decimals=2)
                ind_current = boostlc.bst_ind_current(duty_, output_current)
                input_current = ind_current
                power_in = f"{np.multiply(float(vin.text), input_current):.4f}"
                power_out = f"{np.multiply(float(vo.text), output_current):.4f}"
                ind_cr = boostlc.bst_cr_ind(duty_, float(ro.text), float(fsw.text))
                if ip_ir.text == '':
                    ind_ = np.format_float_scientific(
                        np.multiply(float(ind_cr), 1.25),
                        unique=False,
                        precision=4,
                        trim="-",
                        exp_digits=1, )
                    i_ripple = boostlc.bst_Irp(
                        float(vin.text), duty_, float(fsw.text), float(ind_))
                else:
                    i_ripple = boostlc.bst_ripl_current(
                        ind_current, float(ip_ir.text))
                    ind_ = boostlc.bst_cont_ind(
                        float(vin.text), duty_, float(fsw.text), i_ripple)
                ind_cr_ripple = boostlc.bst_ind_ripl_(
                    float(vin.text), duty_, float(fsw.text), ind_cr)
                max_indcrnt = np.round(
                    np.add(float(ind_current), float(i_ripple) / 2), decimals=2)
                min_indcrnt = np.round(
                    np.subtract(float(ind_current), float(i_ripple) / 2), decimals=2)
                capacitor = boostlc.bst_cap_val(duty_, float(
                    ro.text), float(op_vr.text), float(fsw.text))
                esr = boostlc.Esr(float(op_vr.text), float(vo.text), i_ripple)
                param = [duty_, output_current, ind_current, input_current, power_in, power_out,
                         ind_cr, ind_, i_ripple, ind_cr_ripple, max_indcrnt, min_indcrnt, capacitor, esr]
                ip = [mode.text, vin.text, vo.text, ro.text, fsw.text, ip_ir.text, op_vr.text, ind_, capacitor, duty_]
                op_label.text = label_text(param=param)
                history(inputs=ip, output=label_text(param=param))

            elif mode.text == "Buck":
                duty_ = bucklc.bck_duty_cycle(float(vo.text), float(vin.text))
                output_current = np.round(
                    np.divide(float(vo.text), float(ro.text)), decimals=2)
                ind_current = output_current
                input_current = bucklc.bck_ip_current(duty_, output_current)
                power_in = f"{np.multiply(float(vin.text), input_current):.4f}"
                power_out = f"{np.multiply(float(vo.text), output_current):.4f}"
                ind_cr = bucklc.bck_cr_ind(duty_, float(ro.text), float(fsw.text))
                if ip_ir.text == '':
                    ind_ = np.format_float_scientific(
                        np.multiply(float(ind_cr), 1.25),
                        unique=False,
                        precision=4,
                        trim="-",
                        exp_digits=1, )
                    i_ripple = bucklc.bck_Irp(
                        float(vo.text), duty_, float(fsw.text), float(ind_))
                else:
                    i_ripple = bucklc.bck_ripl_current(
                        ind_current, float(ip_ir.text))
                    ind_ = bucklc.bck_cont_ind(
                        float(vo.text), duty_, float(fsw.text), i_ripple)
                ind_cr_ripple = bucklc.bck_ind_ripl_(
                    float(vo.text), duty_, float(fsw.text), ind_cr)
                max_indcrnt = np.round(
                    np.add(float(ind_current), float(i_ripple) / 2), decimals=2)
                min_indcrnt = np.round(
                    np.subtract(float(ind_current), float(i_ripple) / 2), decimals=2)
                capacitor = bucklc.bck_cap_val(
                    duty_, ind_, float(op_vr.text), float(fsw.text))
                esr = bucklc.Esr(float(op_vr.text), float(vo.text), i_ripple)
                param = [duty_, output_current, ind_current, input_current, power_in, power_out,
                         ind_cr, ind_, i_ripple, ind_cr_ripple, max_indcrnt, min_indcrnt, capacitor, esr]
                ip = [mode.text, vin.text, vo.text, ro.text, fsw.text, ip_ir.text, op_vr.text, ind_, capacitor, duty_]
                op_label.text = label_text(param=param)
                history(inputs=ip, output=label_text(param=param))

            elif mode.text == "BuckBoost":
                duty_ = bckbstlc.bckbst_duty_cycle(float(vo.text), float(vin.text))
                output_current = np.round(
                    np.divide(float(vo.text), float(ro.text)), decimals=2)
                ind_current = bckbstlc.bckbst_ind_current(duty_, output_current)
                input_current = np.round(np.multiply(
                    ind_current, duty_), decimals=3)
                power_in = f"{np.multiply(float(vin.text), input_current):.4f}"
                power_out = f"{np.multiply(float(vo.text), output_current):.4f}"
                ind_cr = bckbstlc.bckbst_cr_ind(
                    duty_, float(ro.text), float(fsw.text))
                if ip_ir.text == '':
                    ind_ = np.format_float_scientific(
                        np.multiply(float(ind_cr), 1.25),
                        unique=False,
                        precision=4,
                        trim="-",
                        exp_digits=1, )
                    i_ripple = bckbstlc.bckbst_Irp(
                        float(vin.text), duty_, float(fsw.text), float(ind_))
                else:
                    i_ripple = bckbstlc.bckbst_ripl_current(
                        input_current, float(ip_ir.text))
                    ind_ = bckbstlc.bckbst_cont_ind(
                        float(vin.text), duty_, float(fsw.text), i_ripple)
                ind_cr_ripple = bckbstlc.bckbst_ind_ripl_(
                    float(vin.text), duty_, float(fsw.text), ind_cr)
                max_indcrnt = np.round(
                    np.add(float(ind_current), float(i_ripple) / 2), decimals=2)
                min_indcrnt = np.round(
                    np.subtract(float(ind_current), float(i_ripple) / 2), decimals=2)
                capacitor = bckbstlc.bckbst_cap_val(duty_, float(
                    ro.text), float(op_vr.text), float(fsw.text))
                esr = bckbstlc.Esr(float(op_vr.text), float(vo.text), i_ripple)
                param = [duty_, output_current, ind_current, input_current, power_in, power_out,
                         ind_cr, ind_, i_ripple, ind_cr_ripple, max_indcrnt, min_indcrnt, capacitor, esr]
                ip = [mode.text, vin.text, vo.text, ro.text, fsw.text, ip_ir.text, op_vr.text, ind_, capacitor, duty_]
                op_label.text = label_text(param=param)
                history(inputs=ip, output=label_text(param=param))

            elif mode.text == "Select Converter Type":
                msg_dialog(icon='alert', text_headline="Empty Text Field!", text_main='Converter type not selected!')

        except ValueError:
            if vin.text == '':
                msg_dialog(icon='alert', text_headline="Empty Text Field!",
                           text_main='Input Voltage field is  empty!')
            if vo.text == '':
                msg_dialog(icon='alert', text_headline="Empty Text Field!",
                           text_main='Output Voltage field is empty!')
            if ro.text == '':
                msg_dialog(icon='alert', text_headline="Empty Text Field!",
                           text_main='Output Resistance field is empty!')
            if fsw.text == '':
                msg_dialog(icon='alert', text_headline="Empty Text Field!", text_main='Frequency field is empty!')
            if op_vr.text == '':
                msg_dialog(icon='alert', text_headline="Empty Text Field!",
                           text_main='Output Voltage Ripple field is empty!')

        finally:
            mode.text = "Select Converter Type"
            vin.text = ""
            vo.text = ""
            ro.text = ""
            fsw.text = ""
            ip_ir.text = ""
            op_vr.text = ""

    def calculate(self):
        calc_proces = threading.Thread(target=self.calculate_process(), args=())
        calc_proces.start()

    def clear_process(self):
        self.screen_manager.get_screen('Main').kv_screen_manager.get_screen('main').main_manager.get_screen(
            'Calculator').label.text = "Converter Parameters:\n  Duty Cycle = 0.0\n" \
                                       "  Power Input = 0.0W\n  Power Output = 0.0W\n" \
                                       "  Output Current = 0.0Amp\n  Inductor Current = 0.0Amp\n" \
                                       "  Input Current = 0.0Amp\n  Ripple Current = 0.0Amp\n" \
                                       "  Critical Inductance(Lcr) = 0.0H\n  Inductance(L) as per calculated ripple current = 0.0H\n" \
                                       "  Ripple Current due to Lcr = 0.0Amp\n  Maximum inductor ripple current = 0.0Amp\n" \
                                       "  Minimum inductor ripple current = 0.0Amp\n  Output Capacitor = 0.0F\n" \
                                       "  Capacitor ESR = 0.0Ohms"

    def clear(self):
        clear_process = threading.Thread(target=self.clear_process, args=())
        clear_process.start()


if __name__ == "__main__":
    MDCalc().run()
