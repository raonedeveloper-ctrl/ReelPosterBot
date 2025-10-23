import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import json
import os

class ContentCalendar:
    """Visual content calendar for planning posts"""
    
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.calendar_file = "data/calendar_events.json"
        self.events = self.load_events()
    
    def load_events(self):
        """Load calendar events from file"""
        if os.path.exists(self.calendar_file):
            with open(self.calendar_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_events(self):
        """Save calendar events to file"""
        with open(self.calendar_file, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def show_calendar(self):
        """Display calendar window"""
        window = tk.Toplevel()
        window.title("📅 Content Calendar")
        window.geometry("900x700")
        
        # Header
        header = tk.Frame(window, bg="#E1306C", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📅 Content Calendar - Plan Your Posts",
            font=("Arial", 16, "bold"),
            bg="#E1306C",
            fg="white"
        ).pack(pady=15)
        
        # Main content
        content = tk.Frame(window)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Calendar widget
        cal_frame = tk.Frame(content)
        cal_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        cal = Calendar(
            cal_frame,
            selectmode='day',
            font=("Arial", 10),
            background='#E1306C',
            foreground='white',
            bordercolor='#E1306C',
            headersbackground='#C13584',
            normalbackground='white',
            weekendbackground='#F0F0F0',
            selectbackground='#4CAF50'
        )
        cal.pack(pady=10)
        
        # Event list
        event_frame = tk.LabelFrame(
            content,
            text="📋 Scheduled Posts",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        event_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Events listbox
        events_list = tk.Listbox(
            event_frame,
            font=("Arial", 10),
            height=20
        )
        events_list.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(event_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        events_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=events_list.yview)
        
        def update_event_list(date_str):
            """Update events for selected date"""
            events_list.delete(0, tk.END)
            
            if date_str in self.events:
                for event in self.events[date_str]:
                    events_list.insert(tk.END, f"⏰ {event['time']} - {event['title']}")
            else:
                events_list.insert(tk.END, "No posts scheduled for this day")
        
        def on_date_select(event):
            """Handle date selection"""
            selected = cal.get_date()
            date_str = datetime.strptime(selected, "%m/%d/%y").strftime("%Y-%m-%d")
            update_event_list(date_str)
            selected_date.set(date_str)
        
        cal.bind("<<CalendarSelected>>", on_date_select)
        
        # Selected date variable
        selected_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        
        # Add event section
        add_frame = tk.Frame(event_frame)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="⏰ Time:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        time_var = tk.StringVar(value="12:00")
        time_entry = tk.Entry(add_frame, textvariable=time_var, width=8)
        time_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(add_frame, text="📝 Title:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        title_var = tk.StringVar()
        title_entry = tk.Entry(add_frame, textvariable=title_var, width=20)
        title_entry.pack(side=tk.LEFT, padx=5)
        
        def add_event():
            """Add new event to calendar"""
            date_str = selected_date.get()
            time_str = time_var.get()
            title = title_var.get()
            
            if not title:
                return
            
            if date_str not in self.events:
                self.events[date_str] = []
            
            self.events[date_str].append({
                'time': time_str,
                'title': title,
                'status': 'pending'
            })
            
            self.save_events()
            update_event_list(date_str)
            title_var.set("")
        
        tk.Button(
            add_frame,
            text="➕ Add",
            command=add_event,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        def delete_event():
            """Delete selected event"""
            selection = events_list.curselection()
            if selection:
                date_str = selected_date.get()
                idx = selection[0]
                
                if date_str in self.events and idx < len(self.events[date_str]):
                    del self.events[date_str][idx]
                    
                    if not self.events[date_str]:
                        del self.events[date_str]
                    
                    self.save_events()
                    update_event_list(date_str)
        
        tk.Button(
            add_frame,
            text="🗑️ Delete",
            command=delete_event,
            bg="#f44336",
            fg="white",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Statistics
        stats_frame = tk.LabelFrame(
            window,
            text="📊 Calendar Statistics",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        total_events = sum(len(events) for events in self.events.values())
        upcoming = len([e for date in self.events for e in self.events[date] 
                       if datetime.strptime(date, "%Y-%m-%d") >= datetime.now()])
        
        tk.Label(
            stats_frame,
            text=f"Total Scheduled: {total_events} | Upcoming: {upcoming}",
            font=("Arial", 10)
        ).pack()
        
        # Initialize with today's events
        update_event_list(datetime.now().strftime("%Y-%m-%d"))

print("✅ Content Calendar Module loaded")
