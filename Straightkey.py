import tkinter as tk
from tkinter import ttk
import pygame
import threading
import time
import numpy as np

class MorseCodeSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Straight Key Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame for audio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Morse code variables
        self.is_transmitting = False
        self.tone_frequency = 600  # Hz
        self.key_down_time = None
        self.morse_sequence = []
        self.current_letter = ""
        self.decoded_text = ""
        
        # Speed control (WPM - Words Per Minute)
        self.wpm = 15  # Default 20 WPM
        self.update_timing_from_wpm()
        
        # Morse code dictionary
        self.morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
            '....-': '4', '.....': '5', '-....': '6', '--...': '7',
            '---..': '8', '----.': '9', '-----': '0'
        }
        
        self.setup_ui()
        self.setup_audio()
        self.bind_keys()
        
        # Start the morse decode timer
        self.last_release_time = time.time()
        self.check_morse_timer()
    
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
        if hasattr(self, 'timing_info'):
            self.timing_info.config(text=self.get_timing_info_text())
    
    def get_timing_info_text(self):
        """Generate timing information text"""
        return (f"Dot: <{self.dash_threshold:.2f}s | Dash: ≥{self.dash_threshold:.2f}s | "
                f"Letter gap: {self.letter_gap:.2f}s | Word gap: {self.word_gap:.2f}s")
    
    def update_speed(self, value):
        """Callback for speed slider changes"""
        self.wpm = int(value)
        self.wpm_display.config(text=f"{self.wpm} WPM")
        self.update_timing_from_wpm()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="MORSE CODE STRAIGHT KEY SIMULATOR", 
                              font=('Courier', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20)
        
        # Key visualization frame
        key_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
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
        
        # Morse display frame
        morse_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
        morse_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(morse_frame, text="CURRENT MORSE SEQUENCE:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=(10,5))
        
        self.morse_display = tk.Label(morse_frame, text="", font=('Courier', 24, 'bold'),
                                     fg='#f39c12', bg='#2c3e50', height=2, relief='sunken', bd=2)
        self.morse_display.pack(pady=5, padx=10, fill='x')
        
        tk.Label(morse_frame, text="DECODED TEXT:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=(20,5))
        
        self.text_display = tk.Text(morse_frame, font=('Courier', 14), height=8,
                                   bg='#2c3e50', fg='#2ecc71', insertbackground='#2ecc71',
                                   relief='sunken', bd=2, wrap='word')
        self.text_display.pack(pady=5, padx=10, fill='both', expand=True)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg='#2c3e50')
        controls_frame.pack(pady=10, fill='x')
        
        # Speed control frame
        speed_frame = tk.Frame(controls_frame, bg='#34495e', relief='raised', bd=2)
        speed_frame.pack(pady=10, padx=20, fill='x')
        
        # Speed label and value display
        speed_label_frame = tk.Frame(speed_frame, bg='#34495e')
        speed_label_frame.pack(pady=10)
        
        tk.Label(speed_label_frame, text="SPEED CONTROL:", font=('Courier', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side='left')
        
        self.wpm_display = tk.Label(speed_label_frame, text=f"{self.wpm} WPM", 
                                   font=('Courier', 12, 'bold'), fg='#3498db', bg='#34495e')
        self.wpm_display.pack(side='right')
        
        # Speed slider
        self.speed_slider = tk.Scale(speed_frame, from_=5, to=60, orient='horizontal',
                                    font=('Courier', 10), fg='#ecf0f1', bg='#34495e',
                                    activebackground='#3498db', troughcolor='#2c3e50',
                                    highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(self.wpm)
        self.speed_slider.pack(pady=5, padx=20, fill='x')
        
        # Timing info display
        self.timing_info = tk.Label(speed_frame, text=self.get_timing_info_text(),
                                   font=('Courier', 8), fg='#95a5a6', bg='#34495e', justify='center')
        self.timing_info.pack(pady=5)
        
        # Instructions
        instructions = tk.Label(controls_frame, 
                               text="Press and hold 'A' key to operate the straight key\n" +
                                    "Timing automatically adjusts based on WPM setting above",
                               font=('Courier', 10), fg='#95a5a6', bg='#2c3e50', justify='center')
        instructions.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(controls_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Clear Text", command=self.clear_text,
                 font=('Courier', 10), bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear Morse", command=self.clear_morse,
                 font=('Courier', 10), bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
    
    def draw_key(self, pressed):
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
        else:
            # Key up position
            self.key_visual.create_line(150, 80, 180, 20, fill='#95a5a6', width=8, capstyle='round')
            self.key_visual.create_oval(145, 75, 155, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
            # Contact point
            self.key_visual.create_oval(175, 15, 185, 25, fill='#bdc3c7', outline='#95a5a6', width=2)
        
        # Knob
        self.key_visual.create_oval(195, 35, 215, 55, fill='#34495e', outline='#2c3e50', width=2)
    
    def setup_audio(self):
        # Generate tone for morse code
        sample_rate = 22050
        duration = 0.1  # seconds
        frames = int(duration * sample_rate)
        
        # Generate sine wave
        arr = np.zeros((frames, 2))
        for i in range(frames):
            wave = np.sin(2 * np.pi * self.tone_frequency * i / sample_rate)
            arr[i][0] = wave * 0.3  # Left channel
            arr[i][1] = wave * 0.3  # Right channel
        
        # Convert to pygame sound
        arr = (arr * 32767).astype(np.int16)
        self.tone_sound = pygame.sndarray.make_sound(arr)
    
    def bind_keys(self):
        self.root.bind('<KeyPress-a>', self.key_down)
        self.root.bind('<KeyRelease-a>', self.key_up)
        self.root.bind('<KeyPress-A>', self.key_down)
        self.root.bind('<KeyRelease-A>', self.key_up)
        self.root.focus_set()  # Make sure window has focus for key events
    
    def key_down(self, event):
        if not self.is_transmitting:
            self.is_transmitting = True
            self.key_down_time = time.time()
            
            # Update UI
            self.key_status.config(text="KEY DOWN", fg='#2ecc71')
            self.draw_key(True)
            
            # Start playing tone
            self.tone_sound.play(-1)  # Loop indefinitely
    
    def key_up(self, event):
        if self.is_transmitting:
            self.is_transmitting = False
            key_duration = time.time() - self.key_down_time
            
            # Update UI
            self.key_status.config(text="KEY UP", fg='#e74c3c')
            self.draw_key(False)
            
            # Stop playing tone
            self.tone_sound.stop()
            
            # Determine if it's a dot or dash based on WPM timing
            if key_duration < self.dash_threshold:  # Short press = dot
                self.morse_sequence.append('.')
            else:  # Long press = dash
                self.morse_sequence.append('-')
            
            # Update morse display
            self.current_letter = ''.join(self.morse_sequence)
            self.morse_display.config(text=self.current_letter)
            
            # Reset the timer for letter/word spacing
            self.last_release_time = time.time()
    
    def check_morse_timer(self):
        """Check if enough time has passed to decode current morse sequence"""
        if self.morse_sequence and not self.is_transmitting:
            time_since_release = time.time() - self.last_release_time
            
            # If pause is long enough, decode the current sequence (letter gap)
            if time_since_release > self.letter_gap:
                self.decode_current_sequence()
                
                # If pause is very long, add a space (word gap)
                if time_since_release > self.word_gap:
                    self.decoded_text += " "
                    self.update_text_display()
        
        # Schedule next check
        self.root.after(50, self.check_morse_timer)  # Check more frequently
    
    def decode_current_sequence(self):
        """Decode the current morse sequence to a letter"""
        if self.morse_sequence:
            morse_code = ''.join(self.morse_sequence)
            if morse_code in self.morse_dict:
                letter = self.morse_dict[morse_code]
                self.decoded_text += letter
                self.update_text_display()
            
            # Clear the current sequence
            self.morse_sequence = []
            self.morse_display.config(text="")
    
    def update_text_display(self):
        """Update the text display with decoded text"""
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.decoded_text)
        self.text_display.see(tk.END)
    
    def clear_text(self):
        """Clear all decoded text"""
        self.decoded_text = ""
        self.text_display.delete(1.0, tk.END)
    
    def clear_morse(self):
        """Clear current morse sequence"""
        self.morse_sequence = []
        self.morse_display.config(text="")

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