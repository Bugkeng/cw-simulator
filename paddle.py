import tkinter as tk
from tkinter import ttk
import pygame
import threading
import time
import numpy as np

class PaddleKeySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Paddle Key Simulator")
        self.root.geometry("850x650")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame for audio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Paddle key variables
        self.dit_pressed = False
        self.dah_pressed = False
        self.paddle_transmitting = False
        self.current_element = None
        self.element_start_time = None
        
        # Morse code variables
        self.morse_sequence = []
        self.current_letter = ""
        self.decoded_text = ""
        
        # Speed control (WPM - Words Per Minute)
        self.wpm = 20  # Default 20 WPM
        self.update_timing_from_wpm()
        
        # Audio variables
        self.tone_frequency = 600  # Hz
        
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
        self.dash_duration = self.dot_duration * 3  # Dash = 3 dots
        self.element_gap = self.dot_duration  # 1 dot unit between elements
        self.letter_gap = self.dot_duration * 3  # 3 dot units between letters
        self.word_gap = self.dot_duration * 7    # 7 dot units between words
        
        # Update timing info display if it exists
        if hasattr(self, 'timing_info'):
            self.timing_info.config(text=self.get_timing_info_text())
    
    def get_timing_info_text(self):
        """Generate timing information text"""
        return (f"Dit: {self.dot_duration:.3f}s | Dah: {self.dash_duration:.3f}s | "
                f"Element gap: {self.element_gap:.3f}s | Letter gap: {self.letter_gap:.2f}s | Word gap: {self.word_gap:.2f}s")
    
    def update_speed(self, value):
        """Callback for speed slider changes"""
        self.wpm = int(value)
        self.wpm_display.config(text=f"{self.wpm} WPM")
        self.update_timing_from_wpm()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="MORSE CODE PADDLE KEY SIMULATOR", 
                              font=('Courier', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20)
        
        # Paddle visualization frame
        paddle_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
        paddle_frame.pack(pady=20, padx=20, fill='x')
        
        # Paddle status
        paddle_status_frame = tk.Frame(paddle_frame, bg='#34495e')
        paddle_status_frame.pack(pady=10)
        
        self.dit_status = tk.Label(paddle_status_frame, text="DIT (A)", font=('Courier', 14, 'bold'),
                                  fg='#95a5a6', bg='#34495e', width=12)
        self.dit_status.pack(side='left', padx=30)
        
        self.dah_status = tk.Label(paddle_status_frame, text="DAH (B)", font=('Courier', 14, 'bold'),
                                  fg='#95a5a6', bg='#34495e', width=12)
        self.dah_status.pack(side='right', padx=30)
        
        # Visual paddle representation
        self.paddle_visual = tk.Canvas(paddle_frame, width=450, height=120, bg='#2c3e50', highlightthickness=0)
        self.paddle_visual.pack(pady=10)
        
        # Draw the paddle in neutral position
        self.draw_paddle(False, False)
        
        # Current element display
        element_frame = tk.Frame(paddle_frame, bg='#34495e')
        element_frame.pack(pady=5)
        
        tk.Label(element_frame, text="SENDING:", font=('Courier', 10, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(side='left')
        
        self.current_element_display = tk.Label(element_frame, text="", font=('Courier', 14, 'bold'),
                                              fg='#f39c12', bg='#34495e', width=8)
        self.current_element_display.pack(side='left', padx=10)
        
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
        
        self.text_display = tk.Text(morse_frame, font=('Courier', 14), height=6,
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
                               text="Press 'A' for DIT (dot) | Press 'B' for DAH (dash)\n" +
                                    "Hold keys for automatic repeat | Elements sent at exact WPM timing\n" +
                                    "Perfect for learning proper paddle technique",
                               font=('Courier', 10), fg='#95a5a6', bg='#2c3e50', justify='center')
        instructions.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(controls_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Clear Text", command=self.clear_text,
                 font=('Courier', 10), bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear Morse", command=self.clear_morse,
                 font=('Courier', 10), bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Test Audio", command=self.test_audio,
                 font=('Courier', 10), bg='#9b59b6', fg='white', padx=20).pack(side='left', padx=5)
    
    def draw_paddle(self, dit_pressed, dah_pressed):
        """Draw the paddle key showing current state"""
        self.paddle_visual.delete("all")
        
        # Base and center post
        self.paddle_visual.create_rectangle(175, 100, 275, 110, fill='#7f8c8d', outline='#34495e', width=2)
        self.paddle_visual.create_rectangle(220, 60, 230, 100, fill='#7f8c8d', outline='#34495e', width=2)
        
        # Dit paddle (left side)
        if dit_pressed:
            # Dit paddle pressed (touching center)
            self.paddle_visual.create_line(120, 80, 220, 80, fill='#e74c3c', width=8, capstyle='round')
            self.paddle_visual.create_oval(115, 75, 125, 85, fill='#c0392b', outline='#a93226', width=2)
            # Contact indicator
            self.paddle_visual.create_oval(215, 75, 225, 85, fill='#f1c40f', outline='#f39c12', width=2)
            # Spark effect
            self.paddle_visual.create_text(220, 80, text="⚡", font=('Arial', 12), fill='#f1c40f')
        else:
            # Dit paddle neutral
            self.paddle_visual.create_line(120, 80, 190, 80, fill='#95a5a6', width=8, capstyle='round')
            self.paddle_visual.create_oval(115, 75, 125, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        
        # Dah paddle (right side)
        if dah_pressed:
            # Dah paddle pressed (touching center)
            self.paddle_visual.create_line(330, 80, 230, 80, fill='#e74c3c', width=8, capstyle='round')
            self.paddle_visual.create_oval(325, 75, 335, 85, fill='#c0392b', outline='#a93226', width=2)
            # Contact indicator
            self.paddle_visual.create_oval(225, 75, 235, 85, fill='#f1c40f', outline='#f39c12', width=2)
            # Spark effect
            self.paddle_visual.create_text(230, 80, text="⚡", font=('Arial', 12), fill='#f1c40f')
        else:
            # Dah paddle neutral
            self.paddle_visual.create_line(330, 80, 260, 80, fill='#95a5a6', width=8, capstyle='round')
            self.paddle_visual.create_oval(325, 75, 335, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        
        # Labels with color coding
        self.paddle_visual.create_text(120, 50, text="DIT", font=('Courier', 12, 'bold'), 
                                      fill='#2ecc71' if dit_pressed else '#ecf0f1')
        self.paddle_visual.create_text(330, 50, text="DAH", font=('Courier', 12, 'bold'), 
                                      fill='#2ecc71' if dah_pressed else '#ecf0f1')
        
        # Center post details
        self.paddle_visual.create_oval(222, 85, 228, 95, fill='#5d6d7e', outline='#34495e', width=1)
    
    def setup_audio(self):
        # Generate tone for morse code using the same method as working code
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
        # Dit paddle (A key)
        self.root.bind('<KeyPress-a>', self.dit_down)
        self.root.bind('<KeyRelease-a>', self.dit_up)
        self.root.bind('<KeyPress-A>', self.dit_down)
        self.root.bind('<KeyRelease-A>', self.dit_up)
        
        # Dah paddle (B key)
        self.root.bind('<KeyPress-b>', self.dah_down)
        self.root.bind('<KeyRelease-b>', self.dah_up)
        self.root.bind('<KeyPress-B>', self.dah_down)
        self.root.bind('<KeyRelease-B>', self.dah_up)
        
        self.root.focus_set()  # Make sure window has focus for key events
    
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
                self.send_element('.')
            elif self.dah_pressed and not self.dit_pressed:
                self.send_element('-')
            elif self.dit_pressed and self.dah_pressed:
                # Both pressed - prioritize dit for simplicity
                self.send_element('.')
    
    def send_element(self, element):
        """Send a dit or dah with proper timing"""
        if self.paddle_transmitting:
            return
            
        self.paddle_transmitting = True
        self.current_element = element
        self.element_start_time = time.time()
        
        # Update display
        self.current_element_display.config(text=element)
        
        # Add element to morse sequence
        self.morse_sequence.append(element)
        self.current_letter = ''.join(self.morse_sequence)
        self.morse_display.config(text=self.current_letter)
        
        # Play tone for the appropriate duration
        self.tone_sound.play(-1)  # Start tone
        
        # Calculate element duration
        if element == '.':
            duration = self.dot_duration
        else:  # dash
            duration = self.dash_duration
        
        # Schedule tone stop and check for next element
        self.root.after(int(duration * 1000), self.stop_element)
    
    def stop_element(self):
        """Stop current element and check for next"""
        self.tone_sound.stop()
        self.current_element_display.config(text="")
        
        # Inter-element gap
        self.root.after(int(self.element_gap * 1000), self.check_continue)
    
    def check_continue(self):
        """Check if paddle should continue sending elements"""
        self.paddle_transmitting = False
        
        # Check if keys are still pressed and send appropriate element
        if self.dit_pressed and not self.dah_pressed:
            self.send_element('.')
        elif self.dah_pressed and not self.dit_pressed:
            self.send_element('-')
        elif self.dit_pressed and self.dah_pressed:
            # Alternate for iambic keying
            if self.current_element == '.':
                self.send_element('-')
            else:
                self.send_element('.')
        else:
            # No keys pressed, reset timing for letter/word spacing
            self.last_release_time = time.time()
    
    def check_morse_timer(self):
        """Check if enough time has passed to decode current morse sequence"""
        if self.morse_sequence and not self.paddle_transmitting:
            time_since_release = time.time() - self.last_release_time
            
            # If pause is long enough, decode the current sequence (letter gap)
            if time_since_release > self.letter_gap:
                self.decode_current_sequence()
                
                # If pause is very long, add a space (word gap)
                if time_since_release > self.word_gap:
                    self.decoded_text += " "
                    self.update_text_display()
        
        # Schedule next check
        self.root.after(50, self.check_morse_timer)
    
    def decode_current_sequence(self):
        """Decode the current morse sequence to a letter"""
        if self.morse_sequence:
            morse_code = ''.join(self.morse_sequence)
            if morse_code in self.morse_dict:
                letter = self.morse_dict[morse_code]
                self.decoded_text += letter
                self.update_text_display()
            else:
                # Unknown sequence - show in brackets
                self.decoded_text += f"[{morse_code}]"
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
    
    def test_audio(self):
        """Test audio with a short beep"""
        try:
            self.tone_sound.play()
            self.root.after(200, lambda: self.tone_sound.stop())
            print("Audio test completed")
        except Exception as e:
            print(f"Audio test failed: {e}")

def main():
    root = tk.Tk()
    app = PaddleKeySimulator(root)
    
    # Make sure the window can receive key events
    root.focus_force()
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()