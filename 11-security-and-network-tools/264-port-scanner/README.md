# Port Scanner - Educational Network Security Tool

A Python tool that demonstrates network port scanning concepts for learning about network security.

## Disclaimer

**WARNING: EDUCATIONAL PURPOSE ONLY**

This tool is designed for **LEARNING** about network security. Do NOT use this tool:
- To scan networks without permission
- For any unauthorized reconnaissance
- For malicious purposes

Always obtain proper written authorization before scanning any network or host.

## What It Does

This tool demonstrates:

1. **TCP Port Scanning**: Check if ports are open on a target host
2. **Network Discovery**: Find devices on your local network
3. **Service Identification**: Identify common services by port number
4. **Security Education**: Learn about network attack surfaces

## How It Works

### TCP Connection Scanning

Port scanning works by attempting to establish a TCP connection:

```
Client                          Server
   |                               |
   |  --- SYN -------------------> |   Client sends SYN
   |                               |
   |  <-- SYN-ACK ---------------- |   Port is OPEN
   |                               |
   |  --- RST --------------------> |   Client resets
   |                               |
   |  --- SYN -------------------> |   Client sends SYN
   |                               |
   |  <-- RST -------------------- |   Port is CLOSED
   |                               |
   |  (no response)               |   Port is FILTERED
```

### Port States

| State    | Meaning                                      |
|----------|----------------------------------------------|
| Open     | Service is listening, connection accepted    |
| Closed   | Port receives traffic but no service listens |
| Filtered | Firewall or filter blocks the connection    |

### Common Port Numbers

| Port | Service  | Risk Level | Notes                        |
|------|----------|------------|------------------------------|
| 21   | FTP      | High       | Unencrypted, often exploited |
| 22   | SSH      | Medium     | Brute force attacks common   |
| 23   | Telnet   | Critical   | Unencrypted, avoid using      |
| 25   | SMTP     | Medium     | Email relay vulnerabilities   |
| 80   | HTTP     | Medium     | Web traffic                   |
| 443  | HTTPS    | Low        | Encrypted web traffic         |
| 445  | SMB      | Critical   | EternalBlue, ransomware      |
| 3306 | MySQL    | High       | Database exposure             |
| 3389 | RDP      | High       | Ransomware target             |
| 5432 | Postgres | High       | Database exposure             |
| 8080 | HTTP-Alt | Medium     | Often dev/testing servers     |

## Installation

```bash
# No dependencies required - uses Python standard library!
git clone <repository-url>
cd port-scanner
```

## Usage

### Quick Scan (Common Ports)

```bash
python port-scanner.py localhost
```

### Scan Specific Port Range

```bash
python port-scanner.py 192.168.1.1 -p 1-1000
```

### Scan Specific Ports

```bash
python port-scanner.py example.com -p 80,443,22,3389
```

### Scan All Ports (Very Slow!)

```bash
python port-scanner.py localhost --all
```

### Network Discovery

```bash
python port-scanner.py --discover
```

### Faster Scan

```bash
python port-scanner.py localhost -t 0.5 -w 100
```

## Security Lessons

### Why Port Scanning Matters for Defense

1. **Know Your Attack Surface**
   - You can't defend what you don't know exists
   - Regular port scans reveal exposed services

2. **Close Unnecessary Ports**
   - Every open port is a potential entry point
   - Disable or firewall services you don't need

3. **Monitor for Changes**
   - New open ports might indicate compromise
   - Set up alerts for unexpected port openings

### Common Attack Patterns

```
Reconnaissance --> Port Scan --> Service Detection --> Exploit --> Access
     |               |               |                    |          |
  "Who's out     "What ports    "What service      "Find      "Gain
   there?"        are open?"     is that?"         vulnerability access"
```

### Defense Strategies

1. **Firewall Rules**
   - Block all inbound connections by default
   - Only allow necessary ports

2. **Port Knocking**
   - Hide ports until correct sequence is "knocked"

3. **Service Hardening**
   - Run services on non-standard ports
   - Use strong authentication
   - Enable encryption (SSH instead of Telnet)

4. **Monitoring**
   - Log all connection attempts
   - Set up alerts for scanning activity
   - Use IDS/IPS systems

### Legal Considerations

Port scanning without authorization is **illegal** in many jurisdictions:

- Computer Fraud and Abuse Act (US)
- Computer Misuse Act (UK)
- Similar laws exist in most countries

**Always get written permission before scanning.**

## Code Structure

```
port-scanner/
├── port-scanner.py   # Main scanner tool
├── requirements.txt  # No external dependencies
└── README.md         # This file
```

## Technical Details

### TCP Connect Scan

The simplest port scan type - completes the full TCP handshake:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((host, port))  # Returns 0 if open
sock.close()
```

### Concurrent Scanning

Uses ThreadPoolExecutor for parallel scanning:

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    future_to_port = {
        executor.submit(scan_port, host, port): port
        for port in ports
    }
```

### Other Scan Types (Educational)

- **SYN Scan**: Send SYN only, don't complete handshake (requires root)
- **UDP Scan**: Check UDP services (slower, less reliable)
- **FIN/NULL/XMAS**: Bypass some firewalls (advanced)

## Real-World Scanning Tools

For professional security testing, use established tools:

- **nmap**: Industry standard port scanner
- **masscan**: Ultra-fast port scanner
- **unicornscan**: High-speed scanner

```bash
# Example: nmap port scan
nmap -sV -p 1-1000 192.168.1.1
```

## Educational Resources

- OWASP Testing Guide
- nmap Documentation
- SANS Institute Resources
- Cybrary.it Courses

## License

Educational use only. Use responsibly and legally.
