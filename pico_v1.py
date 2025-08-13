import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ===== CONFIGURATION =====
# GPIO Pin Configuration
STRAIGHT_KEY_PIN = board.GP15    # Straight key input
PADDLE_DIT_PIN = board.GP15      # Dit paddle input (same as straight key)
PADDLE_DAH_PIN = board.GP10      # Dah paddle input
MODE_SWITCH_PIN = board.GP12     # Mode switch
LED_PIN = board.GP25             # Built-in LED

# Timing Configuration
DEBOUNCE_TIME = 0.005   # 5ms debounce for ultra-responsive operation
LOOP_DELAY = 0.0005     # 0.5ms main loop delay

# ===== HARDWARE SETUP =====
# Initialize straight key
straight_key = digitalio.DigitalInOut(STRAIGHT_KEY_PIN)
straight_key.direction = digitalio.Direction.INPUT
straight_key.pull = digitalio.Pull.UP

# Initialize paddle keys (comment out if not using paddles)
try:
    dit_paddle = digitalio.DigitalInOut(PADDLE_DIT_PIN)
    dit_paddle.direction = digitalio.Direction.INPUT
    dit_paddle.pull = digitalio.Pull.UP
    
    dah_paddle = digitalio.DigitalInOut(PADDLE_DAH_PIN)
    dah_paddle.direction = digitalio.Direction.INPUT
    dah_paddle.pull = digitalio.Pull.UP
    
    PADDLE_AVAILABLE = True
    print("Paddle keys initialized")
except Exception as e:
    PADDLE_AVAILABLE = False
    print(f"Paddle keys not available: {e}")

# Initialize mode switch (comment out if not using)
try:
    mode_switch = digitalio.DigitalInOut(MODE_SWITCH_PIN)
    mode_switch.direction = digitalio.Direction.INPUT
    mode_switch.pull = digitalio.Pull.UP
    MODE_SWITCH_AVAILABLE = True
    print("Mode switch initialized")
except Exception as e:
    MODE_SWITCH_AVAILABLE = False
    print(f"Mode switch not available: {e}")

# Initialize LED
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Initialize USB Keyboard
keyboard = Keyboard(usb_hid.devices)

# ===== STATE VARIABLES =====
# Straight key state
straight_key_pressed = False
last_straight_key_state = True

# Paddle state (if available)
dit_pressed = False
dah_pressed = False
last_dit_state = True
last_dah_state = True

# Mode tracking
current_mode = "STRAIGHT"  # "STRAIGHT" or "PADDLE"
last_mode_switch_state = True

# Timing
last_debounce_time = 0

# ===== HELPER FUNCTIONS =====
def check_mode_switch():
    """Check if mode should be switched"""
    global current_mode, last_mode_switch_state
    
    if not MODE_SWITCH_AVAILABLE:
        return
    
    current_switch_state = mode_switch.value
    if current_switch_state != last_mode_switch_state:
        time.sleep(DEBOUNCE_TIME)
        current_switch_state = mode_switch.value
        
        if current_switch_state != last_mode_switch_state:
            if not current_switch_state:  # Switch pressed
                current_mode = "PADDLE" if current_mode == "STRAIGHT" else "STRAIGHT"
                print(f"Mode switched to: {current_mode}")
                
                # Flash LED to indicate mode change
                for _ in range(3):
                    led.value = True
                    time.sleep(0.1)
                    led.value = False
                    time.sleep(0.1)
            
            last_mode_switch_state = current_switch_state

def handle_straight_key():
    """Handle straight key operation"""
    global straight_key_pressed, last_straight_key_state
    
    current_state = straight_key.value
    
    if current_state != last_straight_key_state:
        time.sleep(DEBOUNCE_TIME)
        current_state = straight_key.value
        
        if current_state != last_straight_key_state:
            if not current_state:  # Key pressed
                if not straight_key_pressed:
                    keyboard.press(Keycode.A)
                    led.value = True
                    straight_key_pressed = True
                    print("Straight Key DOWN")
            else:  # Key released
                if straight_key_pressed:
                    keyboard.release(Keycode.A)
                    led.value = False
                    straight_key_pressed = False
                    print("Straight Key UP")
            
            last_straight_key_state = current_state

def handle_paddle_keys():
    """Handle paddle key operation"""
    global dit_pressed, dah_pressed, last_dit_state, last_dah_state
    
    if not PADDLE_AVAILABLE:
        return
    
    # Handle Dit paddle (GP15 - same as straight key)
    current_dit_state = dit_paddle.value
    if current_dit_state != last_dit_state:
        time.sleep(DEBOUNCE_TIME)
        current_dit_state = dit_paddle.value
        
        if current_dit_state != last_dit_state:
            if not current_dit_state:  # Dit pressed
                if not dit_pressed:
                    keyboard.press(Keycode.A)
                    dit_pressed = True
                    update_led_status()
                    print("Dit DOWN")
            else:  # Dit released
                if dit_pressed:
                    keyboard.release(Keycode.A)
                    dit_pressed = False
                    update_led_status()
                    print("Dit UP")
            
            last_dit_state = current_dit_state
    
    # Handle Dah paddle (GP10)
    current_dah_state = dah_paddle.value
    if current_dah_state != last_dah_state:
        time.sleep(DEBOUNCE_TIME)
        current_dah_state = dah_paddle.value
        
        if current_dah_state != last_dah_state:
            if not current_dah_state:  # Dah pressed
                if not dah_pressed:
                    keyboard.press(Keycode.B)
                    dah_pressed = True
                    update_led_status()
                    print("Dah DOWN")
            else:  # Dah released
                if dah_pressed:
                    keyboard.release(Keycode.B)
                    dah_pressed = False
                    update_led_status()
                    print("Dah UP")
            
            last_dah_state = current_dah_state

def update_led_status():
    """Update LED based on paddle status"""
    if dit_pressed or dah_pressed:
        led.value = True
    else:
        led.value = False

def startup_sequence():
    """Startup indication sequence"""
    print("=== MORSE CODE KEYER STARTING ===")
    print("Straight key: GP15")
    if PADDLE_AVAILABLE:
        print("Dit paddle: GP15 (shared with straight key)")
        print("Dah paddle: GP10")
    else:
        print("Paddle mode: Not available")
    if MODE_SWITCH_AVAILABLE:
        print("Mode switch: GP12")
    else:
        print("Mode switch: Not available")
    print("LED: GP25")
    print(f"Current mode: {current_mode}")
    
    # LED startup sequence
    print("Running startup LED sequence...")
    for i in range(5):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)
    
    print("=== KEYER READY ===")
    print("Instructions:")
    print("- STRAIGHT mode: Use GP15 key for variable-length morse")
    print("- PADDLE mode: GP15=Dit(A), GP10=Dah(B)")
    if MODE_SWITCH_AVAILABLE:
        print("- Press GP12 switch to toggle modes")
    print("- LED shows transmission status")

# ===== MAIN PROGRAM =====
try:
    startup_sequence()
    
    # Main loop
    while True:
        # Check for mode switching
        check_mode_switch()
        
        # Handle input based on current mode
        if current_mode == "STRAIGHT":
            handle_straight_key()
        elif current_mode == "PADDLE" and PADDLE_AVAILABLE:
            handle_paddle_keys()
        else:
            # Fallback to straight key if paddle not available
            handle_straight_key()
        
        # Small delay to prevent excessive CPU usage
        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    print("\nKeyer stopped by user")
    keyboard.release_all()
    led.value = False

except Exception as e:
    print(f"Error: {e}")
    try:
        keyboard.release_all()
        led.value = False
    except:
        pass