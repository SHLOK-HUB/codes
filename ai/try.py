from dearpygui import *
# from dearpygui.core import *
# from dearpygui.simple import *
import requests

def generate_code(sender, data):
    prompt = get_value("Prompt Input").strip()
    if not prompt:
        show_item("Input Error Popup")
        return

    try:
        response = requests.post(
            "http://127.0.0.1:5000/generate",
            json={"prompt": prompt, "max_length": 150, "temperature": 0.7}
        )
        response_data = response.json()
        if "error" in response_data:
            set_value("Error Message", response_data["error"])
            show_item("Error Popup")
            return

        set_value("Generated Code", response_data.get("generated_code", ""))
    except requests.exceptions.ConnectionError:
        set_value("Error Message", "Unable to connect to the backend server.")
        show_item("Error Popup")
    except Exception as e:
        set_value("Error Message", str(e))
        show_item("Error Popup")

def save_code(sender, data):
    code = get_value("Generated Code").strip()
    if not code:
        show_item("Save Error Popup")
        return

    try:
        with open("generated_code.py", "w") as file:
            file.write(code)
        show_item("Success Popup")
    except Exception as e:
        set_value("Error Message", str(e))
        show_item("Error Popup")

with window("AI Code Generator", width=800, height=600):
    add_text("Describe your task in English:")
    add_input_text("Prompt Input", multiline=True, width=750, height=100)
    add_button("Generate Code", callback=generate_code)
    add_text("Generated Code:")
    add_input_text("Generated Code", multiline=True, readonly=True, width=750, height=400)
    add_button("Save Code", callback=save_code)

with popup("Generate Code", "Input Error Popup", modal=True):
    add_text("Task description cannot be empty!")

with popup("Generate Code", "Save Error Popup", modal=True):
    add_text("No code to save.")

with popup("Generate Code", "Success Popup", modal=True):
    add_text("Code saved successfully!")

with popup("Generate Code", "Error Popup", modal=True):
    add_text("An error occurred:")
    add_text("", source="Error Message")

start_dearpygui(primary_window="AI Code Generator")
