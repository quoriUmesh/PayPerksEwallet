import customtkinter as ctk
import datetime
from dashboard_home import DashboardHome
from settings import SettingsManager
from transactions import TransactionManager
import threading
from  session_manager import SessionManager 

class PayPerksDashboard:
    def __init__(self, user_email,db):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.user_email = user_email
        self.db = db
        self.user_data = self.db.get_user_by_email(self.user_email)
        self.window = ctk.CTk(fg_color="white")
        self.window.title('PayPerks Dashboard')
        self.window.geometry('925x500')
        self.window.resizable(False, False)
        
        # Initialize components
        self.dashboard_home = DashboardHome(self.window, user_email,self.user_data,self.db)
        self.settings_manager = SettingsManager(self.window, user_email,self.user_data,self.db)
        self.transaction_manager = TransactionManager(self.window, user_email, self.refresh_dashboard,self.user_data,self.db)
        
        self.setup_sidebar()
        self.setup_frames()
       # self.check_session_expiry()
        
        # Show dashboard by default
        self.show_dashboard()
        threading.Thread(target=self.session_init,daemon=True).start()

    def session_init(self):
        session = SessionManager(self.db)
        result = session.create_session(self.user_data[5])
        self.session_id = result[0]
        self.expiry = result[1]

    def run(self):
        self.window.mainloop()

    def setup_sidebar(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.window, fg_color='#1375d0', width=200, corner_radius=0)
        self.sidebar.pack(side='left', fill='y', padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        button_font = ctk.CTkFont(family='Segoe UI', size=17, weight='bold')
        self.sidebar_buttons = {}
        self.ACTIVE_COLOR = '#4899f0'
        self.INACTIVE_COLOR = '#1375d0'

        # Dashboard Button
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar, text='Dashboard', font=button_font, height=40,
            fg_color=self.ACTIVE_COLOR, hover_color=self.ACTIVE_COLOR,
            text_color='white', corner_radius=8,
            command=self.dashboard_clicked
        )
        self.dashboard_btn.pack(fill='x', padx=20, pady=(20, 5))
        self.sidebar_buttons['dashboard'] = self.dashboard_btn

        # Transactions Button
        self.transactions_btn = ctk.CTkButton(
            self.sidebar, text='Transactions', font=button_font, height=40,
            fg_color=self.INACTIVE_COLOR, hover_color=self.ACTIVE_COLOR,
            text_color='white', corner_radius=8,
            command=self.transactions_clicked
        )
        self.transactions_btn.pack(fill='x', padx=20, pady=5)
        self.sidebar_buttons['transactions'] = self.transactions_btn

        # Settings Button
        self.settings_btn = ctk.CTkButton(
            self.sidebar, text='Settings', font=button_font, height=40,
            fg_color=self.INACTIVE_COLOR, hover_color=self.ACTIVE_COLOR,
            text_color='white', corner_radius=8,
            command=self.settings_clicked
        )
        self.settings_btn.pack(fill='x', padx=20, pady=5)
        self.sidebar_buttons['settings'] = self.settings_btn

        # Logout Button (at the bottom with red color)
        self.logout_btn = ctk.CTkButton(
            self.sidebar, text='Logout', font=button_font, height=40,
            fg_color='#dc3545', hover_color='#c82333',
            text_color='white', corner_radius=8,
            command=self.logout_clicked
        )
        self.logout_btn.pack(side='bottom', fill='x', padx=20, pady=(5, 20))
    def setup_frames(self):
        # Create main content frames
        self.dashboard_frame = self.dashboard_home.create_dashboard_frame()
        self.transaction_frame = self.transaction_manager.create_transaction_frame()
        self.settings_frame = self.settings_manager.create_settings_frame()

    def set_active(self, btn_name):
        for name, btn in self.sidebar_buttons.items():
            if name == btn_name:
                btn.configure(fg_color=self.ACTIVE_COLOR)
            else:
                btn.configure(fg_color=self.INACTIVE_COLOR)

    def dashboard_clicked(self):
        self.set_active('dashboard')
        self.show_dashboard()

    def transactions_clicked(self):
        self.set_active('transactions')
        self.show_transactions()

    def settings_clicked(self):
        self.set_active('settings')
        self.show_settings()

    def show_dashboard(self):
        self.dashboard_frame.place(x=200, y=0)
        self.settings_frame.place_forget()
        self.transaction_frame.place_forget()
        # Force refresh of dashboard data and recreate chart
        self.dashboard_home.refresh_data()
        self.dashboard_home.create_activity_chart()

    def show_transactions(self):
        self.transaction_frame.place(x=200, y=0)
        self.dashboard_frame.place_forget()
        self.settings_frame.place_forget()

    def show_settings(self):
        self.settings_frame.place(x=200, y=0)
        self.dashboard_frame.place_forget()
        self.transaction_frame.place_forget()

    def logout_clicked(self, confirm=True):
        """Handle logout - optionally confirm"""
        from tkinter import messagebox

        def perform_logout():
            self.db.invalidate_session(self.session_id)
            self.db.close()

        if confirm:
            if not messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                return  # Cancel logout if user clicks No

        threading.Thread(target=perform_logout, daemon=True).start()
        self.window.destroy()

        # Import and launch auth window
        from auth_gui import PayPerksAuth
        auth_app = PayPerksAuth()
        auth_app.run()

    def refresh_dashboard(self):
        def task():
            session_manager = SessionManager(self.db)
            new_expiry = session_manager.refresh_session(self.session_id)
            if new_expiry:
                self.expiry = new_expiry
        threading.Thread(target=task, daemon=True).start()
        self.dashboard_home.refresh_data()
        self.dashboard_home.create_activity_chart()

    def check_session_expiry(self):
        now = datetime.datetime.now()
        if now > self.expiry:
            self.logout_clicked(confirm=False)
        else:
            # Check again after 1 minute (60000 ms)
            self.window.after(60000, self.check_session_expiry)


