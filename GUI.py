import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from speech_translator import recognize_from_microphone

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Translation App")
        self.geometry("1000x250")

        # Configure Styles
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font=('Helvetica', 12))
        style.configure("TLabel", font=('Helvetica', 12))
        style.configure("TCombobox", padding=(10, 5), font=('Helvetica', 12))

        # Left Container for Microphone Input
        self.left_panel = tk.Frame(self, bg='#EFEFEF')
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.microphone_input_label = ttk.Label(self.left_panel, text="Microphone Input:", style="TLabel")
        self.microphone_input_label.pack(pady=(10, 5))

        self.microphone_input_textbox = tk.Text(self.left_panel, wrap=tk.WORD, height=10, width=40, font=('Helvetica', 12))
        self.microphone_input_textbox.pack(pady=(0, 10))

        # Right Container for Translation
        self.right_panel = tk.Frame(self, bg='#EFEFEF')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.translated_text_label = ttk.Label(self.right_panel, text="Translated Text:", style="TLabel")
        self.translated_text_label.pack(pady=(10, 5))

        self.translated_text_textbox = tk.Text(self.right_panel, wrap=tk.WORD, height=10, width=40, font=('Helvetica', 12))
        self.translated_text_textbox.pack(pady=(0, 10))

        # Language Selection Dropdowns
        self.source_languages = ["en-ES", "ro-RO", "es-ES", "no-NO", "hu-HU", "gd-GB", "fi-FI", "sv-SE", "ru-RU", "zh-CN", "ja-JP"]
        self.target_languages = ["it", "fr", "es", "ro", "en", "no", "hu", "gd", "fi", "sv", "ru", "zh", "ja"]

        self.selected_source_language = tk.StringVar()
        self.source_language_dropdown = ttk.Combobox(
            self, textvariable=self.selected_source_language, values=self.source_languages, style="TCombobox"
        )
        self.source_language_dropdown.set("Select Source Language")
        self.source_language_dropdown.pack(pady=10)

        self.selected_target_language = tk.StringVar()
        self.target_language_dropdown = ttk.Combobox(
            self, textvariable=self.selected_target_language, values=self.target_languages, style="TCombobox"
        )
        self.target_language_dropdown.set("Select Target Language")
        self.target_language_dropdown.pack(pady=10)

        # Start Button
        self.start_button = ttk.Button(self, text="Translate", command=self.translate_from_microphone, style="TButton")
        self.start_button.pack(pady=(10, 20))

    def translate_from_microphone(self):
        source_language = self.selected_source_language.get()
        target_language = self.selected_target_language.get()

        if not source_language or not target_language:
            messagebox.showwarning("Warning", "Please select both source and target languages.")
            return

        result_text, translated_text = recognize_from_microphone(source_language, target_language)

        print("RESULT:" + result_text, translated_text)
        # Update the text boxes
        self.microphone_input_textbox.delete(1.0, tk.END)
        self.microphone_input_textbox.insert(tk.END, str(result_text))

        self.translated_text_textbox.delete(1.0, tk.END)
        self.translated_text_textbox.insert(tk.END, str(translated_text))

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
