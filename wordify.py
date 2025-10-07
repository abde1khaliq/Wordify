import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.logic import extract_text_from_pdf, save_text_to_word_format
from src.updater import check_for_updates as cfu
import json
import os
from src.path import resource_path

class PdfConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("- Wordify ")
        self.root.geometry("500x500")
        self.root.configure(bg="#121212")

        try:
            image_path = resource_path("src/assets/wordify.png")
            image = Image.open(image_path).resize((40, 40))
            self.logo_image = ImageTk.PhotoImage(image)
        except Exception as e:
            print("⚠️ Failed to load logo image:", e)
            self.logo_image = None

        try:
            config_path = resource_path("src/config/wordify.json")
            with open(config_path, "r") as file:
                version_data = json.load(file)
            self.version = version_data.get("version", "Unknown")
        except Exception as e:
            print("⚠️ Failed to load version config:", e)
            self.version = "Unknown"

        self.bg_dark = "#121212"
        self.header_bg = "#141414"
        self.button_bg = "#1f6eb8"
        self.button_hover = "#195e9e"
        self.text_color = "white"
        self.accent_text = "#94a3b8"
        self.error = 'red'
        self.success = 'green'

        self.selected_file_path = tk.StringVar(value="No file selected")

        self.create_header()
        self.create_content_area()
        self.create_home_page()
        self.create_about_page()

        self.show_home()

    def create_header(self):
        self.header = tk.Frame(self.root, bg=self.header_bg, height=60)
        self.header.pack(fill="x")

        if self.logo_image:
            logo_label = tk.Label(self.header, image=self.logo_image, bg=self.header_bg)
            logo_label.pack(side="left", padx=(10, 5), pady=10)

        nav_items = [("Convert", self.show_home), ("About", self.show_about)]

        for text, command in nav_items:
            try:
                btn = tk.Button(self.header, text=text, bg=self.button_bg, fg=self.text_color,
                                font=("Poppins", 11), relief="flat", bd=0, highlightthickness=0,
                                command=command)
                btn.pack(side="left", padx=10, pady=10, ipadx=10, ipady=4)
                self.add_button_hover_effect(btn)
            except Exception as e:
                print(f"⚠️ Failed to create nav button '{text}':", e)

    def create_content_area(self):
        try:
            self.content_area = tk.Frame(self.root, bg=self.bg_dark)
            self.content_area.pack(fill="both", expand=True)
        except Exception as e:
            print("⚠️ Failed to create content area:", e)

    def create_home_page(self):
        try:
            self.home_page = tk.Frame(self.content_area, bg=self.bg_dark)

            tk.Label(self.home_page, text="Convert your PDF To Word format", bg=self.bg_dark,
                     fg=self.text_color, font=("Poppins", 20)).pack(pady=30)

            upload_btn = tk.Button(self.home_page, text="Select PDF File", bg=self.button_bg,
                                   fg=self.text_color, font=("Poppins", 12), relief="flat",
                                   command=self.upload_file, bd=0, highlightthickness=0)
            upload_btn.pack(pady=10, ipadx=10, ipady=6)
            self.add_button_hover_effect(upload_btn)

            self.file_path_label = tk.Label(self.home_page, textvariable=self.selected_file_path,
                                            bg=self.bg_dark, fg=self.accent_text,
                                            font=("Poppins", 10), wraplength=400)
            self.file_path_label.pack(pady=10)

            convert_btn = tk.Button(self.home_page, text="Start Conversion", bg=self.button_bg,
                                    fg=self.text_color, font=("Poppins", 12), relief="flat",
                                    command=self.start_conversion, bd=0, highlightthickness=0)
            convert_btn.pack(pady=30, ipadx=10, ipady=6)
            self.add_button_hover_effect(convert_btn)

            self.message_label = tk.Label(self.home_page, text="", bg=self.bg_dark,
                                          fg=self.success, font=("Poppins", 10), wraplength=400)
            self.message_label.pack(pady=20)
        except Exception as e:
            print("⚠️ Failed to create home page:", e)

    def create_about_page(self):
        try:
            self.about_page = tk.Frame(self.content_area, bg=self.bg_dark)

            tk.Label(self.about_page, text="About Wordify", bg=self.bg_dark,
                     fg=self.text_color, font=("Poppins", 18)).pack(pady=40)

            tk.Label(self.about_page, text=f' Version {self.version}', bg=self.bg_dark,
                     fg=self.accent_text, font=("Poppins", 12)).pack(pady=10)

            updates_btn = tk.Button(self.about_page, text="Check for Updates", bg=self.button_bg,
                                    fg=self.text_color, font=("Poppins", 11), relief="flat",
                                    command=self.check_for_updates, bd=0, highlightthickness=0)
            updates_btn.pack(pady=20, ipadx=10, ipady=5)
            self.add_button_hover_effect(updates_btn)

            self.about_message_label = tk.Label(self.about_page, text="", bg=self.bg_dark,
                                                fg=self.accent_text, font=("Poppins", 10),
                                                wraplength=400)
            self.about_message_label.pack(pady=10)
        except Exception as e:
            print("⚠️ Failed to create about page:", e)

    def show_home(self):
        try:
            self.about_page.pack_forget()
            self.home_page.pack(fill="both", expand=True)
        except Exception as e:
            print("⚠️ Failed to show home page:", e)

    def show_about(self):
        try:
            self.home_page.pack_forget()
            self.about_page.pack(fill="both", expand=True)
        except Exception as e:
            print("⚠️ Failed to show about page:", e)

    def upload_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                self.selected_file_path.set(file_path)
        except Exception as e:
            print("⚠️ Failed to upload file:", e)
            self.selected_file_path.set("Error selecting file.")

    def start_conversion(self):
        try:
            pdf_path = self.selected_file_path.get()
            if not pdf_path or pdf_path == "No file selected":
                self.selected_file_path.set("Select a PDF file to convert!")
                return

            extracted_text = extract_text_from_pdf(pdf_path)
            save_text_to_word_format(extracted_text, "converted.docx")
            self.message_label.config(text='Successfully Converted your PDF file.', fg=self.success)
        except Exception as e:
            print("⚠️ Conversion failed:", e)
            self.message_label.config(text='Conversion failed. Please try again.', fg=self.error)

    def check_for_updates(self):
        try:
            update_status = cfu()
            if update_status is True:
                self.about_message_label.config(text="Wordify is up to date.", fg=self.success)
            elif update_status is False:
                self.about_message_label.config(
                    text="A new version of Wordify is available.\nDownload the latest release.",
                    fg=self.error
                )
            else:
                self.about_message_label.config(
                    text="Unable to check for updates. Please try again later.",
                    fg=self.error
                )
        except Exception as e:
            print("⚠️ Update check failed:", e)
            self.about_message_label.config(
                text="Error checking for updates.",
                fg=self.error
            )

    def add_button_hover_effect(self, button):
        try:
            button.bind("<Enter>", lambda e: button.configure(bg=self.button_hover))
            button.bind("<Leave>", lambda e: button.configure(bg=self.button_bg))
        except Exception as e:
            print("⚠️ Failed to add hover effect:", e)

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print("⚠️ Application crashed:", e)

if __name__ == "__main__":
    app = PdfConverterApp()
    app.run()
