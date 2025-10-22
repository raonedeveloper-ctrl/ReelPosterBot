import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from instagram_manager import InstagramManager
from database_manager import DatabaseManager
from scheduler import AutoPoster
from config import VIDEO_FOLDER_PATH, AUTO_POSTING_TIMES

class InstagramBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Auto Poster Bot 🤖")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        self.insta_manager = InstagramManager()
        self.db = DatabaseManager()
        self.auto_poster = None
        self.current_folder = VIDEO_FOLDER_PATH
        
        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        """Menu bar create karo"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Account Menu
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Add New Account", command=self.add_account_dialog)
        account_menu.add_command(label="Login to Account", command=self.login_dialog)
        account_menu.add_separator()
        account_menu.add_command(label="View All Accounts", command=self.view_accounts)
        account_menu.add_command(label="Delete Account", command=self.delete_account_dialog)
        
        # Folder Menu
        folder_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Folder", menu=folder_menu)
        folder_menu.add_command(label="Select Video Folder", command=self.select_folder)
        folder_menu.add_command(label="View Current Folder", command=self.show_current_folder)
        
        # Upload Menu
        upload_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Upload", menu=upload_menu)
        upload_menu.add_command(label="Upload Single Video", command=self.upload_single_video)
        upload_menu.add_command(label="Upload All Videos (Folder)", command=self.upload_all_videos)
        
        # Scheduler Menu (NEW)
        scheduler_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Auto-Scheduler", menu=scheduler_menu)
        scheduler_menu.add_command(label="Start Auto-Posting", command=self.start_auto_posting)
        scheduler_menu.add_command(label="Stop Auto-Posting", command=self.stop_auto_posting)
        scheduler_menu.add_command(label="View Schedule", command=self.view_schedule)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Main GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#E1306C", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="Instagram Auto Poster 🚀", 
            font=("Arial", 24, "bold"),
            bg="#E1306C",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Status Frame
        status_frame = tk.LabelFrame(self.root, text="Current Status", font=("Arial", 12, "bold"))
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = tk.Label(
            status_frame, 
            text="❌ Not Logged In", 
            font=("Arial", 11),
            fg="red"
        )
        self.status_label.pack(pady=5)
        
        self.folder_label = tk.Label(
            status_frame, 
            text=f"📁 Folder: {self.current_folder}", 
            font=("Arial", 10)
        )
        self.folder_label.pack(pady=5)
        
        self.scheduler_status = tk.Label(
            status_frame,
            text="⏰ Auto-Poster: OFF",
            font=("Arial", 10),
            fg="red"
        )
        self.scheduler_status.pack(pady=5)
        
        # Main Control Frame
        control_frame = tk.LabelFrame(self.root, text="Quick Actions", font=("Arial", 12, "bold"))
        control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="🔑 Login",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            command=self.login_dialog
        ).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="📂 Select Folder",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=15,
            height=2,
            command=self.select_folder
        ).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="⏰ Start Auto-Post",
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            width=15,
            height=2,
            command=self.start_auto_posting
        ).grid(row=0, column=2, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="📤 Upload Single",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=15,
            height=2,
            command=self.upload_single_video
        ).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="📦 Upload All",
            font=("Arial", 12, "bold"),
            bg="#E91E63",
            fg="white",
            width=15,
            height=2,
            command=self.upload_all_videos
        ).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="⏹️ Stop Auto-Post",
            font=("Arial", 12, "bold"),
            bg="#f44336",
            fg="white",
            width=15,
            height=2,
            command=self.stop_auto_posting
        ).grid(row=1, column=2, padx=10, pady=10)
        
        # Log Frame
        log_frame = tk.LabelFrame(self.root, text="Activity Log", font=("Arial", 12, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Consolas", 9),
            bg="#f5f5f5"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log("🤖 Bot ready! Pehle login karo.")
        self.log(f"⏰ Auto-post times: {', '.join(AUTO_POSTING_TIMES)}")
    
    def log(self, message):
        """Log messages display karo"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_auto_posting(self):
        """Auto-posting scheduler start karo"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Pehle login karo!")
            return
        
        if self.auto_poster and self.auto_poster.is_running:
            messagebox.showinfo("Info", "Auto-poster already running hai!")
            return
        
        # Get credentials
        creds = self.db.get_account_credentials(self.insta_manager.current_username)
        if not creds:
            messagebox.showerror("Error", "Account credentials nahi mile!")
            return
        
        password, _ = creds
        
        self.log("🚀 Starting auto-posting scheduler...")
        
        def start_thread():
            self.auto_poster = AutoPoster(self.insta_manager.current_username, password)
            success, message = self.auto_poster.start_scheduler()
            
            if success:
                self.scheduler_status.config(
                    text=f"⏰ Auto-Poster: ON (Times: {', '.join(AUTO_POSTING_TIMES)})",
                    fg="green"
                )
                self.log("✅ Auto-posting activated!")
                self.log(f"📅 Posting times: {', '.join(AUTO_POSTING_TIMES)}")
                messagebox.showinfo("Success", "Auto-posting started! Videos will post automatically.")
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Error", message)
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_auto_posting(self):
        """Auto-posting stop karo"""
        if not self.auto_poster or not self.auto_poster.is_running:
            messagebox.showinfo("Info", "Auto-poster running nahi hai!")
            return
        
        self.auto_poster.stop_scheduler()
        self.scheduler_status.config(text="⏰ Auto-Poster: OFF", fg="red")
        self.log("⏹️ Auto-posting stopped!")
        messagebox.showinfo("Success", "Auto-posting stopped!")
    
    def view_schedule(self):
        """Schedule timing dikhao"""
        schedule_info = f"""
⏰ Automatic Posting Schedule:

Daily posting times:
{chr(10).join(f'• {time}' for time in AUTO_POSTING_TIMES)}

How it works:
✅ Random video select hogi har scheduled time pe
✅ AI caption automatically generate hoga
✅ Video upload hone ke baad delete ho jayegi
✅ Duplicate videos nahi upload hongi

Current Status: {"🟢 Running" if self.auto_poster and self.auto_poster.is_running else "🔴 Stopped"}
        """
        messagebox.showinfo("Auto-Post Schedule", schedule_info)
    
    def add_account_dialog(self):
        """New account add karne ka dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Account")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Username:", font=("Arial", 11)).pack(pady=10)
        username_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        username_entry.pack()
        
        tk.Label(dialog, text="Password:", font=("Arial", 11)).pack(pady=10)
        password_entry = tk.Entry(dialog, font=("Arial", 11), width=30, show="*")
        password_entry.pack()
        
        def save_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Username aur password dalo!")
                return
            
            success, message = self.insta_manager.login(username, password)
            
            if success:
                self.status_label.config(text=f"✅ Logged in: @{username}", fg="green")
                self.log(f"✅ Account added: @{username}")
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            dialog,
            text="Add & Login",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=save_account
        ).pack(pady=20)
    
    def login_dialog(self):
        """Existing account se login"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("Info", "Pehle account add karo!")
            self.add_account_dialog()
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Login to Account")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Select Account:", font=("Arial", 11)).pack(pady=10)
        
        account_var = tk.StringVar()
        account_dropdown = ttk.Combobox(
            dialog,
            textvariable=account_var,
            values=[acc[0] for acc in accounts],
            state="readonly",
            font=("Arial", 11)
        )
        account_dropdown.pack(pady=10)
        
        def do_login():
            username = account_var.get()
            if not username:
                messagebox.showerror("Error", "Account select karo!")
                return
            
            creds = self.db.get_account_credentials(username)
            if not creds:
                messagebox.showerror("Error", "Account credentials nahi mile!")
                return
            
            password, session_file = creds
            
            self.log(f"🔄 Logging in as @{username}...")
            success, message = self.insta_manager.login(username, password)
            
            if success:
                self.status_label.config(text=f"✅ Logged in: @{username}", fg="green")
                self.log(f"✅ {message}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            dialog,
            text="Login",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=do_login
        ).pack(pady=10)
    
    def select_folder(self):
        """Video folder select karo"""
        folder = filedialog.askdirectory(title="Select Video Folder")
        
        if folder:
            self.current_folder = folder
            self.folder_label.config(text=f"📁 Folder: {folder}")
            self.log(f"📂 Folder selected: {folder}")
    
    def show_current_folder(self):
        """Current folder info dikhao"""
        messagebox.showinfo("Current Folder", f"Videos folder:\n{self.current_folder}")
    
    def upload_single_video(self):
        """Single video upload karo"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Pehle login karo!")
            return
        
        video_file = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video files", "*.mp4 *.mov *.avi"), ("All files", "*.*")]
        )
        
        if not video_file:
            return
        
        self.log(f"📤 Uploading: {os.path.basename(video_file)}")
        
        def upload_thread():
            success, message = self.insta_manager.upload_video(video_file)
            
            if success:
                self.log(message)
                messagebox.showinfo("Success", message)
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Error", message)
        
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def upload_all_videos(self):
        """Folder ke saare videos upload karo"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Pehle login karo!")
            return
        
        if not os.path.isdir(self.current_folder):
            messagebox.showerror("Error", "Invalid folder! Pehle folder select karo.")
            return
        
        confirm = messagebox.askyesno(
            "Confirm",
            f"Folder ke saare videos upload karenge?\nFolder: {self.current_folder}\n\nNote: Videos ke beech 15-30 min delay rahega (safety)"
        )
        
        if not confirm:
            return
        
        self.log("🚀 Bulk upload start...")
        
        def progress_callback(current, total, filename, success, message):
            if success is not None:
                status = "✅" if success else "❌"
                self.log(f"{status} ({current}/{total}) {filename}")
            else:
                self.log(f"⏳ {filename}")
        
        def upload_thread():
            success, summary = self.insta_manager.upload_folder_videos(
                self.current_folder,
                callback=progress_callback
            )
            
            self.log(summary)
            messagebox.showinfo("Complete", summary)
        
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def view_accounts(self):
        """Saare accounts ki list"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("Info", "Koi account nahi hai!")
            return
        
        account_list = "\n".join([f"• @{acc[0]}" for acc in accounts])
        messagebox.showinfo("Saved Accounts", f"Total: {len(accounts)} accounts\n\n{account_list}")
    
    def delete_account_dialog(self):
        """Account delete karo"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("Info", "Koi account nahi hai!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Account")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Select Account to Delete:", font=("Arial", 11)).pack(pady=10)
        
        account_var = tk.StringVar()
        account_dropdown = ttk.Combobox(
            dialog,
            textvariable=account_var,
            values=[acc[0] for acc in accounts],
            state="readonly",
            font=("Arial", 11)
        )
        account_dropdown.pack(pady=10)
        
        def do_delete():
            username = account_var.get()
            if not username:
                messagebox.showerror("Error", "Account select karo!")
                return
            
            confirm = messagebox.askyesno("Confirm", f"Delete @{username}?")
            if confirm:
                self.db.delete_account(username)
                self.log(f"🗑️ Account deleted: @{username}")
                messagebox.showinfo("Success", "Account deleted!")
                dialog.destroy()
        
        tk.Button(
            dialog,
            text="Delete",
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            command=do_delete
        ).pack(pady=10)
    
    def show_instructions(self):
        """Instructions dikhao"""
        instructions = f"""
        📖 How to Use:
        
        1. Account Menu → Add New Account
        2. Login karo apne Instagram account se
        3. Folder Menu → Select Video Folder
        4. Auto-Scheduler → Start Auto-Posting
        
        ⏰ Auto-Posting:
        • Daily posting times: {', '.join(AUTO_POSTING_TIMES)}
        • Random video select hogi
        • AI caption automatically generate hoga
        • Videos upload ke baad delete ho jayengi
        
        ⚠️ Safety Tips:
        • Max 4 posts per day (ban avoid)
        • 15-30 min delay between posts
        • Test account se pehle test karo
        
        📝 Supported formats: .mp4, .mov, .avi
        """
        messagebox.showinfo("Instructions", instructions)
    
    def show_about(self):
        """About info"""
        about_text = """
        Instagram Auto Poster Bot 🤖
        Version: 2.0 (Auto-Scheduler Edition)
        
        Made with ❤️ using Python
        
        Features:
        ✅ Automatic scheduled posting
        ✅ AI-powered captions (OpenAI)
        ✅ Multiple account support
        ✅ Auto-delete after upload
        ✅ Ban protection with delays
        ✅ Random video selection
        
        Stay safe! 🛡️
        """
        messagebox.showinfo("About", about_text)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramBotGUI(root)
    root.mainloop()
