#!/usr/bin/env python3
"""
Morse Code Decoder Module - Handles morse code sequence management and decoding
Converts dot/dash sequences to letters and manages morse code logic
"""

class MorseDecoder:
    def __init__(self):
        """Initialize the morse code decoder with standard international morse code"""
        self.current_sequence = []
        
        # International Morse Code dictionary
        self.morse_dict = {
            # Letters
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z',
            
            # Numbers
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
            '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0',
            
            # Punctuation
            '--..--': ',', '.-.-.-': '.', '..--..': '?', '.----.': "'", '-.-.--': '!',
            '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
            '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
            '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
            
            # Prosigns (procedural signals)
            '.-.-': 'AR',    # End of message
            '-...-': 'BT',   # Break/pause
            '...-.-': 'SK',  # End of work
            '...-.': 'VE',   # Understood
            '.-.-.': 'AR',   # Alternative AR
        }
        
        # Reverse dictionary for encoding (letter to morse)
        self.letter_dict = {v: k for k, v in self.morse_dict.items()}
        
        # Statistics
        self.stats = {
            'total_elements': 0,
            'total_letters': 0,
            'total_words': 0,
            'dots': 0,
            'dashes': 0,
            'errors': 0
        }
    
    def add_element(self, element):
        """
        Add a morse element (dot or dash) to the current sequence
        
        Args:
            element (str): Either '.' for dot or '-' for dash
        """
        if element in ['.', '-']:
            self.current_sequence.append(element)
            self.stats['total_elements'] += 1
            if element == '.':
                self.stats['dots'] += 1
            else:
                self.stats['dashes'] += 1
    
    def get_current_sequence(self):
        """
        Get the current morse sequence as a string
        
        Returns:
            str: Current sequence of dots and dashes
        """
        return ''.join(self.current_sequence)
    
    def has_sequence(self):
        """
        Check if there's a current sequence being built
        
        Returns:
            bool: True if there are elements in the current sequence
        """
        return len(self.current_sequence) > 0
    
    def decode_current_sequence(self):
        """
        Decode the current sequence to a letter and clear the sequence
        
        Returns:
            str: Decoded letter or None if sequence is invalid
        """
        if not self.current_sequence:
            return None
        
        sequence_str = ''.join(self.current_sequence)
        decoded_char = self.morse_dict.get(sequence_str)
        
        # Clear the sequence
        self.current_sequence = []
        
        if decoded_char:
            self.stats['total_letters'] += 1
            return decoded_char
        else:
            self.stats['errors'] += 1
            return f'[{sequence_str}]'  # Return unknown sequence in brackets
    
    def clear_sequence(self):
        """Clear the current morse sequence"""
        self.current_sequence = []
    
    def encode_text(self, text):
        """
        Encode text to morse code
        
        Args:
            text (str): Text to encode
            
        Returns:
            str: Morse code representation with spaces between letters
        """
        morse_words = []
        
        for word in text.upper().split():
            morse_letters = []
            for char in word:
                if char in self.letter_dict:
                    morse_letters.append(self.letter_dict[char])
                elif char == ' ':
                    continue  # Skip spaces within words
                else:
                    morse_letters.append(f'[{char}]')  # Unknown character
            morse_words.append(' '.join(morse_letters))
        
        return '  '.join(morse_words)  # Double space between words
    
    def validate_sequence(self, sequence):
        """
        Validate if a morse sequence is a known character
        
        Args:
            sequence (str): Morse sequence to validate
            
        Returns:
            tuple: (is_valid, character_or_none)
        """
        char = self.morse_dict.get(sequence)
        return char is not None, char
    
    def get_similar_sequences(self, sequence, max_suggestions=3):
        """
        Get similar valid sequences for error correction
        
        Args:
            sequence (str): Invalid morse sequence
            max_suggestions (int): Maximum number of suggestions
            
        Returns:
            list: List of (sequence, character) tuples for similar valid sequences
        """
        suggestions = []
        seq_len = len(sequence)
        
        # Look for sequences with similar length
        for morse_seq, char in self.morse_dict.items():
            if abs(len(morse_seq) - seq_len) <= 1:  # Within 1 element
                # Calculate similarity (simple character difference count)
                diff_count = sum(1 for i, c in enumerate(sequence) 
                               if i < len(morse_seq) and c != morse_seq[i])
                if diff_count <= 1:  # Allow 1 character difference
                    suggestions.append((morse_seq, char, diff_count))
        
        # Sort by similarity and return top suggestions
        suggestions.sort(key=lambda x: x[2])
        return [(seq, char) for seq, char, _ in suggestions[:max_suggestions]]
    
    def get_stats(self):
        """
        Get decoding statistics
        
        Returns:
            dict: Statistics dictionary
        """
        stats = self.stats.copy()
        if stats['total_elements'] > 0:
            stats['accuracy'] = (stats['total_letters'] / 
                               (stats['total_letters'] + stats['errors']) * 100)
            stats['dots_percentage'] = stats['dots'] / stats['total_elements'] * 100
            stats['dashes_percentage'] = stats['dashes'] / stats['total_elements'] * 100
        else:
            stats['accuracy'] = 0
            stats['dots_percentage'] = 0
            stats['dashes_percentage'] = 0
        
        return stats
    
    def reset_stats(self):
        """Reset all statistics"""
        self.stats = {
            'total_elements': 0,
            'total_letters': 0,
            'total_words': 0,
            'dots': 0,
            'dashes': 0,
            'errors': 0
        }
    
    def get_morse_reference(self):
        """
        Get a reference of all morse code characters
        
        Returns:
            dict: Dictionary organized by category
        """
        reference = {
            'letters': {},
            'numbers': {},
            'punctuation': {},
            'prosigns': {}
        }
        
        for morse, char in self.morse_dict.items():
            if char.isalpha() and len(char) == 1:
                reference['letters'][char] = morse
            elif char.isdigit():
                reference['numbers'][char] = morse
            elif len(char) == 1:
                reference['punctuation'][char] = morse
            else:
                reference['prosigns'][char] = morse
        
        return reference
    
    def is_valid_element(self, element):
        """
        Check if an element is a valid morse code element
        
        Args:
            element (str): Element to check
            
        Returns:
            bool: True if valid (. or -)
        """
        return element in ['.', '-']
    
    def format_sequence_display(self, sequence=None):
        """
        Format morse sequence for display with visual enhancements
        
        Args:
            sequence (str): Sequence to format (uses current if None)
            
        Returns:
            str: Formatted sequence
        """
        if sequence is None:
            sequence = self.get_current_sequence()
        
        # Replace dashes with longer visual representation
        formatted = sequence.replace('-', '—')  # Em dash for better visibility
        
        return formatted if formatted else "..."  # Show dots when empty