# Blowfish Encryption Demonstration

A comprehensive Computer Security project demonstrating the Blowfish encryption algorithm through two distinct implementations: an **educational manual walkthrough** and a **production-ready secure implementation**.

## Overview

Blowfish is a symmetric-key block cipher designed in 1993 by Bruce Schneier. It features:
- **Block Size:** 64-bit
- **Key Length:** Variable from 32 bits to 448 bits
- **Structure:** 16-round Feistel Network
- **Components:** Key expansion and data encryption. It uses four 8x32-bit S-boxes and one 18x32-bit P-array.

### Implementation Comparison

| Feature | `manual_blowfish.py` (Educational) | `secure_blowfish.py` (Production) |
| :--- | :--- | :--- |
| **Library** | Pure Python (No external dependencies) | PyCryptodome (C-optimized) |
| **Mode** | Electronic Codebook (ECB) | Cipher Block Chaining (CBC) |
| **Padding** | Simple Null Padding | PKCS7 Padding |
| **Security** | **Low (Academic Use Only)** | **High (Standard Cryptography)** |
| **Features** | Transparent internal logic | Random IVs, Base64 encoding |

---

## Security Notes

> [!WARNING]
> While Blowfish is significantly faster than DES and has no known major cryptanalytic breaks on the full 16 rounds, its **64-bit block size** makes it vulnerable to birthday attacks in high-bandwidth applications. **Modern systems should prefer AES (128-bit blocks or higher).**

## Requirements

The secure implementation requires the `pycryptodome` library.

```bash
pip install -r requirements.txt
```

---

## How to Run

The `demo.py` script provides a command-line interface for testing both string and file encryption.

### 1. Interactive Mode
Run the script without arguments to use the interactive menu:
```bash
python demo.py
```

### 2. String Encryption Demo
Provide a key and text via CLI arguments:
```bash
python demo.py --key "MySecretKey" --text "Hello, Computer Security!"
```

### 3. File Encryption Demo
Encrypt and decrypt a file securely:
```bash
python demo.py --key "SuperSecureKey" --file "secret_document.txt"
```

---

## Project Structure

- `manual_blowfish.py`: Contains the `ManualBlowfish` class. It implements the Feistel structure, F-function, and a simplified key schedule for educational clarity.
- `secure_blowfish.py`: Contains the `SecureBlowfish` class. Uses industry-standard practices including CBC mode and cryptographically secure IV management.
- `demo.py`: A CLI interface to bridge both implementations.
- `requirements.txt`: Project dependencies.
- `README.md`: Project documentation and security context.

---

## Academic Context

This project was built for a Computer Security course to demonstrate:
1. The mechanics of the **Feistel Network**.
2. The importance of **Initialization Vectors (IV)** and **Padding**.
3. Why library-grade implementations are preferred over manual ones for security.
