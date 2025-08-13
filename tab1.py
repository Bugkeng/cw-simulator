#!/usr/bin/env python3
"""
Straight Key Tab - Tab 1 of Morse Code Simulator
Handles traditional straight key operation
"""

import tkinter as tk
import time

class StraightKeyTab:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
        # State variables
        self.is_transmitting = False
        self.key_down_time = None
        
        # Create the tab frame
        self.frame = tk.Frame(parent, bg='#2c3e50')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Key visualization frame
        key_frame = tk.Frame(self.frame, bg='#34495e', relief='raised', bd=3)
        key_frame.pack(pady=20, padx=20, fill='x')
        
        # Key status
        self.key_status = tk.Label(key_frame, text="KEY UP", font=('Courier', 16, 'bold'),
                                  fg='#e74c3c', bg='#34495e')
        self.key_status.pack(pady=10)
        
        # Visual key representation
        self.key_visual = tk.Canvas(key_frame, width=300, height=100, bg='#2c3e50', highlightthickness=0)
        self.key_visual.pack(pady=10)
        
        # Draw the key in up position
        self.draw_key(False)
        
        # Instructions for straight key
        instructions = tk.Label(self.frame, 
                               text="Press and hold 'A' key to operate the straight key\n" +
                                    "Short press = DOT (.) | Long press = DASH (-)\n" +
                                    "Timing automatically adjusts based on WPM setting",
                               font=('Courier', 10), fg='#95a5a6', bg='#2c3e50', justify='center')
        instructions.pack(pady=20)
        
        # Technique tips
        tips_frame = tk.Frame(self.frame, bg='#34495e', relief='raised', bd=2)
        tips_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(tips_frame, text="STRAIGHT KEY TECHNIQUE TIPS:", 
                font=('Courier', 10, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=5)
        
        tips_text = ("• Use your wrist, not your whole arm\n"
                    "• Keep contacts clean for best tone\n"
                    "• Practice consistent timing\n"
                    "• Relax - tension affects your sending")
        
        tk.Label(tips_frame, text=tips_text, font=('Courier', 9), 
                fg='#bdc3c7', bg='#34495e', justify='left').pack(pady=5)
    
    def draw_key(self, pressed):
        """Draw the straight key in up or down position"""
        self.key_visual.delete("all")
        
        # Base
        self.key_visual.create_rectangle(50, 80, 250, 90, fill='#7f8c8d', outline='#34495e', width=2)
        
        # Key lever
        if pressed:
            # Key down position
            self.key_visual.create_line(150, 80, 200, 40, fill='#e74c3c', width=8, capstyle='round')
            self.key_visual.create_oval(145, 75, 155, 85, fill='#c0392b', outline='#a93226', width=2)
            # Contact point
            self.key_visual.create_oval(195, 35, 205, 45, fill='#f1c40f', outline='#f39c12', width=2)
            # Spark effect
            self.key_visual.create_text(200, 40, text="⚡", font=('Arial', 12), fill='#f1c40f')
        else:
            # Key up position
            self.key_visual.create_line(150, 80, 180, 20, fill='#95a5a6', width=8, capstyle='round')
            self.key_visual.create_oval(145, 75, 155, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
            # Contact point
            self.key_visual.create_oval(175, 15, 185, 25, fill='#bdc3c7', outline='#95a5a6', width=2)
        
        # Knob
        self.key_visual.create_oval(195, 35, 215, 55, fill='#34495e', outline='#2c3e50', width=2)
        
        # Base details
        self.key_visual.create_rectangle(140, 85, 160, 90, fill='#5d6d7e', outline='#34495e', width=1)
    
    def key_down(self, event):
        """Handle straight key press"""
        if not self.is_transmitting:
            self.is_transmitting = True
            self.key_down_time = time.time()
            
            # Update UI
            self.key_status.config(text="KEY DOWN", fg='#2ecc71')
            self.draw_key(True)
            
            # Start playing tone
            self.main_app.audio_manager.start_tone()
    
    def key_up(self, event):
        """Handle straight key release"""
        if self.is_transmitting:
            self.is_transmitting = False
            key_duration = time.time() - self.key_down_time
            
            # Update UI
            self.key_status.config(text="KEY UP", fg='#e74c3c')
            self.draw_key(False)
            
            # Stop playing tone
            self.main_app.audio_manager.stop_tone()
            
            # Determine if it's a dot or dash based on WPM timing
            if key_duration < self.main_app.dash_threshold:
                self.main_app.add_morse_element('.')
            else:
                self.main_app.add_morse_element('-')
    
    def get_timing_info(self):
        """Get current timing information for display"""
        return (f"Dot: <{self.main_app.dash_threshold:.2f}s | "
                f"Dash: ≥{self.main_app.dash_threshold:.2f}s | "
                f"Letter gap: {self.main_app.letter_gap:.2f}s | "
                f"Word gap: {self.main_app.word_gap:.2f}s")