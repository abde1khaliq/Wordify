import customtkinter as ctk
from tkinter import filedialog
from logic import extract_text_from_pdf, save_text_to_word_format
from updater_file import check_for_updates as cfu
import json
import os

class Wordify:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title('Wordify')
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Color scheme
        self.bg_color = "#121212"
        self.header_bg = "#171717"
        self.card_bg = "#171717"
        self.secondary_card_bg = "#1a1a1a"
        self.btn_orange = "#f59e0b"
        self.btn_hover = "#f2a118"
        self.text_color = "white"
        self.accent_text = "#94a3b8"
        self.success = "#10b981"
        self.error = "#ef4444"

        # Fonts
        self.font_title = ("Montserrat", 24, "bold")
        self.font_header = ("Montserrat", 18, "bold")
        self.font_normal = ("Montserrat", 14, "bold")
        self.font_small = ("Montserrat", 12, "bold")

        self.selected_file_path = ctk.StringVar(value="No file selected")
        self.output_file_path = ctk.StringVar(value='No file selected')
        
        with open('wordify.json', 'r') as file:
            config = json.load(file)
            output_file = config['output_file_path']
            self.output_file_path.set(value=output_file)
            
        
        # Configure root background
        self.root.configure(fg_color=self.bg_color)
        
        self.create_header()
        self.create_navigation()
        self.create_pages()
        
        # Show home page by default
        self.show_page("home")

    def create_header(self):
        self.header = ctk.CTkFrame(
            self.root, 
            height=80, 
            corner_radius=0,
            fg_color=self.header_bg
        )
        self.header.pack(fill='x', padx=0, pady=0)
        
        # App title in header
        self.title_label = ctk.CTkLabel(
            self.header,
            text="Wordify",
            font=self.font_title,
            text_color=self.text_color
        )
        self.title_label.pack(side='left', padx=20, pady=20)

    def create_navigation(self):
        self.nav_frame = ctk.CTkFrame(
            self.root,
            height=60,
            corner_radius=0,
            fg_color=self.header_bg
        )
        self.nav_frame.pack(fill='x', padx=0, pady=0)
        
        # Navigation buttons
        self.home_btn = ctk.CTkButton(
            self.nav_frame,
            text="Home",
            font=self.font_normal,
            fg_color="transparent",
            hover_color="#2d2d2d",
            text_color=self.text_color,
            command=lambda: self.show_page("home")
        )
        self.home_btn.pack(side='left', padx=10, pady=10)
        
        self.about_btn = ctk.CTkButton(
            self.nav_frame,
            text="About",
            font=self.font_normal,
            fg_color="transparent",
            hover_color="#2d2d2d",
            text_color=self.text_color,
            command=lambda: self.show_page("about")
        )
        self.about_btn.pack(side='left', padx=10, pady=10)
        
        self.settings_btn = ctk.CTkButton(
            self.nav_frame,
            text="Settings",
            font=self.font_normal,
            fg_color="transparent",
            hover_color="#2d2d2d",
            text_color=self.text_color,
            command=lambda: self.show_page("settings")
        )
        self.settings_btn.pack(side='left', padx=10, pady=10)

    def create_pages(self):
        # Container for pages
        self.pages_container = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color
        )
        self.pages_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Home Page
        self.home_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )
        
        # Home page content
        home_title = ctk.CTkLabel(
            self.home_page,
            text="Convert Your PDFs",
            font=self.font_header,
            text_color=self.text_color
        )
        home_title.pack(pady=(30, 10))
        
        home_subtitle = ctk.CTkLabel(
            self.home_page,
            text="Select a file to convert to word format",
            font=self.font_small,
            text_color=self.accent_text
        )
        home_subtitle.pack(pady=(0, 30))
        
        # File selection area
        file_frame = ctk.CTkFrame(
            self.home_page,
            fg_color=self.secondary_card_bg,
            corner_radius=10
        )
        file_frame.pack(fill='x', padx=30, pady=10)
        
        select_btn = ctk.CTkButton(
            file_frame,
            text="Select File",
            font=self.font_normal,
            fg_color=self.btn_orange,
            hover_color=self.btn_hover,
            text_color=self.text_color,
            command=self.select_file
        )
        select_btn.pack(pady=20)
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.selected_file_path,
            font=self.font_small,
            text_color=self.accent_text,
            wraplength=400
        )
        self.file_label.pack(pady=(0, 20))
        
        # Convert button
        convert_btn = ctk.CTkButton(
            self.home_page,
            text="Convert",
            font=self.font_normal,
            fg_color=self.btn_orange,
            hover_color=self.btn_hover,
            text_color=self.text_color,
            height=40,
            width=150,
            command=self.start_conversion
        )
        convert_btn.pack(pady=30)
        
        # About Page
        self.about_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )
        
        # About page content
        about_title = ctk.CTkLabel(
            self.about_page,
            text="About Wordify",
            font=self.font_header,
            text_color=self.text_color
        )
        about_title.pack(pady=(30, 20))
        
        about_text = ctk.CTkLabel(
            self.about_page,
            text="Wordify is a document conversion tool that helps you transform your file to Word format",
            font=self.font_normal,
            text_color=self.accent_text,
            wraplength=400,
            justify="center"
        )
        about_text.pack(pady=10, padx=30)
        
        # Check for updates
        update_frame = ctk.CTkFrame(
            self.about_page,
            fg_color=self.secondary_card_bg,
            corner_radius=10
        )
        update_frame.pack(fill='x', padx=30, pady=20)
        
        update_title = ctk.CTkLabel(
            update_frame,
            text="Check for Updates",
            font=("Poppins", 16, "bold"),
            text_color=self.text_color
        )
        update_title.pack(pady=(15, 10))
        
        update_text = ctk.CTkLabel(
            update_frame,
            text="Ensure you're using the latest version of Wordify",
            font=self.font_small,
            text_color=self.accent_text
        )
        update_text.pack(pady=(0, 15))
        
        check_update_btn = ctk.CTkButton(
            update_frame,
            text="Check Now",
            font=self.font_normal,
            fg_color=self.btn_orange,
            hover_color=self.btn_hover,
            text_color=self.text_color,
            command=self.check_for_updates
        )
        check_update_btn.pack(pady=(0, 15))
        
        # Version info
        version_label = ctk.CTkLabel(
            self.about_page,
            text="Version 1.0.0",
            font=self.font_small,
            text_color=self.accent_text
        )
        version_label.pack(pady=20)

        self.about_message_label = ctk.CTkLabel(
            self.about_page,
            text='',
            font=self.font_small
        )
        self.about_message_label.pack(pady=10, padx=10)
    
        # Settings Page
        self.settings_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )
        
        # Settings page content
        settings_title = ctk.CTkLabel(
            self.settings_page,
            text="Settings",
            font=self.font_header,
            text_color=self.text_color
        )
        settings_title.pack(pady=(30, 20))
        
        # Appearance settings
        appearance_frame = ctk.CTkFrame(
            self.settings_page,
            fg_color=self.secondary_card_bg,
            corner_radius=10
        )
        appearance_frame.pack(fill='x', padx=30, pady=10)
        
        appearance_title = ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=("Poppins", 16, "bold"),
            text_color=self.text_color
        )
        appearance_title.pack(pady=(15, 10))
        
        # Theme selector
        theme_label = ctk.CTkLabel(
            appearance_frame,
            text="Theme:",
            font=self.font_normal,
            text_color=self.accent_text
        )
        theme_label.pack(pady=(5, 5))
        
        theme_option = ctk.CTkOptionMenu(
            appearance_frame,
            values=["Dark", "Light", "System"],
            fg_color=self.btn_orange,
            button_color=self.btn_orange,
            button_hover_color=self.btn_hover
        )
        theme_option.set("Dark")
        theme_option.pack(pady=(0, 15))
        
        # Conversion settings
        conversion_frame = ctk.CTkFrame(
            self.settings_page,
            fg_color=self.secondary_card_bg,
            corner_radius=10
        )
        conversion_frame.pack(fill='x', padx=30, pady=10)
        
        conversion_title = ctk.CTkLabel(
            conversion_frame,
            text="Conversion",
            font=("Poppins", 16, "bold"),
            text_color=self.text_color
        )
        conversion_title.pack(pady=(15, 10))
        
        # Output location
        output_label = ctk.CTkLabel(
            conversion_frame,
            text="Default Output Location:",
            font=self.font_normal,
            text_color=self.accent_text
        )
        output_label.pack(pady=(5, 5))
        
        output_btn = ctk.CTkButton(
            conversion_frame,
            text="Choose Folder",
            font=self.font_small,
            fg_color=self.btn_orange,
            hover_color=self.btn_hover,
            text_color=self.text_color,
            width=120,
            command=self.select_output_folder
        )
        output_btn.pack(pady=(0, 15))

        self.output_path = ctk.CTkLabel(
            conversion_frame,
            textvariable=self.output_file_path,
            font=self.font_small
        )
        self.output_path.pack(pady=10, padx=10)


    def show_page(self, page_name):
        # Hide all pages
        self.home_page.pack_forget()
        self.about_page.pack_forget()
        self.settings_page.pack_forget()
        
        # Show selected page
        if page_name == "home":
            self.home_page.pack(fill='both', expand=True)
        elif page_name == "about":
            self.about_page.pack(fill='both', expand=True)
        elif page_name == "settings":
            self.settings_page.pack(fill='both', expand=True)

    def select_file(self):
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

            with open('wordify.json', 'r') as file:
                config = json.load(file)
                output_folder = config.get("output_file_path")

            if not output_folder or not os.path.isdir(output_folder):
                print("⚠️ Invalid or missing output folder path.")
                return

            output_file_path = os.path.join(output_folder, "converted.docx")

            extracted_text = extract_text_from_pdf(pdf_path)
            save_text_to_word_format(extracted_text, output_file_path)

            print(f"✅ Conversion complete. Saved to: {output_file_path}")
        except Exception as e:
            print("⚠️ Conversion failed:", e)

    def check_for_updates(self):
        try:
            update_status = cfu()
            if update_status is True:
                self.about_message_label.configure(
                    text="Wordify is up to date.",
                    text_color=self.success
                )
            elif update_status is False:
                self.about_message_label.configure(
                    text="A new version of Wordify is available.\nDownload the latest release.",
                    text_color=self.error
                )
            else:
                self.about_message_label.configure(
                    text="Unable to check for updates. Please try again later.",
                    text_color=self.error
                )
        except Exception as e:
            print("⚠️ Update check failed:", e)
            self.about_message_label.configure(
                text="Error checking for updates.",
                text_color=self.error
            )

    def select_output_folder(self):
        try:
            folder_path = filedialog.askdirectory(title="Select Output Folder")
            if folder_path:
                self.output_file_path.set(folder_path)

                # Load existing JSON data
                with open('wordify.json', 'r') as file:
                    data = json.load(file)

                # Update or create the output_file_path entry
                data['output_file_path'] = folder_path

                # Write back to the file
                with open('wordify.json', 'w') as file:
                    json.dump(data, file, indent=4)

                print(f"✅ Saved output folder path: {folder_path}")
        except Exception as e:
            print("⚠️ Failed to update wordify.json:", e)
            self.output_file_path.set("Error selecting folder.")
            
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print('Application Crashed', e)

if __name__ == "__main__":
    app = Wordify()
    app.run()