import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ModernTheme:
    """Modern UI theme with dark mode support"""
    
    THEMES = {
        'light': 'flatly',
        'dark': 'darkly',
        'blue': 'cosmo',
        'purple': 'superhero'
    }
    
    @staticmethod
    def apply_theme(root, theme='dark'):
        """Apply modern theme to window"""
        style = ttk.Style(theme=ModernTheme.THEMES.get(theme, 'darkly'))
        
        # Custom colors
        colors = {
            'primary': '#E1306C',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#f44336',
            'info': '#00BCD4',
            'bg': '#1a1a1a' if theme == 'dark' else '#ffffff',
            'fg': '#ffffff' if theme == 'dark' else '#000000'
        }
        
        # Configure styles
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Stats.TLabel', font=('Arial', 12))
        
        return style, colors

print("✅ Modern Theme Module loaded")
