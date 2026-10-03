# File Encrypter

A Python utility for encrypting and decrypting files using Fernet symmetric encryption.

## Features

- **Fernet Symmetric Encryption**: Industry-standard encryption with built-in authentication
- **Secure Key Derivation**: Uses PBKDF2 with 480,000 iterations to derive keys from passwords
- **Salt Protection**: Random salt generation prevents rainbow table attacks
- **File Integrity**: Fernet includes HMAC for tamper detection
- **Educational**: Well-commented code explains encryption concepts

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Encrypt a File

```bash
python file-encrypter.py encrypt myfile.txt
```

You'll be prompted for a password. Or provide it via command line:

```bash
python file-encrypter.py encrypt myfile.txt -p MySecretPassword
```

The encrypted file will be saved as `myfile.txt.encrypted`.

### Decrypt a File

```bash
python file-encrypter.py decrypt myfile.txt.encrypted
```

Provide the password when prompted.

### Custom Output Path

```bash
python file-encrypter.py encrypt document.pdf -o encrypted_document.bin
python file-encrypter.py decrypt encrypted_document.bin -o restored_document.pdf
```

### Use a Specific Salt (for reproducible key derivation)

```bash
# First encryption
python file-encrypter.py encrypt file.txt -s 0123456789abcdef0123456789abcdef

# Decryption with same salt
python file-encrypter.py decrypt file.txt.encrypted -s 0123456789abcdef0123456789abcdef
```

## How It Works

### Encryption Process

1. **Password Input**: User provides a password
2. **Salt Generation**: Random 16-byte salt is generated
3. **Key Derivation**: PBKDF2-HMAC-SHA256 derives a 32-byte key (480,000 iterations)
4. **Encryption**: Fernet encrypts the file data (uses AES-128-CBC + HMAC-SHA256)
5. **Output**: Salt + ciphertext written to file

### Security Features

| Feature | Description |
|---------|-------------|
| PBKDF2 | Prevents GPU-accelerated brute force attacks |
| Random Salt | Each encryption produces different ciphertext |
| Fernet | Provides confidentiality + integrity + authentication |
| No Key Storage | Password is never saved; only used to derive key |

## File Format

```
┌─────────────┬──────────────────────────┐
│   Salt      │      Ciphertext          │
│  (16 bytes) │   (Fernet encrypted)      │
└─────────────┴──────────────────────────┘
```

## Important Notes

1. **No Password Recovery**: There is no backdoor. If you forget your password, the data is unrecoverable.

2. **Password Strength**: Use strong passwords (12+ characters with mixed case, numbers, symbols).

3. **Key Reuse**: The same password with different salts produces different ciphertexts, but it's best to use different passwords for different files when possible.

4. **Large Files**: This implementation loads entire files into memory. For very large files, consider chunk-based encryption.

## License

MIT License - Educational purposes
