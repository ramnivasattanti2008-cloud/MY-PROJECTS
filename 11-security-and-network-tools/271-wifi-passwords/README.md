# WiFi Passwords

A Windows utility to view saved WiFi passwords stored on your computer. View all saved WiFi networks or look up specific passwords.

## WARNING

**This tool accesses sensitive network information.**

- Requires administrator privileges to reveal passwords
- Only use on your own computer
- WiFi passwords may be visible to anyone watching your screen
- Use responsibly and ethically

## Features

- List all saved WiFi profiles
- Show password for any specific network
- Display all saved WiFi passwords at once
- Export results to text file
- JSON output format
- Colorful terminal interface
- Admin privilege checker

## Installation

No installation required! Just download and run.

```bash
python wifi-passwords.py
```

## Usage

### View All Saved Passwords

```bash
# Run as administrator for full access
python wifi-passwords.py --all
```

### List All WiFi Profiles

```bash
python wifi-passwords.py --list
```

### Get Password for Specific Network

```bash
python wifi-passwords.py --password "MyHomeWiFi"
```

### Export to Text File

```bash
python wifi-passwords.py --export wifi_passwords.txt
```

### JSON Output

```bash
python wifi-passwords.py --all --json
```

### Check Admin Status

```bash
python wifi-passwords.py --admin-check
```

## Examples

### View all passwords with formatted table

```
    ╔═══════════════════════════════════════════════╗
    ║          WiFi Passwords Viewer v1.0            ║
    ╚═══════════════════════════════════════════════╝

Fetching all WiFi passwords...

Network Name         Auth           Password
----------------------------------------------------
HomeWiFi_5G          WPA2-Personal  mysecretpassword123
OfficeNetwork        WPA2-Enterprise ********
GuestWiFi            WPA2-Personal  guest12345
NeighborsWiFi        WPA2-Personal  neighborpass456

Total: 4 networks
```

### Get specific password

```
Fetching password for: HomeWiFi_5G

  Network: HomeWiFi_5G
  Password: mysecretpassword123
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--all, -a` | Show all saved WiFi passwords |
| `--list, -l` | List all WiFi profile names only |
| `--password, -p` | Show password for specific network |
| `--export, -e` | Export all passwords to file |
| `--json` | Output in JSON format |
| `--admin-check` | Check if running as administrator |
| `--no-ansi` | Disable colored output |

## Using as a Python Module

```python
from wifi-passwords import WiFiPasswordManager

# Create manager
manager = WiFiPasswordManager()

# List all profiles
profiles = manager.list_profiles()
print(f"Found {len(profiles)} networks: {profiles}")

# Get password for specific network
password = manager.get_password("MyHomeWiFi")
print(f"Password: {password}")

# Get all passwords with details
profiles = manager.get_all_passwords()
for profile in profiles:
    print(f"{profile.name}: {profile.password}")

# Export to file
manager.export_to_file("wifi_backup.txt")

# Check if running as admin
is_admin = manager.is_admin()
print(f"Admin: {is_admin}")
```

## WiFiProfile Object

```python
@dataclass
class WiFiProfile:
    name: str           # Network name (SSID)
    authentication: str # Auth type (WPA2-Personal, etc.)
    encryption: str     # Encryption type
    password: str       # The saved password
```

## Requirements

- Windows 7/8/10/11
- Python 3.6+
- Administrator privileges (for revealing passwords)

## Troubleshooting

**"Failed to list WiFi profiles"**
- Run the script as Administrator
- Right-click on Command Prompt/PowerShell and select "Run as administrator"

**"Access denied"**
- Administrator privileges required
- The current user may not have permission to access network settings

**No WiFi profiles found**
- Make sure you've connected to WiFi networks on this computer
- Profiles are stored per-user on Windows

**Empty password shown**
- The network might be an open network (no password)
- Or you connected using a different authentication method

## How It Works

The script uses Windows built-in tools:

1. `netsh wlan show profiles` - Lists all saved WiFi profiles
2. `netsh wlan show profile name="X" key=clear` - Shows details including password

These commands access the Windows Credential Manager where WiFi passwords are securely stored.

## Security Notes

- WiFi passwords are stored encrypted in Windows
- This tool simply decrypts and displays them using Windows APIs
- Anyone with admin access can view saved WiFi passwords
- Be careful about sharing the output of this tool
- Never share passwords without permission

## License

MIT License - Use responsibly and ethically.
