# Hash Cracker - Educational Security Tool

A Python tool that demonstrates password hash vulnerabilities through dictionary attacks.

## Disclaimer

**WARNING: EDUCATIONAL PURPOSE ONLY**

This tool is designed for **LEARNING** about password security. Do NOT use this tool:
- To access accounts or systems you don't own
- For any unauthorized activities
- For malicious purposes

Always obtain proper authorization before testing any system.

## What It Does

This tool demonstrates:

1. **Hash Generation**: Create hashes for any password using MD5, SHA1, SHA256, or SHA512
2. **Dictionary Attack**: Check if a hash matches passwords in a wordlist
3. **Hash Identification**: Auto-detect hash algorithm based on length
4. **Security Education**: Learn why proper password hashing matters

## How It Works

### Hashing Basics

```
Password: "password123"
        |
        v
    [HASH]  -->  "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
        |
        v
    Stored in database (NOT the password!)
```

Hashing is a **one-way function**: you can compute a hash from a password, but you cannot reverse it.

### Dictionary Attack

A dictionary attack tries common passwords against hashes:

```
Hash: "5f4dcc3b5aa765d61d8327deb882cf99"
        |
        v
Try "123456"   --> Hash --> Compare --> No match
Try "password" --> Hash --> Compare --> No match
Try "dragon"   --> Hash --> Compare --> No match
...
Try "password123" --> Hash --> Compare --> MATCH! Found!
```

### Hash Lengths

| Algorithm | Length | Example |
|-----------|--------|---------|
| MD5       | 32 hex | `5f4dcc3b5aa765d61d8327deb882cf99` |
| SHA1      | 40 hex | `96e79218965eb72c92a549dd5a330112` |
| SHA256    | 64 hex | `ef92b778bafe771e89245b89ecbc08a...` |
| SHA512    | 128 hex| `ef92b778bafe771e89245b89ecbc08a...` |

## Installation

```bash
# No dependencies required - uses Python standard library!
git clone <repository-url>
cd hash-cracker
```

## Usage

### Generate hashes for a password

```bash
python hash-cracker.py -g password123
```

Output:
```
[*] Generating hashes for: 'password123'
[*] Password length: 11 characters

  md5      : 482c811da5d5b4bc6d497ffa98491e38
  sha1     : 96e79218965eb72c92a549dd5a330112
  sha256   : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  sha512   : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f...
```

### Crack a hash (auto-detect algorithm)

```bash
python hash-cracker.py 5f4dcc3b5aa765d61d8327deb882cf99
```

### Crack with specific algorithm

```bash
python hash-cracker.py 5f4dcc3b5aa765d61d8327deb882cf99 -a md5
```

### Check hash information

```bash
python hash-cracker.py -i e10adc3949ba59abbe56e057f20f883e
```

## Security Lessons

### Why Hashing Matters

1. **Plaintext is dangerous**: If database is leaked, all passwords are exposed
2. **Hashing protects**: Even if hash is stolen, password remains hidden
3. **Salting is essential**: Random salt prevents rainbow table attacks
4. **Strong algorithms**: MD5/SHA1 are broken; use bcrypt/Argon2

### Rainbow Tables

A rainbow table is a precomputed list of hash -> password mappings:

```
Table lookup: "5f4dcc3b5aa765d61d8327deb882cf99"  -->  "password"
```

**Defense against rainbow tables:**
- Use unique salt per password
- Use slow hash functions (bcrypt, Argon2, scrypt)
- Never use MD5 or SHA1 for passwords

### Good Password Practices

1. **Length over complexity**: 16+ characters is better than complex short ones
2. **Unique passwords**: Never reuse passwords across sites
3. **Password manager**: Use Bitwarden, KeePass, or 1Password
4. **Two-factor authentication**: Enable 2FA wherever possible
5. **Check breaches**: Use HaveIBeenPwned.com to check if your email was in a breach

## Code Structure

```
hash-cracker/
├── hash-cracker.py   # Main CLI tool
├── wordlist.py       # Embedded wordlist (educational sample)
├── requirements.txt  # No external dependencies
└── README.md         # This file
```

## Real-World Hashing

For actual password hashing, use proven libraries:

```python
# Python - bcrypt (recommended)
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Python - argon2-cffi
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)

# Node.js - bcrypt
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);
```

## Legal Notice

This tool is for **educational purposes only**. Unauthorized access to computer systems is illegal in most jurisdictions. Always:
- Get written permission before testing any system
- Follow responsible disclosure practices
- Use these concepts to improve security, not break it

## License

Educational use only. Use responsibly.
