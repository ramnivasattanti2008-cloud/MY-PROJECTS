#!/usr/bin/env python3
"""
System Info - Display comprehensive system information.
Shows OS, CPU, RAM, disk space, network info, and more.
"""

import os
import sys
import platform
import subprocess
import json
import argparse
from pathlib import Path


def get_platform():
    """Get detailed platform information."""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0],
    }


def get_cpu_info():
    """Get CPU information."""
    info = {
        'physical_cores': 0,
        'logical_cores': 0,
        'max_frequency': 'N/A',
        'current_frequency': 'N/A',
        'usage': 'N/A',
    }

    if sys.platform == 'win32':
        try:
            output = subprocess.check_output(
                ['wmic', 'cpu', 'get', 'NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed,CurrentClockSpeed', '/format:csv'],
                text=True, stderr=subprocess.DEVNULL
            )
            lines = output.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split(',')
                if len(parts) >= 4:
                    info['physical_cores'] = int(parts[1]) if parts[1] else 0
                    info['logical_cores'] = int(parts[2]) if parts[2] else 0
                    info['max_frequency'] = f"{parts[3]} MHz" if parts[3] else 'N/A'
                    info['current_frequency'] = f"{parts[4]} MHz" if len(parts) > 4 and parts[4] else 'N/A'
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    elif sys.platform == 'darwin':
        try:
            output = subprocess.check_output(
                ['sysctl', '-n', 'hw.physicalcpu', 'hw.logicalcpu', 'hw.cpufrequency', 'hw.cpufrequency_max'],
                text=True
            )
            lines = output.strip().split('\n')
            if len(lines) >= 4:
                info['physical_cores'] = int(lines[0])
                info['logical_cores'] = int(lines[1])
                freq_mhz = int(lines[2]) / 1000000
                info['max_frequency'] = f"{freq_mhz:.0f} MHz"
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    elif sys.platform == 'linux':
        try:
            # Try to read from /proc/cpuinfo
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()

            # Count cores
            info['physical_cores'] = cpuinfo.count('physical id') + 1 if 'physical id' in cpuinfo else os.cpu_count()
            info['logical_cores'] = os.cpu_count() or 0

            # Get frequency
            try:
                with open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq', 'r') as f:
                    freq_khz = int(f.read().strip())
                    info['max_frequency'] = f"{freq_khz / 1000:.0f} MHz"
            except (FileNotFoundError, ValueError):
                pass
        except FileNotFoundError:
            pass

    return info


def get_memory_info():
    """Get memory/RAM information."""
    info = {
        'total': 0,
        'available': 0,
        'used': 0,
        'percent': 0,
    }

    if sys.platform == 'win32':
        try:
            output = subprocess.check_output(
                ['wmic', 'OS', 'get', 'TotalVisibleMemorySize,FreePhysicalMemory', '/format:csv'],
                text=True, stderr=subprocess.DEVNULL
            )
            lines = output.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split(',')
                if len(parts) >= 3:
                    total_kb = int(parts[1]) if parts[1] else 0
                    free_kb = int(parts[2]) if parts[2] else 0
                    info['total'] = total_kb * 1024
                    info['available'] = free_kb * 1024
                    info['used'] = info['total'] - info['available']
                    info['percent'] = (info['used'] / info['total'] * 100) if info['total'] else 0
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    elif sys.platform in ['darwin', 'linux']:
        try:
            import resource
            # macOS and Linux
            if sys.platform == 'darwin':
                output = subprocess.check_output(
                    ['vm_stat'],
                    text=True
                )
                # Parse vm_stat output
                lines = output.strip().split('\n')
                free_pages = 0
                active_pages = 0
                inactive_pages = 0
                wired_pages = 0
                page_size = 4096  # Default

                for line in lines:
                    if 'page size' in line.lower():
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if p == 'bytes':
                                page_size = int(parts[i-1])
                    elif 'free pages:' in line.lower():
                        free_pages = int(line.split()[-1].rstrip('.'))
                    elif 'active pages:' in line.lower():
                        active_pages = int(line.split()[-1].rstrip('.'))
                    elif 'inactive pages:' in line.lower():
                        inactive_pages = int(line.split()[-1].rstrip('.'))
                    elif 'wired pages:' in line.lower():
                        wired_pages = int(line.split()[-1].rstrip('.'))

                info['total'] = info.get('total', 0) or (free_pages + active_pages + inactive_pages + wired_pages) * page_size
                info['available'] = free_pages * page_size
                info['used'] = (active_pages + wired_pages) * page_size
                info['percent'] = (info['used'] / info['total'] * 100) if info['total'] else 0
            else:
                # Linux using os.total_memory alternative
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = {}
                        for line in f:
                            parts = line.split(':')
                            if len(parts) == 2:
                                meminfo[parts[0].strip()] = parts[1].strip()

                    if 'MemTotal' in meminfo:
                        info['total'] = int(meminfo['MemTotal'].split()[0]) * 1024
                    if 'MemAvailable' in meminfo:
                        info['available'] = int(meminfo['MemAvailable'].split()[0]) * 1024
                    elif 'MemFree' in meminfo:
                        info['available'] = int(meminfo['MemFree'].split()[0]) * 1024

                    info['used'] = info['total'] - info['available']
                    info['percent'] = (info['used'] / info['total'] * 100) if info['total'] else 0
                except (FileNotFoundError, KeyError, ValueError):
                    pass
        except Exception:
            pass

    # Fallback using psutil-like calculation if needed
    if info['total'] == 0:
        try:
            import resource
            info['total'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except:
            pass

    return info


def get_disk_info():
    """Get disk space information."""
    disks = []

    if sys.platform == 'win32':
        try:
            output = subprocess.check_output(
                ['wmic', 'logicaldisk', 'get', 'DeviceID,Size,FreeSpace,FileSystem,DriveType', '/format:csv'],
                text=True, stderr=subprocess.DEVNULL
            )
            lines = output.strip().split('\n')[1:]
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 5 and parts[1]:
                    drive_type = {'2': 'Removable', '3': 'Local', '4': 'Network', '5': 'CD-ROM'}
                    disks.append({
                        'device': parts[1],
                        'total': int(parts[2]) if parts[2].isdigit() else 0,
                        'free': int(parts[3]) if parts[3].isdigit() else 0,
                        'file_system': parts[4],
                        'drive_type': drive_type.get(parts[5], 'Unknown'),
                    })
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    elif sys.platform in ['darwin', 'linux']:
        import shutil
        try:
            if sys.platform == 'darwin':
                volumes = ['/']
            else:
                # Try to get mount points
                try:
                    with open('/proc/mounts', 'r') as f:
                        mounts = f.readlines()
                    volumes = []
                    for m in mounts:
                        parts = m.split()
                        if len(parts) >= 2 and parts[1] in ['/', '/home'] and 'overlay' not in parts[2]:
                            volumes.append(parts[1])
                except:
                    volumes = ['/']

            for volume in set(volumes):
                try:
                    usage = shutil.disk_usage(volume)
                    disks.append({
                        'device': volume,
                        'total': usage.total,
                        'free': usage.free,
                        'used': usage.used,
                        'percent': (usage.used / usage.total * 100) if usage.total else 0,
                    })
                except FileNotFoundError:
                    pass
        except Exception:
            pass

    return disks


def get_network_info():
    """Get network information."""
    info = {
        'hostname': platform.node(),
        'interfaces': [],
    }

    if sys.platform == 'win32':
        try:
            output = subprocess.check_output(
                ['ipconfig', '/all'],
                text=True, stderr=subprocess.DEVNULL
            )
            # Parse IP config output
            current_adapter = None
            for line in output.split('\n'):
                line = line.strip()
                if line and not line.startswith(' '):
                    if 'adapter' in line.lower():
                        current_adapter = line.split()[0].rstrip(':')
                elif current_adapter and 'IPv4' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        info['interfaces'].append({
                            'name': current_adapter,
                            'ipv4': parts[1].strip(),
                        })
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    elif sys.platform in ['darwin', 'linux']:
        try:
            import socket
            info['hostname'] = socket.gethostname()
            try:
                info['ipv4'] = socket.gethostbyname(socket.gethostname())
            except:
                pass

            # Try to get interface info
            if sys.platform == 'darwin':
                output = subprocess.check_output(
                    ['ifconfig'],
                    text=True, stderr=subprocess.DEVNULL
                )
                current_iface = None
                for line in output.split('\n'):
                    if line and not line.startswith(' '):
                        current_iface = line.split(':')[0]
                    elif 'inet ' in line and current_iface:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            info['interfaces'].append({
                                'name': current_iface,
                                'ipv4': parts[1],
                            })
            else:
                # Linux
                try:
                    with open('/proc/net/dev', 'r') as f:
                        lines = f.readlines()
                    for line in lines[2:]:
                        parts = line.strip().split(':')
                        if len(parts) >= 2:
                            iface = parts[0].strip()
                            if iface and iface != 'lo':
                                info['interfaces'].append({
                                    'name': iface,
                                    'ipv4': 'N/A',
                                })
                except FileNotFoundError:
                    pass
        except Exception:
            pass

    return info


def get_uptime():
    """Get system uptime."""
    if sys.platform == 'win32':
        try:
            output = subprocess.check_output(
                ['wmic', 'os', 'get', 'LastBootUpTime', '/format:csv'],
                text=True, stderr=subprocess.DEVNULL
            )
            lines = output.strip().split('\n')
            if len(lines) > 1:
                return "Windows system uptime detected"
        except:
            pass
    elif sys.platform in ['darwin', 'linux']:
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.read().split()[0])
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                return f"{days}d {hours}h {minutes}m"
        except:
            pass

    return "N/A"


def format_bytes(bytes_val):
    """Format bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def print_system_info(json_output=False):
    """Print all system information."""
    info = {
        'platform': get_platform(),
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info(),
        'uptime': get_uptime(),
    }

    if json_output:
        # Convert bytes to formatted strings for JSON
        json_info = info.copy()
        json_info['memory'] = {
            'total': format_bytes(info['memory']['total']),
            'available': format_bytes(info['memory']['available']),
            'used': format_bytes(info['memory']['used']),
            'percent': f"{info['memory']['percent']:.1f}%",
        }
        json_info['disk'] = [
            {
                'device': d['device'],
                'total': format_bytes(d.get('total', 0)),
                'free': format_bytes(d.get('free', 0)),
                'used': format_bytes(d.get('used', 0)),
                'percent': f"{d.get('percent', 0):.1f}%",
                'file_system': d.get('file_system', 'N/A'),
            }
            for d in info['disk']
        ]
        print(json.dumps(json_info, indent=2))
        return

    # Pretty print
    print("\n" + "=" * 60)
    print("                    SYSTEM INFORMATION")
    print("=" * 60)

    # Platform
    print("\n[ PLATFORM ]")
    p = info['platform']
    print(f"  Operating System : {p['system']}")
    print(f"  Release          : {p['release']}")
    print(f"  Version          : {p['version']}")
    print(f"  Machine          : {p['machine']}")
    print(f"  Architecture     : {p['architecture']}")

    # CPU
    print("\n[ CPU ]")
    c = info['cpu']
    print(f"  Processor        : {p['processor']}")
    print(f"  Physical Cores   : {c['physical_cores']}")
    print(f"  Logical Cores    : {c['logical_cores']}")
    print(f"  Max Frequency    : {c['max_frequency']}")

    # Memory
    print("\n[ MEMORY (RAM) ]")
    m = info['memory']
    total = m['total']
    used = m['used']
    available = m['available']
    percent = m['percent']

    print(f"  Total            : {format_bytes(total)}")
    print(f"  Used             : {format_bytes(used)} ({percent:.1f}%)")
    print(f"  Available        : {format_bytes(available)}")

    # Memory bar
    bar_length = 40
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"  [{bar}]")

    # Disk
    print("\n[ DISK ]")
    for d in info['disk']:
        total = d.get('total', 0)
        free = d.get('free', 0)
        used = d.get('used', total - free)
        percent = (used / total * 100) if total else 0

        print(f"  {d['device']}:")
        print(f"    Total          : {format_bytes(total)}")
        print(f"    Used          : {format_bytes(used)} ({percent:.1f}%)")
        print(f"    Free          : {format_bytes(free)}")

        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"    [{bar}]")

    # Network
    print("\n[ NETWORK ]")
    n = info['network']
    print(f"  Hostname         : {n['hostname']}")
    if n.get('ipv4'):
        print(f"  IP Address       : {n['ipv4']}")
    if n['interfaces']:
        print("  Interfaces:")
        for iface in n['interfaces'][:5]:  # Limit to 5
            ipv4 = iface.get('ipv4', 'N/A')
            print(f"    - {iface['name']}: {ipv4}")

    # Uptime
    print("\n[ UPTIME ]")
    print(f"  {info['uptime']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="System Info - Display comprehensive system information"
    )
    parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()
    print_system_info(json_output=args.json)
    return 0


if __name__ == "__main__":
    exit(main())
