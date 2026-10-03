# System Info

A Python command-line tool to display comprehensive system information including OS, CPU, RAM, disk space, network info, and more.

## Features

- **Operating System**: System name, release, version, machine type
- **CPU Information**: Processor name, physical/logical cores, frequency
- **Memory (RAM)**: Total, used, available with visual progress bar
- **Disk Space**: Per-drive/total with visual progress bars
- **Network**: Hostname, IP address, network interfaces
- **Uptime**: System running time
- **Cross-platform**: Works on Windows, macOS, and Linux
- **JSON output**: Option to output machine-readable data
- **No dependencies**: Uses only Python standard library

## Installation

```bash
pip install -r requirements.txt
```

Note: No external dependencies required.

## Usage

### Basic usage (human-readable)

```bash
python system-info.py
```

### JSON output

```bash
python system-info.py --json
```

### Short option

```bash
python system-info.py -j
```

## Sample Output

```
============================================================
                    SYSTEM INFORMATION
============================================================

[ PLATFORM ]
  Operating System : Windows
  Release          : 11
  Version          : 10.0.22631N/A Build 22631
  Machine          : AMD64
  Architecture     : 64bit

[ CPU ]
  Processor        : Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz
  Physical Cores   : 8
  Logical Cores    : 16
  Max Frequency    : 3801 MHz

[ MEMORY (RAM) ]
  Total            : 32.00 GB
  Used             : 16.50 GB (51.6%)
  Available        : 15.50 GB
  [████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░]

[ DISK ]
  C::
    Total          : 500.00 GB
    Used          : 250.00 GB (50.0%)
    Free          : 250.00 GB
    [████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░]

[ NETWORK ]
  Hostname         : MY-PC
  IP Address       : 192.168.1.100
  Interfaces:
    - Ethernet: 192.168.1.100
    - Wi-Fi: 192.168.1.101

[ UPTIME ]
  5d 12h 30m

============================================================
```

## JSON Output

```bash
python system-info.py --json
```

Returns:
```json
{
  "platform": {
    "system": "Windows",
    "release": "11",
    "version": "10.0.22631N/A Build 22631",
    "machine": "AMD64",
    "architecture": "64bit"
  },
  "cpu": {
    "physical_cores": 8,
    "logical_cores": 16,
    "max_frequency": "3801 MHz"
  },
  "memory": {
    "total": "32.00 GB",
    "available": "15.50 GB",
    "used": "16.50 GB (51.6%)",
    "percent": "51.6%"
  },
  "disk": [
    {
      "device": "C:",
      "total": "500.00 GB",
      "free": "250.00 GB",
      "used": "250.00 GB",
      "percent": "50.0%"
    }
  ],
  "network": {
    "hostname": "MY-PC",
    "ipv4": "192.168.1.100",
    "interfaces": [...]
  },
  "uptime": "5d 12h 30m"
}
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--json` | `-j` | Output as JSON format |
| `--version` | `-v` | Show version number |

## Use Cases

### System Monitoring

```bash
# Add to a monitoring script
python system-info.py --json > system_status.json
```

### Quick System Check

```bash
# Run and see what's available
python system-info.py
```

### Automated Reporting

```bash
# Cron job or scheduled task
0 */6 * * * /usr/bin/python3 /path/to/system-info.py --json >> /var/log/system-report.json
```

## System Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux
- No external dependencies

## License

MIT License
