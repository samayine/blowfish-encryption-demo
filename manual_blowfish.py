"""
Educational Implementation of the Blowfish Encryption Algorithm.

WARNING:
This is an educational implementation designed to demonstrate the internal workings
of the Blowfish cipher, such as its Feistel network structure, F-function, and key schedule.
It uses a simplified initialization for S-boxes and P-arrays to keep the code readable.
DO NOT USE THIS FOR REAL CRYPTOGRAPHY. It is NOT secure. For production environments,
always use a vetted cryptographic library such as PyCryptodome.

Overview:
- 64-bit block size (split into two 32-bit halves)
- 16 rounds of Feistel network
- F-Function using simplified S-boxes
- Key-dependent variations via a key schedule
"""

import struct
from typing import List, Tuple

# Constants
ROUNDS = 16

class ManualBlowfish:
    def __init__(self, key: bytes):
        """
        Initializes the Blowfish cipher with a custom key.
        The P-array and S-boxes are typically initialized with the digits of pi.
        For this simplified educational version, we generate pseudo-random initial values.
        """
        if not key:
            raise ValueError("Key cannot be empty.")
            
        # In actual Blowfish, P-array is 18 32-bit integers,
        # S-boxes are four arrays of 256 32-bit integers.
        # We start with pseudo-random mock initial states.
        self.p_array = self._generate_mock_initial_p()
        self.s_boxes = self._generate_mock_initial_s()
        
        # Key Schedule: XOR P-array with the key, then encrypt an all-zero block
        # iteratively to replace P-array and S-boxes.
        self._key_schedule(key)

    def _generate_mock_initial_p(self) -> List[int]:
        """Minimal mock initialization for P-array"""
        return [(0x243f6a88 ^ (i * 0x85a308d3)) & 0xFFFFFFFF for i in range(ROUNDS + 2)]

    def _generate_mock_initial_s(self) -> List[List[int]]:
        """Minimal mock initialization for the 4 S-boxes (256 entries each)"""
        return [[(0x13198a2e ^ (i * j * 0x03707344)) & 0xFFFFFFFF for j in range(256)] for i in range(4)]

    def _f_function(self, x: int) -> int:
        """
        The F-function: splits 32-bit input into four 8-bit quarters.
        Operates on them via the four S-boxes.
        """
        a = (x >> 24) & 0xFF
        b = (x >> 16) & 0xFF
        c = (x >> 8) & 0xFF
        d = x & 0xFF

        # F(x) = (((S1[a] + S2[b]) ^ S3[c]) + S4[d]) mod 2^32
        res = (self.s_boxes[0][a] + self.s_boxes[1][b]) & 0xFFFFFFFF
        res = (res ^ self.s_boxes[2][c])
        res = (res + self.s_boxes[3][d]) & 0xFFFFFFFF
        return res

    def _key_schedule(self, key: bytes):
        """
        Expands the key into the P-array and S-boxes.
        """
        key_len = len(key)
            
        # XOR P-array with the key
        for i in range(ROUNDS + 2):
            # Form 32-bit word from the key
            key_word = 0
            for j in range(4):
                key_word = (key_word << 8) | key[(i * 4 + j) % key_len]
            self.p_array[i] ^= key_word

        # Iteratively encrypt an all-zero block to replace P-array and S-boxes
        l, r = 0, 0
        
        # Replace P-array
        for i in range(0, ROUNDS + 2, 2):
            l, r = self._encrypt_block(l, r)
            self.p_array[i] = l
            self.p_array[i+1] = r

        # Replace S-boxes
        for i in range(4):
            for j in range(0, 256, 2):
                l, r = self._encrypt_block(l, r)
                self.s_boxes[i][j] = l
                self.s_boxes[i][j+1] = r

    def _encrypt_block(self, l: int, r: int) -> Tuple[int, int]:
        """
        Encrypts a 64-bit block split into two 32-bit halves (l, r).
        Uses 16 rounds of the Feistel network.
        """
        for i in range(ROUNDS):
            l ^= self.p_array[i]
            r ^= self._f_function(l)
            l, r = r, l # Swap

        # Undo last swap and XOR with last two P-array entries
        l, r = r, l
        r ^= self.p_array[ROUNDS]
        l ^= self.p_array[ROUNDS + 1]

        return l, r

    def _decrypt_block(self, l: int, r: int) -> Tuple[int, int]:
        """
        Decrypts a 64-bit block split into two 32-bit halves (l, r).
        Runs the Feistel network in reverse.
        """
        for i in range(ROUNDS + 1, 1, -1):
            l ^= self.p_array[i]
            r ^= self._f_function(l)
            l, r = r, l # Swap

        # Undo last swap and XOR with first two P-array entries
        l, r = r, l
        r ^= self.p_array[1]
        l ^= self.p_array[0]

        return l, r

    def encrypt_message(self, message: bytes) -> bytes:
        """
        Encrypts a byte message using ECB mode (for educational simplicity).
        Zero-pads the message to a multiple of 8 bytes (64 bits).
        """
        # zero padding
        padding_len = (8 - len(message) % 8) % 8
        padded_msg = message + b'\0' * padding_len
        ciphertext = bytearray()

        for i in range(0, len(padded_msg), 8):
            block = padded_msg[i:i+8]
            l, r = struct.unpack('>LL', block)
            enc_l, enc_r = self._encrypt_block(l, r)
            ciphertext.extend(struct.pack('>LL', enc_l, enc_r))

        return bytes(ciphertext)

    def decrypt_message(self, ciphertext: bytes) -> bytes:
        """
        Decrypts a byte message using ECB mode.
        """
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext length must be a multiple of 8 bytes.")
            
        plaintext = bytearray()
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            l, r = struct.unpack('>LL', block)
            dec_l, dec_r = self._decrypt_block(l, r)
            plaintext.extend(struct.pack('>LL', dec_l, dec_r))

        return bytes(plaintext).rstrip(b'\0')
