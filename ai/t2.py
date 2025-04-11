from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import requests

class CodeGeneratorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.prompt_label = Label(text="Describe your task in English:")
        self.add_widget(self.prompt_label)

        self.prompt_input = TextInput(size_hint_y=None, height=100, multiline=True)
        self.add_widget(self.prompt_input)

        self.generate_button = Button(text="Generate Code", size_hint_y=None, height=50)
        self.generate_button.bind(on_press=self.generate_code)
        self.add_widget(self.generate_button)

        self.result_label = Label(text="Generated Code:")
        self.add_widget(self.result_label)

        self.result_output = TextInput(size_hint_y=None, height=400, readonly=True, multiline=True)
        self.add_widget(ScrollView(size_hint=(1, None), height=400, content=self.result_output))

        self.save_button = Button(text="Save Code", size_hint_y=None, height=50)
        self.save_button.bind(on_press=self.save_generated_code)
        self.add_widget(self.save_button)

    def generate_code(self, instance):
        prompt = self.prompt_input.text.strip()
        if not prompt:
            self.show_popup("Input Error", "Task description cannot be empty!")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/generate",
                json={"prompt": prompt, "max_length": 150, "temperature": 0.7}
            )
            response_data = response.json()
            if "error" in response_data:
                self.show_popup("Error", response_data["error"])
                return

            self.result_output.text = response_data.get("generated_code", "")
        except requests.exceptions.ConnectionError:
            self.show_popup("Connection Error", "Unable to connect to the backend server.")
        except Exception as e:
            self.show_popup("Error", str(e))

    def save_generated_code(self, instance):
        code = self.result_output.text.strip()
        if not code:
            self.show_popup("Save Error", "No code to save.")
            return

        try:
            with open("generated_code.py", "w") as file:
                file.write(code)
            self.show_popup("Success", "Code saved successfully!")
        except Exception as e:
            self.show_popup("Error", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class MyApp(App):
    def build(self):
        return CodeGeneratorApp()

if __name__ == "__main__":
    MyApp().run()
