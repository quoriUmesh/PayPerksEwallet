import customtkinter as ctk
from tkinter import messagebox

class SettingsManager:
    def __init__(self, parent_window, user_email,user_data,db):
        self.parent_window = parent_window
        self.user_email = user_email
        self.user_data = user_data
        self.db = db

    def create_settings_frame(self):
        """Create and return the settings frame"""
        self.settings_frame = ctk.CTkScrollableFrame(
            self.parent_window, fg_color='white', width=725, height=500
        )
        
        self.create_profile_section()
        self.create_security_section()
        self.create_notifications_section()
        self.create_support_section()
        
        return self.settings_frame

    def create_profile_section(self):
        """Create profile settings section"""
        profile_frame = ctk.CTkFrame(
            self.settings_frame, fg_color='white', border_color='#e0e1e2', 
            border_width=2, corner_radius=10
        )
        profile_frame.pack(pady=10, padx=10, fill='x')

        profile_label = ctk.CTkLabel(
            profile_frame, text="Profile Settings", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color='#1375d0'
        )
        profile_label.pack(anchor='w', padx=20, pady=(10, 5))

        # Full Name
        full_name_label = ctk.CTkLabel(
            profile_frame, text="Full Name:", 
            font=ctk.CTkFont(size=16), text_color='#222'
        )
        full_name_label.pack(anchor='w', padx=20)

        name_frame = ctk.CTkFrame(
            profile_frame, height=35, border_color='#e0e1e2', 
            border_width=1, corner_radius=5, fg_color='white'
        )
        name_frame.pack(padx=20, pady=(0, 10), fill='x')
        
        name_text = self.user_data[0] if self.user_data else "N/A"
        name_label = ctk.CTkLabel(
            name_frame, text=name_text, 
            font=ctk.CTkFont(size=18), text_color='#222'
        )
        name_label.pack(anchor='w', padx=10, pady=5)

        # Email
        email_label = ctk.CTkLabel(
            profile_frame, text="Email:", 
            font=ctk.CTkFont(size=16), text_color='#222'
        )
        email_label.pack(anchor='w', padx=20)

        email_frame = ctk.CTkFrame(
            profile_frame, height=35, border_color='#e0e1e2', 
            border_width=1, corner_radius=5, fg_color='white'
        )
        email_frame.pack(padx=20, pady=(0, 10), fill='x')
        
        email_label = ctk.CTkLabel(
            email_frame, text=self.user_email, 
            font=ctk.CTkFont(size=18), text_color='#222'
        )
        email_label.pack(anchor='w', padx=10, pady=5)

    def create_security_section(self):
        """Create security settings section"""
        security_frame = ctk.CTkFrame(
            self.settings_frame, fg_color='white', border_color='#e0e1e2', 
            border_width=2, corner_radius=10
        )
        security_frame.pack(pady=10, padx=10, fill='x')

        security_label = ctk.CTkLabel(
            security_frame, text="Security Settings", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color='#1375d0'
        )
        security_label.pack(anchor='w', padx=20, pady=(10, 5))

        change_password_btn = ctk.CTkButton(
            security_frame, text="Change Password", font=ctk.CTkFont(size=16),
            width=200, height=40, fg_color='#4899f0', hover_color='#0052cc',
            command=self.change_password
        )
        change_password_btn.pack(padx=20, pady=(10, 20), anchor='w')

    def create_notifications_section(self):
        """Create notifications section"""
        notifications_frame = ctk.CTkFrame(
            self.settings_frame, fg_color='white', border_color='#e0e1e2', 
            border_width=2, corner_radius=10
        )
        notifications_frame.pack(pady=10, padx=10, fill='x')
        
        notifications_label = ctk.CTkLabel(
            notifications_frame, text="Notification Settings", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color='#1375d0'
        )
        notifications_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        notifications_switch = ctk.CTkSwitch(
            notifications_frame, text="Enable Email Notifications", 
            font=ctk.CTkFont(size=16), 
            command=lambda: print("Notifications toggled")
        )
        notifications_switch.pack(anchor='w', padx=20, pady=(0, 10))

    def create_support_section(self):
        """Create support section"""
        support_frame = ctk.CTkFrame(
            self.settings_frame, fg_color='white', border_color='#e0e1e2', 
            border_width=2, corner_radius=10
        )
        support_frame.pack(pady=10, padx=10, fill='x')
        
        support_label = ctk.CTkLabel(
            support_frame, text="Support and Feedback", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color='#1375d0'
        )
        support_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        support_text = ctk.CTkLabel(
            support_frame, text="For any issues or feedback, please contact us"
        )
        support_text.pack(anchor='w', padx=20, pady=(0, 10))
        
        contact_btn = ctk.CTkButton(
            support_frame, text="Contact Support", font=ctk.CTkFont(size=16),
            width=200, height=40, fg_color='#4899f0', hover_color='#0052cc',
            command=lambda: messagebox.showinfo("Contact", "Email: support@payperks.com")
        )
        contact_btn.pack(padx=20, pady=(0, 10), anchor='w')

    def change_password(self):
        """Open change password popup"""
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title("Change Password")
        popup.geometry("400x400")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()
        
        # Labels and entries
        ctk.CTkLabel(
            popup, text="Change Password", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(popup, text="Current Password:").pack(pady=5)
        current_password_entry = ctk.CTkEntry(popup, width=300, show="*")
        current_password_entry.pack(pady=5)
        
        ctk.CTkLabel(popup, text="New Password:").pack(pady=5)
        new_password_entry = ctk.CTkEntry(popup, width=300, show="*")
        new_password_entry.pack(pady=5)
        
        ctk.CTkLabel(popup, text="Confirm New Password:").pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(popup, width=300, show="*")
        confirm_password_entry.pack(pady=5)
        
        def submit_change():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not all([current_password, new_password, confirm_password]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            # Verify current password and update
            if self.db.authenticate_user(self.user_email, current_password):
                if self.db.update_password(self.user_email, new_password):
                    messagebox.showinfo("Success", "Password changed successfully!")
                    popup.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update password")
            else:
                messagebox.showerror("Error", "Current password is incorrect")
        
        submit_btn = ctk.CTkButton(popup, text="Submit", command=submit_change)
        submit_btn.pack(pady=20)