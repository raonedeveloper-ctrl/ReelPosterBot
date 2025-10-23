import json
import os

class SettingsManager:
    """Manage bot settings and preferences"""
    
    def __init__(self):
        self.settings_file = "data/settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            'theme': 'dark',
            'auto_like_comments': True,
            'max_posts_per_day': 4,
            'delay_between_posts': [30, 60],
            'auto_post_to_story': True,
            'track_analytics': True,
            'shadow_ban_check_enabled': True,
            'notification_sound': True,
            'auto_backup': False,
            'backup_frequency_days': 7,
            'ai_caption_enabled': True,
            'competitor_tracking_enabled': True,
            'engagement_automation_enabled': False,
            'max_engagement_actions': 100
        }
        
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                loaded = json.load(f)
                default_settings.update(loaded)
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def show_settings_window(self, root):
        """Show settings GUI"""
        import tkinter as tk
        from tkinter import ttk
        
        window = tk.Toplevel(root)
        window.title("⚙️ Settings")
        window.geometry("600x700")
        
        # Header
        header = tk.Frame(window, bg="#E1306C", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⚙️ Bot Settings & Preferences",
            font=("Arial", 16, "bold"),
            bg="#E1306C",
            fg="white"
        ).pack(pady=15)
        
        # Content
        content = tk.Frame(window)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create settings sections
        sections = [
            ("🎨 Appearance", [
                ('theme', 'Theme', 'combobox', ['light', 'dark', 'blue', 'purple'])
            ]),
            ("📤 Posting", [
                ('max_posts_per_day', 'Max Posts Per Day', 'spinbox', (1, 10)),
                ('auto_post_to_story', 'Auto-Post to Story', 'checkbox', None),
                ('ai_caption_enabled', 'AI Caption Generation', 'checkbox', None)
            ]),
            ("📊 Analytics", [
                ('track_analytics', 'Track Analytics', 'checkbox', None),
                ('shadow_ban_check_enabled', 'Shadow Ban Check', 'checkbox', None)
            ]),
            ("🤖 Automation", [
                ('engagement_automation_enabled', 'Auto-Engagement', 'checkbox', None),
                ('max_engagement_actions', 'Max Actions/Day', 'spinbox', (10, 200)),
                ('competitor_tracking_enabled', 'Competitor Tracking', 'checkbox', None)
            ]),
            ("💾 Backup", [
                ('auto_backup', 'Auto Backup', 'checkbox', None),
                ('backup_frequency_days', 'Backup Every (days)', 'spinbox', (1, 30))
            ]),
            ("🔔 Notifications", [
                ('notification_sound', 'Sound Notifications', 'checkbox', None)
            ])
        ]
        
        for section_title, settings in sections:
            section = tk.LabelFrame(
                content,
                text=section_title,
                font=("Arial", 11, "bold"),
                padx=15,
                pady=10
            )
            section.pack(fill=tk.X, pady=10)
            
            for key, label, widget_type, options in settings:
                row = tk.Frame(section)
                row.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    row,
                    text=label,
                    font=("Arial", 10),
                    width=25,
                    anchor="w"
                ).pack(side=tk.LEFT)
                
                if widget_type == 'checkbox':
                    var = tk.BooleanVar(value=self.get(key))
                    cb = tk.Checkbutton(row, variable=var)
                    cb.pack(side=tk.LEFT)
                    cb.config(command=lambda k=key, v=var: self.set(k, v.get()))
                
                elif widget_type == 'spinbox':
                    var = tk.IntVar(value=self.get(key))
                    sb = tk.Spinbox(row, from_=options[0], to=options[1], textvariable=var, width=10)
                    sb.pack(side=tk.LEFT)
                    sb.config(command=lambda k=key, v=var: self.set(k, v.get()))
                
                elif widget_type == 'combobox':
                    var = tk.StringVar(value=self.get(key))
                    cb = ttk.Combobox(row, textvariable=var, values=options, state='readonly', width=15)
                    cb.pack(side=tk.LEFT)
                    cb.bind('<<ComboboxSelected>>', lambda e, k=key, v=var: self.set(k, v.get()))
        
        # Save button
        tk.Button(
            window,
            text="💾 Save & Close",
            command=window.destroy,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

print("✅ Settings Manager Module loaded")

