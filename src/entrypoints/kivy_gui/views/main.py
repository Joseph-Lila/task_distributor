from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout


class DateField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:


class MyTextField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    icon = StringProperty()
    input_filter = ObjectProperty()
    disabled = BooleanProperty()
    # Here specify the required parameters for MDTextFieldRound:

