import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Define button GPIO pin for the straight key
button_pin = board.GP15  # Using only one button for the straight key

# Initialize button with pull-up resistor
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Define built-in LED for visual feedback
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# Initialize USB Keyboard
keyboard = Keyboard(usb_hid.devices)

# Key to send (A key for the Morse simulator)
morse_key = Keycode.A

# State tracking
button_pressed = False
last_button_state = True  # True = not pressed (pull-up), False = pressed

# Debounce settings (much shorter for responsive morse code)
DEBOUNCE_TIME = 0.01  # 10ms debounce for quick response

print("Morse Code Straight Key ready...")
print("Press and hold the button to send morse code")

while True:
    current_button_state = button.value  # True = not pressed, False = pressed
    current_time = time.monotonic()
    
    # Check for state change with minimal debouncing
    if current_button_state != last_button_state:
        time.sleep(DEBOUNCE_TIME)  # Small debounce delay
        current_button_state = button.value  # Re-read after debounce
        
        if current_button_state != last_button_state:  # State actually changed
            if not current_button_state:  # Button pressed (goes LOW)
                if not button_pressed:
                    keyboard.press(morse_key)  # Press and HOLD the A key
                    led.value = True  # LED on for visual feedback
                    button_pressed = True
                    print("Key DOWN")
            
            else:  # Button released (goes HIGH)
                if button_pressed:
                    keyboard.release(morse_key)  # Release the A key
                    led.value = False  # LED off
                    button_pressed = False
                    print("Key UP")
            
            last_button_state = current_button_state
    
    time.sleep(0.001)  # Very small delay for responsive operation
