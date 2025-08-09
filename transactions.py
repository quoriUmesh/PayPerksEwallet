import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class TransactionManager:
    def __init__(self, parent_window, user_email, refresh_callback,user_data,db):
        self.parent_window = parent_window
        self.user_email = user_email
        self.refresh_callback = refresh_callback
        self.user_data = user_data
        self.db = db
    def load_user_data(self):
        """Load user data from database"""
        self.user_data = self.db.get_user_by_email(self.user_email)


    def create_transaction_frame(self):
        """Create and return the transaction frame"""
        self.transaction_frame = ctk.CTkFrame(
            self.parent_window, fg_color='white', width=725, height=500
        )
        
        # Transaction Label
        transaction_label = ctk.CTkLabel(
            self.transaction_frame, text="Transactions", 
            font=ctk.CTkFont(family='Segoe UI', size=40, weight="bold"), 
            text_color='#1375d0'
        )
        transaction_label.place(x=65, y=65)
        
        # PayPerks Logo
        logo_img = ctk.CTkImage(light_image=Image.open('img/PAYPERKS2.png'), size=(250, 250))
        logo_label = ctk.CTkLabel(self.transaction_frame, image=logo_img, text="")
        logo_label.place(x=400, y=-50)

        self.create_main_transaction_buttons()
        self.create_utility_payment_section()
        
        return self.transaction_frame

    def create_main_transaction_buttons(self):
        """Create main transaction buttons"""
        # Send Money
        icon_img = ctk.CTkImage(light_image=Image.open('img/icon/send.png'), size=(40, 40))
        send_button = ctk.CTkButton(
            self.transaction_frame, text="Send Money",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color='black', image=icon_img,
            compound="left", command=self.send_money,
            fg_color='white', hover_color='#e0e1e2',
            width=150, height=50,
            border_color='#e0e1e2', border_width=1, corner_radius=10
        )
        send_button.place(x=210, y=150)

        # Load Money
        icon2_img = ctk.CTkImage(light_image=Image.open('img/icon/load.png'), size=(40, 40))
        load_button = ctk.CTkButton(
            self.transaction_frame, text="Load Money",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color='black', image=icon2_img,
            compound="left", command=self.load_money,
            fg_color='white', hover_color='#e0e1e2',
            width=150, height=50,
            border_color='#e0e1e2', border_width=1, corner_radius=10
        )
        load_button.place(x=20, y=150)

        # Transaction History
        icon3_img = ctk.CTkImage(light_image=Image.open('img/icon/transaction.png'), size=(40, 40))
        transaction_button = ctk.CTkButton(
            self.transaction_frame, text="Transaction History",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color='black', image=icon3_img,
            compound="left", command=self.show_transaction_history,
            fg_color='white', hover_color='#e0e1e2',
            width=150, height=50,
            border_color='#e0e1e2', border_width=1, corner_radius=10
        )
        transaction_button.place(x=20, y=225)

        # Redeem Rewards
        icon4_img = ctk.CTkImage(light_image=Image.open('img/icon/token.png'), size=(40, 40))
        redeem_button = ctk.CTkButton(
            self.transaction_frame, text="Redeem Rewards Points",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color='black', image=icon4_img,
            compound="left", command=self.redeem_rewards,
            fg_color='white', hover_color='#e0e1e2',
            width=180, height=50,
            border_color='#e0e1e2', border_width=1, corner_radius=10
        )
        redeem_button.place(x=400, y=150)

    def create_utility_payment_section(self):
        """Create utility payment buttons"""
        # Utility Label
        utility_label = ctk.CTkLabel(
            self.transaction_frame, text="Utility & Bill Payments", 
            font=ctk.CTkFont(family='Segoe UI', size=20, weight="bold"), 
            text_color='#1375d0'
        )
        utility_label.place(x=20, y=300)

        # Utility buttons data
        utilities = [
            ("TopUp Mobile", "img/icon/topup.png", (20, 350)),
            ("Electricity Bill", "img/icon/electricity.png", (210, 350)),
            ("Internet Bill", "img/icon/internet.png", (400, 350)),
            ("Water Bill", "img/icon/water.png", (20, 425)),
            ("Education Fee", "img/icon/education.png", (210, 425)),
            ("Healthcare Payment", "img/icon/health.png", (400, 425))
        ]

        for text, icon_path, position in utilities:
            icon_img = ctk.CTkImage(light_image=Image.open(icon_path), size=(40, 40))
            button = ctk.CTkButton(
                self.transaction_frame, text=text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color='black', image=icon_img,
                compound="left", command=lambda t=text: self.utility_payment(t),
                fg_color='white', hover_color='#e0e1e2',
                width=150 if position[0] != 400 else 180, height=50,
                border_color='#e0e1e2', border_width=0, corner_radius=10
            )
            button.place(x=position[0], y=position[1])

    def send_money(self):
        """Open send money popup"""
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title("Send Money")
        popup.geometry("400x300")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        ctk.CTkLabel(popup, text="Send Money", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(popup, text="Recipient Email:").pack(pady=5)
        email_entry = ctk.CTkEntry(popup, width=300, placeholder_text="Enter recipient email")
        email_entry.pack(pady=5)
        
        ctk.CTkLabel(popup, text="Amount:").pack(pady=5)
        amount_entry = ctk.CTkEntry(popup, width=300, placeholder_text="Enter amount")
        amount_entry.pack(pady=5)

        def process_send():
            recipient_email = email_entry.get()
            amount_str = amount_entry.get()
            
            if not recipient_email or not amount_str:
                messagebox.showerror("Error", "All fields are required")
                return
            elif self.user_email == recipient_email:
                messagebox.showerror("Error", "Cannot send to own account")
                return
            
            elif self.db.email_exists(recipient_email) is None or False:
                messagebox.showerror("Error", "Recipent Email not exists")
                return
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                if amount > self.user_data[1]:
                    messagebox.showerror('Error','Insuffient Balance')
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return
            
            if self.db.process_send_money(self.user_email, recipient_email, amount):
                messagebox.showinfo('Success',f'Sucessfully sent ${amount:.2f} to {recipient_email}')
                popup.destroy()

            else:
                    messagebox.showerror("Error", "Transaction failed")

        send_btn = ctk.CTkButton(popup, text="Send", command=process_send)
        send_btn.pack(pady=20)


    def load_money(self):
        """Open load money popup"""
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title("Load Money")
        popup.geometry("400x350")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        ctk.CTkLabel(popup, text="Load Money", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(popup, text="Select Payment Method:").pack(pady=5)
        
        method_var = ctk.StringVar(value="Bank")
        methods = ["Bank", "eSewa", "Khalti"]
        
        for method in methods:
            ctk.CTkRadioButton(popup, text=method, variable=method_var, value=method).pack(pady=2)
        
        ctk.CTkLabel(popup, text="Amount:").pack(pady=5)
        amount_entry = ctk.CTkEntry(popup, width=300, placeholder_text="Enter amount")
        amount_entry.pack(pady=5)

        def process_load():
            amount_str = amount_entry.get()
            method = method_var.get()
            if not amount_str:
                messagebox.showerror("Error", "Amount is required")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return

            if self.db.process_load_money(self.user_email,amount,method):
                messagebox.showinfo("Success", f"Sucessfully loaded ${amount:.2f} via {method}")
                popup.destroy()
                self.load_user_data()
                self.refresh_callback()
            else:
                messagebox.showerror("Error", "Payment failed")
    
        load_btn = ctk.CTkButton(popup, text="Load", command=process_load)
        load_btn.pack(pady=20)

    def redeem_rewards(self):
        """Open redeem rewards popup"""
        # Refresh user data to get latest points
        self.load_user_data()
        
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title("Redeem Rewards")
        popup.geometry("400x250")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        ctk.CTkLabel(popup, text="Redeem Reward Points", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        current_points = self.user_data[2] if self.user_data else 0
        points_label = ctk.CTkLabel(popup, text=f"Available Points: {current_points}", 
                                   font=ctk.CTkFont(size=14, weight="bold"), text_color="#1375d0")
        points_label.pack(pady=5)
        
        ctk.CTkLabel(popup, text="Exchange Rate: 1 Point = $1.00", 
                    font=ctk.CTkFont(size=12), text_color="#666").pack(pady=5)
        
        ctk.CTkLabel(popup, text="Points to Redeem:").pack(pady=5)
        points_entry = ctk.CTkEntry(popup, width=300, placeholder_text="Enter points")
        points_entry.pack(pady=5)
        
        # Add validation message label
        message_label = ctk.CTkLabel(popup, text="", font=ctk.CTkFont(size=11), text_color="red")
        message_label.pack(pady=2)

        def process_redeem():
            points_str = points_entry.get()
            
            if not points_str:
                message_label.configure(text="Points amount is required")
                return
            
            try:
                points = float(points_str)
                if points <= 0:
                    messagebox.showerror('Error','Point must be in Postive')
                    return
                if points > current_points:
                    messagebox.showerror('Error','Insufficient points. You have {current_points} points')
                    return
            except ValueError:
                message_label.showerror('Error','Please enter a valid number')
                return
            
            # Clear any previous error messages
            message_label.configure(text="")

            if self.db.process_redeem_points(self.user_email, points):
                messagebox.showinfo("Success", f"Successfully redeemed {points} points for ${points:.2f}")
                popup.destroy()
                # Refresh user data and callback to update dashboard
                self.load_user_data()
                self.refresh_callback()
            else:
                message_label.configure(text="Redemption failed. Please try again.")

        ctk.CTkButton(popup, text="Redeem", command=process_redeem).place(x=125,y=200)

    def utility_payment(self, payment_type):
        """Open utility payment popup"""
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title(f"{payment_type}")
        popup.geometry("400x250")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"{payment_type}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(popup, text="Amount:").pack(pady=5)
        amount_entry = ctk.CTkEntry(popup, width=300, placeholder_text="Enter amount")
        amount_entry.pack(pady=5)

        def process_payment():
            amount_str = amount_entry.get()
            
            if not amount_str:
                messagebox.showerror("Error", "Amount is required")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return

            if self.db.process_utility_payment(self.user_email,amount,payment_type):
                messagebox.showinfo('Sucess',f'Sucessfully paid ${amount:.2f} for {payment_type}')
                popup.destroy()
                self.load_user_data()
                self.refresh_callback()
            else:
                messagebox.showerror("Error", "Payment failed")

        utility_btn =ctk.CTkButton(popup, text="Pay", command=process_payment)
        utility_btn.pack(pady=20)

    def show_transaction_history(self):
        """Show transaction history popup"""
        popup = ctk.CTkToplevel(self.parent_window)
        popup.title("Transaction History")
        popup.geometry("600x400")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        ctk.CTkLabel(popup, text="Transaction History", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Create scrollable frame for transactions
        scrollable_frame = ctk.CTkScrollableFrame(popup, width=550, height=300)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Get transaction history
        user_id = self.user_data[5] if self.user_data else None
        transactions = self.db.get_user_transactions(user_id)

        if transactions:
            for transaction in transactions:
                date_str = transaction[0].strftime("%Y-%m-%d %H:%M") if transaction[0] else "N/A"
                trans_type = transaction[1].title()
                amount = transaction[2]

                trans_frame = ctk.CTkFrame(scrollable_frame, fg_color='#f0f0f0', corner_radius=5)
                trans_frame.pack(fill='x', pady=2, padx=5)
                
                # Color code based on transaction type
                if transaction[1] in ['load', 'redeem']:
                    amount_color = "#28a745"  # Green for income
                    amount_text = f"+${amount:.2f}"

                elif transaction[1] == 'send':
                    if transaction[4] == self.user_data[5]:
                        amount_color = "#dc3545"  # Red for expenses
                        amount_text = f"-${amount:.2f}"
                    else:
                        amount_color = "#28a745"  # Green for income
                        amount_text = f"+${amount:.2f}"  

                else:
                    amount_color = "#dc3545"  # Red for expenses
                    amount_text = f"-${amount:.2f}"
                
                # Create info frame with better layout
                info_frame = ctk.CTkFrame(trans_frame, fg_color='transparent')
                info_frame.pack(fill='x', padx=10, pady=5)
                
                # Date and type
                ctk.CTkLabel(info_frame, text=f"{date_str} | {trans_type}", 
                           font=ctk.CTkFont(size=12, weight="bold")).pack(anchor='w')
                
                # Amount with color
                ctk.CTkLabel(info_frame, text=amount_text, 
                           font=ctk.CTkFont(size=12, weight="bold"), 
                           text_color=amount_color).pack(anchor='e', side='right')
                
                # Description if available
                if transaction[3]:  # Description
                    ctk.CTkLabel(info_frame, text=transaction[3], 
                               font=ctk.CTkFont(size=10), 
                               text_color="#666").pack(anchor='w')
        else:
            no_trans_frame = ctk.CTkFrame(scrollable_frame, fg_color='#f8f9fa', corner_radius=10)
            no_trans_frame.pack(fill='x', pady=20, padx=20)
            ctk.CTkLabel(no_trans_frame, text="No transactions found", 
                        font=ctk.CTkFont(size=14), text_color="#666").pack(pady=30)

        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=10)