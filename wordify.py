from updater_file import check_for_updates as cfu
from logic import pdf_extraction_process
from res_path import resource_path
from tkinter import filedialog
import customtkinter as ctk
import webbrowser
import threading
import json
import os
import sys

class LabelRedirector:
    def __init__(self, label_widget, success_color="#10b981", error_color="#ef4444"):
        self.label = label_widget
        self.success_color = success_color
        self.error_color = error_color

    def write(self, message):
        if message.strip():
            text = message.strip()

            # Check for error prefix
            if text.lower().startswith("error") or "failed" in text.lower():
                self.label.configure(text=text, text_color=self.error_color)
            else:
                self.label.configure(text=text, text_color=self.success_color)

    def flush(self):
        pass

class Wordify:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title('Wordify')
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.iconbitmap(resource_path('shark.ico'))
        
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
        
        with open(resource_path("wordify.json"), 'r') as file:
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
        self.pages_container = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color
        )
        self.pages_container.pack(fill='both', expand=True, padx=20, pady=20)
    
        self.home_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )
        
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
        
        file_frame = ctk.CTkFrame(
            self.home_page,
            fg_color=self.secondary_card_bg,
            corner_radius=10
        )
        file_frame.pack(fill='x', padx=20, pady=10)
        
        select_btn = ctk.CTkButton(
            file_frame,
            text="Select File",
            font=self.font_normal,
            fg_color=self.btn_orange,
            hover_color=self.btn_hover,
            text_color=self.text_color,
            command=self.select_file
        )
        select_btn.pack(pady=10)
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.selected_file_path,
            font=self.font_small,
            text_color=self.accent_text,
            wraplength=400
        )
        self.file_label.pack(pady=(0, 20))

        # Label for output filename
        output_label = ctk.CTkLabel(
            file_frame,
            text="Output file name:",
            font=self.font_small,
            text_color=self.accent_text
        )
        output_label.pack(pady=(0, 5))

        # Entry field for output filename
        self.output_filename_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="e.g. my_document.docx",
            font=self.font_small,
            width=300
        )
        self.output_filename_entry.pack(pady=(0, 20))

        
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
        convert_btn.pack(pady=10)

        self.converstion_message = ctk.CTkLabel(
            self.home_page,
            text='',
            font=self.font_small
        )
        self.converstion_message.pack()
        
        self.about_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )

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
            command=lambda: threading.Thread(target=self.check_for_updates, daemon=True).start()
        )
        check_update_btn.pack(pady=(0, 15))
        
        try:
            with open(resource_path("wordify.json"), 'r') as file:
                config = json.load(file)
                version = config.get("version", "Unknown")
        except Exception as e:
            print("⚠️ Failed to load version:", e)
            version = "Unknown"

        version_label = ctk.CTkLabel(
            self.about_page,
            text=f"Version {version}",
            font=self.font_small,
            text_color=self.accent_text
        )
        version_label.pack(pady=5)


        self.about_message_label = ctk.CTkLabel(
            self.about_page,
            text='',
            font=self.font_small
        )
        self.about_message_label.pack()
    
        self.settings_page = ctk.CTkFrame(
            self.pages_container,
            fg_color=self.card_bg,
            corner_radius=15
        )

        settings_title = ctk.CTkLabel(
            self.settings_page,
            text="Settings",
            font=self.font_header,
            text_color=self.text_color
        )
        settings_title.pack(pady=(10, 20))

        # appearance_frame = ctk.CTkFrame(
        #     self.settings_page,
        #     fg_color=self.secondary_card_bg,
        #     corner_radius=10
        # )
        # appearance_frame.pack(fill='x', padx=30, pady=10)
        
        # appearance_title = ctk.CTkLabel(
        #     appearance_frame,
        #     text="Appearance",
        #     font=("Poppins", 16, "bold"),
        #     text_color=self.text_color
        # )
        # appearance_title.pack(pady=(10, 10))

        # color_label = ctk.CTkLabel(
        #     appearance_frame,
        #     text="Primary button color (hex):",
        #     font=self.font_small,
        #     text_color=self.accent_text
        # )
        # color_label.pack(pady=(0, 5))

        # self.color_entry = ctk.CTkEntry(
        #     appearance_frame,
        #     placeholder_text="#FF8800",
        #     font=self.font_small,
        #     width=200
        # )
        # self.color_entry.pack(pady=(0, 10))

        # apply_color_btn = ctk.CTkButton(
        #     appearance_frame,
        #     text="Apply Color",
        #     font=self.font_small,
        #     fg_color=self.btn_orange,
        #     hover_color=self.btn_orange,
        #     command=self.apply_btn_orange
        # )
        # apply_color_btn.pack(pady=(0, 20))


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

    def apply_btn_orange(self):
        hex_color = self.color_entry.get().strip()

        if not hex_color.startswith("#") or len(hex_color) != 7:
            self.converstion_message.configure(
                text="Error: Invalid hex color. Use format #RRGGBB.",
                text_color="red"
            )
            return

        self.btn_orange = hex_color
        self.converstion_message.configure(
            text=f"✅ Button color updated to {hex_color}",
            text_color="green"
        )

    def start_conversion(self):
        def run_conversion():
            try:
                pdf_path = self.selected_file_path.get()
                if not pdf_path or pdf_path == "No file selected":
                    self.selected_file_path.set("Select a PDF file to convert!")
                    return

                with open(resource_path("wordify.json"), 'r') as file:
                    config = json.load(file)
                    output_folder = config.get("output_file_path")

                if not output_folder or not os.path.isdir(output_folder):
                    print("Error: Invalid or missing output folder path.")
                    self.converstion_message.configure(
                        text='Invalid Output path. Head to settings to set your preferred output path.',
                        text_color=self.error
                    )
                    return

                filename = self.output_filename_entry.get().strip()
                if not filename:
                    print("Error: Output filename is empty.")
                    self.converstion_message.configure(
                        text='Please enter a valid output filename.',
                        text_color=self.error
                    )
                    return
                if not filename.endswith(".docx"):
                    filename += ".docx"

                output_file_path = os.path.join(output_folder, filename)

                # Redirect print to label
                sys.stdout = LabelRedirector(self.converstion_message, success_color=self.success, error_color=self.error)
                sys.stderr = LabelRedirector(self.converstion_message, success_color=self.success, error_color=self.error)

                # Run the OCR pipeline
                pdf_extraction_process(
                    file_path=pdf_path,
                    output_path=output_file_path,
                    max_retries=3,
                    resume_from=0
                )

                print(f"✅ Conversion complete. Saved to: {output_file_path}")

            except Exception as e:
                print(f"Error: Conversion failed — {e}")
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

        threading.Thread(target=run_conversion, daemon=True).start()

    def check_for_updates(self):
        try:
            update_status = cfu()

            if update_status is True:
                self.about_message_label.configure(
                    text="Wordify is up to date.",
                    text_color=self.success,
                    cursor=""
                )

                if hasattr(self, "download_link_label"):
                    self.download_link_label.pack_forget()

            elif update_status is False:
                download_url = "https://yourdomain.com/wordify/download"

                self.about_message_label.configure(
                    text="A new version of Wordify is available.",
                    text_color=self.error,
                    cursor=""
                )

                self.download_link_label = ctk.CTkLabel(
                    master=self.about_message_label.master,
                    text="Click here to download.",
                    text_color="#1E90FF",
                    cursor="hand2",
                    font=self.font_small
                )
                self.download_link_label.pack()

                def open_download_link(event):
                    webbrowser.open_new(download_url)

                self.download_link_label.bind("<Button-1>", open_download_link)

            else:
                self.about_message_label.configure(
                    text="Unable to check for updates. Please try again later.",
                    text_color=self.error,
                    cursor=""
                )

                if hasattr(self, "download_link_label"):
                    self.download_link_label.pack_forget()

        except Exception as e:
            print("⚠️ Update check failed:", e)
            self.about_message_label.configure(
                text="Error checking for updates.",
                text_color=self.error,
                cursor=""
            )

            if hasattr(self, "download_link_label"):
                self.download_link_label.pack_forget()

    def select_output_folder(self):
        try:
            folder_path = filedialog.askdirectory(title="Select Output Folder")
            if folder_path:
                self.output_file_path.set(folder_path)

                # Load existing JSON data
                with open(resource_path("wordify.json"), 'r') as file:
                    data = json.load(file)

                # Update or create the output_file_path entry
                data['output_file_path'] = folder_path

                # Write back to the file
                with open(resource_path("wordify.json"), 'w') as file:
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