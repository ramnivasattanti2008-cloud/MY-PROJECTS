# SSH Key Generator - Educational Security Tool

A Python tool that demonstrates SSH key pair generation for learning about public-key cryptography.

## What It Does

This tool demonstrates:

1. **Key Generation**: Create RSA, Ed25519, or ECDSA SSH key pairs
2. **Key Information**: View details about existing keys
3. **Key Listing**: List all SSH keys in your .ssh directory
4. **Security Education**: Learn SSH key best practices

## How SSH Keys Work

### Public-Key Cryptography Basics

```
                        ALICE                              BOB
                          |                                 |
                          |      [Generate Key Pair]        |
                          |      Private Key: SECRET        |
                          |      Public Key: SHAREABLE       |
                          |                                 |
  Bob has Alice's        |                                 |
  public key             |                                 |
        |                | [Public Key] ─────────────────> |
        |                |                                 |
        |                |              Alice encrypts     |
        |                |              message with        |
        |                |              Bob's public key    |
        |                |                                 |
        |                | [Encrypted] ──────────────────> |
        |                |                                 |
        |                |              Bob decrypts with   |
        |                |              his private key     |
        |                |                                 |
```

### SSH Authentication Flow

```
Client (has private key)              Server (has public key in authorized_keys)
       |                                           |
       |  1. Connect to server                     |
       | ────────────────────────────────────────> |
       |                                           |
       |  2. Server sends challenge                |
       | <──────────────────────────────────────── |
       |                                           |
       |  3. Client signs with private key         |
       | ────────────────────────────────────────> |
       |                                           |
       |  4. Server verifies with public key        |
       |     ACCESS GRANTED if valid!             |
       |                                           |
```

### Key Types Compared

| Algorithm | Key Size | Security | Speed   | Compatibility | Recommendation |
|-----------|----------|----------|---------|---------------|----------------|
| RSA       | 2048-4096 | Good    | Slow    | Excellent     | Legacy only    |
| Ed25519   | 256       | Excellent| Fast    | Modern        | **RECOMMENDED**|
| ECDSA     | 256-521   | Good    | Fast    | Good          | Alternative    |

## Installation

```bash
git clone <repository-url>
cd ssh-keygen-tool
pip install -r requirements.txt  # Optional: for paramiko fallback
```

**Requirements:**
- **Preferred**: OpenSSH installed (Linux/macOS have it by default; Windows 10+ or Git includes it)
- **Optional**: paramiko library for Python-based key generation

## Usage

### Generate Ed25519 Key (Recommended)

```bash
python ssh-keygen-tool.py -t ed25519 -f mykey -e user@example.com
```

### Generate RSA Key

```bash
python ssh-keygen-tool.py -t rsa -b 4096 -f server_key
```

### List Existing Keys

```bash
python ssh-keygen-tool.py --list
```

### View Key Information

```bash
python ssh-keygen-tool.py --info ~/.ssh/id_ed25519
```

## Command Line Options

| Option          | Description                           | Default           |
|-----------------|---------------------------------------|-------------------|
| `-t, --type`    | Key type (rsa, ed25519, ecdsa)       | ed25519           |
| `-b, --bits`    | Key size in bits (RSA/ECDSA only)   | 4096 / 521        |
| `-f, --filename`| Output filename                      | id_ed25519        |
| `-p, --passphrase` | Passphrase for private key        | None              |
| `-e, --email`   | Email address (in comment)            | None              |
| `-d, --directory`| Output directory                     | ~/.ssh/           |
| `--list`        | List existing SSH keys                | False             |
| `--info`        | Show info about a specific key        | None              |

## SSH Key Security

### Permission Settings

On Linux/macOS, set proper permissions:

```bash
# Private key - read/write for user only
chmod 600 ~/.ssh/id_ed25519

# Public key - readable by anyone
chmod 644 ~/.ssh/id_ed25519.pub

# SSH directory
chmod 700 ~/.ssh
```

### Using SSH-Agent

Cache your passphrase so you don't have to enter it every time:

```bash
# Start ssh-agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519

# Now SSH will use cached credentials
ssh user@server.com
```

### SSH Config File

Create `~/.ssh/config` for easy connections:

```
Host myserver
    HostName server.example.com
    User admin
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

Now connect with just: `ssh myserver`

## How SSH Keys Protect You

### Password vs Key Authentication

| Aspect           | Password                   | SSH Key                    |
|-----------------|----------------------------|----------------------------|
| Transmission    | Sent over network          | Never sent over network    |
| Storage         | Server stores hash         | Server stores only public  |
| Brute Force     | Vulnerable                 | Extremely difficult        |
| Phishing        | Susceptible                | Immune                     |
|遗忘           | Can forget                 | Back up required           |

### Why Ed25519 is Recommended

1. **Smaller keys**: 256 bits vs 4096 for RSA
2. **Faster**: 10x faster than RSA
3. **Smaller signatures**: Easier to manage
4. **Resistant**: Not vulnerable to certain RSA attacks
5. **Modern**: Designed by cryptographers in 2011

## Code Structure

```
ssh-keygen-tool/
├── ssh-keygen-tool.py    # Main tool
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Understanding Key Files

```
~/.ssh/
├── id_ed25519          # YOUR PRIVATE KEY - KEEP SECRET!
│                        # Do NOT share, upload, or lose this!
├── id_ed25519.pub      # Public key - can be shared
│                        # Add contents to server's authorized_keys
├── known_hosts         # Fingerprints of servers you've connected to
├── config             # Your SSH connection settings
└── authorized_keys     # (On servers) Public keys allowed to connect
```

## Adding Key to Server

### Method 1: ssh-copy-id

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server.com
```

### Method 2: Manual

```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub

# SSH to server
ssh user@server.com

# Add to authorized_keys
echo "ssh-ed25519 AAAA..." >> ~/.ssh/authorized_keys
```

## Security Best Practices

1. **Use Ed25519** for new keys
2. **Always use a passphrase** on private keys
3. **Protect your private key** file
4. **Rotate keys** periodically
5. **Use different keys** for different purposes
6. **Never share private keys**
7. **Backup keys** securely
8. **Use SSH agent** for convenience + security

## Troubleshooting

### "ssh-keygen not found"

Install OpenSSH:
- **Windows**: Install Git or Windows Subsystem for Linux
- **macOS**: Usually pre-installed
- **Linux**: `sudo apt install openssh-client` or equivalent

### "Permissions too open"

Fix permissions:
```bash
chmod 600 ~/.ssh/id_ed25519
chmod 700 ~/.ssh
```

### "Connection refused"

1. Verify server has SSH running
2. Check firewall allows port 22
3. Verify public key is in authorized_keys

## Legal Notice

This tool is for **educational purposes only**. Always follow ethical guidelines and use these concepts responsibly.

## License

Educational use only. Use responsibly.
