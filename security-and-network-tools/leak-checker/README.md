# Leak Checker - Educational Data Breach Checker

A Python tool that checks if emails or passwords have appeared in known data breaches using the HaveIBeenPwned API.

## Disclaimer

**WARNING: EDUCATIONAL PURPOSE ONLY**

This tool is for **LEARNING** about data breach exposure. Use responsibly:
- Check YOUR OWN email and passwords
- Do NOT use this to check others without permission
- Take action to protect your accounts based on results

## What It Does

This tool demonstrates:

1. **Email Breach Check**: Check if an email appears in known data breaches
2. **Password Breach Check**: Check if a password has been exposed (uses k-Anonymity)
3. **Paste Dump Check**: Check if email appears in paste site leaks
4. **Security Education**: Learn about breach exposure and protection

## How It Works

### Email Breach Check

```
Your Email ─────────────────────────────────────────> HaveIBeenPwned API
                                                           |
  "user@example.com" ─────────────────────────────────>    |
                                                           |
                                                           v
                                                    [Database Lookup]
                                                           |
                                                           v
                   <──────────────────────────────────────
                   |
  Response: Found in 5 breaches!
  - LinkedIn (2021)
  - Adobe (2013)
  - DropBox (2012)
  - ...
```

### Password Breach Check (k-Anonymity)

Your password never leaves your machine in plain text:

```
Step 1: Hash locally
  "password123" ──> SHA-1 ──> "ef92b778bafe771e89245b89ecbc08a..."

Step 2: Send only first 5 chars
              ef92b ──────────────────────────> HIBP API
              (prefix)

Step 3: API returns all matching hashes
  ef92b778bafe771e89245b89ecbc08a44a4e166c: 12345
  ef92bb1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d: 6789
  ef92b9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l: 2
  ...

Step 4: Check locally if YOUR hash is in the list
  Your hash: ef92b778bafe771e89245b89ecbc08a44a4e166c
  Found: 12,345 times in breaches!
  Status: COMPROMISED - DO NOT USE!
```

### k-Anonymity Explained

k-Anonymity ensures privacy by:

1. **Hashing**: Convert password to SHA-1 hash
2. **Partial send**: Only send first 5 characters of hash
3. **Server blind**: API doesn't know your full hash
4. **Local check**: Compare full hash locally

This means even if the API is compromised, your password remains hidden.

## Installation

```bash
git clone <repository-url>
cd leak-checker

# No dependencies required - uses Python standard library!
```

## Usage

### Check Email for Breaches

```bash
python leak-checker.py user@example.com
```

### Check Email with Paste Dumps

```bash
python leak-checker.py user@example.com --pastes
```

### Check if Password is Compromised

```bash
# Direct input
python leak-checker.py --password "myPassword123"

# Secure input (prompts for password)
python leak-checker.py --check-password
```

### Check Both Email and Password

```bash
python leak-checker.py user@example.com --check-password
```

## Understanding Results

### If Breaches Are Found

```
[!] WARNING: Your email was found in 5 data breaches!

BREACH #1: LinkedIn (2021)
  - 700 million users affected
  - Exposed: Email, phone, professional info

BREACH #2: Adobe (2013)
  - 153 million accounts
  - Exposed: Email, password hints, usernames

WHAT TO DO:
1. Change passwords for ALL affected accounts
2. Enable 2FA on important accounts
3. Use unique passwords going forward
4. Consider using a password manager
```

### If No Breaches Found

```
[OK] Good news! No breaches found for this email.

This doesn't mean:
- Your email is completely safe
- Your passwords are secure
- You're immune to future breaches

STAY SAFE:
- Use unique passwords
- Enable 2FA
- Use a password manager
- Check periodically
```

## Why This Matters

### Major Recent Breaches

| Breach | Year | Records | What Was Exposed |
|--------|------|---------|------------------|
| LinkedIn | 2021 | 700M | Emails, phone, professional data |
| Facebook | 2019 | 533M | Phone, location, birthdate |
| Yahoo | 2013 | 3B | Names, emails, security Q&A |
| Adobe | 2013 | 153M | Email, encrypted passwords |
| eBay | 2014 | 145M | Names, emails, passwords |

### How Your Data Gets Compromised

1. **Company Data Breach**: Hackers steal from company databases
2. **Phishing**: You unknowingly give credentials to attackers
3. **Credential Stuffing**: Reusing passwords on multiple sites
4. **Malware**: Keyloggers steal typed passwords
5. **Public Leaks**: Data from public records, social media

### What Attackers Do With Breached Data

```
Breached Data ──┬──> Sell on dark web
               │
               ├──> Credential stuffing attacks
               │     (try same password everywhere)
               │
               ├──> Identity theft
               │     (open accounts in your name)
               │
               ├──> Account takeover
               │     (steal money, data, access)
               │
               └──> Social engineering
                    (spear phishing with personal info)
```

## Security Recommendations

### Immediate Actions

1. **Change Passwords**
   - Any password found in a breach
   - Any password you reuse across sites
   - Default passwords on devices

2. **Enable 2FA**
   - Especially on email, banking, social media
   - Use authenticator app over SMS when possible

3. **Monitor Accounts**
   - Set up alerts for unusual activity
   - Check credit reports regularly
   - Review login history

### Long-term Security

1. **Use a Password Manager**
   - Generate unique, random passwords
   - Encrypted storage
   - Examples: Bitwarden, KeePass, 1Password

2. **Unique Passwords**
   - Never reuse passwords
   - Different password for every account

3. **Regular Checks**
   - Check your email periodically
   - Update passwords annually
   - Remove unused accounts

4. **Be Informed**
   - Know what data breaches you're in
   - Remove unnecessary data from services
   - Minimize your online footprint

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `email` | Email to check | `user@example.com` |
| `--password` | Check password | `--password "secret"` |
| `--check-password` | Secure password prompt | Interactive |
| `--pastes` | Include paste dumps | Check pastes too |
| `--no-unverified` | Exclude unverified breaches | Cleaner results |
| `-q, --quiet` | Minimal output | Script-friendly |

## API Information

This tool uses the **HaveIBeenPwned.com** free API:

- **Rate Limit**: 1 request per 1.6 seconds
- **Authentication**: None required (free tier)
- **Privacy**: No data stored, minimal logging
- **Website**: https://haveibeenpwned.com

### k-Anonymity for Passwords

The password check uses the **Pwned Passwords API**:

- **Endpoint**: `https://api.pwnedpasswords.com/range/{hash_prefix}`
- **Privacy**: Only sends first 5 chars of SHA-1 hash
- **Data**: Over 600 million passwords
- **Research**: Troy Hunt's research and collection

## Code Structure

```
leak-checker/
├── leak-checker.py   # Main tool
├── requirements.txt  # No external dependencies
└── README.md        # This file
```

## Technical Details

### Email Breach Check

```python
# API call for email breach check
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
request = urllib.request.Request(url, headers={"User-Agent": "..."})
response = urllib.request.urlopen(request)
breaches = json.loads(response.read())
```

### Password Check with k-Anonymity

```python
# Hash password locally
sha1 = hashlib.sha1(password.encode()).hexdigest().upper()

# Send only prefix
prefix = sha1[:5]
url = f"https://api.pwnedpasswords.com/range/{prefix}"

# Parse response and check locally
# API never sees your full hash or password!
```

## Legal Notice

This tool is for **educational purposes only**. Always:
- Check only your own accounts
- Respect privacy and legal boundaries
- Use results to improve your security
- Never use this for malicious purposes

## Resources

- HaveIBeenPwned: https://haveibeenpwned.com
- Pwned Passwords: https://haveibeenpwned.com/Passwords
- OWASP Password Guidelines: https://cheatsheetseries.owasp.org
- Have I Been Pwned API: https://haveibeenpwned.com/API/v3

## License

Educational use only. Use responsibly and legally.
