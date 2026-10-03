#!/usr/bin/env python3
"""
WiFi Passwords - Show saved WiFi passwords on Windows

WARNING: This script accesses sensitive network information.
It requires administrator privileges to reveal WiFi passwords.
Only use on your own computer or with permission.

Features:
- List all saved WiFi profiles
- Show WiFi password for any profile
- Export results to text file
- Show detailed network information
- Colorful terminal output

Usage:
    python wifi-passwords.py
    python wifi-passwords.py --list
    python wifi-passwords.py --password "MyWiFi"
    python wifi-passwords.py --export results.txt
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class WiFiProfile:
    """Represents a WiFi network profile."""
    name: str
    authentication: str
    encryption: str
    password: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'authentication': self.authentication,
            'encryption': self.encryption,
            'password': self.password
        }


class WiFiPasswordManager:
    """Manage and retrieve WiFi passwords on Windows."""

    def __init__(self, use_powershell: bool = True):
        """
        Initialize the WiFi password manager.

        Args:
            use_powershell: Use PowerShell instead of netsh (more reliable)
        """
        self.use_powershell = use_powershell

    def _run_command(self, command: str) -> tuple[str, str, int]:
        """
        Run a shell command and return output.

        Args:
            command: Command to run

        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def _run_powershell(self, script: str) -> tuple[str, str, int]:
        """
        Run a PowerShell command.

        Args:
            script: PowerShell script to execute

        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        command = ['powershell', '-NoProfile', '-Command', script]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def list_profiles(self) -> list[str]:
        """
        Get list of all saved WiFi profiles.

        Returns:
            List of WiFi profile names
        """
        if self.use_powershell:
            script = 'netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object { $_.Line.Split(":")[1].Trim() }'
            stdout, _, returncode = self._run_powershell(script)
        else:
            stdout, _, returncode = self._run_command('netsh wlan show profiles')

        if returncode != 0:
            raise RuntimeError("Failed to list WiFi profiles. Run as Administrator.")

        if self.use_powershell:
            profiles = [p.strip() for p in stdout.strip().split('\n') if p.strip()]
        else:
            # Parse netsh output
            profiles = []
            for line in stdout.split('\n'):
                if 'All User Profile' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        profiles.append(parts[1].strip())

        return profiles

    def get_profile_info(self, profile_name: str) -> WiFiProfile:
        """
        Get detailed information about a WiFi profile.

        Args:
            profile_name: Name of the WiFi network

        Returns:
            WiFiProfile object with all details
        """
        if self.use_powershell:
            # Use PowerShell for more reliable parsing
            script = f'''
            $profile = netsh wlan show profile name="{profile_name}" key=clear
            $auth = ($profile | Select-String "Authentication").ToString().Split(":")[1].Trim()
            $cipher = ($profile | Select-String "Cipher").ToString().Split(":")[1].Trim()
            $key = ($profile | Select-String "Key Content").ToString().Split(":")[1].Trim()
            Write-Output "$auth|$cipher|$key"
            '''

            stdout, stderr, returncode = self._run_powershell(script)

            if returncode != 0:
                raise RuntimeError(f"Failed to get profile info: {stderr or 'Unknown error'}")

            parts = stdout.strip().split('|')
            auth = parts[0] if len(parts) > 0 else "Unknown"
            cipher = parts[1] if len(parts) > 1 else "Unknown"
            password = parts[2] if len(parts) > 2 else ""

            # Try to get encryption type
            script2 = f'''
            $profile = netsh wlan show profile name="{profile_name}" key=clear
            $encryption = ($profile | Select-String "Encryption").ToString().Split(":")[1].Trim()
            Write-Output $encryption
            '''
            stdout2, _, _ = self._run_powershell(script2)
            encryption = stdout2.strip() if stdout2.strip() else cipher

        else:
            # Use netsh directly
            stdout, stderr, returncode = self._run_command(
                f'netsh wlan show profile name="{profile_name}" key=clear'
            )

            if returncode != 0:
                raise RuntimeError(f"Failed to get profile info: {stderr or 'Unknown error'}")

            # Parse output
            password = ""
            authentication = ""
            encryption = ""

            for line in stdout.split('\n'):
                line = line.strip()
                if 'Key Content' in line:
                    password = line.split(':')[1].strip() if ':' in line else ""
                elif 'Authentication' in line:
                    authentication = line.split(':')[1].strip() if ':' in line else ""
                elif 'Encryption' in line:
                    encryption = line.split(':')[1].strip() if ':' in line else ""

        return WiFiProfile(
            name=profile_name,
            authentication=authentication,
            encryption=encryption,
            password=password
        )

    def get_password(self, profile_name: str) -> str:
        """
        Get the password for a WiFi network.

        Args:
            profile_name: Name of the WiFi network

        Returns:
            WiFi password
        """
        profile = self.get_profile_info(profile_name)
        return profile.password

    def get_all_passwords(self) -> list[WiFiProfile]:
        """
        Get all saved WiFi passwords.

        Returns:
            List of WiFiProfile objects with passwords
        """
        profiles = self.list_profiles()
        results = []

        for profile_name in profiles:
            try:
                profile = self.get_profile_info(profile_name)
                results.append(profile)
            except Exception as e:
                # Some profiles might be inaccessible
                print(f"Warning: Could not get info for '{profile_name}': {e}")

        return results

    def export_to_file(self, filepath: str, include_passwords: bool = True):
        """
        Export all WiFi profiles to a text file.

        Args:
            filepath: Output file path
            include_passwords: Include passwords in export
        """
        profiles = self.get_all_passwords()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("WiFi Passwords Export\n")
            f.write(f"Generated: {subprocess.getoutput('date /t')} {subprocess.getoutput('time /t')}\n")
            f.write("=" * 60 + "\n\n")

            for profile in profiles:
                f.write(f"Network Name: {profile.name}\n")
                f.write(f"Authentication: {profile.authentication}\n")
                f.write(f"Encryption: {profile.encryption}\n")
                if include_passwords:
                    f.write(f"Password: {profile.password}\n")
                f.write("-" * 40 + "\n\n")

        print(f"Exported {len(profiles)} profiles to: {filepath}")

    def is_admin(self) -> bool:
        """
        Check if running with administrator privileges.

        Returns:
            True if running as admin
        """
        try:
            # Try to access system network configuration
            output, _, _ = self._run_command('net session')
            return True
        except:
            pass

        # Alternative check via PowerShell
        script = '''
        $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($identity)
        $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        '''
        stdout, _, _ = self._run_powershell(script)
        return 'True' in stdout


def print_banner():
    """Print a colorful banner."""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║          WiFi Passwords Viewer v1.0            ║
    ║     Access saved WiFi passwords on Windows     ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)


def print_warning():
    """Print a warning message."""
    warning = """
    ┌────────────────────────────────────────────────────┐
    │  ⚠️  WARNING: This tool accesses sensitive data.   │
    │                                                    │
    │  - Requires administrator privileges               │
    │  - Only use on your own computer                  │
    │  - WiFi passwords may be visible to others        │
    └────────────────────────────────────────────────────┘
    """
    print(warning)


def format_table(profiles: list[WiFiProfile]) -> str:
    """
    Format profiles as a table.

    Args:
        profiles: List of WiFiProfile objects

    Returns:
        Formatted table string
    """
    # Calculate column widths
    name_width = max(20, max(len(p.name) for p in profiles) + 2)
    auth_width = 15
    pass_width = 30

    # Header
    header = f"{'Network Name':<{name_width}} {'Auth':<{auth_width}} {'Password':<{pass_width}}"
    separator = "-" * len(header)

    lines = [header, separator]

    for profile in profiles:
        name = profile.name[:name_width-2] + ".." if len(profile.name) > name_width else profile.name
        auth = profile.authentication[:auth_width-1] + "." if len(profile.authentication) > auth_width else profile.authentication
        password = profile.password[:pass_width-2] + ".." if len(profile.password) > pass_width else profile.password
        lines.append(f"{name:<{name_width}} {auth:<{auth_width}} {password:<{pass_width}}")

    return "\n".join(lines)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Show saved WiFi passwords on Windows',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--list', '-l', action='store_true',
                        help='List all saved WiFi profiles')
    parser.add_argument('--password', '-p', metavar='NAME',
                        help='Show password for specific WiFi network')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Show all WiFi passwords')
    parser.add_argument('--export', '-e', metavar='FILE',
                        help='Export all passwords to file')
    parser.add_argument('--no-ansi', action='store_true',
                        help='Disable colored output')
    parser.add_argument('--json', action='store_true',
                        help='Output in JSON format')
    parser.add_argument('--admin-check', action='store_true',
                        help='Check if running as administrator')

    args = parser.parse_args()

    try:
        print_banner()

        manager = WiFiPasswordManager()

        # Admin check
        if args.admin_check:
            is_admin = manager.is_admin()
            if is_admin:
                print("[OK] Running with administrator privileges")
            else:
                print("[!] NOT running as administrator")
                print("    Some features may not work. Run as admin for full access.")
            return

        # Check admin status
        if not manager.is_admin():
            print_warning()
            print("[!] Not running as administrator. Run 'Run as administrator' for full access.\n")

        # Handle different modes
        if args.list:
            # List all profiles
            profiles = manager.list_profiles()
            print(f"\nFound {len(profiles)} saved WiFi profiles:\n")
            for i, profile in enumerate(profiles, 1):
                print(f"  {i}. {profile}")
            print()

        elif args.password:
            # Get specific password
            print(f"\nFetching password for: {args.password}\n")
            try:
                password = manager.get_password(args.password)
                if password:
                    print(f"  Network: {args.password}")
                    print(f"  Password: {password}")
                else:
                    print(f"  Network: {args.password}")
                    print(f"  Password: [No password stored - may be open network]")
            except RuntimeError as e:
                print(f"  Error: {e}")

        elif args.all:
            # Get all passwords
            print("\nFetching all WiFi passwords...\n")
            try:
                profiles = manager.get_all_passwords()

                if args.json:
                    import json
                    print(json.dumps([p.to_dict() for p in profiles], indent=2))
                else:
                    print(format_table(profiles))

                print(f"\nTotal: {len(profiles)} networks")
            except RuntimeError as e:
                print(f"Error: {e}")

        elif args.export:
            # Export to file
            print(f"\nExporting to: {args.export}\n")
            manager.export_to_file(args.export)

        else:
            # Default: show all passwords
            print("\nFetching all WiFi passwords...\n")
            try:
                profiles = manager.get_all_passwords()

                if args.json:
                    import json
                    print(json.dumps([p.to_dict() for p in profiles], indent=2))
                else:
                    print(format_table(profiles))

                print(f"\nTotal: {len(profiles)} networks")
            except RuntimeError as e:
                print(f"Error: {e}")
                print("\nTip: Try running as administrator (right-click > Run as administrator)")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
