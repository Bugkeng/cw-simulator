import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ===== SIMPLE PADDLE CONFIGURATION =====
DIT_PIN = board.GP15      # Dit paddle (dot) - sends '['
DAH_PIN = board.GP10      # Dah paddle (dash) - sends ']'
LED_PIN = board.GP25      # Status LED

DEBOUNCE_TIME = 0.005     # 5ms debounce
LOOP_DELAY = 0.001        # 1ms loop delay

print("=== SIMPLE PADDLE KEYER ===")

# ===== HARDWARE SETUP =====
# Dit paddle
dit_paddle = digitalio.DigitalInOut(DIT_PIN)
dit_paddle.direction = digitalio.Direction.INPUT
dit_paddle.pull = digitalio.Pull.UP

# Dah paddle
dah_paddle = digitalio.DigitalInOut(DAH_PIN)
dah_paddle.direction = digitalio.Direction.INPUT
dah_paddle.pull = digitalio.Pull.UP

# LED
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Keyboard
keyboard = Keyboard(usb_hid.devices)

print("✓ Hardware initialized")
print("Dit paddle: GP15 → '[' key")
print("Dah paddle: GP10 → ']' key")

# ===== STATE VARIABLES =====
dit_pressed = False
dah_pressed = False
last_dit_state = True
last_dah_state = True
last_dit_time = 0
last_dah_time = 0

# ===== STARTUP INDICATION =====
for i in range(3):
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)

print("✓ Ready for paddle input!")

# ===== MAIN LOOP =====
try:
    while True:
        current_time = time.monotonic()
        
        # === DIT PADDLE HANDLING ===
        current_dit_state = dit_paddle.value
        if (current_dit_state != last_dit_state and 
            current_time - last_dit_time > DEBOUNCE_TIME):
            
            if not current_dit_state:  # Pressed (LOW)
                if not dit_pressed:
                    keyboard.press(Keycode.LEFT_BRACKET)
                    dit_pressed = True
                    print("Dit ON")
            else:  # Released (HIGH)
                if dit_pressed:
                    keyboard.release(Keycode.LEFT_BRACKET)
                    dit_pressed = False
                    print("Dit OFF")
            
            last_dit_state = current_dit_state
            last_dit_time = current_time
        
        # === DAH PADDLE HANDLING ===
        current_dah_state = dah_paddle.value
        if (current_dah_state != last_dah_state and 
            current_time - last_dah_time > DEBOUNCE_TIME):
            
            if not current_dah_state:  # Pressed (LOW)
                if not dah_pressed:
                    keyboard.press(Keycode.RIGHT_BRACKET)
                    dah_pressed = True
                    print("Dah ON")
            else:  # Released (HIGH)
                if dah_pressed:
                    keyboard.release(Keycode.RIGHT_BRACKET)
                    dah_pressed = False
                    print("Dah OFF")
            
            last_dah_state = current_dah_state
            last_dah_time = current_time
        
        # === LED STATUS ===
        led.value = dit_pressed or dah_pressed
        
        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    print("\nStopping paddle keyer...")
    keyboard.release_all()
    led.value = False
    print("✓ Stopped cleanly")

except Exception as e:
    print(f"Error: {e}")
    keyboard.release_all()
    led.value = False
    
