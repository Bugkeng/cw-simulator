import tkinter as tk
from tkinter import ttk
import pygame
import threading
import time
import numpy as np

class PaddleKeySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Paddle Key Simulator (Iambic Mode B)")
        self.root.geometry("850x750")
        self.root.configure(bg='#2c3e50')
        
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.dit_pressed = False
        self.dah_pressed = False
        self.paddle_transmitting = False
        self.current_element = None
        self.element_start_time = None
        self.iambic_memory = None  # For Iambic Mode B completion

        self.morse_sequence = []
        self.current_letter = ""
        self.decoded_text = ""
        
        self.wpm = 20
        self.update_timing_from_wpm()
        
        self.tone_frequency = 600
        
        self.morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
            '....-': '4', '.....': '5', '-....': '6', '--...': '7',
            '---..': '8', '----.': '9', '-----': 'Ø', '..--..': '?', '-..-.': '/'
        }
        
        self.setup_ui()
        self.setup_audio()
        self.bind_keys()
        
        self.last_release_time = time.time()
        self.check_morse_timer()

    def update_timing_from_wpm(self):
        self.dot_duration = 60.0 / (self.wpm * 50)
        self.dash_duration = self.dot_duration * 3
        self.element_gap = self.dot_duration
        self.letter_gap = self.dot_duration * 3
        self.word_gap = self.dot_duration * 7
        
        if hasattr(self, 'timing_info'):
            self.timing_info.config(text=self.get_timing_info_text())

    def get_timing_info_text(self):
        return (f"Dit: {self.dot_duration:.3f}s | Dah: {self.dash_duration:.3f}s | "
                f"Element gap: {self.element_gap:.3f}s | Letter gap: {self.letter_gap:.2f}s | Word gap: {self.word_gap:.2f}s")

    def update_speed(self, value):
        self.wpm = int(value)
        self.wpm_display.config(text=f"{self.wpm} WPM")
        self.update_timing_from_wpm()

    def update_audio_settings(self, value):
        self.tone_frequency = int(value)
        self.freq_display.config(text=f"{self.tone_frequency} Hz")
        self.setup_audio()

    def setup_ui(self):
        # UI setup code remains the same...
        title_label = tk.Label(self.root, text="MORSE CODE PADDLE KEY SIMULATOR (Iambic Mode B)", 
                               font=('Courier', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=10)
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20)
        paddle_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
        paddle_frame.pack(pady=10, padx=20, fill='x')
        paddle_status_frame = tk.Frame(paddle_frame, bg='#34495e')
        paddle_status_frame.pack(pady=10)
        self.dit_status = tk.Label(paddle_status_frame, text="DIT ([)", font=('Courier', 14, 'bold'), fg='#95a5a6', bg='#34495e', width=12)
        self.dit_status.pack(side='left', padx=30)
        self.dah_status = tk.Label(paddle_status_frame, text="DAH (])", font=('Courier', 14, 'bold'), fg='#95a5a6', bg='#34495e', width=12)
        self.dah_status.pack(side='right', padx=30)
        self.paddle_visual = tk.Canvas(paddle_frame, width=450, height=120, bg='#2c3e50', highlightthickness=0)
        self.paddle_visual.pack(pady=10)
        self.draw_paddle(False, False)
        element_frame = tk.Frame(paddle_frame, bg='#34495e')
        element_frame.pack(pady=5)
        tk.Label(element_frame, text="SENDING:", font=('Courier', 10, 'bold'), fg='#ecf0f1', bg='#34495e').pack(side='left')
        self.current_element_display = tk.Label(element_frame, text="", font=('Courier', 14, 'bold'), fg='#f39c12', bg='#34495e', width=8)
        self.current_element_display.pack(side='left', padx=10)
        morse_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
        morse_frame.pack(pady=10, padx=20, fill='both', expand=True)
        tk.Label(morse_frame, text="CURRENT MORSE SEQUENCE:", font=('Courier', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10,5))
        self.morse_display = tk.Label(morse_frame, text="", font=('Courier', 24, 'bold'), fg='#f39c12', bg='#2c3e50', height=2, relief='sunken', bd=2)
        self.morse_display.pack(pady=5, padx=10, fill='x')
        tk.Label(morse_frame, text="DECODED TEXT:", font=('Courier', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10,5))
        self.text_display = tk.Text(morse_frame, font=('Courier', 14), height=4, bg='#2c3e50', fg='#2ecc71', insertbackground='#2ecc71', relief='sunken', bd=2, wrap='word')
        self.text_display.pack(pady=5, padx=10, fill='both', expand=True)
        self.text_display.config(state=tk.DISABLED)
        controls_frame = tk.Frame(main_frame, bg='#2c3e50')
        controls_frame.pack(pady=10, fill='x')
        speed_frame = tk.Frame(controls_frame, bg='#34495e', relief='raised', bd=2)
        speed_frame.pack(pady=10, padx=20, fill='x')
        speed_label_frame = tk.Frame(speed_frame, bg='#34495e')
        speed_label_frame.pack(pady=10)
        tk.Label(speed_label_frame, text="SPEED CONTROL:", font=('Courier', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(side='left')
        self.wpm_display = tk.Label(speed_label_frame, text=f"{self.wpm} WPM", font=('Courier', 12, 'bold'), fg='#3498db', bg='#34495e')
        self.wpm_display.pack(side='right')
        self.speed_slider = tk.Scale(speed_frame, from_=5, to=60, orient='horizontal', font=('Courier', 10), fg='#ecf0f1', bg='#34495e', activebackground='#3498db', troughcolor='#2c3e50', highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(self.wpm)
        self.speed_slider.pack(pady=5, padx=20, fill='x')
        self.timing_info = tk.Label(speed_frame, text=self.get_timing_info_text(), font=('Courier', 8), fg='#95a5a6', bg='#34495e', justify='center')
        self.timing_info.pack(pady=5)
        audio_frame = tk.Frame(controls_frame, bg='#34495e', relief='raised', bd=2)
        audio_frame.pack(pady=10, padx=20, fill='x')
        audio_label_frame = tk.Frame(audio_frame, bg='#34495e')
        audio_label_frame.pack(pady=10)
        tk.Label(audio_label_frame, text="TONE FREQUENCY:", font=('Courier', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(side='left')
        self.freq_display = tk.Label(audio_label_frame, text=f"{self.tone_frequency} Hz", font=('Courier', 12, 'bold'), fg='#3498db', bg='#34495e')
        self.freq_display.pack(side='right')
        self.freq_slider = tk.Scale(audio_frame, from_=300, to=1200, orient='horizontal', font=('Courier', 10), fg='#ecf0f1', bg='#34495e', activebackground='#3498db', troughcolor='#2c3e50', highlightthickness=0, command=self.update_audio_settings)
        self.freq_slider.set(self.tone_frequency)
        self.freq_slider.pack(pady=5, padx=20, fill='x')
        button_frame = tk.Frame(controls_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Clear Text", command=self.clear_text, font=('Courier', 10), bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Morse", command=self.clear_morse, font=('Courier', 10), bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Test Audio", command=self.test_audio, font=('Courier', 10), bg='#9b59b6', fg='white', padx=20).pack(side='left', padx=5)


    def draw_paddle(self, dit_pressed, dah_pressed):
        # This function remains the same
        self.paddle_visual.delete("all")
        self.paddle_visual.create_rectangle(175, 100, 275, 110, fill='#7f8c8d', outline='#34495e', width=2)
        self.paddle_visual.create_rectangle(220, 60, 230, 100, fill='#7f8c8d', outline='#34495e', width=2)
        if dit_pressed:
            self.paddle_visual.create_line(120, 80, 220, 80, fill='#e74c3c', width=8, capstyle='round')
            self.paddle_visual.create_oval(115, 75, 125, 85, fill='#c0392b', outline='#a93226', width=2)
            self.paddle_visual.create_oval(215, 75, 225, 85, fill='#f1c40f', outline='#f39c12', width=2)
            self.paddle_visual.create_text(220, 80, text="⚡", font=('Arial', 12), fill='#f1c40f')
        else:
            self.paddle_visual.create_line(120, 80, 190, 80, fill='#95a5a6', width=8, capstyle='round')
            self.paddle_visual.create_oval(115, 75, 125, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        if dah_pressed:
            self.paddle_visual.create_line(330, 80, 230, 80, fill='#e74c3c', width=8, capstyle='round')
            self.paddle_visual.create_oval(325, 75, 335, 85, fill='#c0392b', outline='#a93226', width=2)
            self.paddle_visual.create_oval(225, 75, 235, 85, fill='#f1c40f', outline='#f39c12', width=2)
            self.paddle_visual.create_text(230, 80, text="⚡", font=('Arial', 12), fill='#f1c40f')
        else:
            self.paddle_visual.create_line(330, 80, 260, 80, fill='#95a5a6', width=8, capstyle='round')
            self.paddle_visual.create_oval(325, 75, 335, 85, fill='#7f8c8d', outline='#6c7b7d', width=2)
        self.paddle_visual.create_text(120, 50, text="DIT", font=('Courier', 12, 'bold'), fill='#2ecc71' if dit_pressed else '#ecf0f1')
        self.paddle_visual.create_text(330, 50, text="DAH", font=('Courier', 12, 'bold'), fill='#2ecc71' if dah_pressed else '#ecf0f1')
        self.paddle_visual.create_oval(222, 85, 228, 95, fill='#5d6d7e', outline='#34495e', width=1)

    def setup_audio(self):
        # This function remains the same
        sample_rate = 22050
        duration = 0.1
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            wave = np.sin(2 * np.pi * self.tone_frequency * i / sample_rate)
            arr[i][0] = wave * 0.3
            arr[i][1] = wave * 0.3
        arr = (arr * 32767).astype(np.int16)
        self.tone_sound = pygame.sndarray.make_sound(arr)

    def bind_keys(self):
        # This function remains the same
        self.root.bind('<KeyPress-bracketleft>', self.dit_down)
        self.root.bind('<KeyRelease-bracketleft>', self.dit_up)
        self.root.bind('<KeyPress-bracketright>', self.dah_down)
        self.root.bind('<KeyRelease-bracketright>', self.dah_up)
        self.root.focus_set()

    def dit_down(self, event):
        if not self.dit_pressed:
            self.dit_pressed = True
            self.dit_status.config(fg='#2ecc71')
            self.draw_paddle(True, self.dah_pressed)
            self.handle_paddle_logic()

    def dit_up(self, event):
        if self.dit_pressed:
            self.dit_pressed = False
            self.dit_status.config(fg='#95a5a6')
            self.draw_paddle(False, self.dah_pressed)

    def dah_down(self, event):
        if not self.dah_pressed:
            self.dah_pressed = True
            self.dah_status.config(fg='#2ecc71')
            self.draw_paddle(self.dit_pressed, True)
            self.handle_paddle_logic()

    def dah_up(self, event):
        if self.dah_pressed:
            self.dah_pressed = False
            self.dah_status.config(fg='#95a5a6')
            self.draw_paddle(self.dit_pressed, False)

    def handle_paddle_logic(self):
        if not self.paddle_transmitting:
            if self.dit_pressed and not self.dah_pressed:
                self.iambic_memory = None # Not an iambic sequence
                self.send_element('.')
            elif self.dah_pressed and not self.dit_pressed:
                self.iambic_memory = None # Not an iambic sequence
                self.send_element('-')
            elif self.dit_pressed and self.dah_pressed:
                self.iambic_memory = '.' # Start with DIT, remember for release
                self.send_element('.')

    def send_element(self, element):
        if self.paddle_transmitting:
            return
            
        self.paddle_transmitting = True
        self.current_element = element
        self.element_start_time = time.time()
        
        self.current_element_display.config(text=element)
        
        self.morse_sequence.append(element)
        self.current_letter = ''.join(self.morse_sequence)
        self.morse_display.config(text=self.current_letter)
        
        self.tone_sound.play(-1)
        
        if element == '.':
            duration = self.dot_duration
        else:
            duration = self.dash_duration
        
        self.root.after(int(duration * 1000), self.stop_element)

    def stop_element(self):
        self.tone_sound.stop()
        self.current_element_display.config(text="")
        
        self.root.after(int(self.element_gap * 1000), self.check_continue)

    def check_continue(self):
        """Check if paddle should continue sending elements with Iambic Mode B logic."""
        self.paddle_transmitting = False

        # Mode B: Both paddles are currently pressed (continue the iambic sequence)
        if self.dit_pressed and self.dah_pressed:
            if self.current_element == '.':
                self.iambic_memory = '-'
                self.send_element('-')
            else:
                self.iambic_memory = '.'
                self.send_element('.')

        # Only one paddle is pressed
        elif self.dit_pressed:
            self.iambic_memory = None
            self.send_element('.')
        elif self.dah_pressed:
            self.iambic_memory = None
            self.send_element('-')

        # No paddles are pressed
        else:
            # Mode B feature: If there's a final element in memory, send it
            if self.iambic_memory:
                element_to_send = self.iambic_memory
                self.iambic_memory = None
                self.send_element(element_to_send)
            else:
                # No keys pressed and no memory, reset timing for letter/word spacing
                self.last_release_time = time.time()

    def check_morse_timer(self):
        # This function remains the same
        if self.morse_sequence and not self.paddle_transmitting:
            time_since_release = time.time() - self.last_release_time
            if time_since_release > self.letter_gap:
                self.decode_current_sequence()
                if time_since_release > self.word_gap:
                    if not self.decoded_text.endswith(" "):
                         self.decoded_text += " "
                         self.update_text_display()
        self.root.after(50, self.check_morse_timer)

    def decode_current_sequence(self):
        # This function remains the same
        if self.morse_sequence:
            morse_code = ''.join(self.morse_sequence)
            if morse_code in self.morse_dict:
                letter = self.morse_dict[morse_code]
                self.decoded_text += letter
                self.update_text_display()
            else:
                self.decoded_text += f"[{morse_code}]"
                self.update_text_display()
            self.morse_sequence = []
            self.morse_display.config(text="")

    def update_text_display(self):
        # This function remains the same
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.decoded_text)
        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)

    def clear_text(self):
        # This function remains the same
        self.decoded_text = ""
        self.update_text_display()

    def clear_morse(self):
        # This function remains the same
        self.morse_sequence = []
        self.morse_display.config(text="")

    def test_audio(self):
        # This function remains the same
        try:
            self.tone_sound.play()
            self.root.after(200, lambda: self.tone_sound.stop())
        except Exception as e:
            print(f"Audio test failed: {e}")

def main():
    root = tk.Tk()
    app = PaddleKeySimulator(root)
    root.focus_force()
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()
