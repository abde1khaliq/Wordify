import tkinter as tk
from tkinter import filedialog, PhotoImage
from PIL import Image, ImageTk
import fitz
from docx import Document


class PdfConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("- Wordify ")
        self.root.geometry("500x500")
        self.root.configure(bg="#121212")

        image = Image.open("icons/wordify.png").resize((40, 40))
        self.logo_image = ImageTk.PhotoImage(image)

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

        logo_label = tk.Label(
            self.header, image=self.logo_image, bg=self.header_bg)
        logo_label.pack(side="left", padx=(10, 5), pady=10)

        nav_items = [
            ("Convert", self.show_home),
            ("About", self.show_about)
        ]

        for text, command in nav_items:
            btn = tk.Button(self.header, text=text, bg=self.button_bg, fg=self.text_color,
                            font=("Poppins", 11), relief="flat", bd=0, highlightthickness=0,
                            command=command)
            btn.pack(side="left", padx=10, pady=10, ipadx=10, ipady=4)
            self.add_button_hover_effect(btn)

    def create_content_area(self):
        self.content_area = tk.Frame(self.root, bg=self.bg_dark)
        self.content_area.pack(fill="both", expand=True)

    def create_home_page(self):
        self.home_page = tk.Frame(self.content_area, bg=self.bg_dark)

        tk.Label(self.home_page, text="Convert your PDF To Word format", bg=self.bg_dark,
                 fg=self.text_color, font=("Poppins", 20)).pack(pady=30)

        upload_btn = tk.Button(self.home_page, text="Select PDF File", bg=self.button_bg,
                               fg=self.text_color, font=("Poppins", 12), relief="flat",
                               command=self.upload_file, bd=0, highlightthickness=0)
        upload_btn.pack(pady=10, ipadx=10, ipady=6)
        self.add_button_hover_effect(upload_btn)

        self.file_path_label = tk.Label(self.home_page, textvariable=self.selected_file_path,
                                        bg=self.bg_dark, fg=self.accent_text, font=("Poppins", 10), wraplength=400)
        self.file_path_label.pack(pady=10)

        convert_btn = tk.Button(self.home_page, text="Start Conversion", bg=self.button_bg,
                                fg=self.text_color, font=("Poppins", 12), relief="flat",
                                command=self.start_conversion, bd=0, highlightthickness=0)
        convert_btn.pack(pady=30, ipadx=10, ipady=6)
        self.add_button_hover_effect(convert_btn)

        self.message_label = tk.Label(self.home_page, textvariable='',
                                 bg=self.bg_dark, fg=self.success, font=("Poppins", 10), wraplength=400)
        self.message_label.pack(pady=20)

    def create_about_page(self):
        self.about_page = tk.Frame(self.content_area, bg=self.bg_dark)

        tk.Label(self.about_page, text="About PDFER", bg=self.bg_dark,
                 fg=self.text_color, font=("Poppins", 18)).pack(pady=40)

        tk.Label(self.about_page, text="Version 1.0.0", bg=self.bg_dark,
                 fg=self.accent_text, font=("Poppins", 12)).pack(pady=10)

        updates_btn = tk.Button(self.about_page, text="Check for Updates", bg=self.button_bg,
                                fg=self.text_color, font=("Poppins", 11), relief="flat",
                                command=self.check_for_updates, bd=0, highlightthickness=0)
        updates_btn.pack(pady=20, ipadx=10, ipady=5)
        self.add_button_hover_effect(updates_btn)

    def show_home(self):
        self.about_page.pack_forget()
        self.home_page.pack(fill="both", expand=True)

    def show_about(self):
        self.home_page.pack_forget()
        self.about_page.pack(fill="both", expand=True)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.selected_file_path.set(file_path)

    def extract_text_from_pdf(self, pdf_path):
        pdf_file = fitz.open(pdf_path)
        full_text = ""
        for page in pdf_file:
            full_text += page.get_text() + '\n'
        pdf_file.close()
        return full_text

    def save_text_to_word_format(self, extracted_content, output_file):
        doc = Document()
        for line in extracted_content.splitlines():
            doc.add_paragraph(line)
        doc.save(output_file)

    def start_conversion(self):
        pdf_path = self.selected_file_path.get()
        if not pdf_path or pdf_path == "No file selected":
            self.selected_file_path.set("Select a PDF file to convert!")
            return
        extracted_text = self.extract_text_from_pdf(pdf_path)
        self.save_text_to_word_format(extracted_text, "converted.docx")
        self.message_label.config(text='Successfully Converted your PDF file.')

    def check_for_updates(self):
        # TODO: Add your update check logic here
        pass

    def add_button_hover_effect(self, button):
        button.bind("<Enter>", lambda e: button.configure(
            bg=self.button_hover))
        button.bind("<Leave>", lambda e: button.configure(bg=self.button_bg))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PdfConverterApp()
    app.run()
