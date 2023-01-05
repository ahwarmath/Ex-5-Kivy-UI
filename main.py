import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.animation import Animation
s = Slider(orientation='horizontal')
from kivy.clock import Clock
from pidev.Joystick import Joystick
from datetime import datetime
import pygame

time = datetime



MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN_NAME = 'new'

joy = Joystick(0, True)


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

buttonstate = "On"
buttonstate2 = "Motor On"
joyposition = "0.0, 0.0"

class MainScreen(Screen):

    def __init__(self, **kwargs):
        Clock.schedule_interval(self.joy_update, .1)
        print("clock schedule created")
        super(MainScreen, self).__init__(**kwargs)

    buttonstate = ObjectProperty()
    buttonstate2 = ObjectProperty()
    joyposition = ObjectProperty()
    button_number = ObjectProperty()

    def admin_action(self):

        SCREEN_MANAGER.current = 'passCode'

    def counter_increment(self, val):
        return str(int(val)+1)


    def on_off(self, buttonstate):
        if buttonstate == "On":
            buttonstate = "Off"
        else:
            buttonstate = "On"
        return str(buttonstate)

    def motoron_off(self, buttonstate2):
        if buttonstate2 == "Motor On":
            buttonstate2 = "Motor Off"
        else:
            buttonstate2 = "Motor On"
        return str(buttonstate2)

    def imagebutton(self):
        SCREEN_MANAGER.current = NEW_SCREEN_NAME

    def animate_it(self, *args):
        animate = Animation(x=50) + Animation(size=(80,100), duration=3)
        animate.start(self)
        SCREEN_MANAGER.current = NEW_SCREEN_NAME

    def joystick_position(self, joyposition):
        joyposition = joy.get_axis('x'), joy.get_axis('y')
        return "Position: " + str(joyposition)

    def get_button(self, button_number):
        button_number = joy.get_button_state(1)
        if button_number == 1:
            return "She is Pressed"
        else:
            return "She is not Pressed"


    def get_button_combo(self, button_combo):
        button_combo = joy.button_combo_check(1, 2)
        if button_combo == 1:
            return "They are Pressed"
        else:
            return "They are not Pressed"

    def joy_update(self, dt=None):
        self.x_val, self.y_val = joy.get_both_axes()
        self.ids.x.text = "X: " + str(round(self.x_val, 2))
        self.ids.y.text = "Y: " + str(round(self.y_val, 2))


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()

class NewScreen(Screen):

    def imagebutton2(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def animate_it2(self, *args):
        animate = Animation(x=150) + Animation(y=100) + Animation(x=1200) + Animation(y=400) + Animation(size=(500,80), duration=1) + Animation(size=(500,400), duration=1)
        widget = self.ids.animate_image_button2
        animate.start(widget)
        #SCREEN_MANAGER.current = MAIN_SCREEN_NAME

"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
