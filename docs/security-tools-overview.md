# Python Security & Utility Tools

A collection of educational Python tools for learning about cybersecurity concepts.

## Disclaimer

**ALL TOOLS ARE FOR EDUCATIONAL PURPOSES ONLY**

These tools are designed to help you **LEARN** about security concepts. Do NOT use them:
- For unauthorized access to systems
- For malicious purposes
- In any way that violates laws or ethical guidelines

**Always obtain proper authorization before testing any system.**

---

## Available Tools

### 1. Hash Cracker (`hash-cracker/`)

**Purpose**: Learn about password hashing and why it's important.

**Features**:
- Generate hashes (MD5, SHA1, SHA256, SHA512)
- Dictionary attack against wordlists
- Hash identification by length
- Educational security lessons

**Quick Start**:
```bash
cd hash-cracker
python hash-cracker.py -g password123      # Generate hashes
python hash-cracker.py <hash>             # Crack a hash
```

---

### 2. Port Scanner (`port-scanner/`)

**Purpose**: Learn about network scanning and port security.

**Features**:
- TCP port scanning (localhost and networks)
- Concurrent scanning for speed
- Service identification
- Network discovery

**Quick Start**:
```bash
cd port-scanner
python port-scanner.py localhost          # Scan localhost
python port-scanner.py 192.168.1.1 -p 1-1000  # Scan IP range
python port-scanner.py --discover         # Discover local network
```

---

### 3. SSH Key Generator (`ssh-keygen-tool/`)

**Purpose**: Learn about SSH key pairs and public-key cryptography.

**Features**:
- Generate RSA, Ed25519, ECDSA keys
- Key information display
- Security best practices
- SSH config generation

**Quick Start**:
```bash
cd ssh-keygen-tool
python ssh-keygen-tool.py -t ed25519 -f mykey  # Generate key
python ssh-keygen-tool.py --list              # List existing keys
```

---

### 4. Leak Checker (`leak-checker/`)

**Purpose**: Check if emails/passwords appear in data breaches.

**Features**:
- Email breach checking (HaveIBeenPwned API)
- Password breach checking (k-Anonymity)
- Paste dump checking
- Security recommendations

**Quick Start**:
```bash
cd leak-checker
python leak-checker.py user@example.com      # Check email
python leak-checker.py --password "mypass"   # Check password
```

---

### 5. SSL Certificate Checker (`cert-checker/`)

**Purpose**: Learn about SSL/TLS certificates and HTTPS security.

**Features**:
- Certificate inspection
- Expiration checking
- Issuer verification
- Security grading

**Quick Start**:
```bash
cd cert-checker
python cert-checker.py example.com           # Check certificate
python cert-checker.py example.com --json     # JSON output
```

---

## Learning Path

### Beginner

1. Start with **cert-checker** - Safe, no special permissions needed
2. Try **hash-cracker** - Understand password security
3. Explore **leak-checker** - Learn about data breaches

### Intermediate

4. Use **ssh-keygen-tool** - Master SSH authentication
5. Experiment with **port-scanner** - Network fundamentals

### Each Tool Teaches

| Tool | Concept | Real-World Application |
|------|---------|----------------------|
| hash-cracker | Cryptographic hashing | Password security, rainbow tables |
| port-scanner | TCP/IP networking | Network reconnaissance, firewall testing |
| ssh-keygen-tool | Public-key cryptography | Secure server access, authentication |
| leak-checker | Data breach exposure | Credential stuffing, account security |
| cert-checker | TLS/SSL certificates | HTTPS, man-in-the-middle prevention |

---

## Requirements

**All tools use Python standard library** - no external dependencies required!

- Python 3.6+
- Internet connection (for leak-checker and cert-checker)

### Optional Dependencies

```bash
# For ssh-keygen-tool (fallback key generation)
pip install paramiko

# For enhanced output
pip install colorama
```

---

## Security Lessons Summary

### Why These Tools Matter

Understanding these concepts helps you:

1. **Defend networks** - Know what attackers look for
2. **Protect accounts** - Use strong, unique passwords
3. **Secure communications** - Understand encryption
4. **Identify risks** - Recognize security issues
5. **Build secure systems** - Apply best practices

### Common Vulnerabilities

```
┌─────────────────────────────────────────────────────────────┐
│                     ATTACKER VIEW                           │
├─────────────────────────────────────────────────────────────┤
│  1. Reconnaissance - Port scan to find open services       │
│  2. Enumeration - Identify specific versions/services      │
│  3. Exploitation - Use known vulnerabilities                │
│  4. Persistence - Install backdoors/steal credentials       │
│  5. Exfiltration - Take data or encrypt for ransom         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     DEFENDER VIEW                           │
├─────────────────────────────────────────────────────────────┤
│  1. Minimize attack surface - Close unused ports            │
│  2. Strong authentication - SSH keys, 2FA                  │
│  3. Keep software updated - Patch vulnerabilities           │
│  4. Monitor and log - Detect suspicious activity           │
│  5. Incident response - Know what to do when breached       │
└─────────────────────────────────────────────────────────────┘
```

---

## Legal Notice

**These tools are for EDUCATIONAL purposes only.**

Unauthorized access to computer systems is illegal in most jurisdictions.

Always:
- Only scan/test systems you own or have written permission to test
- Use knowledge responsibly and ethically
- Follow responsible disclosure practices
- Report vulnerabilities to system owners

---

## Contributing

Found a bug or want to improve these tools?

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## Resources

### Learning More

- **OWASP**: https://owasp.org
- **SANS Institute**: https://www.sans.org
- **Cybrary**: https://www.cybrary.it
- **PortSwigger Academy**: https://portswigger.net/web-security

### Practice Platforms

- **Hack The Box**: https://www.hackthebox.eu
- **TryHackMe**: https://tryhackme.com
- **VulnHub**: https://www.vulnhub.com
- **OverTheWire**: https://overthewire.org

### Documentation

- Python `ssl` module: https://docs.python.org/3/library/ssl.html
- Python `socket` module: https://docs.python.org/3/library/socket.html
- HaveIBeenPwned API: https://haveibeenpwned.com/API/v3

---

## License

Educational use only. Use responsibly and legally.

---

**Remember**: The best security professionals use their knowledge to protect systems, not to break into them.
