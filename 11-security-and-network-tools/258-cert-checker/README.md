# SSL Certificate Checker - Educational Security Tool

A Python tool that demonstrates SSL/TLS certificate inspection for learning about web security and HTTPS implementation.

## Disclaimer

**WARNING: EDUCATIONAL PURPOSE ONLY**

This tool is for **LEARNING** about SSL/TLS certificates. Do NOT use this tool:
- To impersonate websites
- For malicious certificate spoofing
- For any unauthorized activities

Always use certificates ethically and legally.

## What It Does

This tool demonstrates:

1. **Certificate Inspection**: View SSL/TLS certificate details
2. **Expiration Checking**: Check if certificates are valid or expired
3. **Issuer Verification**: Examine certificate authority information
4. **Hostname Validation**: Check certificate-hostname matching
5. **Security Grading**: Simple security assessment

## How SSL/TLS Works

### TLS Handshake Overview

```
Client (Browser)                          Server
      |                                       |
      |  1. Client Hello (TLS version,        |
      |     supported ciphers)                |
      | ────────────────────────────────────> |
      |                                       |
      |  2. Server Hello (chosen cipher)      |
      |     + Server Certificate              |
      | <──────────────────────────────────── |
      |                                       |
      |  3. Key Exchange                      |
      |     (Client key exchange)             |
      | ────────────────────────────────────> |
      |                                       |
      |  4. Finished                          |
      | <──────────────────────────────────── |
      |                                       |
      |  [Encrypted Connection Established]   |
```

### Certificate Chain

```
                    Root CA (Certificate Authority)
                    | Self-signed, trusted by OS/browser
                    |
                    +-- Intermediate CA 1
                        | Signed by Root
                        |
                        +-- Intermediate CA 2
                            | Signed by CA 1
                            |
                            +-- YOUR CERTIFICATE
                                | Signed by CA 2
                                | Issued for your domain
```

### What Certificates Contain

```json
{
  "Subject": {
    "commonName": "example.com",
    "organizationName": "Example Inc."
  },
  "Issuer": {
    "commonName": "Let's Encrypt Authority X3",
    "organizationName": "Let's Encrypt"
  },
  "Validity": {
    "notBefore": "2024-01-01 00:00:00",
    "notAfter": "2024-04-01 00:00:00"
  },
  "SubjectAlternativeNames": [
    "example.com",
    "www.example.com"
  ],
  "PublicKey": {
    "algorithm": "RSA",
    "size": 2048
  }
}
```

## Installation

```bash
git clone <repository-url>
cd cert-checker

# No dependencies required - uses Python standard library!
```

## Usage

### Check a Website Certificate

```bash
python cert-checker.py example.com
```

### Check with URL

```bash
python cert-checker.py https://example.com
```

### Check Custom Port

```bash
python cert-checker.py example.com:8443
```

### JSON Output (for scripting)

```bash
python cert-checker.py example.com --json
```

### Check Expiration Details

```bash
python cert-checker.py example.com --check-expiry
```

### Verbose Output

```bash
python cert-checker.py example.com -v
```

## Understanding Results

### Sample Output

```
============================================================
                  SSL CERTIFICATE INFORMATION
============================================================

  Target:        example.com
  Common Name:   example.com
  Organization:  Example Inc.

  Issuer:
    Common Name:   Let's Encrypt Authority X3
    Organization:  Let's Encrypt

  Validity:
    Valid From:   2024-01-01 00:00:00 UTC
    Valid Until:  2024-04-01 00:00:00 UTC
    Days Remaining: 90 days

  Valid Hostnames:
    - example.com
    - www.example.com

  Security Grade: A

============================================================
```

### Security Grades

| Grade | Meaning                              |
|-------|--------------------------------------|
| A     | Excellent - Valid, well-configured   |
| B     | Good - Minor issues                  |
| C     | Fair - Some concerns                 |
| D     | Poor - Significant issues           |
| F     | Failing - Critical problems         |

## Certificate Security Issues

### Expired Certificate

```
[!] WARNING: Certificate has expired!

What this means:
- The website hasn't renewed their certificate
- Connection may be insecure
- Browser will show warning

What to do:
- Don't enter sensitive data
- Contact the website owner
```

### Self-Signed Certificate

```
[!] Certificate is self-signed (not from trusted CA)

What this means:
- Certificate wasn't verified by trusted CA
- Could be legitimate or a phishing attempt
- Common on internal/dev servers

What to do:
- Verify you trust the website
- Don't trust on public websites
```

### Hostname Mismatch

```
[!] Certificate hostname mismatch!

What this means:
- Certificate is for different domain
- Possible phishing site
- Configuration error

What to do:
- Don't proceed to the site
- Check the URL carefully
- Report suspicious sites
```

## SSL/TLS Best Practices

### For Website Owners

1. **Use Trusted CAs**
   - Let's Encrypt (free)
   - DigiCert
   - Comodo
   - GoDaddy

2. **Keep Certificates Updated**
   - Set renewal reminders (30 days before)
   - Use automatic renewal where possible
   - Monitor certificate expiration

3. **Strong Configuration**
   - TLS 1.2 or 1.3 only
   - Strong ciphers (AES-256)
   - HSTS enabled
   - OCSP stapling

4. **Complete Certificate Chain**
   - Include all intermediate certificates
   - Test with SSL Labs

### For Users

1. **Trust Browser Warnings**
   - Don't ignore certificate errors
   - Ask yourself why the warning appears

2. **Keep Browsers Updated**
   - Modern browsers have current CA stores
   - Security fixes are included in updates

3. **Check Before Entering Sensitive Data**
   - Look for HTTPS + lock icon
   - Verify correct domain name
   - Don't proceed past warnings

4. **Report Suspicious Sites**
   - Phishing sites with bad certs
   - Expired certs on login pages

## Certificate Types

### Domain Validation (DV)

```
Verification: Domain ownership only
Time to issue: Minutes to hours
Cost: Free (Let's Encrypt) to $10-50
Use: Most websites, blogs
```

### Organization Validation (OV)

```
Verification: Domain + organization identity
Time to issue: Days to weeks
Cost: $50-200/year
Use: Business websites
```

### Extended Validation (EV)

```
Verification: Strict domain + organization + legal entity
Time to issue: Weeks
Cost: $200-500/year
Use: Banks, high-security sites
Display: Green address bar in browser
```

## SSL/TLS Protocols

### Protocol Versions

| Version | Status | Notes |
|---------|--------|-------|
| SSL 2.0 | Deprecated | Insecure, don't use |
| SSL 3.0 | Deprecated | POODLE vulnerability |
| TLS 1.0 | Deprecated | Security concerns |
| TLS 1.1 | Deprecated | Security concerns |
| TLS 1.2 | Recommended | Current standard |
| TLS 1.3 | Recommended | Latest, fastest, most secure |

### Cipher Suites

Strong ciphers to look for:
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- ECDHE-RSA-AES256-GCM-SHA384

Weak ciphers to avoid:
- RC4
- DES
- 3DES
- MD5

## How to Verify Certificates

### Online Tools

1. **SSL Labs SSL Test**
   - https://www.ssllabs.com/ssltest/
   - Comprehensive analysis

2. **crt.sh**
   - https://crt.sh/
   - Certificate Transparency logs

3. **Certificate Transparency**
   - View all issued certificates
   - Detect unauthorized certs

### Command Line

```bash
# OpenSSL
openssl s_client -connect example.com:443 -showcerts

# Check certificate
openssl x509 -in cert.pem -text -noout

# Check expiration
openssl x509 -in cert.pem -noout -dates
```

## Code Structure

```
cert-checker/
├── cert-checker.py   # Main tool
├── requirements.txt  # No external dependencies
└── README.md        # This file
```

## Technical Details

### Getting Certificate with Python

```python
import ssl
import socket

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection(("example.com", 443)) as sock:
    with context.wrap_socket(sock, server_hostname="example.com") as ssock:
        cert = ssock.getpeercert()
        print(cert)
```

### Parsing Certificate

```python
from urllib.parse import urlparse

url = "https://example.com:443/path"
parsed = urlparse(url)
host = parsed.hostname  # "example.com"
port = parsed.port or 443  # 443
```

## Legal Notice

This tool is for **educational purposes only**. Always:
- Use certificates ethically
- Don't impersonate websites
- Respect security and privacy
- Report vulnerabilities responsibly

## Resources

- OWASP TLS Cheat Sheet: https://cheatsheetseries.owasp.org
- SSL Labs: https://www.ssllabs.com
- Mozilla SSL Configuration Generator
- Let's Encrypt: https://letsencrypt.org

## License

Educational use only. Use responsibly and legally.
