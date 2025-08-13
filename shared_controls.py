#!/usr/bin/env python3
"""
Shared Controls Module - Common UI elements for Morse Code Simulator
Handles morse display, text output, speed control, and control buttons
"""

import tkinter as tk
from tkinter import ttk

class SharedControls:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.decoded_text = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Shared controls frame at bottom
        self.shared_frame = tk.Frame(self.parent, bg='#2c3e50')
        self.shared_frame.pack(fill='x', padx=20, pady=10)
        
        # Morse display frame
        self.setup_morse_display()
        
        # Speed control frame
        self.setup_speed_control()
        
        # Control buttons
        self.setup_control_buttons()
    
    def setup_morse_display(self):
        """Setup the morse code sequence and decoded text display"""
        morse_frame = tk.Frame(self.shared_frame, bg='#34495e', relief='raised', bd=3)
        morse_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(morse_frame, text="CURRENT MORSE SEQUENCE:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=(10,5))
        
        self.morse_display = tk.Label(morse_frame, text="", font=('Courier', 20, 'bold'),
                                     fg='#f39c12', bg='#2c3e50', height=1, relief='sunken', bd=2)
        self.morse_display.pack(pady=5, padx=10, fill='x')
        
        tk.Label(morse_frame, text="DECODED TEXT:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=(20,5))
        
        # Text display with scrollbar
        text_frame = tk.Frame(morse_frame, bg='#34495e')
        text_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.text_display = tk.Text(text_frame, font=('Courier', 14), height=4,
                                   bg='#2c3e50', fg='#2ecc71', insertbackground='#2ecc71',
                                   relief='sunken', bd=2, wrap='word')
        self.text_display.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for text display
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.text_display.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_display.config(yscrollcommand=scrollbar.set)
    
    def setup_speed_control(self):
        """Setup the WPM speed control section"""
        speed_frame = tk.Frame(self.shared_frame, bg='#34495e', relief='raised', bd=2)
        speed_frame.pack(pady=10, padx=20, fill='x')
        
        # Speed label and value display
        speed_label_frame = tk.Frame(speed_frame, bg='#34495e')
        speed_label_frame.pack(pady=10)
        
        tk.Label(speed_label_frame, text="SPEED CONTROL:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side='left')
        
        self.wpm_display = tk.Label(speed_label_frame, text=f"{self.main_app.wpm} WPM", 
                                   font=('Courier', 12, 'bold'), fg='#3498db', bg='#34495e')
        self.wpm_display.pack(side='right')
        
        # Speed slider
        self.speed_slider = tk.Scale(speed_frame, from_=5, to=60, orient='horizontal',
                                    font=('Courier', 10), fg='#ecf0f1', bg='#34495e',
                                    activebackground='#3498db', troughcolor='#2c3e50',
                                    highlightthickness=0, command=self.main_app.update_speed)
        self.speed_slider.set(self.main_app.wpm)
        self.speed_slider.pack(pady=5, padx=20, fill='x')
        
        # Timing info display
        self.timing_info = tk.Label(speed_frame, text=self.get_timing_info_text(),
                                   font=('Courier', 8), fg='#95a5a6', bg='#34495e', justify='center')
        self.timing_info.pack(pady=5)
        
        # Status info (shows which tab is active and current state)
        self.status_info = tk.Label(speed_frame, text="Ready", font=('Courier', 9),
                                   fg='#bdc3c7', bg='#34495e')
        self.status_info.pack(pady=2)
    
    def setup_control_buttons(self):
        """Setup the control buttons section"""
        button_frame = tk.Frame(self.shared_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # Main control buttons
        tk.Button(button_frame, text="Clear Text", command=self.main_app.clear_text,
                 font=('Courier', 10), bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear Morse", command=self.main_app.clear_morse,
                 font=('Courier', 10), bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Copy Text", command=self.copy_text,
                 font=('Courier', 10), bg='#3498db', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Save Text", command=self.save_text,
                 font=('Courier', 10), bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
        
        # Audio controls
        audio_frame = tk.Frame(self.shared_frame, bg='#2c3e50')
        audio_frame.pack(pady=5)
        
        tk.Button(audio_frame, text="Test Audio", command=self.test_audio,
                 font=('Courier', 9), bg='#9b59b6', fg='white', padx=15).pack(side='left', padx=3)
        
        tk.Button(audio_frame, text="Audio Info", command=self.show_audio_info,
                 font=('Courier', 9), bg='#34495e', fg='white', padx=15).pack(side='left', padx=3)
        
        # Volume control
        volume_frame = tk.Frame(audio_frame, bg='#2c3e50')
        volume_frame.pack(side='left', padx=10)
        
        tk.Label(volume_frame, text="Vol:", font=('Courier', 8), 
                fg='#bdc3c7', bg='#2c3e50').pack(side='left')
        
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient='horizontal',
                                   font=('Courier', 8), fg='#ecf0f1', bg='#2c3e50',
                                   activebackground='#9b59b6', troughcolor='#34495e',
                                   highlightthickness=0, length=80, command=self.update_volume)
        self.volume_scale.set(30)  # Default 30% volume
        self.volume_scale.pack(side='left')
    
    def get_timing_info_text(self):
        """Generate timing information text"""
        return (f"Dot: <{self.main_app.dash_threshold:.2f}s | Dash: ≥{self.main_app.dash_threshold:.2f}s | "
                f"Letter gap: {self.main_app.letter_gap:.2f}s | Word gap: {self.main_app.word_gap:.2f}s")
    
    def update_timing_display(self):
        """Update the timing information display"""
        if hasattr(self, 'timing_info'):
            self.timing_info.config(text=self.get_timing_info_text())
    
    def update_wpm_display(self):
        """Update the WPM display"""
        if hasattr(self, 'wpm_display'):
            self.wpm_display.config(text=f"{self.main_app.wpm} WPM")
    
    def update_morse_display(self):
        """Update the morse sequence display"""
        current_sequence = self.main_app.morse_decoder.get_current_sequence()
        self.morse_display.config(text=current_sequence)
    
    def clear_morse_display(self):
        """Clear the morse sequence display"""
        self.morse_display.config(text="")
    
    def add_decoded_text(self, text):
        """Add decoded text to the display"""
        self.decoded_text += text
        self.update_text_display()
    
    def update_text_display(self):
        """Update the text display with decoded text"""
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.decoded_text)
        self.text_display.see(tk.END)
    
    def clear_text(self):
        """Clear all decoded text"""
        self.decoded_text = ""
        self.text_display.delete(1.0, tk.END)
    
    def copy_text(self):
        """Copy decoded text to clipboard"""
        if self.decoded_text:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(self.decoded_text)
            self.update_status("Text copied to clipboard")
    
    def save_text(self):
        """Save decoded text to file"""
        if self.decoded_text:
            try:
                from tkinter import filedialog
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Save Morse Code Text"
                )
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(self.decoded_text)
                    self.update_status(f"Text saved to {filename}")
            except Exception as e:
                self.update_status(f"Error saving file: {str(e)}")
    
    def update_status(self, message):
        """Update the status information"""
        if hasattr(self, 'status_info'):
            self.status_info.config(text=message)
            # Clear status after 3 seconds
            self.parent.after(3000, lambda: self.status_info.config(text="Ready"))
    
    def test_audio(self):
        """Test audio system"""
        success = self.main_app.audio_manager.test_audio()
        if success:
            self.update_status("Audio test successful!")
        else:
            self.update_status("Audio test failed - check audio info")
    
    def show_audio_info(self):
        """Show detailed audio information in a popup"""
        try:
            import tkinter.messagebox as msgbox
            
            self.main_app.audio_manager.print_audio_status()  # Print to console
            info = self.main_app.audio_manager.get_audio_info()
            
            # Create info message
            if info['available']:
                message = f"""Audio System: WORKING ✓
                
Tone Frequency: {info['frequency']} Hz
Sample Rate: {info.get('mixer_frequency', 'unknown')} Hz
Format: {info.get('mixer_format', 'unknown')}
Channels: {info.get('mixer_channels', 'unknown')}
Buffer Size: {info.get('mixer_buffer', 'unknown')}
Currently Playing: {info['playing']}

If you can't hear sound, check:
• System volume
• Speaker/headphone connections
• Audio drivers
• Windows audio settings"""
            else:
                message = f"""Audio System: NOT WORKING ✗

Error: {info.get('error', 'Unknown error')}

Common fixes:
• Install/update audio drivers
• Check Windows audio settings
• Try restarting the application
• Use different audio device
• Install pygame audio dependencies

The visual interface will still work normally."""
            
            msgbox.showinfo("Audio System Information", message)
            
        except Exception as e:
            self.update_status(f"Error showing audio info: {e}")
    
    def update_volume(self, value):
        """Update audio volume"""
        try:
            volume = float(value) / 100.0  # Convert to 0.0-1.0 range
            self.main_app.audio_manager.set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {e}")