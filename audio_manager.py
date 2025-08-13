#!/usr/bin/env python3
"""
Audio Manager Module - Simplified version based on working code
Uses the same audio approach as the working simple version
"""

import pygame
import numpy as np
import time

class AudioManager:
    def __init__(self, frequency=600, sample_rate=22050):
        """
        Initialize audio manager with simple, proven approach
        
        Args:
            frequency (int): Tone frequency in Hz (default 600Hz)
            sample_rate (int): Audio sample rate (default 22050Hz)
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.is_playing = False
        self.tone_sound = None
        self.audio_available = False
        
        print("Initializing audio system...")
        self.initialize_audio()
    
    def initialize_audio(self):
        """Initialize audio using the same method as working code"""
        try:
            # Use the exact same initialization as your working code
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            print("✓ Pygame mixer initialized")
            self.setup_audio()
            self.audio_available = True
            print("✓ Audio system ready")
        except Exception as e:
            print(f"✗ Audio initialization failed: {e}")
            self.audio_available = False
    
    def setup_audio(self):
        """Generate tone using the exact same method as working code"""
        if not self.audio_available:
            return
            
        try:
            # Use the exact same audio generation as your working code
            duration = 0.1  # seconds
            frames = int(duration * self.sample_rate)
            
            # Generate sine wave - same method as working code
            arr = np.zeros((frames, 2))
            for i in range(frames):
                wave = np.sin(2 * np.pi * self.frequency * i / self.sample_rate)
                arr[i][0] = wave * 0.3  # Left channel
                arr[i][1] = wave * 0.3  # Right channel
            
            # Convert to pygame sound - same method as working code
            arr = (arr * 32767).astype(np.int16)
            self.tone_sound = pygame.sndarray.make_sound(arr)
            print(f"✓ Tone generated ({self.frequency}Hz)")
            
        except Exception as e:
            print(f"✗ Tone generation failed: {e}")
            self.audio_available = False
    
    def start_tone(self):
        """Start playing the morse code tone"""
        if not self.audio_available or self.is_playing:
            return
        
        try:
            self.is_playing = True
            if self.tone_sound:
                self.tone_sound.play(-1)  # Loop indefinitely - same as working code
        except Exception as e:
            print(f"Failed to start tone: {e}")
            self.is_playing = False
    
    def stop_tone(self):
        """Stop playing the morse code tone"""
        if not self.audio_available or not self.is_playing:
            return
        
        try:
            self.is_playing = False
            if self.tone_sound:
                self.tone_sound.stop()  # Same as working code
        except Exception as e:
            print(f"Failed to stop tone: {e}")
    
    def set_frequency(self, frequency):
        """Change the tone frequency"""
        if frequency != self.frequency:
            self.frequency = frequency
            was_playing = self.is_playing
            if was_playing:
                self.stop_tone()
            self.setup_audio()
            if was_playing:
                self.start_tone()
    
    def set_volume(self, volume):
        """Set the audio volume (0.0 to 1.0)"""
        if self.audio_available and self.tone_sound:
            try:
                self.tone_sound.set_volume(max(0.0, min(1.0, volume)))
            except Exception as e:
                print(f"Failed to set volume: {e}")
    
    def test_audio(self):
        """Test audio functionality with a short beep"""
        if not self.audio_available:
            print("Audio not available for testing")
            return False
        
        try:
            print("Testing audio with short beep...")
            self.start_tone()
            time.sleep(0.2)  # 200ms beep
            self.stop_tone()
            print("✓ Audio test completed")
            return True
        except Exception as e:
            print(f"✗ Audio test failed: {e}")
            return False
    
    def get_audio_info(self):
        """Get audio system information"""
        info = {
            'available': self.audio_available,
            'playing': self.is_playing,
            'frequency': self.frequency,
            'sample_rate': self.sample_rate
        }
        
        if self.audio_available:
            try:
                mixer_info = pygame.mixer.get_init()
                if mixer_info:
                    info['mixer_frequency'] = mixer_info[0]
                    info['mixer_format'] = mixer_info[1] 
                    info['mixer_channels'] = mixer_info[2]
            except:
                pass
        
        return info
    
    def print_audio_status(self):
        """Print audio status information"""
        info = self.get_audio_info()
        print("\n=== AUDIO SYSTEM STATUS ===")
        print(f"Available: {info['available']}")
        print(f"Playing: {info['playing']}")
        print(f"Tone Frequency: {info['frequency']}Hz")
        
        if info['available']:
            print(f"Sample Rate: {info.get('mixer_frequency', 'unknown')}Hz")
            print(f"Format: {info.get('mixer_format', 'unknown')}")
            print(f"Channels: {info.get('mixer_channels', 'unknown')}")
        else:
            print("Audio is not available")
    
    def cleanup(self):
        """Clean up audio resources"""
        try:
            self.stop_tone()
            if self.audio_available:
                pygame.mixer.quit()
        except Exception as e:
            print(f"Audio cleanup failed: {e}")
    
    def get_status(self):
        """Get current audio status information"""
        return {
            'available': self.audio_available,
            'playing': self.is_playing,
            'frequency': self.frequency,
            'sample_rate': self.sample_rate
        }