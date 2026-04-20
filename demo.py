import sys
import os
import argparse
import base64
from manual_blowfish import ManualBlowfish
from secure_blowfish import SecureBlowfish, HAS_PYCRYPTODOME

def print_banner():
    print("=" * 60)
    print("      BLOWFISH ENCRYPTION DEMONSTRATION SYSTEM")
    print("=" * 60)

def handle_string_demo(key: str, text: str):
    print("\n[+] DEMO 1: Educational Implementation (ManualBlowfish)")
    print("    Warning: Simplified S-boxes, ECB mode, No padding security.")
    try:
        manual_cipher = ManualBlowfish(key.encode('utf-8'))
        manual_enc = manual_cipher.encrypt_message(text.encode('utf-8'))
        manual_b64 = base64.b64encode(manual_enc).decode('utf-8')
        print(f"    - Ciphertext (Base64): {manual_b64}")
        
        manual_dec = manual_cipher.decrypt_message(manual_enc).decode('utf-8')
        print(f"    - Decrypted text:      {manual_dec}")
    except Exception as e:
        print(f"    - Error: {e}")

    print("\n[+] DEMO 2: Production Implementation (SecureBlowfish)")
    print("    Features: CBC mode, PKCS7 padding, Random IV, Secure library.")
    
    if not HAS_PYCRYPTODOME:
        print("    [!] Warning: SecureBlowfish is unavailable because 'pycryptodome' is not installed.")
        print("        Run 'pip install -r requirements.txt' to enable this feature.")
        return

    try:
        secure_cipher = SecureBlowfish(key)
        secure_enc = secure_cipher.encrypt_string(text)
        print(f"    - Secure Ciphertext (IV+Msg B64): {secure_enc}")
        
        secure_dec = secure_cipher.decrypt_string(secure_enc)
        print(f"    - Decrypted text:                {secure_dec}")
    except Exception as e:
        print(f"    - Error: {e}")

def handle_file_demo(key: str, input_file: str):
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' not found.")
        return

    encrypted_file = input_file + ".enc"
    decrypted_file = input_file + ".dec"

    print(f"\n[+] Production File Encryption (SecureBlowfish)")
    
    if not HAS_PYCRYPTODOME:
        print("    [!] Error: File encryption requires 'pycryptodome'. Please install it first.")
        return

    try:
        secure_cipher = SecureBlowfish(key)
        
        # Encrypt
        print(f"    - Encrypting '{input_file}' to '{encrypted_file}'...")
        secure_cipher.encrypt_file(input_file, encrypted_file)
        
        # Decrypt
        print(f"    - Decrypting '{encrypted_file}' to '{decrypted_file}'...")
        secure_cipher.decrypt_file(encrypted_file, decrypted_file)
        
        print(f"    - Success! Check '{decrypted_file}' to verify content.")
    except Exception as e:
        print(f"    - Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Blowfish Encryption Demonstration CLI")
    parser.add_argument("--key", type=str, help="Encryption key (4-56 characters)")
    parser.add_argument("--text", type=str, help="Text message to encrypt")
    parser.add_argument("--file", type=str, help="Path to file for encryption/decryption demo")
    
    args = parser.parse_args()

    print_banner()

    # Get key
    key = args.key
    if not key:
        key = input("[?] Enter encryption key (4-56 characters): ").strip()

    if not (4 <= len(key) <= 56):
        print("[-] Error: Key length must be between 4 and 56 characters.")
        sys.exit(1)

    # Mode selection
    if args.file:
        handle_file_demo(key, args.file)
    elif args.text:
        handle_string_demo(key, args.text)
    else:
        # Interactive mode
        print("\n[ Selection ]")
        print("1. Encrypt/Decrypt Text (String Demo)")
        print("2. Encrypt/Decrypt File (File Demo)")
        choice = input("\n[?] Select an option (1/2): ").strip()
        
        if choice == '1':
            text = input("[?] Enter text to encrypt: ")
            handle_string_demo(key, text)
        elif choice == '2':
            file_path = input("[?] Enter file path: ")
            handle_file_demo(key, file_path)
        else:
            print("[-] Invalid choice.")

if __name__ == "__main__":
    main()
