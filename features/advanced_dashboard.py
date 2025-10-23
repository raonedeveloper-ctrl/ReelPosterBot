import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import numpy as np

class AdvancedDashboard:
    """Advanced analytics with charts and insights"""
    
    def __init__(self, analytics_manager):
        self.analytics = analytics_manager
    
    def show_dashboard(self, username):
        """Show advanced analytics dashboard"""
        window = tk.Toplevel()
        window.title("📊 Advanced Analytics")
        window.geometry("1200x800")
        
        # Header
        header = tk.Frame(window, bg="#E1306C", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📊 Advanced Analytics Dashboard - @{username}",
            font=("Arial", 18, "bold"),
            bg="#E1306C",
            fg="white"
        ).pack(pady=20)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Performance Overview
        overview_tab = tk.Frame(notebook)
        notebook.add(overview_tab, text="📈 Performance")
        self._create_performance_tab(overview_tab, username)
        
        # Tab 2: Engagement Analysis
        engagement_tab = tk.Frame(notebook)
        notebook.add(engagement_tab, text="💬 Engagement")
        self._create_engagement_tab(engagement_tab, username)
        
        # Tab 3: Growth Trends
        growth_tab = tk.Frame(notebook)
        notebook.add(growth_tab, text="📊 Growth")
        self._create_growth_tab(growth_tab, username)
        
        # Tab 4: Insights & Recommendations
        insights_tab = tk.Frame(notebook)
        notebook.add(insights_tab, text="💡 Insights")
        self._create_insights_tab(insights_tab, username)
    
    def _create_performance_tab(self, parent, username):
        """Create performance overview tab"""
        # Get data
        dashboard_data = self.analytics.get_dashboard_data(username, days=30)
        
        if not dashboard_data:
            tk.Label(
                parent,
                text="No data available yet. Start posting to see analytics!",
                font=("Arial", 14),
                fg="gray"
            ).pack(pady=100)
            return
        
        # Stats grid
        stats_frame = tk.Frame(parent)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stats = [
            ("Total Posts", dashboard_data.get('total_posts', 0), "📤", "#2196F3"),
            ("Total Likes", f"{dashboard_data.get('total_likes', 0):,}", "❤️", "#f44336"),
            ("Total Comments", dashboard_data.get('total_comments', 0), "💬", "#4CAF50"),
            ("Total Views", f"{dashboard_data.get('total_views', 0):,}", "👁️", "#FF9800"),
            ("Avg Engagement", f"{dashboard_data.get('avg_engagement', 0)}%", "📊", "#9C27B0"),
            ("Viral Score", f"{dashboard_data.get('avg_viral_score', 0)}/100", "🔥", "#E91E63")
        ]
        
        for idx, (label, value, icon, color) in enumerate(stats):
            card = tk.Frame(stats_frame, relief=tk.RAISED, borderwidth=2, bg=color)
            card.grid(row=idx//3, column=idx%3, padx=10, pady=10, sticky="ew")
            
            tk.Label(card, text=icon, font=("Arial", 30), bg=color, fg="white").pack(pady=5)
            tk.Label(card, text=str(value), font=("Arial", 18, "bold"), bg=color, fg="white").pack()
            tk.Label(card, text=label, font=("Arial", 10), bg=color, fg="white").pack(pady=5)
        
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Chart: Posts over time
        chart_frame = tk.LabelFrame(
            parent,
            text="📈 Performance Over Time",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self._create_performance_chart(chart_frame, username)
    
    def _create_performance_chart(self, parent, username):
        """Create performance line chart"""
        # Generate sample data (replace with real data)
        days = list(range(1, 31))
        posts = np.random.randint(0, 5, 30)
        likes = np.random.randint(100, 1000, 30)
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        
        # Posts chart
        ax1.plot(days, posts, marker='o', color='#2196F3', linewidth=2)
        ax1.set_title('Daily Posts', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Posts')
        ax1.grid(True, alpha=0.3)
        
        # Likes chart
        ax2.plot(days, likes, marker='o', color='#f44336', linewidth=2)
        ax2.set_title('Daily Likes', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Day')
        ax2.set_ylabel('Likes')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _create_engagement_tab(self, parent, username):
        """Create engagement analysis tab"""
        # Engagement heatmap by time
        tk.Label(
            parent,
            text="⏰ Best Times to Post (Heatmap)",
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sample data (replace with real data)
        hours = list(range(24))
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        data = np.random.randint(10, 100, (7, 24))
        
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(range(24))
        ax.set_xticklabels([f"{h}:00" for h in hours], rotation=45)
        ax.set_yticks(range(7))
        ax.set_yticklabels(days_of_week)
        
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Day of Week')
        ax.set_title('Engagement by Time (Higher = Better)', fontweight='bold')
        
        plt.colorbar(im, ax=ax, label='Engagement Score')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def _create_growth_tab(self, parent, username):
        """Create growth trends tab"""
        tk.Label(
            parent,
            text="📊 Follower Growth Trend",
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
        # Growth chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sample data (replace with real data)
        days = list(range(1, 31))
        followers = [1000 + i*10 + np.random.randint(-5, 15) for i in range(30)]
        
        ax.plot(days, followers, marker='o', color='#4CAF50', linewidth=2)
        ax.fill_between(days, followers, alpha=0.3, color='#4CAF50')
        
        ax.set_title('30-Day Follower Growth', fontsize=14, fontweight='bold')
        ax.set_xlabel('Day')
        ax.set_ylabel('Followers')
        ax.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(days, followers, 1)
        p = np.poly1d(z)
        ax.plot(days, p(days), "--", color='red', alpha=0.8, label='Trend')
        ax.legend()
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Growth stats
        stats_frame = tk.LabelFrame(
            parent,
            text="📈 Growth Statistics",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        growth_rate = ((followers[-1] - followers[0]) / followers[0]) * 100
        
        tk.Label(
            stats_frame,
            text=f"📊 30-Day Growth Rate: {growth_rate:.2f}%",
            font=("Arial", 11)
        ).pack(pady=5)
        
        tk.Label(
            stats_frame,
            text=f"👥 New Followers: +{followers[-1] - followers[0]}",
            font=("Arial", 11)
        ).pack(pady=5)
    
    def _create_insights_tab(self, parent, username):
        """Create insights and recommendations tab"""
        tk.Label(
            parent,
            text="💡 AI-Powered Insights & Recommendations",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Insights list
        insights_frame = tk.Frame(parent)
        insights_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        insights = [
            ("🔥", "Peak Performance", "Your posts between 6-9 PM get 45% more engagement"),
            ("📈", "Growth Opportunity", "Weekends show 30% higher reach - post more on Sat/Sun"),
            ("💬", "Engagement Tip", "Posts with questions get 2x more comments"),
            ("🏷️", "Hashtag Strategy", "#reels and #viral are your best performing tags"),
            ("⏰", "Consistency", "You post most actively on weekdays - try to balance"),
            ("🎯", "Content Type", "Videos 15-30s perform 60% better than longer ones"),
            ("👥", "Audience Insight", "Your audience is most active during lunch (12-2 PM)"),
            ("📊", "Recommendation", "Increase posting frequency to 2-3 posts/day for growth")
        ]
        
        for icon, title, description in insights:
            card = tk.Frame(insights_frame, relief=tk.RAISED, borderwidth=1)
            card.pack(fill=tk.X, pady=10)
            
            header = tk.Frame(card, bg="#E1306C")
            header.pack(fill=tk.X)
            
            tk.Label(
                header,
                text=f"{icon} {title}",
                font=("Arial", 12, "bold"),
                bg="#E1306C",
                fg="white"
            ).pack(anchor="w", padx=10, pady=5)
            
            tk.Label(
                card,
                text=description,
                font=("Arial", 10),
                wraplength=900,
                justify="left"
            ).pack(anchor="w", padx=20, pady=10)

print("✅ Advanced Dashboard Module loaded")
