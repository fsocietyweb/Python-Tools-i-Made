import random
import string
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from faker import Faker

# Initialize Faker
fake = Faker()

# Set the overall theme to Dark and Green
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class PrivacyDataForge(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window - Expanded to 800x650 for a clean single-screen layout
        self.title("Data Forge")
        self.geometry("800x650")
        self.resizable(False, False)

        # Data Storage
        self.generated_data = {}
        self.select_all_state = False

        # 21 Privacy-focused Fields
        self.options = [
            "IPv4 Address", "IPv6 Address", "MAC Address", "User-Agent",
            "Username", "Password", "Secret Key (Hex)", "UUIDv4",
            "Full Name", "Fake Email", "Phone Number", "Birthdate", "SSN/ID Mock",
            "Country", "City", "Street Address",
            "Company Name", "Job Title", "Credit Card", "Card CVV", "Card Expiry"
        ]
        
        self.checkbox_vars = {}

        # Build UI
        self.create_about_section()
        self.create_warning_section()
        self.create_options_section()
        self.create_output_section()

    def create_about_section(self):
        """Creates the Header & Dedicated About Section."""
        about_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#141414")
        about_frame.pack(fill="x", padx=20, pady=(15, 5))

        title_label = ctk.CTkLabel(
            about_frame, 
            text="DATA FORGE v1.4", 
            font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
            text_color="#00FF66"
        )
        title_label.pack(pady=(10, 2))

        about_text = (
            "ABOUT THIS TOOL:\n"
            "Data Forge is an offline identity-masking utility engineered for privacy advocates. "
            "When web services demand personal telemetry data that they don't actually need, "
            "this application generates cryptographically randomized credentials, network routes, "
            "and personas. Use these mock profiles to poison data trackers, safeguard your digital footprint, "
            "and sign up for services without surrendering your true identity."
        )
        about_details = ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=ctk.CTkFont(size=11),
            text_color="#A0A0A0",
            wraplength=740,
            justify="left"
        )
        about_details.pack(pady=(5, 10), padx=15)

    def create_warning_section(self):
        warning_frame = ctk.CTkFrame(self, corner_radius=5, border_width=1, border_color="#FF3333", fg_color="#1A0A0A")
        warning_frame.pack(fill="x", padx=20, pady=5)

        warning_text = (
            "NOTICE: Generated items are simulated attributes meant to substitute real personal identifiers. "
            "Any mathematical overlap with existing data is purely coincidental."
        )
        warning_label = ctk.CTkLabel(
            warning_frame, 
            text=warning_text, 
            font=ctk.CTkFont(size=11),
            text_color="#FF6666",
            wraplength=740,
            justify="center"
        )
        warning_label.pack(pady=6, padx=10)

    def create_options_section(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(5, 2))

        options_label = ctk.CTkLabel(header_frame, text="Select Profile Items to Spoof", font=ctk.CTkFont(weight="bold", size=14))
        options_label.pack(side="left")

        self.toggle_all_btn = ctk.CTkButton(
            header_frame, text="Select All", width=80, height=20,
            font=ctk.CTkFont(size=11), fg_color="#222222", text_color="#00FF66",
            hover_color="#333333", command=self.toggle_all_fields
        )
        self.toggle_all_btn.pack(side="right")

        # Standard non-scrollable frame - items fit perfectly in a 4-column grid
        grid_frame = ctk.CTkFrame(self, fg_color="#0D0D0D", corner_radius=8)
        grid_frame.pack(fill="x", padx=20, pady=5)

        for index, field in enumerate(self.options):
            var = tk.BooleanVar()
            self.checkbox_vars[field] = var
            
            cb = ctk.CTkCheckBox(
                grid_frame, text=field, variable=var, 
                font=ctk.CTkFont(size=12), text_color="#E0E0E0",
                fg_color="#00FF66", hover_color="#00CC52"
            )
            # Organised into 4 columns to perfectly distribute all 21 options on one screen
            row = index // 4
            col = index % 4
            cb.grid(row=row, column=col, sticky="w", padx=15, pady=6)

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.gen_button = ctk.CTkButton(
            btn_frame, text="GENERATE PRIVACY PROFILE", font=ctk.CTkFont(weight="bold"),
            fg_color="#00FF66", text_color="#000000", hover_color="#00CC52",
            command=self.generate_data_action
        )
        self.gen_button.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.save_button = ctk.CTkButton(
            btn_frame, text="EXPORT TO FILE", font=ctk.CTkFont(weight="bold"),
            state="disabled", command=self.save_data_action
        )
        self.save_button.pack(side="right", expand=True, fill="x", padx=(10, 0))

    def create_output_section(self):
        output_label = ctk.CTkLabel(self, text="Obfuscated Output Stream", font=ctk.CTkFont(weight="bold", size=14))
        output_label.pack(anchor="w", padx=25, pady=(5, 2))

        self.output_textbox = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Courier", size=12),
            fg_color="#0A0A0A", text_color="#00FF66",
            border_width=1, border_color="#222222"
        )
        self.output_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.output_textbox.configure(state="disabled")

    def toggle_all_fields(self):
        self.select_all_state = not self.select_all_state
        for var in self.checkbox_vars.values():
            var.set(self.select_all_state)
        self.toggle_all_btn.configure(text="Deselect All" if self.select_all_state else "Select All")

    def generate_field(self, field_type):
        """Advanced Mock Engine."""
        if field_type == "IPv4 Address": return fake.ipv4()
        elif field_type == "IPv6 Address": return fake.ipv6()
        elif field_type == "MAC Address": return fake.mac_address()
        elif field_type == "User-Agent": return fake.user_agent()
        elif field_type == "Username": return fake.user_name()
        elif field_type == "Password":
            pool = string.ascii_letters + string.digits + "!@#$%^&*"
            return "".join(random.choice(pool) for _ in range(16))
        elif field_type == "Secret Key (Hex)": return f"0x{random.getrandbits(128):032x}"
        elif field_type == "UUIDv4": return fake.uuid4()
        elif field_type == "Full Name": return fake.name()
        elif field_type == "Fake Email": return fake.free_email()
        elif field_type == "Phone Number": return fake.phone_number()
        elif field_type == "Birthdate": return str(fake.date_of_birth(minimum_age=18, maximum_age=70))
        elif field_type == "SSN/ID Mock": return fake.ssn()
        elif field_type == "Country": return fake.country()
        elif field_type == "City": return fake.city()
        elif field_type == "Street Address": return fake.street_address()
        elif field_type == "Company Name": return fake.company()
        elif field_type == "Job Title": return fake.job()
        elif field_type == "Credit Card": return fake.credit_card_number()
        elif field_type == "Card CVV": return str(random.randint(100, 999))
        elif field_type == "Card Expiry": return fake.credit_card_expire()
        return "Unknown"

    def generate_data_action(self):
        self.generated_data.clear()
        selected_fields = [field for field, var in self.checkbox_vars.items() if var.get()]

        if not selected_fields:
            messagebox.showwarning("Selection Missing", "Please tick at least one item to generate.")
            return

        display_text = "--- GENERATED PRIVACY MANIFEST ---\n\n"
        for field in selected_fields:
            val = self.generate_field(field)
            self.generated_data[field] = val
            display_text += f"{field.replace(' ', '_')}={val}\n"
        display_text += "\n-----------------------------------"

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", tk.END)
        self.output_textbox.insert("1.0", display_text)
        self.output_textbox.configure(state="disabled")
        self.save_button.configure(state="normal")

    def save_data_action(self):
        if not self.generated_data: return
        filename = "F_infos.chesty"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for key, value in self.generated_data.items():
                    f.write(f"{key.replace(' ', '_')}={value}\n")
            messagebox.showinfo("Success", f"Privacy manifest exported safely to '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile:\n{str(e)}")

if __name__ == "__main__":
    app = PrivacyDataForge()
    app.mainloop()
