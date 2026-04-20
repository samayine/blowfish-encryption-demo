"""
Production-Ready Blowfish Implementation.

This module uses PyCryptodome to provide a secure implementation of Blowfish.
Security Best Practices Included:
- Cipher Block Chaining (CBC) Mode (instead of insecure ECB)
- Cryptographically secure random Initialization Vector (IV)
- Standard PKCS7 Padding for handling arbitrary message lengths
- Base64 encoding for safe transport and storage of string data
- IV prepended to the ciphertext
"""

import base64
import os
from typing import Union

try:
    from Crypto.Cipher import Blowfish
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    HAS_PYCRYPTODOME = True
except ImportError:
    HAS_PYCRYPTODOME = False

class SecureBlowfish:
    def __init__(self, key: Union[str, bytes]):
        """
        Initializes the secure Blowfish encryption class.
        """
        if not HAS_PYCRYPTODOME:
            raise ImportError(
                "PyCryptodome is not installed. Please run 'pip install -r requirements.txt' "
                "to use the secure implementation."
            )
            
        if isinstance(key, str):
            key = key.encode('utf-8')
            
        # Blowfish keys must be between 4 and 56 bytes.
        if len(key) < 4 or len(key) > 56:
            raise ValueError("Blowfish key length must be between 4 and 56 bytes.")
        
        self.key = key
        self.block_size = Blowfish.block_size # 8 bytes

    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypts a string and returns a base64 encoded string containing IV + Ciphertext.
        """
        # 1. Generate a random IV for CBC
        iv = get_random_bytes(self.block_size)
        
        # 2. Instantiate cipher
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        
        # 3. Apply PKCS7 padding to plaintext
        padded_data = pad(plaintext.encode('utf-8'), self.block_size)
        
        # 4. Encrypt
        ciphertext = cipher.encrypt(padded_data)
        
        # 5. Prepend IV and base64 encode
        combined = iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    def decrypt_string(self, b64_ciphertext: str) -> str:
        """
        Decrypts a base64 encoded string (IV + Ciphertext) and returns the original string.
        """
        try:
            combined = base64.b64decode(b64_ciphertext)
            if len(combined) < self.block_size:
                raise ValueError("Ciphertext is too short to contain an IV.")
            
            # 1. Extract IV and ciphertext
            iv = combined[:self.block_size]
            ciphertext = combined[self.block_size:]
            
            # 2. Instantiate cipher
            cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
            
            # 3. Decrypt
            padded_data = cipher.decrypt(ciphertext)
            
            # 4. Remove PKCS7 padding
            plaintext = unpad(padded_data, self.block_size)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed. Invalid key or corrupted data. ({e})")

    def encrypt_file(self, input_path: str, output_path: str):
        """
        Encrypts a file securely using Blowfish CBC mode.
        Reads the entire file, pads it, and writes the IV + ciphertext to the output file.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        iv = get_random_bytes(self.block_size)
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        
        with open(input_path, 'rb') as f_in:
            plaintext = f_in.read()
            
        padded_data = pad(plaintext, self.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
        with open(output_path, 'wb') as f_out:
            f_out.write(iv) # Prepended immediately before ciphertext
            f_out.write(ciphertext)

    def decrypt_file(self, input_path: str, output_path: str):
        """
        Decrypts a file securely using Blowfish CBC mode.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with open(input_path, 'rb') as f_in:
            iv = f_in.read(self.block_size)
            if len(iv) < self.block_size:
                raise ValueError("File is too short to contain an IV.")
            
            ciphertext = f_in.read()
            
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        
        try:
            padded_data = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_data, self.block_size)
        except Exception as e:
            raise ValueError(f"Decryption failed. Invalid key, wrong file format, or corrupted data. ({e})")
            
        with open(output_path, 'wb') as f_out:
            f_out.write(plaintext)
