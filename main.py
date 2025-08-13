#!/usr/bin/env python3
"""
Morse Code Simulator - Main Application
Supports both Straight Key and Paddle Key operation
"""

import tkinter as tk
from tkinter import ttk
import pygame
import time
from tab1 import StraightKeyTab
from tab2 import PaddleKeyTab
from shared_controls import SharedControls
from audio_manager import AudioManager
from morse_decoder import MorseDecoder

class MorseCodeSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Simulator - Straight Key & Paddle")
        self.root.geometry("850x650")
        self.root.configure(bg='#2c3e50')
        
        # Initialize components
        self.audio_manager = AudioManager()
        self.morse_decoder = MorseDecoder()
        
        # Speed control (WPM - Words Per Minute)
        self.wpm = 20  # Default 20 WPM
        
        # Initialize shared_controls to None first
        self.shared_controls = None
        
        # Calculate initial timing values
        self.update_timing_from_wpm()
        
        # Timing variables
        self.last_release_time = time.time()
        
        # Setup UI
        self.setup_ui()
        self.bind_keys()
        
        # Start the morse decode timer
        self.check_morse_timer()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="MORSE CODE SIMULATOR", 
                              font=('Courier', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Create tab instances
        self.straight_key_tab = StraightKeyTab(self.notebook, self)
        self.paddle_key_tab = PaddleKeyTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.straight_key_tab.frame, text="Straight Key")
        self.notebook.add(self.paddle_key_tab.frame, text="Paddle Key")
        
        # Shared controls at bottom
        self.shared_controls = SharedControls(self.root, self)
    
    def update_timing_from_wpm(self):
        """Calculate timing values based on WPM setting"""
        # Standard: PARIS = 50 dot units, so 1 WPM = 50 dot units per minute
        # Dot duration in seconds = 60 / (WPM * 50)
        self.dot_duration = 60.0 / (self.wpm * 50)
        
        # Standard morse timing ratios
        self.dash_threshold = self.dot_duration * 2.5  # Dash = 3 dots, threshold at 2.5
        self.letter_gap = self.dot_duration * 3  # 3 dot units between letters
        self.word_gap = self.dot_duration * 7    # 7 dot units between words
        
        # Update timing info display if it exists
        if self.shared_controls and hasattr(self.shared_controls, 'timing_info'):
            self.shared_controls.update_timing_display()
    
    def update_speed(self, value):
        """Callback for speed slider changes"""
        self.wpm = int(value)
        self.update_timing_from_wpm()
        if hasattr(self.shared_controls, 'wpm_display'):
            self.shared_controls.update_wpm_display()
    
    def bind_keys(self):
        # Key bindings with tab-aware handling
        self.root.bind('<KeyPress-a>', self.handle_a_key_down)
        self.root.bind('<KeyRelease-a>', self.handle_a_key_up)
        self.root.bind('<KeyPress-A>', self.handle_a_key_down)
        self.root.bind('<KeyRelease-A>', self.handle_a_key_up)
        
        self.root.bind('<KeyPress-b>', self.handle_b_key_down)
        self.root.bind('<KeyRelease-b>', self.handle_b_key_up)
        self.root.bind('<KeyPress-B>', self.handle_b_key_down)
        self.root.bind('<KeyRelease-B>', self.handle_b_key_up)
        
        self.root.focus_set()  # Make sure window has focus for key events
    
    def handle_a_key_down(self, event):
        """Handle A key press - works as straight key or dit depending on active tab"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # Straight key tab
            self.straight_key_tab.key_down(event)
        else:  # Paddle key tab
            self.paddle_key_tab.dit_down(event)
    
    def handle_a_key_up(self, event):
        """Handle A key release - works as straight key or dit depending on active tab"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # Straight key tab
            self.straight_key_tab.key_up(event)
        else:  # Paddle key tab
            self.paddle_key_tab.dit_up(event)
    
    def handle_b_key_down(self, event):
        """Handle B key press - only works in paddle tab"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Paddle key tab only
            self.paddle_key_tab.dah_down(event)
    
    def handle_b_key_up(self, event):
        """Handle B key release - only works in paddle tab"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Paddle key tab only
            self.paddle_key_tab.dah_up(event)
    
    def add_morse_element(self, element):
        """Add a morse element (dot or dash) to the current sequence"""
        self.morse_decoder.add_element(element)
        self.shared_controls.update_morse_display()
        self.last_release_time = time.time()
    
    def check_morse_timer(self):
        """Check if enough time has passed to decode current morse sequence"""
        if (self.morse_decoder.has_sequence() and 
            not self.is_any_key_transmitting()):
            
            time_since_release = time.time() - self.last_release_time
            
            # If pause is long enough, decode the current sequence (letter gap)
            if time_since_release > self.letter_gap:
                decoded_letter = self.morse_decoder.decode_current_sequence()
                if decoded_letter:
                    self.shared_controls.add_decoded_text(decoded_letter)
                
                # If pause is very long, add a space (word gap)
                if time_since_release > self.word_gap:
                    self.shared_controls.add_decoded_text(" ")
        
        # Schedule next check
        self.root.after(50, self.check_morse_timer)
    
    def is_any_key_transmitting(self):
        """Check if any key is currently being transmitted"""
        return (self.straight_key_tab.is_transmitting or 
                self.paddle_key_tab.is_transmitting())
    
    def clear_text(self):
        """Clear all decoded text"""
        self.shared_controls.clear_text()
    
    def clear_morse(self):
        """Clear current morse sequence"""
        self.morse_decoder.clear_sequence()
        self.shared_controls.clear_morse_display()

def main():
    root = tk.Tk()
    app = MorseCodeSimulator(root)
    
    # Make sure the window can receive key events
    root.focus_force()
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()