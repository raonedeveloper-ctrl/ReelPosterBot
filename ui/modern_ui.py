import customtkinter as ctk
from tkinter import PhotoImage
import tkinter as tk

class ModernUI:
    """Modern UI components with Instagram-style design"""
    
    # Instagram color palette
    COLORS = {
        'primary': '#E1306C',      # Instagram pink
        'secondary': '#C13584',    # Instagram purple
        'accent': '#833AB4',       # Dark purple
        'success': '#4CAF50',
        'warning': '#FF9800',
        'danger': '#f44336',
        'info': '#00BCD4',
        'bg_dark': '#1a1a1a',
        'bg_light': '#2d2d2d',
        'text_light': '#ffffff',
        'text_dark': '#cccccc',
        'border': '#404040'
    }
    
    @staticmethod
    def create_gradient_button(parent, text, command, icon="", width=200, height=50):
        """Create Instagram-style gradient button"""
        button = ctk.CTkButton(
            parent,
            text=f"{icon} {text}",
            command=command,
            width=width,
            height=height,
            font=("Arial", 13, "bold"),
            corner_radius=10,
            fg_color=(ModernUI.COLORS['primary'], ModernUI.COLORS['secondary']),
            hover_color=ModernUI.COLORS['accent'],
            border_width=0
        )
        return button
    
    @staticmethod
    def create_card(parent, title, value, icon, color):
        """Create modern stats card"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=ModernUI.COLORS['bg_light'],
            border_width=2,
            border_color=color
        )
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 40),
            text_color=color
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 24, "bold"),
            text_color=ModernUI.COLORS['text_light']
        )
        value_label.pack(pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11),
            text_color=ModernUI.COLORS['text_dark']
        )
        title_label.pack(pady=(5, 15))
        
        return card
    
    @staticmethod
    def create_header(parent, text, subtitle=""):
        """Create modern header with gradient"""
        header = ctk.CTkFrame(
            parent,
            height=80,
            corner_radius=0,
            fg_color=(ModernUI.COLORS['primary'], ModernUI.COLORS['accent'])
        )
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Main title
        title = ctk.CTkLabel(
            header,
            text=text,
            font=("Arial", 20, "bold"),
            text_color=ModernUI.COLORS['text_light']
        )
        title.pack(pady=(15, 0))
        
        # Subtitle
        if subtitle:
            sub = ctk.CTkLabel(
                header,
                text=subtitle,
                font=("Arial", 11),
                text_color=ModernUI.COLORS['text_dark']
            )
            sub.pack(pady=(5, 10))
        
        return header
    
    @staticmethod
    def create_status_badge(parent, text, status='active'):
        """Create status indicator badge"""
        colors = {
            'active': ModernUI.COLORS['success'],
            'inactive': ModernUI.COLORS['danger'],
            'pending': ModernUI.COLORS['warning']
        }
        
        badge = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=colors.get(status, ModernUI.COLORS['info']),
            height=30
        )
        
        label = ctk.CTkLabel(
            badge,
            text=text,
            font=("Arial", 10, "bold"),
            text_color="white"
        )
        label.pack(padx=15, pady=5)
        
        return badge

print("✅ Modern UI Module loaded")
