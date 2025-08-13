#!/usr/bin/env python3
"""
Paddle Key Tab - Tab 2 of Morse Code Simulator
Handles iambic paddle key operation
"""

import tkinter as tk
import time

class PaddleKeyTab:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
        # State variables
        self.dit_pressed = False
        self.dah_pressed = False
        self.paddle_transmitting = False
        self.last_paddle_element = None
        self.current_element_start = None
        
        # Create the tab frame
        self.frame = tk.Frame(parent, bg='#2c3e50')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Paddle visualization frame
        paddle_frame = tk.Frame(self.frame, bg='#34495e', relief='raised', bd=3)
        paddle_frame.pack(pady=20, padx=20, fill='x')
        
        # Paddle status
        paddle_status_frame = tk.Frame(paddle_frame, bg='#34495e')
        paddle_status_frame.pack(pady=10)
        
        self.dit_status = tk.Label(paddle_status_frame, text="DIT (A)", font=('Courier', 14, 'bold'),
                                  fg='#95a5a6', bg='#34495e', width=10)
        self.dit_status.pack(side='left', padx=20)
        
        self.dah_status = tk.Label(paddle_status_frame, text="DAH (B)", font=('Courier', 14, 'bold'),
                                  fg='#95a5a6', bg='#34495e', width=10)
        self.dah_status.pack(side='right', padx=20)
        
        # Visual paddle representation
        self.paddle_visual = tk.Canvas(paddle_frame, width=400, height=120, bg='#2c3e50', highlightthickness=0)
        self.paddle_visual.pack(pady=10)
        
        # Draw the paddle in neutral position
        self.draw_paddle(False, False)
        
        # Current element display
        element_frame = tk.Frame(paddle_frame, bg='#34495e')
        element_frame.pack(pady=5)
        
        tk.Label(element_frame, text="SENDING:", font=('Courier', 10, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side='left')
        
        self.current_element = tk.Label(element_frame, text="", font=('Courier', 12, 'bold'),
                                       fg='#f39c12', bg='#34495e', width=5)
        self.current_element.pack(side='left', padx=10)
        
        # Instructions for paddle key
        instructions = tk.Label(self.frame, 
                               text="Press 'A' for DIT (dot) | Press 'B' for DAH (dash)\n" +
                                    "Hold keys for automatic repeat | Hold both for iambic keying\n" +
                                    "Elements are sent automatically at the set WPM speed",
                               font=('Courier', 10), fg='#95a5a6', bg='#2c3e50', justify='center')
        instructions.pack(pady=20)
        
        # Paddle technique tips
        tips_frame = tk.Frame(self.frame, bg='#34495e', relief='raised', bd=2)
        tips_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(tips_frame, text="PADDLE KEY TECHNIQUE TIPS:", 
                font=('Courier', 10, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=5)
        
        tips_text = ("• Use thumb and index finger for dit/dah\n"
                    "• Light touch - don't squeeze the paddles\n"
                    "• Let the keyer handle timing automatically\n"
                    "• Practice squeeze keying (both paddles) for efficiency")
        
        tk.Label(tips_frame, text=tips_text, font=('Courier', 9), 
                fg='#bdc3c7', bg='#34495e', justify='left').pack(pady=5)
    
    def draw_paddle(self, dit_pressed, dah_pressed):
        """Draw the paddle key showing current state"""
        self.paddle_visual.delete("all")
        
        # Base and center post
        self.paddle_visual.create_rectangle(150, 100, 250, 110, fill='#7f8c8d', outline='#34495e', width=2)
        self.paddle_visual.create_rectangle(195, 60, 205, 100, fill='#7f8c8d', outline='#34495e', width=2)
        
        # Dit paddle (left side)
        if dit_pressed:
            # Dit paddle pressed (touching center)
            self.paddle_visual.create_line(100, 80, 195, 80, fill='#e74c3c', width=6, capstyle='round')
            self.paddle_visual.create_oval(95, 75, 105, 85, fill='#c0392b', outline='#a93226', width=2)
            # Contact indicator
            self.paddle_visual.create_oval(190, 75, 200, 85, fill='#f1c40f', outline='#f39c12', width=2)
            # Spark effect
            self.paddle_visual.create_text(195, 80, text="⚡", font=('Arial', 10), fill='#f1c40f')
        else:
            # Dit paddle neutral
            self.paddle_visual.create_line(100, 80, 170, 80, fill='#95a5a6', width=6, capstyle='round')
            self.paddle_visual.create_oval(95, 75, 105, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        
        # Dah paddle (right side)
        if dah_pressed:
            # Dah paddle pressed (touching center)
            self.paddle_visual.create_line(300, 80, 205, 80, fill='#e74c3c', width=6, capstyle='round')
            self.paddle_visual.create_oval(295, 75, 305, 85, fill='#c0392b', outline='#a93226', width=2)
            # Contact indicator
            self.paddle_visual.create_oval(200, 75, 210, 85, fill='#f1c40f', outline='#f39c12', width=2)
            # Spark effect
            self.paddle_visual.create_text(205, 80, text="⚡", font=('Arial', 10), fill='#f1c40f')
        else:
            # Dah paddle neutral
            self.paddle_visual.create_line(300, 80, 230, 80, fill='#95a5a6', width=6, capstyle='round')
            self.paddle_visual.create_oval(295, 75, 305, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        
        # Labels with color coding
        self.paddle_visual.create_text(100, 50, text="DIT", font=('Courier', 10, 'bold'), 
                                      fill='#2ecc71' if dit_pressed else '#ecf0f1')
        self.paddle_visual.create_text(300, 50, text="DAH", font=('Courier', 10, 'bold'), 
                                      fill='#2ecc71' if dah_pressed else '#ecf0f1')
        
        # Center post details
        self.paddle_visual.create_oval(197, 85, 203, 95, fill='#5d6d7e', outline='#34495e', width=1)
    
    def dit_down(self, event):
        """Handle dit paddle press"""
        if not self.dit_pressed:
            self.dit_pressed = True
            self.dit_status.config(fg='#2ecc71')
            self.draw_paddle(True, self.dah_pressed)
            self.handle_paddle_logic()
    
    def dit_up(self, event):
        """Handle dit paddle release"""
        if self.dit_pressed:
            self.dit_pressed = False
            self.dit_status.config(fg='#95a5a6')
            self.draw_paddle(False, self.dah_pressed)
    
    def dah_down(self, event):
        """Handle dah paddle press"""
        if not self.dah_pressed:
            self.dah_pressed = True
            self.dah_status.config(fg='#2ecc71')
            self.draw_paddle(self.dit_pressed, True)
            self.handle_paddle_logic()
    
    def dah_up(self, event):
        """Handle dah paddle release"""
        if self.dah_pressed:
            self.dah_pressed = False
            self.dah_status.config(fg='#95a5a6')
            self.draw_paddle(self.dit_pressed, False)
    
    def handle_paddle_logic(self):
        """Handle paddle key logic - send appropriate element when pressed"""
        if not self.paddle_transmitting:
            if self.dit_pressed and not self.dah_pressed:
                self.send_paddle_element('.')
            elif self.dah_pressed and not self.dit_pressed:
                self.send_paddle_element('-')
            elif self.dit_pressed and self.dah_pressed:
                # Both pressed - alternate starting with dit if no previous element
                if self.last_paddle_element is None or self.last_paddle_element == '-':
                    self.send_paddle_element('.')
                else:
                    self.send_paddle_element('-')
    
    def send_paddle_element(self, element):
        """Send a dit or dah with proper timing"""
        if self.paddle_transmitting:
            return
            
        self.paddle_transmitting = True
        self.last_paddle_element = element
        self.current_element_start = time.time()
        
        # Update current element display
        self.current_element.config(text=element)
        
        # Add element to morse sequence
        self.main_app.add_morse_element(element)
        
        # Play tone for the appropriate duration
        self.main_app.audio_manager.start_tone()
        
        # Calculate element duration
        if element == '.':
            duration = self.main_app.dot_duration
        else:  # dash
            duration = self.main_app.dot_duration * 3
        
        # Schedule tone stop and check for next element
        self.main_app.root.after(int(duration * 1000), self.stop_paddle_element)
    
    def stop_paddle_element(self):
        """Stop current paddle element and check for next"""
        self.main_app.audio_manager.stop_tone()
        self.current_element.config(text="")
        
        # Inter-element gap
        self.main_app.root.after(int(self.main_app.dot_duration * 1000), self.check_paddle_continue)
    
    def check_paddle_continue(self):
        """Check if paddle should continue sending elements"""
        self.paddle_transmitting = False
        
        # Check if keys are still pressed and send appropriate element
        if self.dit_pressed and self.dah_pressed:
            # Alternate elements when both are pressed (iambic keying)
            if self.last_paddle_element == '.':
                self.send_paddle_element('-')
            else:
                self.send_paddle_element('.')
        elif self.dit_pressed:
            self.send_paddle_element('.')
        elif self.dah_pressed:
            self.send_paddle_element('-')
        else:
            # No keys pressed, reset timing for letter/word spacing
            self.main_app.last_release_time = time.time()
    
    def is_transmitting(self):
        """Check if paddle is currently transmitting"""
        return self.paddle_transmitting
    
    def get_status_info(self):
        """Get current paddle status for display"""
        status = []
        if self.dit_pressed:
            status.append("DIT")
        if self.dah_pressed:
            status.append("DAH")
        if self.paddle_transmitting:
            status.append(f"TX:{self.last_paddle_element}")
        return " | ".join(status) if status else "READY"