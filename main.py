import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from datetime import datetime
from instagram_manager import InstagramManager
from database_manager import DatabaseManager
from scheduler import AutoPoster
from video_queue_manager import VideoQueueManager
from advanced_analytics import AdvancedAnalytics
from config import VIDEO_FOLDER_PATH, APP_VERSION

class InstagramBotPro:
    """Professional Instagram Automation Dashboard"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"Instagram Auto Poster PRO v{APP_VERSION} 🚀")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Core managers
        self.insta_manager = InstagramManager()
        self.db = DatabaseManager()
        self.analytics = AdvancedAnalytics()
        self.queue_manager = VideoQueueManager()
        self.auto_poster = None
        self.current_folder = VIDEO_FOLDER_PATH
        
        # UI Setup
        self.setup_styles()
        self.create_menu()
        self.create_main_layout()
        
    def setup_styles(self):
        """Professional styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'primary': '#E1306C',
            'secondary': '#4CAF50',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#f44336',
            'info': '#2196F3',
            'dark': '#2c3e50',
            'light': '#ecf0f1'
        }
    
    def create_menu(self):
        """Professional menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Account Menu
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👤 Account", menu=account_menu)
        account_menu.add_command(label="Add New Account", command=self.add_account_dialog)
        account_menu.add_command(label="Login to Account", command=self.login_dialog)
        account_menu.add_separator()
        account_menu.add_command(label="View All Accounts", command=self.view_accounts)
        account_menu.add_command(label="Switch Account", command=self.login_dialog)
        account_menu.add_command(label="Delete Account", command=self.delete_account_dialog)
        
        # Folder Menu
        folder_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 Folder", menu=folder_menu)
        folder_menu.add_command(label="Select Video Folder", command=self.select_folder)
        folder_menu.add_command(label="View Current Folder", command=self.show_current_folder)
        folder_menu.add_command(label="Open Folder", command=self.open_folder)
        
        # Upload Menu
        upload_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📤 Upload", menu=upload_menu)
        upload_menu.add_command(label="Upload Single Video", command=self.upload_single_video)
        upload_menu.add_command(label="Upload All Videos", command=self.upload_all_videos)
        upload_menu.add_separator()
        upload_menu.add_command(label="Upload History", command=self.show_upload_history)
        
        # Queue Menu
        queue_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📦 Queue", menu=queue_menu)
        queue_menu.add_command(label="View Queue", command=self.show_queue_window)
        queue_menu.add_command(label="Add to Queue", command=self.add_to_queue)
        queue_menu.add_command(label="Manage Queue", command=self.show_queue_window)
        queue_menu.add_separator()
        queue_menu.add_command(label="Pause Queue", command=self.pause_queue)
        queue_menu.add_command(label="Resume Queue", command=self.resume_queue)
        queue_menu.add_command(label="Clear Queue", command=self.clear_queue)
        
        # Scheduler Menu
        scheduler_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⏰ Scheduler", menu=scheduler_menu)
        scheduler_menu.add_command(label="Start Auto-Posting", command=self.start_auto_posting)
        scheduler_menu.add_command(label="Stop Auto-Posting", command=self.stop_auto_posting)
        scheduler_menu.add_command(label="View Schedule", command=self.view_schedule)
        scheduler_menu.add_separator()
        scheduler_menu.add_command(label="AI Time Optimizer", command=self.show_time_optimizer)
        
        # Analytics Menu
        analytics_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📊 Analytics", menu=analytics_menu)
        analytics_menu.add_command(label="Performance Dashboard", command=self.show_dashboard)
        analytics_menu.add_command(label="Hashtag Performance", command=self.show_hashtag_analytics)
        analytics_menu.add_command(label="Caption A/B Testing", command=self.show_caption_analytics)
        analytics_menu.add_separator()
        analytics_menu.add_command(label="Shadow Ban Check", command=self.check_shadow_ban)
        analytics_menu.add_command(label="Account Growth", command=self.show_growth_chart)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Tools", menu=tools_menu)
        tools_menu.add_command(label="Reload Captions", command=self.reload_captions)
        tools_menu.add_command(label="Edit Captions File", command=self.edit_captions)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.show_settings)
        tools_menu.add_command(label="View Logs", command=self.show_logs)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_layout(self):
        """Professional multi-panel layout"""
        
        # ========== HEADER ==========
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=f"Instagram Auto Poster PRO v{APP_VERSION}",
            font=("Arial", 22, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Header buttons
        btn_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        btn_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(
            btn_frame,
            text="🚀 Start Auto-Post",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.start_auto_posting,
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="📊 Dashboard",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.show_dashboard,
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        # ========== MAIN CONTAINER ==========
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel (Status & Controls)
        left_panel = tk.Frame(main_container, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        self.create_status_panel(left_panel)
        self.create_controls_panel(left_panel)
        
        # Right Panel (Logs & Queue)
        right_panel = tk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_logs_panel(right_panel)
        self.create_quick_stats_panel(right_panel)
        
        # ========== STATUS BAR ==========
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Not logged in",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial log
        self.log("✅ Bot initialized successfully")
        self.log(f"📁 Default folder: {self.current_folder}")
        self.log("👉 Login to get started!")
    
    def create_status_panel(self, parent):
        """Status information panel"""
        status_frame = tk.LabelFrame(
            parent,
            text="📊 Current Status",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Account status
        self.account_status = tk.Label(
            status_frame,
            text="❌ Not Logged In",
            font=("Arial", 11, "bold"),
            fg="red"
        )
        self.account_status.pack(pady=5)
        
        # Folder status
        self.folder_status = tk.Label(
            status_frame,
            text=f"📁 Folder: {os.path.basename(self.current_folder)}",
            font=("Arial", 9)
        )
        self.folder_status.pack(pady=3)
        
        # Scheduler status
        self.scheduler_status = tk.Label(
            status_frame,
            text="⏰ Auto-Poster: OFF",
            font=("Arial", 9),
            fg="red"
        )
        self.scheduler_status.pack(pady=3)
        
        # Queue status
        self.queue_status = tk.Label(
            status_frame,
            text="📦 Queue: 0 videos",
            font=("Arial", 9)
        )
        self.queue_status.pack(pady=3)
        
        # Today's posts
        self.posts_today = tk.Label(
            status_frame,
            text="📤 Posts Today: 0/4",
            font=("Arial", 9)
        )
        self.posts_today.pack(pady=3)
    
    def create_controls_panel(self, parent):
        """Quick action controls"""
        controls_frame = tk.LabelFrame(
            parent,
            text="⚡ Quick Actions",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        controls_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons with icons - UPDATED WITH STOP BUTTON
        buttons = [
            ("🔑 Login", self.login_dialog, "#4CAF50"),
            ("📂 Select Folder", self.select_folder, "#2196F3"),
            ("📤 Upload Single", self.upload_single_video, "#FF9800"),
            ("📦 Upload All", self.upload_all_videos, "#E91E63"),
            ("🎬 Manage Queue", self.show_queue_window, "#9C27B0"),
            ("⏰ Start Auto-Post", self.start_auto_posting, "#4CAF50"),  # Green
            ("⏹️ Stop Auto-Post", self.stop_auto_posting, "#f44336"),   # Red - NEW!
            ("📊 Analytics", self.show_dashboard, "#00BCD4"),
            ("🔍 Shadow Ban", self.check_shadow_ban, "#FF5722"),
        ]
        
        for idx, (text, command, color) in enumerate(buttons):
            row = idx // 2
            col = idx % 2
            
            btn = tk.Button(
                controls_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                command=command,
                width=18,
                height=2
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

    
    def create_logs_panel(self, parent):
        """Activity logs panel"""
        logs_frame = tk.LabelFrame(
            parent,
            text="📜 Activity Log",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        logs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            height=20,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = tk.Frame(logs_frame)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(
            log_controls,
            text="Clear Logs",
            command=self.clear_logs,
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            log_controls,
            text="Export Logs",
            command=self.export_logs,
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=2)
    
    def create_quick_stats_panel(self, parent):
        """Quick statistics panel"""
        stats_frame = tk.LabelFrame(
            parent,
            text="📈 Quick Stats (Last 7 Days)",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        stats_frame.pack(fill=tk.X)
        
        # Stats grid
        stats_grid = tk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Stat boxes
        self.stat_boxes = {}
        stats = [
            ("Total Posts", "0", "📤"),
            ("Total Likes", "0", "❤️"),
            ("Avg Engagement", "0%", "📊"),
            ("Followers Growth", "0", "📈")
        ]
        
        for idx, (label, value, icon) in enumerate(stats):
            box = tk.Frame(stats_grid, relief=tk.RAISED, borderwidth=1)
            box.grid(row=idx//2, column=idx%2, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                box,
                text=icon,
                font=("Arial", 20)
            ).pack()
            
            value_label = tk.Label(
                box,
                text=value,
                font=("Arial", 14, "bold")
            )
            value_label.pack()
            
            tk.Label(
                box,
                text=label,
                font=("Arial", 8)
            ).pack()
            
            self.stat_boxes[label] = value_label
        
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        
        # Refresh button
        tk.Button(
            stats_frame,
            text="🔄 Refresh Stats",
            command=self.refresh_quick_stats,
            font=("Arial", 9)
        ).pack(pady=(10, 0))
    
    def log(self, message):
        """Add timestamped log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_msg)
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status_bar(self, message):
        """Update bottom status bar"""
        self.status_bar.config(text=message)
        self.root.update()

    # ==================== ACCOUNT MANAGEMENT ====================
    
    def add_account_dialog(self):
        """Add new Instagram account"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Account")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        
        tk.Label(
            dialog,
            text="Add Instagram Account",
            font=("Arial", 14, "bold")
        ).pack(pady=15)
        
        # Username
        tk.Label(dialog, text="Username:", font=("Arial", 11)).pack(pady=(10, 0))
        username_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        username_entry.pack(pady=5)
        
        # Password
        tk.Label(dialog, text="Password:", font=("Arial", 11)).pack(pady=(10, 0))
        password_entry = tk.Entry(dialog, font=("Arial", 11), width=30, show="●")
        password_entry.pack(pady=5)
        
        def save_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password!")
                return
            
            self.log(f"🔄 Adding account: @{username}...")
            self.update_status_bar(f"Logging in as @{username}...")
            
            success, message = self.insta_manager.login(username, password)
            
            if success:
                self.account_status.config(
                    text=f"✅ Logged in: @{username}",
                    fg="green"
                )
                self.log(f"✅ Account added successfully: @{username}")
                self.update_status_bar(f"Logged in as @{username}")
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_quick_stats()
            else:
                self.log(f"❌ Login failed: {message}")
                messagebox.showerror("Login Failed", message)
        
        tk.Button(
            dialog,
            text="Add & Login",
            font=("Arial", 12, "bold"),
            bg=self.colors['success'],
            fg="white",
            command=save_account,
            width=20,
            height=2
        ).pack(pady=20)
    
    def login_dialog(self):
        """Login to existing account"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("No Accounts", "No saved accounts found. Please add a new account.")
            self.add_account_dialog()
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Login to Account")
        dialog.geometry("350x200")
        
        tk.Label(
            dialog,
            text="Select Account",
            font=("Arial", 13, "bold")
        ).pack(pady=15)
        
        account_var = tk.StringVar()
        account_dropdown = ttk.Combobox(
            dialog,
            textvariable=account_var,
            values=[acc[0] for acc in accounts],
            state="readonly",
            font=("Arial", 11),
            width=25
        )
        account_dropdown.pack(pady=10)
        
        def do_login():
            username = account_var.get()
            if not username:
                messagebox.showerror("Error", "Please select an account!")
                return
            
            creds = self.db.get_account_credentials(username)
            if not creds:
                messagebox.showerror("Error", "Account credentials not found!")
                return
            
            password, session_file = creds
            
            self.log(f"🔄 Logging in as @{username}...")
            self.update_status_bar(f"Logging in...")
            
            success, message = self.insta_manager.login(username, password)
            
            if success:
                self.account_status.config(
                    text=f"✅ Logged in: @{username}",
                    fg="green"
                )
                self.log(f"✅ {message}")
                self.update_status_bar(f"Logged in as @{username}")
                dialog.destroy()
                self.refresh_quick_stats()
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Login Failed", message)
        
        tk.Button(
            dialog,
            text="Login",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg="white",
            command=do_login,
            width=15,
            height=2
        ).pack(pady=15)
    
    def view_accounts(self):
        """View all saved accounts"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("No Accounts", "No saved accounts found!")
            return
        
        account_list = "\n".join([f"• @{acc[0]}" for acc in accounts])
        messagebox.showinfo(
            "Saved Accounts",
            f"Total: {len(accounts)} account(s)\n\n{account_list}"
        )
    
    def delete_account_dialog(self):
        """Delete saved account"""
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            messagebox.showinfo("No Accounts", "No accounts to delete!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Account")
        dialog.geometry("350x180")
        
        tk.Label(
            dialog,
            text="Select Account to Delete",
            font=("Arial", 12, "bold")
        ).pack(pady=15)
        
        account_var = tk.StringVar()
        account_dropdown = ttk.Combobox(
            dialog,
            textvariable=account_var,
            values=[acc[0] for acc in accounts],
            state="readonly",
            font=("Arial", 11),
            width=25
        )
        account_dropdown.pack(pady=10)
        
        def do_delete():
            username = account_var.get()
            if not username:
                messagebox.showerror("Error", "Please select an account!")
                return
            
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete account @{username}?\n\nThis will remove saved credentials."
            )
            
            if confirm:
                self.db.delete_account(username)
                self.log(f"🗑️ Account deleted: @{username}")
                messagebox.showinfo("Success", "Account deleted successfully!")
                dialog.destroy()
        
        tk.Button(
            dialog,
            text="Delete",
            font=("Arial", 11, "bold"),
            bg=self.colors['danger'],
            fg="white",
            command=do_delete,
            width=15
        ).pack(pady=10)
    
    # ==================== FOLDER MANAGEMENT ====================
    
    def select_folder(self):
        """Select video folder"""
        folder = filedialog.askdirectory(title="Select Video Folder")
        
        if folder:
            self.current_folder = folder
            self.folder_status.config(text=f"📁 Folder: {os.path.basename(folder)}")
            self.log(f"📂 Folder selected: {folder}")
            self.update_status_bar(f"Folder: {folder}")
            
            # Auto-populate queue
            self.queue_manager.auto_populate_from_folder(folder)
            self.update_queue_status()
    
    def show_current_folder(self):
        """Show current folder info"""
        messagebox.showinfo(
            "Current Folder",
            f"Videos folder:\n\n{self.current_folder}"
        )
    
    def open_folder(self):
        """Open folder in file explorer"""
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                subprocess.Popen(f'explorer "{self.current_folder}"')
            elif os.name == 'posix':  # Mac/Linux
                subprocess.Popen(['open', self.current_folder])
        except Exception as e:
            self.log(f"❌ Could not open folder: {e}")
    
    # ==================== UPLOAD FUNCTIONS ====================
    
    def upload_single_video(self):
        """Upload single video"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Please login first!")
            return
        
        video_file = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi"),
                ("All files", "*.*")
            ]
        )
        
        if not video_file:
            return
        
        self.log(f"📤 Uploading: {os.path.basename(video_file)}")
        self.update_status_bar("Uploading video...")
        
        def upload_thread():
            success, message = self.insta_manager.upload_video(video_file)
            
            if success:
                self.log(f"✅ {message}")
                messagebox.showinfo("Success", message)
                self.refresh_quick_stats()
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Upload Failed", message)
            
            self.update_status_bar("Ready")
        
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def upload_all_videos(self):
        """Upload all videos from folder"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Please login first!")
            return
        
        if not os.path.isdir(self.current_folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Bulk Upload",
            f"Upload all videos from:\n{self.current_folder}\n\n"
            "Note: There will be 15-30 minute delays between posts for safety."
        )
        
        if not confirm:
            return
        
        self.log("🚀 Starting bulk upload...")
        
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
            messagebox.showinfo("Upload Complete", summary)
            self.refresh_quick_stats()
        
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def show_upload_history(self):
        """Show upload history"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        videos = self.db.get_uploaded_videos_list(self.insta_manager.current_username)
        
        if not videos:
            messagebox.showinfo("Upload History", "No uploads yet!")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Upload History")
        history_window.geometry("600x400")
        
        tk.Label(
            history_window,
            text="Recent Uploads",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Create listbox
        listbox = tk.Listbox(
            history_window,
            font=("Consolas", 9),
            height=20
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for video, date in videos:
            listbox.insert(tk.END, f"{date} - {video}")
    
    # ==================== QUEUE MANAGEMENT ====================
    
    def show_queue_window(self):
        """Show queue management window"""
        queue_window = tk.Toplevel(self.root)
        queue_window.title("Video Queue Manager")
        queue_window.geometry("700x500")
        
        tk.Label(
            queue_window,
            text="📦 Video Queue",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Queue status
        status = self.queue_manager.get_queue_status()
        status_text = f"Queued: {status['total_queued']} | History: {status['total_history']} | Status: {'⏸️ Paused' if status['is_paused'] else '▶️ Active'}"
        
        tk.Label(
            queue_window,
            text=status_text,
            font=("Arial", 10)
        ).pack(pady=5)
        
        # Queue list
        list_frame = tk.Frame(queue_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        queue_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set
        )
        queue_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=queue_listbox.yview)
        
        # Populate queue
        queued_videos = self.queue_manager.get_all_queued_videos()
        for video in queued_videos:
            queue_listbox.insert(
                tk.END,
                f"[P{video['priority']}] {video['filename']}"
            )
        
        # Control buttons
        btn_frame = tk.Frame(queue_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Add Video",
            command=self.add_to_queue
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Clear Queue",
            command=self.clear_queue
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="⏸️ Pause",
            command=self.pause_queue
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="▶️ Resume",
            command=self.resume_queue
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=lambda: self.refresh_queue_display(queue_listbox)
        ).pack(side=tk.LEFT, padx=5)
    
    def add_to_queue(self):
        """Add video to queue"""
        video_file = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video files", "*.mp4 *.mov *.avi"), ("All files", "*.*")]
        )
        
        if video_file:
            success, message = self.queue_manager.add_video_to_queue(video_file)
            if success:
                self.log(f"✅ Added to queue: {os.path.basename(video_file)}")
                self.update_queue_status()
            else:
                self.log(f"❌ {message}")
    
    def pause_queue(self):
        """Pause queue"""
        self.queue_manager.pause_queue()
        self.log("⏸️ Queue paused")
        self.update_queue_status()
    
    def resume_queue(self):
        """Resume queue"""
        self.queue_manager.resume_queue()
        self.log("▶️ Queue resumed")
        self.update_queue_status()
    
    def clear_queue(self):
        """Clear entire queue"""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Clear entire queue?\n\nThis cannot be undone."
        )
        
        if confirm:
            self.queue_manager.clear_queue()
            self.log("🗑️ Queue cleared")
            self.update_queue_status()
    
    def update_queue_status(self):
        """Update queue status display"""
        status = self.queue_manager.get_queue_status()
        self.queue_status.config(text=f"📦 Queue: {status['total_queued']} videos")
    
    def refresh_queue_display(self, listbox):
        """Refresh queue listbox"""
        listbox.delete(0, tk.END)
        queued_videos = self.queue_manager.get_all_queued_videos()
        for video in queued_videos:
            listbox.insert(tk.END, f"[P{video['priority']}] {video['filename']}")
    
    # ==================== SCHEDULER ====================
    
    def start_auto_posting(self):
        """Start automatic posting scheduler"""
        if not self.insta_manager.current_username:
            messagebox.showerror("Error", "Please login first!")
            return
        
        if self.auto_poster and self.auto_poster.is_running:
            messagebox.showinfo("Info", "Auto-poster is already running!")
            return
        
        creds = self.db.get_account_credentials(self.insta_manager.current_username)
        if not creds:
            messagebox.showerror("Error", "Account credentials not found!")
            return
        
        password, _ = creds
        
        self.log("🚀 Starting auto-posting scheduler...")
        self.update_status_bar("Starting scheduler...")
        
        def start_thread():
            self.auto_poster = AutoPoster(
                self.insta_manager.current_username,
                password
            )
            success, message = self.auto_poster.start_scheduler()
            
            if success:
                self.scheduler_status.config(
                    text="⏰ Auto-Poster: ON",
                    fg="green"
                )
                self.log("✅ Auto-posting activated!")
                self.log(f"📅 Schedule: {', '.join(self.auto_poster.posting_times)}")
                self.update_status_bar("Auto-posting active")
                messagebox.showinfo("Success", "Auto-posting started!")
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Error", message)
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_auto_posting(self):
        """Stop auto-posting"""
        if not self.auto_poster or not self.auto_poster.is_running:
            messagebox.showinfo("Info", "Auto-poster is not running!")
            return
        
        self.auto_poster.stop_scheduler()
        self.scheduler_status.config(
            text="⏰ Auto-Poster: OFF",
            fg="red"
        )
        self.log("⏹️ Auto-posting stopped!")
        self.update_status_bar("Auto-posting stopped")
        messagebox.showinfo("Success", "Auto-posting stopped!")
    
    def view_schedule(self):
        """View posting schedule"""
        if self.auto_poster and self.auto_poster.is_running:
            schedule_info = f"""
⏰ Automatic Posting Schedule

Daily posting times:
{chr(10).join(f'  • {time}' for time in self.auto_poster.posting_times)}

Features:
✅ AI-optimized posting times
✅ Random video selection
✅ Auto-caption generation
✅ Auto-delete after upload
✅ No duplicate uploads
✅ Analytics tracking

Status: 🟢 Active
Next post: {self.auto_poster.get_next_post_time() or 'Calculating...'}
            """
        else:
            schedule_info = """
⏰ Auto-Posting Schedule

Status: 🔴 Not Active

Click "Start Auto-Posting" to begin!
            """
        
        messagebox.showinfo("Posting Schedule", schedule_info)
    
    def show_time_optimizer(self):
        """Show AI time optimizer"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        best_times = self.analytics.predict_best_posting_times(
            self.insta_manager.current_username
        )
        
        times_info = f"""
🤖 AI Time Optimizer

Recommended posting times based on your engagement data:

{chr(10).join(f'  • {time}' for time in best_times)}

These times are optimized for maximum engagement!
        """
        
        messagebox.showinfo("AI Time Optimizer", times_info)
    
    # ==================== ANALYTICS FUNCTIONS ====================
    
    def show_dashboard(self):
        """Professional analytics dashboard"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        self.log("📊 Loading dashboard...")
        
        # Create dashboard window
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Performance Dashboard")
        dashboard.geometry("900x700")
        
        # Header
        header = tk.Frame(dashboard, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📊 Performance Dashboard - @{self.insta_manager.current_username}",
            font=("Arial", 16, "bold"),
            bg=self.colors['primary'],
            fg="white"
        ).pack(pady=15)
        
        # Get dashboard data
        try:
            data = self.insta_manager.get_performance_dashboard(days=7)
            
            if not data:
                messagebox.showerror("Error", "Could not load dashboard data!")
                dashboard.destroy()
                return
            
            # Scrollable content
            canvas = tk.Canvas(dashboard)
            scrollbar = tk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Overall Stats
            stats_frame = tk.LabelFrame(
                scrollable_frame,
                text="📈 Last 7 Days Overview",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=15
            )
            stats_frame.pack(fill=tk.X, padx=10, pady=10)
            
            stats_grid = tk.Frame(stats_frame)
            stats_grid.pack()
            
            stats = [
                ("Total Posts", data['total_posts'], "📤"),
                ("Total Likes", f"{data['total_likes']:,}", "❤️"),
                ("Total Comments", data['total_comments'], "💬"),
                ("Total Views", f"{data['total_views']:,}", "👁️"),
                ("Avg Engagement", f"{data['avg_engagement']}%", "📊"),
                ("Viral Score", f"{data['avg_viral_score']}/100", "🔥")
            ]
            
            for idx, (label, value, icon) in enumerate(stats):
                box = tk.Frame(stats_grid, relief=tk.RAISED, borderwidth=2, padx=15, pady=10)
                box.grid(row=idx//3, column=idx%3, padx=10, pady=10)
                
                tk.Label(box, text=icon, font=("Arial", 24)).pack()
                tk.Label(box, text=str(value), font=("Arial", 16, "bold")).pack()
                tk.Label(box, text=label, font=("Arial", 9)).pack()
            
            # Best Post
            best_frame = tk.LabelFrame(
                scrollable_frame,
                text="🏆 Best Performing Post",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=15
            )
            best_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(
                best_frame,
                text=f"📹 {data['best_post']['filename']}",
                font=("Arial", 11)
            ).pack(pady=5)
            
            tk.Label(
                best_frame,
                text=f"Engagement: {data['best_post']['engagement']}% | Viral Score: {data['best_post']['viral_score']}/100",
                font=("Arial", 10)
            ).pack()
            
            # Shadow Ban Check
            shadow_frame = tk.LabelFrame(
                scrollable_frame,
                text="🔍 Shadow Ban Status",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=15
            )
            shadow_frame.pack(fill=tk.X, padx=10, pady=10)
            
            shadow_data = data.get('shadow_ban', {})
            
            if shadow_data.get('is_shadow_banned'):
                status_color = "red"
                status_text = "⚠️ POSSIBLE SHADOW BAN DETECTED"
            else:
                status_color = "green"
                status_text = "✅ No Shadow Ban Detected"
            
            tk.Label(
                shadow_frame,
                text=status_text,
                font=("Arial", 12, "bold"),
                fg=status_color
            ).pack(pady=5)
            
            tk.Label(
                shadow_frame,
                text=f"Reach Change: {shadow_data.get('drop_percentage', 0)}%",
                font=("Arial", 10)
            ).pack()
            
            # Top Hashtags
            hashtag_frame = tk.LabelFrame(
                scrollable_frame,
                text="🏷️ Top Performing Hashtags",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=15
            )
            hashtag_frame.pack(fill=tk.X, padx=10, pady=10)
            
            top_hashtags = data.get('top_hashtags', [])
            
            if top_hashtags:
                for i, hashtag in enumerate(top_hashtags[:5], 1):
                    tk.Label(
                        hashtag_frame,
                        text=f"{i}. #{hashtag['hashtag']} (Score: {hashtag['score']}, Used: {hashtag['used']}x)",
                        font=("Arial", 10)
                    ).pack(anchor="w", pady=2)
            else:
                tk.Label(
                    hashtag_frame,
                    text="Not enough data yet. Keep posting!",
                    font=("Arial", 10),
                    fg="gray"
                ).pack()
            
            # Recommended Times
            times_frame = tk.LabelFrame(
                scrollable_frame,
                text="⏰ AI-Recommended Posting Times",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=15
            )
            times_frame.pack(fill=tk.X, padx=10, pady=10)
            
            recommended_times = data.get('recommended_times', [])
            times_text = ", ".join(recommended_times)
            
            tk.Label(
                times_frame,
                text=times_text,
                font=("Arial", 12, "bold"),
                fg=self.colors['info']
            ).pack(pady=5)
            
            tk.Label(
                times_frame,
                text="Based on your historical engagement data",
                font=("Arial", 9),
                fg="gray"
            ).pack()
            
            # Pack canvas
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.log("✅ Dashboard loaded successfully")
            
        except Exception as e:
            self.log(f"❌ Dashboard error: {e}")
            messagebox.showerror("Error", f"Could not load dashboard: {e}")
    
    def show_hashtag_analytics(self):
        """Hashtag performance analytics"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Hashtag Performance")
        window.geometry("700x500")
        
        tk.Label(
            window,
            text="🏷️ Hashtag Performance Analytics",
            font=("Arial", 14, "bold")
        ).pack(pady=15)
        
        # Get hashtag data
        best_hashtags = self.analytics.get_best_performing_hashtags(
            self.insta_manager.current_username,
            limit=20
        )
        
        if not best_hashtags:
            tk.Label(
                window,
                text="No hashtag data available yet.\nKeep posting to build analytics!",
                font=("Arial", 11),
                fg="gray"
            ).pack(pady=50)
            return
        
        # Create table
        columns = ("Rank", "Hashtag", "Score", "Times Used", "Avg Engagement")
        tree = ttk.Treeview(window, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        # Populate data
        for idx, hashtag in enumerate(best_hashtags, 1):
            tree.insert("", "end", values=(
                idx,
                f"#{hashtag['hashtag']}",
                round(hashtag['score'], 1),
                hashtag['used'],
                round(hashtag['avg_engagement'], 1)
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Export button
        tk.Button(
            window,
            text="📊 Export to CSV",
            command=lambda: self.export_hashtag_data(best_hashtags),
            font=("Arial", 10)
        ).pack(pady=10)
    
    def show_caption_analytics(self):
        """Caption A/B testing results"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Caption A/B Testing")
        window.geometry("800x500")
        
        tk.Label(
            window,
            text="📝 Caption Performance (A/B Testing)",
            font=("Arial", 14, "bold")
        ).pack(pady=15)
        
        # Get caption variants
        best_captions = self.analytics.get_best_caption_variants(limit=10)
        
        if not best_captions:
            tk.Label(
                window,
                text="No caption data available yet.\nA/B testing will start after a few posts!",
                font=("Arial", 11),
                fg="gray"
            ).pack(pady=50)
            return
        
        # Create list
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            frame,
            font=("Arial", 10),
            yscrollcommand=scrollbar.set
        )
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for idx, caption in enumerate(best_captions, 1):
            caption_text = caption[0][:60] + "..." if len(caption[0]) > 60 else caption[0]
            listbox.insert(
                tk.END,
                f"{idx}. {caption_text} | Engagement: {caption[1]:.1f}% | Used: {caption[2]}x"
            )
        
        tk.Label(
            window,
            text="💡 Top performing captions are used more frequently",
            font=("Arial", 9),
            fg="gray"
        ).pack(pady=10)
    
    def check_shadow_ban(self):
        """Run shadow ban detection"""
        if not self.insta_manager.current_username:
            messagebox.showinfo("Info", "Please login first!")
            return
        
        self.log("🔍 Running shadow ban check...")
        self.update_status_bar("Checking for shadow ban...")
        
        result = self.analytics.check_shadow_ban(self.insta_manager.current_username)
        
        if result['is_shadow_banned']:
            message = f"""
🚫 POSSIBLE SHADOW BAN DETECTED!

Reach Drop: {result['drop_percentage']:.1f}%

Last 7 days avg reach: {result['avg_reach_last_7']}
Previous 7 days avg reach: {result['avg_reach_previous_7']}

{result['suggestions']}
            """
            messagebox.showwarning("Shadow Ban Detected", message)
            self.log("⚠️ Shadow ban detected!")
        else:
            message = f"""
✅ NO SHADOW BAN DETECTED

Your account appears to be healthy!

Last 7 days avg reach: {result['avg_reach_last_7']}
Previous 7 days avg reach: {result['avg_reach_previous_7']}

Keep up the good work! 🎉
            """
            messagebox.showinfo("Shadow Ban Check", message)
            self.log("✅ No shadow ban detected")
        
        self.update_status_bar("Ready")
    
    def show_growth_chart(self):
        """Show account growth"""
        messagebox.showinfo(
            "Growth Chart",
            "📈 Account Growth\n\n"
            "Growth tracking is active!\n"
            "Data is being collected daily.\n\n"
            "Full chart visualization coming soon!"
        )
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def refresh_quick_stats(self):
        """Refresh quick stats panel"""
        if not self.insta_manager.current_username:
            return
        
        self.log("🔄 Refreshing stats...")
        
        try:
            data = self.analytics.get_dashboard_data(
                self.insta_manager.current_username,
                days=7
            )
            
            if data:
                self.stat_boxes["Total Posts"].config(text=str(data['total_posts']))
                self.stat_boxes["Total Likes"].config(text=f"{data['total_likes']:,}")
                self.stat_boxes["Avg Engagement"].config(text=f"{data['avg_engagement']}%")
                
                # Get follower count
                account_info = self.insta_manager.get_account_info()
                if account_info:
                    self.stat_boxes["Followers Growth"].config(
                        text=str(account_info['followers'])
                    )
            
            # Update posts today
            today_count = self.db.get_today_post_count(self.insta_manager.current_username)
            self.posts_today.config(text=f"📤 Posts Today: {today_count}/4")
            
            self.log("✅ Stats refreshed")
        except Exception as e:
            self.log(f"❌ Stats refresh error: {e}")
    
    def reload_captions(self):
        """Reload captions from file"""
        count = self.insta_manager.caption_gen.reload_captions()
        self.log(f"🔄 Captions reloaded: {count} captions found")
        messagebox.showinfo("Captions Reloaded", f"Loaded {count} captions from file")
    
    def edit_captions(self):
        """Open captions file for editing"""
        try:
            import subprocess
            caption_file = "captions.txt"
            
            if os.name == 'nt':  # Windows
                os.startfile(caption_file)
            elif os.name == 'posix':  # Mac/Linux
                subprocess.call(['open', caption_file])
            
            self.log(f"📝 Opened captions file for editing")
        except Exception as e:
            self.log(f"❌ Could not open captions file: {e}")
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def export_hashtag_data(self, hashtags):
        """Export hashtag data to CSV"""
        try:
            import csv
            filename = f"hashtag_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Rank', 'Hashtag', 'Score', 'Times Used', 'Avg Engagement'])
                
                for idx, h in enumerate(hashtags, 1):
                    writer.writerow([
                        idx,
                        f"#{h['hashtag']}",
                        round(h['score'], 2),
                        h['used'],
                        round(h['avg_engagement'], 2)
                    ])
            
            self.log(f"✅ Hashtag data exported: {filename}")
            messagebox.showinfo("Export Success", f"Data exported to:\n{filename}")
        except Exception as e:
            self.log(f"❌ Export error: {e}")
            messagebox.showerror("Export Failed", str(e))
    
    def clear_logs(self):
        """Clear log display"""
        self.log_text.delete(1.0, tk.END)
        self.log("🗑️ Logs cleared")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            filename = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            
            self.log(f"✅ Logs exported: {filename}")
            messagebox.showinfo("Export Success", f"Logs saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "⚙️ Settings\n\n"
            "Configuration is managed via config.py\n\n"
            "Key settings:\n"
            "• Max posts per day: 4\n"
            "• Delay between posts: 15-30 min\n"
            "• Auto-delete after upload: ON\n"
            "• Analytics tracking: ON\n"
            "• Story cross-posting: ON"
        )
    
    def show_logs(self):
        """Show logs window"""
        messagebox.showinfo(
            "Logs",
            "📜 Activity Logs\n\n"
            "Logs are displayed in the main window.\n\n"
            "Use 'Export Logs' to save to file."
        )
    
    def show_user_guide(self):
        """Show user guide"""
        guide_text = """
📖 USER GUIDE

GETTING STARTED:
1. Add your Instagram account (Account → Add New Account)
2. Login to your account
3. Select video folder (Folder → Select Video Folder)
4. Start auto-posting (Scheduler → Start Auto-Posting)

FEATURES:
• Auto-Posting: Schedule posts at optimal times
• Queue Management: Organize videos for posting
• Analytics Dashboard: Track performance metrics
• Shadow Ban Detection: Monitor account health
• Hashtag Optimizer: Use best performing hashtags
• Caption A/B Testing: Improve engagement

SAFETY:
• Max 4 posts per day
• 15-30 minute delays between posts
• Automatic duplicate detection
• Session management for security

TIPS:
• Use high-quality videos (1080p recommended)
• Keep videos under 30MB
• Add diverse captions to captions.txt
• Check analytics regularly
• Monitor shadow ban status weekly

For support, check the Help menu.
        """
        
        window = tk.Toplevel(self.root)
        window.title("User Guide")
        window.geometry("600x500")
        
        text = scrolledtext.ScrolledText(
            window,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(1.0, guide_text)
        text.config(state=tk.DISABLED)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        messagebox.showinfo(
            "Keyboard Shortcuts",
            "⌨️ Keyboard Shortcuts\n\n"
            "Ctrl+L - Login\n"
            "Ctrl+O - Open Folder\n"
            "Ctrl+U - Upload Single\n"
            "Ctrl+A - Upload All\n"
            "Ctrl+D - Dashboard\n"
            "Ctrl+Q - Quit\n\n"
            "More shortcuts coming soon!"
        )
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
Instagram Auto Poster PRO 🚀
Version {APP_VERSION}

Professional Instagram automation tool with advanced features.

Features:
✅ AI-powered scheduling
✅ Advanced analytics dashboard
✅ Hashtag performance tracking
✅ Caption A/B testing
✅ Shadow ban detection
✅ Queue management
✅ Story cross-posting
✅ Growth tracking

Developed with ❤️ using Python

Stay safe and grow your Instagram! 🎯
        """
        messagebox.showinfo("About", about_text)

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramBotPro(root)
    root.mainloop()
