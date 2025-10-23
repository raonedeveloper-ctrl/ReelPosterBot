import customtkinter as ctk

class UIAnimations:
    """Smooth animations for UI elements"""
    
    @staticmethod
    def button_hover_effect(button):
        """Add hover animation to button"""
        def on_enter(e):
            button.configure(cursor="hand2")
            # Scale up slightly
        
        def on_leave(e):
            button.configure(cursor="arrow")
            # Scale back
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    @staticmethod
    def fade_in(widget, duration=300):
        """Fade in animation"""
        widget.attributes('-alpha', 0.0)
        
        def animate(alpha=0.0):
            if alpha < 1.0:
                alpha += 0.1
                widget.attributes('-alpha', alpha)
                widget.after(duration//10, lambda: animate(alpha))
        
        animate()
    
    @staticmethod
    def slide_in(widget, direction='left'):
        """Slide in animation"""
        # Implementation for sliding effect
        pass

print("✅ UI Animations Module loaded")
