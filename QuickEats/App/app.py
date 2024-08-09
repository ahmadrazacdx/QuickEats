import re
import json
import webbrowser
import tkinter as tk
from database import Db
import ttkbootstrap as ttk
from graph_plot import Plot
from datetime import datetime
from tkinter import messagebox
from tkinter import font as tkfont


class App:

    def __init__(self):
        self.db = Db()
        self.plt = Plot()
        self.root = ttk.Window(themename="flatly")
        self.root.geometry('400x600')
        self.root.title('QuickEats')
        self.login()
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=('Trebuchet MS', 10))
        self.root.mainloop()

    def login(self):
        self.clear()
        heading = ttk.Label(text='QuickEats')
        heading.pack(pady=15)
        heading.configure(font=('Playwrite AR', 18, 'bold'))

        text_label1 = ttk.Label(text='Email', width=29, bootstyle="dark")
        text_label1.pack(padx=10, pady=3)
        text_label1.configure(font=('Comfortaa', 10, 'bold'))

        self.login_email_entry = ttk.Entry(width=35, bootstyle="dark")
        self.login_email_entry.pack(padx=10, pady=6)

        text_label2 = ttk.Label(text='Password', width=29, bootstyle="dark")
        text_label2.pack(padx=10, pady=3)
        text_label2.configure(font=('Comfortaa', 10, 'bold'))

        self.login_pass_entry = ttk.Entry(width=35, bootstyle="dark", show='*')
        self.login_pass_entry.pack(padx=10, pady=6)

        login_button = ttk.Button(text='Login', width=10, command=self.login_verify)
        login_button.pack(padx=10, pady=17)
        login_button.configure(style='my.TButton')

        text_label3 = ttk.Label(text='Not a member?', bootstyle="dark")
        text_label3.pack(padx=10, pady=10)
        text_label3.configure(font=('Comfortaa', 10, 'bold'))

        register_button = ttk.Button(text='Register', width=10, bootstyle="success", command=self.register)
        register_button.pack(padx=10, pady=2)
        register_button.configure(style='my.TButton')

    def login_verify(self):
        self.login_mail = self.login_email_entry.get()
        login_pass = self.login_pass_entry.get()

        if not self.login_mail or not login_pass:
            messagebox.showerror('Error', 'Please fill in all fields: Email/Password.')
            return

        if not self.email_validate(self.login_mail):
            messagebox.showerror('Error', 'Incorrect Email Format!')
            return

        response = self.db.log_in(self.login_mail, login_pass)
        if response:
            messagebox.showinfo('Success', 'Login Successful!')
            self.home()
        else:
            messagebox.showerror('Error', 'Incorrect Email/Password!')
            self.login_email_entry.delete(0, tk.END)
            self.login_pass_entry.delete(0, tk.END)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.update_idletasks()

    def register(self):
        self.clear()
        space_label = ttk.Label(text='', width=29, bootstyle="dark")
        space_label.pack(padx=10, pady=15)

        text_label1 = ttk.Label(text='Name', width=29, bootstyle="dark")
        text_label1.pack(padx=10, pady=5)
        text_label1.configure(font=('Comfortaa', 10, 'bold'))

        self.reg_name_entry = ttk.Entry(width=35, bootstyle="dark")
        self.reg_name_entry.pack(padx=10, pady=6)

        text_label2 = ttk.Label(text='Email', width=29, bootstyle="dark")
        text_label2.pack(padx=10, pady=3)
        text_label2.configure(font=('Comfortaa', 10, 'bold'))

        self.reg_email_entry = ttk.Entry(width=35, bootstyle="dark")
        self.reg_email_entry.pack(padx=10, pady=6)

        text_label3 = ttk.Label(text='Password', width=29, bootstyle="dark")
        text_label3.pack(padx=10, pady=3)
        text_label3.configure(font=('Comfortaa', 10, 'bold'))

        self.reg_pass_entry = ttk.Entry(width=35, bootstyle="dark")
        self.reg_pass_entry.pack(padx=10, pady=6)

        text_label4 = ttk.Label(text='Address', width=29, bootstyle="dark")
        text_label4.pack(padx=10, pady=3)
        text_label4.configure(font=('Comfortaa', 10, 'bold'))

        self.reg_address_entry = ttk.Entry(width=35, bootstyle="dark")
        self.reg_address_entry.pack(padx=10, pady=6)

        register_button = ttk.Button(text='Register', width=10, command=self.register_verify)
        register_button.pack(padx=10, pady=17)
        register_button.configure(style='my.TButton')

        goback_button = ttk.Button(text='Go Back', width=10, bootstyle="success", command=self.login)
        goback_button.pack(padx=10, pady=2)
        goback_button.configure(style='my.TButton')

    def register_verify(self):
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_pass_entry.get().strip()
        address = self.reg_address_entry.get().strip()

        if not name or not email or not password or not address:
            messagebox.showerror('Error', 'Please fill in all fields: name, email, password, and address.')
            return

        if not self.name_validate(name):
            messagebox.showerror('Error', "Name cannot contain numbers or special characters.")
            return

        if not self.email_validate(email):
            messagebox.showerror('Error', 'Incorrect Email Format!')
            return

        if not self.pass_validate(password):
            messagebox.showerror('Error',
                                 "Password must be at least 6 characters long and include a combination of letters, numbers, and special characters.")
            return

        if not self.address_validate(address):
            messagebox.showerror('Error', "Address cannot contain numbers or special characters.")
            return

        response = self.db.regis_ter(name, email, password, address)
        if response:
            messagebox.showinfo('Success', 'Registration Successful!')
            self.login()
        else:
            messagebox.showerror('Error', 'Email already exists! Please Login...')
            self.clear_registration_entries()

    def clear_registration_entries(self):
        self.reg_name_entry.delete(0, tk.END)
        self.reg_email_entry.delete(0, tk.END)
        self.reg_pass_entry.delete(0, tk.END)
        self.reg_address_entry.delete(0, tk.END)

    def email_validate(self, email):
        return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

    def name_validate(self, name):
        return re.match(r'^[A-Za-z ]+$', name) is not None

    def pass_validate(self, password):
        if len(password) < 6:
            return False
        if (re.search(r'[A-Za-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[^A-Za-z0-9]', password)):
            return True
        return False

    def address_validate(self, address):
        return re.match(r'^[A-Za-z\s,.-]+$', address) is not None

    def home(self):
        self.clear()
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.update_idletasks()

        name = self.db.get_name(self.login_mail)
        text = 'Welcome {}'.format(str(name).title())

        text_label = ttk.Label(self.root, text='', width=29, bootstyle="dark")
        text_label.pack(padx=10, pady=10)

        heading = ttk.Label(self.root, text=text)
        heading.pack(pady=10, padx=10)
        heading.configure(font=('Trebuchet MS', 14, 'bold'))

        profile_button = ttk.Button(self.root, text='My Profile', width=16, bootstyle="success",
                                    command=self.show_profile)
        profile_button.pack(padx=7, pady=13)
        profile_button.configure(style='my.TButton')

        serv_button = ttk.Button(self.root, text='Services', width=16, bootstyle="success", command=self.services)
        serv_button.pack(padx=7, pady=13)
        serv_button.configure(style='my.TButton')

        analytics_button = ttk.Button(self.root, text='Analytics', width=16, bootstyle="success",
                                      command=self.show_analytics)
        analytics_button.pack(padx=7, pady=13)
        analytics_button.configure(style='my.TButton')

        fb_button = ttk.Button(self.root, text='FeedBack', width=16, bootstyle="success",
                               command=self.get_feedback)
        fb_button.pack(padx=7, pady=13)
        fb_button.configure(style='my.TButton')

        logout_button = ttk.Button(self.root, text='Logout', width=16, bootstyle="success",
                                   command=self.login)
        logout_button.pack(padx=7, pady=14)
        logout_button.configure(style='my.TButton')

        delete_button = ttk.Button(self.root, text='Delete Account', width=16, bootstyle="success",
                                   command=self.acc_delete_gui)
        delete_button.pack(padx=7, pady=13)
        delete_button.configure(style='my.TButton')

    def show_analytics(self):
        self.clear()
        title_label = ttk.Label(self.root, text='Analytics', width=29, bootstyle="default")
        title_label.pack(padx=10, pady=10)
        title_label.configure(font=('Trebuchet MS', 14, 'bold'))

        description_text = tk.Text(self.root, wrap=tk.WORD, height=6, width=50, font=('Trebuchet MS', 11))
        description_text.insert(tk.END,
                                "This graph visualizes the revenue distribution of various dishes in your menu.\n"
                                "You can view which dishes are generating the most revenue and analyze their contributions.\n"
                                "Use the 'Save Graph' button to save this visualization as a PNG file for your records.")
        description_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=False)
        description_text.config(state=tk.DISABLED)

        save_button = ttk.Button(self.root, text='Save Graph', width=16, bootstyle="success", command=self.save_graph)
        save_button.pack(padx=7, pady=13)
        save_button.configure(style='my.TButton')

        goback_button = ttk.Button(self.root, text='Go Back', width=16, bootstyle="success",command=self.home)
        goback_button.pack(padx=7, pady=13)
        goback_button.configure(style='my.TButton')

        self.root.update_idletasks()

    def save_graph(self):
        if self.plt.check_user_entries():
            result, file = self.plt.create_and_save_chart()
            if result == 1:
                messagebox.showinfo("Success", f'Graph saved in {file}')
                self.home()
            else:
                messagebox.showerror("Error", file)
        else:
            messagebox.showwarning("No Entries",
                                   "No entries found. Please make an order first to proceed.")
            self.home()

    def acc_delete_gui(self):
        self.clear()
        space_label = ttk.Label(text='', width=29, bootstyle="dark")
        space_label.pack(padx=10, pady=15)

        get_email_label = ttk.Label(text='Email', width=29, bootstyle="dark")
        get_email_label.pack(padx=10, pady=3)
        get_email_label.configure(font=('Comfortaa', 10, 'bold'))

        self.del_email_entry = ttk.Entry(width=35, bootstyle="dark")
        self.del_email_entry.pack(padx=10, pady=6)

        get_pass_label = ttk.Label(text='Password', width=29, bootstyle="dark")
        get_pass_label.pack(padx=10, pady=5)
        get_pass_label.configure(font=('Comfortaa', 10, 'bold'))

        self.del_pass_entry = ttk.Entry(width=35, bootstyle="dark")
        self.del_pass_entry.pack(padx=10, pady=6)

        delete_button = ttk.Button(text='Delete', width=10, bootstyle="success",
                                   command=self.acc_delete)
        delete_button.pack(padx=10, pady=5)
        delete_button.configure(style='my.TButton')

    def acc_delete(self):
        email = self.del_email_entry.get()
        password = self.del_pass_entry.get()

        if not email or not password:
            messagebox.showerror('Error', 'Please fill in all fields: email/password.')
            return

        if not self.email_validate(email):
            messagebox.showerror('Error', 'Incorrect Email Format!')
            return

        if messagebox.askyesno('Confirm Deletion', 'Are you sure to delete your account?'):
            response = self.db.delete_acc(email, password)
            if response:
                messagebox.showinfo('Success', 'Account Deleted Successfully!')
                self.login()
            else:
                messagebox.showerror('Error', 'Wrong Email/Password')
                self.del_email_entry.delete(0, tk.END)
                self.del_pass_entry.delete(0, tk.END)
        else:
            messagebox.showinfo('Cancelled', 'Account deletion cancelled.')
            self.home()

    def show_profile(self):
        self.clear()
        name, email, password, address_var = (
            self.db.get_name(self.login_mail),
            self.login_mail,
            self.db.get_pass(self.login_mail),
            self.db.get_address(self.login_mail)
        )

        style = ttk.Style()
        style.configure('TLabel', padding=10, anchor='w')
        bold_font = tkfont.Font(family='Trebuchet MS', size=11, weight='bold')
        details_bold_font = tkfont.Font(family='Trebuchet MS', size=16, weight='bold')
        regular_font = tkfont.Font(family='Comfortaa', size=10)

        for i in range(12):
            self.root.grid_rowconfigure(i, weight=0)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(11, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=1)

        details = ttk.Label(self.root, text='Details', font=details_bold_font)
        details.grid(row=0, column=0, columnspan=2, pady=10)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        get_name = ttk.Label(self.root, text='Name:', font=bold_font)
        get_name.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        name_label = ttk.Label(self.root, text=str(name).title(), font=regular_font)
        name_label.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=2, sticky='ew')

        get_mail = ttk.Label(self.root, text='Email Address:', font=bold_font)
        get_mail.grid(row=4, column=0, sticky='e', padx=5, pady=5)
        mail_label = ttk.Label(self.root, text=str(email), font=regular_font)
        mail_label.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=5, column=0, columnspan=2, sticky='ew')

        get_pass = ttk.Label(self.root, text='Password:', font=bold_font)
        get_pass.grid(row=6, column=0, sticky='e', padx=5, pady=5)
        pass_label = ttk.Label(self.root, text=str(password), font=regular_font)
        pass_label.grid(row=6, column=1, sticky='w', padx=5, pady=5)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky='ew', pady=(0, 10))

        get_address = ttk.Label(self.root, text='Address:', font=bold_font)
        get_address.grid(row=8, column=0, sticky='e', padx=5, pady=5)
        address_label = ttk.Label(self.root, text=str(address_var), font=regular_font)
        address_label.grid(row=8, column=1, sticky='w', padx=5, pady=5)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=9, column=0, columnspan=2, sticky='ew', pady=(0, 10))

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=10, column=0, columnspan=2, pady=18, sticky='n')

        update_name = ttk.Button(button_frame, text='Update Name', width=15, bootstyle="success")
        update_name.configure(style='my.TButton', command=self.update_name_gui)

        update_email = ttk.Button(button_frame, text='Update Email', width=15, bootstyle="success",
                                  command=self.update_email_gui)
        update_email.configure(style='my.TButton')

        update_pass = ttk.Button(button_frame, text='Update Password', width=15, bootstyle="success",
                                 command=self.update_pass_gui)
        update_pass.configure(style='my.TButton')

        update_add = ttk.Button(button_frame, text='Update Address', width=15, bootstyle="success",
                                command=self.update_address_gui)
        update_add.configure(style='my.TButton')

        back_button = ttk.Button(button_frame, text='Go Back', width=10,bootstyle="success",
                                 command=self.home)
        back_button.configure(style='my.TButton')

        update_name.grid(row=0, column=0, padx=5, pady=5)
        update_email.grid(row=0, column=1, padx=5, pady=5)
        update_pass.grid(row=1, column=0, padx=5, pady=5)
        update_add.grid(row=1, column=1, padx=5, pady=5)

        back_button_frame = ttk.Frame(button_frame)
        back_button_frame.grid(row=2, column=0, columnspan=2, pady=4, sticky='ew')

        back_button = ttk.Button(back_button_frame, text='Go Back',
                                 width=10, bootstyle="success", command=self.home)
        back_button.configure(style='my.TButton')
        back_button.pack(expand=True)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def update_email_gui(self):
        self.clear()
        existing_mail_label = ttk.Label(text='Enter Existing Email', width=29,
                                        bootstyle="dark")
        existing_mail_label.pack(padx=10, pady=5)
        existing_mail_label.configure(font=('Comfortaa', 10, 'bold'))

        self.existing_mail_entry = ttk.Entry(width=35, bootstyle="dark")
        self.existing_mail_entry.pack(padx=10, pady=6)

        new_mail_label = ttk.Label(text='Email', width=29, bootstyle="dark")
        new_mail_label.pack(padx=10, pady=3)
        new_mail_label.configure(font=('Comfortaa', 10, 'bold'))

        self.new_email_entry = ttk.Entry(width=35, bootstyle="dark")
        self.new_email_entry.pack(padx=10, pady=6)

        update_email = ttk.Button(text='Save Changes', width=16, bootstyle="success",
                                  command=self.update_email)
        update_email.pack(padx=7, pady=13)
        update_email.configure(style='my.TButton')

        back_button = ttk.Button(text='Go Back', width=16, bootstyle="success",
                                 command=self.show_profile)
        back_button.pack(padx=7, pady=13)
        back_button.configure(style='my.TButton')

    def update_email(self):
        existing_email = self.existing_mail_entry.get()
        new_email = self.new_email_entry.get()

        if self.email_validate(new_email):
            self.login_mail = new_email
            response = self.db.set_email(existing_email, new_email)
            if response:
                messagebox.showinfo('Success', 'Email Updated Successfully!')
                self.show_profile()
            else:
                messagebox.showerror('Error', 'Enter Correct Email')
                self.existing_mail_entry(0, tk.END)
                self.new_email_entry(0, tk.END)
        else:
            messagebox.showerror('Error', 'Incorrect Email Format!')

    def update_pass_gui(self):
        self.clear()
        ex_pass = ttk.Label(text='Enter Existing Password:', width=29, bootstyle="dark")
        ex_pass.pack(padx=10, pady=5)
        ex_pass.configure(font=('Comfortaa', 10, 'bold'))

        self.existing_pass = ttk.Entry(width=35, bootstyle="dark")
        self.existing_pass.pack(padx=10, pady=6)

        new_pass = ttk.Label(text='Enter New Password:', width=29, bootstyle="dark")
        new_pass.pack(padx=10, pady=5)
        new_pass.configure(font=('Comfortaa', 10, 'bold'))

        self.new_pass = ttk.Entry(width=35, bootstyle="dark")
        self.new_pass.pack(padx=10, pady=6)

        update_pass = ttk.Button(text='Save Changes', width=16, bootstyle="success", command=self.update_user_password)
        update_pass.pack(padx=7, pady=13)
        update_pass.configure(style='my.TButton')

        back_button = ttk.Button(text='Go Back', width=16, bootstyle="success", command=self.show_profile)
        back_button.pack(padx=7, pady=13)
        back_button.configure(style='my.TButton')

    def update_user_password(self):
        old_pass = self.existing_pass.get()
        new_pass = self.new_pass.get()
        match_pass = self.db.get_pass(self.login_mail)

        if old_pass == match_pass:
            response = self.db.set_password(new_pass, self.login_mail)
            if response:
                messagebox.showinfo('Success', 'Password Updated Successfully!')
                self.show_profile()
            else:
                messagebox.showerror('Error', 'Error Occurred Please Retry!')
                self.existing_pass(0, tk.END)
                self.new_pass(0, tk.END)

    def update_name_gui(self):
        self.clear()
        new_name = ttk.Label(text='Enter New Name:', width=29, bootstyle="dark")
        new_name.pack(padx=10, pady=5)
        new_name.configure(font=('Comfortaa', 10, 'bold'))

        self.new_name_entry = ttk.Entry(self.root, width=35, bootstyle="dark")
        self.new_name_entry.pack(padx=10, pady=6)

        update_name = ttk.Button(text='Save Changes', width=16, bootstyle="success", command=self.update_username)
        update_name.pack(padx=7, pady=13)
        update_name.configure(style='my.TButton')

        back_button = ttk.Button(text='Go Back', width=16, bootstyle="success", command=self.show_profile)
        back_button.pack(padx=7, pady=13)
        back_button.configure(style='my.TButton')

    def update_username(self):
        new_name = self.new_name_entry.get()
        response = self.db.set_name(new_name, self.login_mail)

        if response:
            messagebox.showinfo('Success', 'Name Updated Successfully!')
            self.show_profile()
        else:
            messagebox.showerror('Error', 'Error Occurred Please Retry!')
            self.new_name_entry.delete(0, tk.END)

    def update_address_gui(self):
        self.clear()
        new_address = ttk.Label(text='Enter New Address:', width=29, bootstyle="dark")
        new_address.pack(padx=10, pady=5)
        new_address.configure(font=('Comfortaa', 10, 'bold'))

        self.new_address_entry = ttk.Entry(self.root, width=35, bootstyle="dark")
        self.new_address_entry.pack(padx=10, pady=6)

        update_address = ttk.Button(text='Save Changes', width=16, bootstyle="success", command=self.update_address)
        update_address.pack(padx=7, pady=13)
        update_address.configure(style='my.TButton')

        back_button = ttk.Button(text='Go Back', width=16, bootstyle="success", command=self.show_profile)
        back_button.pack(padx=7, pady=13)
        back_button.configure(style='my.TButton')

    def update_address(self):
        new_address = self.new_address_entry.get()
        response = self.db.set_address(new_address, self.login_mail)

        if response:
            messagebox.showinfo('Success', 'Name Updated Successfully!')
            self.show_profile()
        else:
            messagebox.showerror('Error', 'Error Occurred Please Retry!')
            self.new_address_entry.delete(0, tk.END)

    def get_feedback(self):
        url = 'https://forms.office.com/r/63hqdWRjGb'
        webbrowser.open_new_tab(url)
        self.home()

    def services(self):
        self.clear()
        text_label = ttk.Label(text='', width=29, bootstyle="dark")
        text_label.pack(padx=10, pady=20)

        order_button = ttk.Button(text='Order Food', width=16, bootstyle="success", command=self.order_gui)
        order_button.pack(padx=8, pady=13)
        order_button.configure(style='my.TButton')

        send_parcel_button = ttk.Button(text='Send Parcel', width=16, bootstyle="success", command=self.send_parcel_gui)
        send_parcel_button.pack(padx=8, pady=13)
        send_parcel_button.configure(style='my.TButton')

        goback_button = ttk.Button(text='Go Back', width=16, bootstyle="success", command=self.home)
        goback_button.pack(padx=8, pady=13)
        goback_button.configure(style='my.TButton')

    def order_gui(self):
        self.clear()
        self.selected_items = {}
        self.quantity_labels = {}
        self.menu_buttons = {}
        menu = self.db.get_menu()

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        headers = [" ", "Items", "Price"]
        for col, text in enumerate(headers):
            header_label = ttk.Label(self.scrollable_frame, text=text, font=('Trebuchet MS', 12, 'bold'))
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky='ew')

        for idx, (dish, price) in enumerate(menu.items(), start=1):
            var = tk.IntVar()
            chk = ttk.Checkbutton(self.scrollable_frame, variable=var,
                                  command=lambda d=dish, v=var, p=price: self.update_selection(d, v, p))
            chk.grid(row=idx, column=0, padx=3, pady=4, sticky='ew')

            label = ttk.Label(self.scrollable_frame, text=dish)
            label.grid(row=idx, column=1, padx=3, pady=4, sticky='ew')

            price_label = ttk.Label(self.scrollable_frame, text=f"PKR {price}")
            price_label.grid(row=idx, column=2, padx=3, pady=4, sticky='ew')
            # Create and disable the minus button initially
            minus_btn = ttk.Button(self.scrollable_frame, text="-", state="disabled",
                                   command=lambda d=dish: self.update_quantity(d, -1))
            minus_btn.grid(row=idx, column=3, padx=3, pady=4, sticky='ew')

            # Create and disable the quantity label
            qty_label = ttk.Label(self.scrollable_frame, text="1")
            qty_label.grid(row=idx, column=4, padx=3, pady=4, sticky='ew')
            self.quantity_labels[dish] = qty_label

            # Create and disable the plus button initially
            plus_btn = ttk.Button(self.scrollable_frame, text="+", state="disabled",
                                  command=lambda d=dish: self.update_quantity(d, 1))
            plus_btn.grid(row=idx, column=5, padx=3, pady=4, sticky='ew')

            # Store buttons for enabling/disabling
            self.menu_buttons[dish] = {"minus": minus_btn, "plus": plus_btn}

        submit_btn = ttk.Button(self.scrollable_frame, text="Check Out", command=self.check_out)
        submit_btn.grid(row=idx + 1, column=0, columnspan=6, pady=10)

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_selection(self, dish, var, price):
        if var.get() == 1:
            self.selected_items[dish] = {'price': price, 'quantity': 1}
            self.menu_buttons[dish]["minus"].config(state="normal")
            self.menu_buttons[dish]["plus"].config(state="normal")
        else:
            if dish in self.selected_items:
                del self.selected_items[dish]
                self.menu_buttons[dish]["minus"].config(state="disabled")
                self.menu_buttons[dish]["plus"].config(state="disabled")

    def update_quantity(self, dish, delta):
        qty_label = self.quantity_labels[dish]
        current_qty = self.selected_items[dish]['quantity']
        new_qty = max(1, current_qty + delta)

        self.selected_items[dish]['quantity'] = new_qty
        qty_label.configure(text=str(new_qty))

        if new_qty < 1:
            del self.selected_items[dish]
            self.menu_buttons[dish]["minus"].config(state="disabled")
            self.menu_buttons[dish]["plus"].config(state="disabled")

    def check_out_total(self):
        total_bill = 0
        for dish, details in self.selected_items.items():
            quantity = details['quantity']
            price = details['price']
            total_price = quantity * price
            total_bill += total_price
        return total_bill

    def check_out(self):
        self.clear()
        user_name = self.db.get_name(self.login_mail)
        today_date = datetime.today().strftime('%d-%m-%Y')
        gst = self.check_out_total() * 0.15

        style = ttk.Style()
        style.configure('TLabel', padding=10, anchor='w')
        bold_font = tkfont.Font(family='Trebuchet MS', size=11, weight='bold')
        title_font = tkfont.Font(family='Trebuchet MS', size=13, weight='bold')
        regular_font = tkfont.Font(family='Comfortaa', size=10)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_columnconfigure(2, weight=1)
        container.grid_columnconfigure(3, weight=1)

        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(10, weight=1)

        title_label = ttk.Label(container, text='Receipt', font=title_font)
        title_label.grid(row=0, column=1, columnspan=2, pady=(25,3), sticky='n')

        v_separator_left = ttk.Separator(container, orient='vertical', style='secondary.Vertical.TSeparator')
        v_separator_left.grid(row=0, column=0, rowspan=11, sticky='ns', padx=10)

        v_separator_right = ttk.Separator(container, orient='vertical', style='secondary.Vertical.TSeparator')
        v_separator_right.grid(row=0, column=3, rowspan=11, sticky='ns', padx=10)

        def add_receipt_item(row, label, value):
            separator = ttk.Separator(container, orient='horizontal', style='secondary.Horizontal.TSeparator')
            separator.grid(row=row, column=1, columnspan=2, sticky='ew', pady=(0, 10))

            label_widget = ttk.Label(container, text=label, font=bold_font)
            label_widget.grid(row=row + 1, column=1, padx=5, pady=5, sticky='w')

            value_widget = ttk.Label(container, text=value, font=regular_font)
            value_widget.grid(row=row + 1, column=2, padx=5, pady=5, sticky='w')

        add_receipt_item(row=1, label='Name', value=str(user_name))
        add_receipt_item(row=3, label='Dated', value=today_date)
        add_receipt_item(row=5, label='Inc. GST (15%)', value=str(gst))
        add_receipt_item(row=7, label='Total', value=str(self.check_out_total() + gst))

        pay_button = ttk.Button(container, text='Pay', width=10, bootstyle="success", command=self.pay)
        pay_button.configure(style='my.TButton')
        pay_button.grid(row=10, column=1, columnspan=2, pady=18, sticky='n')

    def pay(self):
        messagebox.showinfo('Thank You For Purchase', 'Your order will be delivered to your address soon!')
        self.selected_items_to_db()
        self.home()

    def selected_items_to_db(self):
        with open('data_files/records.json', 'w') as f:
            json.dump(self.selected_items, f, indent=4)

    def send_parcel_gui(self):
        self.clear()
        parcel_detail = ttk.Label(text='Parcel Details', width=29, bootstyle="dark")
        parcel_detail.pack(padx=10, pady=(5,3))
        parcel_detail.configure(font=('Comfortaa', 10, 'bold'))

        self.parcel_detail_entry = ttk.Entry(width=35, bootstyle="dark")
        self.parcel_detail_entry.pack(padx=10, pady=(2,3))

        weight = ttk.Label(text='Parcel Weightage(kg)', width=29, bootstyle="dark")
        weight.pack(padx=10, pady=(3,3))
        weight.configure(font=('Comfortaa', 10, 'bold'))

        self.weight_entry = ttk.Entry(width=35, bootstyle="dark")
        self.weight_entry.pack(padx=10, pady=(2,3))

        location = ttk.Label(text='Deliver From', width=29, bootstyle="dark")
        location.pack(padx=10, pady=(3,3))
        location.configure(font=('Comfortaa', 10, 'bold'))

        self.location_entry = ttk.Entry(width=35, bootstyle="dark")
        self.location_entry.pack(padx=10, pady=(2,3))

        destination = ttk.Label(text='Deliver To', width=29, bootstyle="dark")
        destination.pack(padx=10, pady=(3,3))
        destination.configure(font=('Comfortaa', 10, 'bold'))

        self.destination_entry = ttk.Entry(width=35, bootstyle="dark")
        self.destination_entry.pack(padx=10, pady=(2,3))

        recipient = ttk.Label(text='Recipient Name', width=29, bootstyle="dark")
        recipient.pack(padx=10, pady=(3,3))
        recipient.configure(font=('Comfortaa', 10, 'bold'))

        self.recipient_entry = ttk.Entry(width=35, bootstyle="dark")
        self.recipient_entry.pack(padx=10, pady=(2,3))

        contact = ttk.Label(text='Recipient Contact', width=29, bootstyle="dark")
        contact.pack(padx=10, pady=(3,3))
        contact.configure(font=('Comfortaa', 10, 'bold'))

        self.contact_entry = ttk.Entry(width=35, bootstyle="dark")
        self.contact_entry.pack(padx=10, pady=(2,3))

        proceed = ttk.Button(text='Proceed', width=10, bootstyle="success", command=self.proceed)
        proceed.configure(style='my.TButton')
        proceed.pack(padx=10, pady=(7,2))

        goback_button = ttk.Button(text='Go Back', width=10, bootstyle="success", command=self.services)
        goback_button.configure(style='my.TButton')
        goback_button.pack(padx=10, pady=(4,3))


    def proceed(self):
        parcel_detail = self.parcel_detail_entry.get().strip()
        self.parcel_weight = self.weight_entry.get().strip()
        location = self.location_entry.get().strip()
        destination = self.destination_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        contact = self.contact_entry.get().strip()
        self.data_list = [parcel_detail, self.parcel_weight, location, destination, recipient, contact]

        if not parcel_detail or not self.parcel_weight or not location or not destination or not recipient or not contact:
            messagebox.showerror('Error', 'Please fill in all fields.')
            return

        if not self.text_validate(parcel_detail) or not self.text_validate(location) or not self.text_validate(
                destination) or not self.text_validate(recipient):
            messagebox.showerror('Error',
                                 'Parcel details, location, destination, and recipient name cannot contain numbers or special characters.')
            return

        if not self.weight_validate(self.parcel_weight):
            messagebox.showerror('Error', 'Weight must be a valid number/Greater than 1kg.')
            return

        if not self.contact_validate(contact):
            messagebox.showerror('Error', 'Contact must be a valid number and can start with +.')
            return

        self.clear()
        weight = float(self.parcel_weight)
        charges = 0
        if weight < 3.0:
            charges = weight * 100
        elif weight < 10:
            charges = weight * 200
        else:
            charges = weight * 350

        title_label = ttk.Label(self.root, text='Checkout', width=29, bootstyle="default")
        title_label.pack(padx=10, pady=10)
        title_label.configure(font=('Trebuchet MS', 12, 'bold'))

        text = tk.Text(self.root, wrap=tk.WORD, height=6, width=50, font=('Trebuchet MS', 11))
        text.insert(tk.END,
                    f"Dear User, your delivery charges are {charges} pkr inc tax. Our rider will "
                    f"approach you for pickup soon!")
        text.pack(padx=5, pady=5, fill=tk.BOTH, expand=False)
        text.config(state=tk.DISABLED)

        pay = ttk.Button(text='Pay', width=10, bootstyle="success", command=self.parcel_pay)
        pay.configure(style='my.TButton')
        pay.pack(padx=10, pady=6)

    def parcel_pay(self):
        messagebox.showinfo('Thank You For Choosing Us', 'Our rider will be there to deliver soon!')
        self.home()
        self.db.update_to_delivery_records(self.login_mail, self.data_list)

    def text_validate(self, text):
        return text.replace(" ", "").isalpha()

    def weight_validate(self, weight):
        try:
            1 <= float(weight)
            return True
        except ValueError:
            return False

    def contact_validate(self, contact):
        if contact.startswith("+"):
            contact = contact[1:]
        return contact.isdigit() and len(contact) >= 1


app = App()
