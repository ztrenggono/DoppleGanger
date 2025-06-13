#!/usr/bin/env python3

import os
import sys
import random
import subprocess
import netifaces
import requests
import uuid
import json
from typing import Dict, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt, Confirm
from datetime import datetime

console = Console()

class Doppelganger:
    def __init__(self):
        self.original_state = {}
        self.spoofed_state = {}
        self.console = Console()
        
    def show_banner(self):
        banner = """
        ██████╗  ██████╗ ██████╗ ███████╗██╗     ██╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
        ██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║     ██║██╔════╝ ██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
        ██║  ██║██║   ██║██████╔╝█████╗  ██║     ██║██║  ███╗███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
        ██║  ██║██║   ██║██╔═══╝ ██╔══╝  ██║     ██║██║   ██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
        ██████╔╝╚██████╔╝██║     ███████╗███████╗██║╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
        ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        """
        self.console.print(Panel(banner, title="Digital Identity Spoofing Tool", border_style="blue"))
        self.console.print("[bold blue]Your Digital Privacy Guardian[/bold blue]")
        self.console.print("\n")

    def get_mac_address(self) -> str:
        """Get current MAC address of the primary network interface"""
        try:
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface != 'lo':  # Skip loopback
                    mac = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
                    return mac
        except Exception as e:
            self.console.print(f"[red]Error getting MAC address: {str(e)}[/red]")
        return "Unknown"

    def get_hostname(self) -> str:
        """Get current hostname"""
        try:
            return subprocess.check_output(['hostname']).decode().strip()
        except Exception as e:
            self.console.print(f"[red]Error getting hostname: {str(e)}[/red]")
            return "Unknown"

    def get_public_ip(self) -> str:
        """Get current public IP"""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except Exception as e:
            self.console.print(f"[red]Error getting public IP: {str(e)}[/red]")
            return "Unknown"

    def get_dns_servers(self) -> List[str]:
        """Get current DNS servers"""
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_servers = [line.split()[1] for line in f if line.startswith('nameserver')]
            return dns_servers
        except Exception as e:
            self.console.print(f"[red]Error getting DNS servers: {str(e)}[/red]")
            return ["Unknown"]

    def get_locale(self) -> str:
        """Get current locale"""
        try:
            return os.environ.get('LANG', 'Unknown')
        except Exception as e:
            self.console.print(f"[red]Error getting locale: {str(e)}[/red]")
            return "Unknown"

    def get_hardware_serial(self) -> str:
        """Get hardware serial number"""
        try:
            with open('/sys/class/dmi/id/product_serial', 'r') as f:
                return f.read().strip()
        except Exception as e:
            self.console.print(f"[red]Error getting hardware serial: {str(e)}[/red]")
            return "Unknown"

    def backup_current_state(self):
        """Backup current system state"""
        self.original_state = {
            'mac': self.get_mac_address(),
            'hostname': self.get_hostname(),
            'public_ip': self.get_public_ip(),
            'dns': self.get_dns_servers(),
            'locale': self.get_locale(),
            'hardware_serial': self.get_hardware_serial(),
            'uuid': str(uuid.uuid4())
        }

    def spoof_mac(self) -> bool:
        """Spoof MAC address"""
        try:
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface != 'lo':
                    new_mac = ':'.join(['%02x' % random.randint(0x00, 0xff) for _ in range(6)])
                    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'down'])
                    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'address', new_mac])
                    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'up'])
                    self.spoofed_state['mac'] = new_mac
                    return True
        except Exception as e:
            self.console.print(f"[red]Error spoofing MAC: {str(e)}[/red]")
        return False

    def spoof_hostname(self) -> bool:
        """Spoof hostname"""
        try:
            new_hostname = f"host-{random.randint(1000, 9999)}"
            # Update /etc/hosts first
            with open('/etc/hosts', 'r') as f:
                hosts_content = f.read()
            
            # Add new hostname to /etc/hosts
            with open('/etc/hosts', 'w') as f:
                f.write(hosts_content)
                f.write(f"\n127.0.1.1 {new_hostname}\n")
            
            # Set the new hostname
            subprocess.run(['sudo', 'hostnamectl', 'set-hostname', new_hostname])
            self.spoofed_state['hostname'] = new_hostname
            return True
        except Exception as e:
            self.console.print(f"[red]Error spoofing hostname: {str(e)}[/red]")
        return False

    def spoof_dns(self) -> bool:
        """Spoof DNS servers"""
        try:
            dns_servers = ['1.1.1.1', '9.9.9.9']
            with open('/etc/resolv.conf', 'w') as f:
                for dns in dns_servers:
                    f.write(f'nameserver {dns}\n')
            self.spoofed_state['dns'] = dns_servers
            return True
        except Exception as e:
            self.console.print(f"[red]Error spoofing DNS: {str(e)}[/red]")
        return False

    def spoof_locale(self) -> bool:
        """Spoof locale"""
        try:
            locales = ['fr_FR.UTF-8', 'de_DE.UTF-8', 'es_ES.UTF-8', 'it_IT.UTF-8']
            new_locale = random.choice(locales)
            os.environ['LANG'] = new_locale
            self.spoofed_state['locale'] = new_locale
            return True
        except Exception as e:
            self.console.print(f"[red]Error spoofing locale: {str(e)}[/red]")
        return False

    def show_spoofing_summary(self):
        """Display spoofing summary"""
        table = Table(title="Spoofing Summary")
        table.add_column("Field", style="cyan")
        table.add_column("Before", style="green")
        table.add_column("After", style="yellow")

        for field, before in self.original_state.items():
            after = self.spoofed_state.get(field, "Not spoofed")
            table.add_row(field, str(before), str(after))

        self.console.print(table)

    def show_webrtc_info(self):
        """Display WebRTC protection information"""
        info = """
        [bold yellow]WebRTC Protection Information[/bold yellow]
        
        WebRTC can leak your real IP address even when using a VPN.
        To protect yourself:
        
        1. Install uBlock Origin extension
        2. Enable "Prevent WebRTC from leaking local IP address"
        3. Or use WebRTC Leak Prevent extension
        
        Note: This protection must be done at the browser level.
        """
        self.console.print(Panel(info, title="WebRTC Protection", border_style="yellow"))

    def check_device_status(self):
        """Display current device status"""
        current_state = {
            'mac': self.get_mac_address(),
            'hostname': self.get_hostname(),
            'dns': self.get_dns_servers(),
            'locale': self.get_locale()
        }
        
        table = Table(title="Current Device Status")
        table.add_column("Setting", style="cyan")
        table.add_column("Current Value", style="green")
        table.add_column("Original Value", style="yellow")
        table.add_column("Status", style="blue")
        
        for setting, current_value in current_state.items():
            original_value = self.original_state.get(setting, current_value)  # Use current value as original if no backup
            status = "✅ Spoofed" if setting in self.spoofed_state else "🔄 Original"
            
            # Format values for better readability
            if setting == 'dns':
                current_value = str(current_value)
                original_value = str(original_value)
            
            table.add_row(
                setting.replace('_', ' ').title(),
                str(current_value),
                str(original_value),
                status
            )
        
        self.console.print(table)
        
        # Add summary
        if self.spoofed_state:
            self.console.print("\n[bold cyan]Spoofing Summary:[/bold cyan]")
            self.console.print(f"Total settings spoofed: {len(self.spoofed_state)}")
            self.console.print("Spoofed settings: " + ", ".join(self.spoofed_state.keys()))
        else:
            self.console.print("\n[yellow]No settings have been spoofed yet.[/yellow]")

    def main_menu(self):
        """Display main menu"""
        choices = [
            'Spoof This Device',
            'Restore Original State',
            'Check Device Status',
            'Exit'
        ]
        self.console.print("\n[bold cyan]Available Options:[/bold cyan]")
        for i, choice in enumerate(choices, 1):
            self.console.print(f"[cyan]{i}.[/cyan] {choice}")
        
        while True:
            try:
                choice = Prompt.ask("\nSelect an option", choices=[str(i) for i in range(1, len(choices) + 1)])
                return choices[int(choice) - 1]
            except ValueError:
                self.console.print("[red]Invalid choice. Please try again.[/red]")

    def spoofing_menu(self):
        """Display spoofing options"""
        options = [
            'MAC Address',
            'Hostname',
            'DNS Servers',
            'Locale',
            'Show WebRTC Info'
        ]
        
        selected = []
        self.console.print("\n[bold cyan]Select options to spoof:[/bold cyan]")
        
        for option in options:
            if Confirm.ask(f"Spoof {option}?"):
                selected.append(option)
        
        return selected

    def restore_mac(self) -> bool:
        """Restore original MAC address"""
        try:
            if 'mac' in self.original_state:
                interfaces = netifaces.interfaces()
                for iface in interfaces:
                    if iface != 'lo':
                        subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'down'])
                        subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'address', self.original_state['mac']])
                        subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'up'])
                return True
        except Exception as e:
            self.console.print(f"[red]Error restoring MAC address: {str(e)}[/red]")
        return False

    def restore_hostname(self) -> bool:
        """Restore original hostname"""
        try:
            if 'hostname' in self.original_state:
                # Update /etc/hosts
                with open('/etc/hosts', 'r') as f:
                    hosts_content = f.read()
                
                # Remove the spoofed hostname line and add original
                lines = hosts_content.split('\n')
                filtered_lines = [line for line in lines if not line.endswith(self.spoofed_state['hostname'])]
                
                with open('/etc/hosts', 'w') as f:
                    f.write('\n'.join(filtered_lines))
                    f.write(f"\n127.0.1.1 {self.original_state['hostname']}\n")
                
                # Set the original hostname
                subprocess.run(['sudo', 'hostnamectl', 'set-hostname', self.original_state['hostname']])
                return True
        except Exception as e:
            self.console.print(f"[red]Error restoring hostname: {str(e)}[/red]")
        return False

    def restore_dns(self) -> bool:
        """Restore original DNS servers"""
        try:
            if 'dns' in self.original_state:
                with open('/etc/resolv.conf', 'w') as f:
                    for dns in self.original_state['dns']:
                        f.write(f'nameserver {dns}\n')
                return True
        except Exception as e:
            self.console.print(f"[red]Error restoring DNS servers: {str(e)}[/red]")
        return False

    def restore_locale(self) -> bool:
        """Restore original locale"""
        try:
            if 'locale' in self.original_state:
                os.environ['LANG'] = self.original_state['locale']
                return True
        except Exception as e:
            self.console.print(f"[red]Error restoring locale: {str(e)}[/red]")
        return False

    def restore_state(self):
        """Restore all spoofed settings to their original state"""
        if not self.original_state:
            self.console.print("[yellow]No original state found. Nothing to restore.[/yellow]")
            return

        self.console.print("\n[bold cyan]Restoring original settings...[/bold cyan]")
        
        # Create a table to show restore progress
        table = Table(title="Restore Progress")
        table.add_column("Setting", style="cyan")
        table.add_column("Before", style="yellow")
        table.add_column("After", style="green")
        table.add_column("Status", style="blue")
        
        # Restore each setting
        if 'mac' in self.spoofed_state:
            status = "✅" if self.restore_mac() else "❌"
            table.add_row("MAC Address", 
                         self.spoofed_state['mac'],
                         self.original_state['mac'],
                         status)
            
        if 'hostname' in self.spoofed_state:
            status = "✅" if self.restore_hostname() else "❌"
            table.add_row("Hostname",
                         self.spoofed_state['hostname'],
                         self.original_state['hostname'],
                         status)
            
        if 'dns' in self.spoofed_state:
            status = "✅" if self.restore_dns() else "❌"
            table.add_row("DNS Servers",
                         str(self.spoofed_state['dns']),
                         str(self.original_state['dns']),
                         status)
            
        if 'locale' in self.spoofed_state:
            status = "✅" if self.restore_locale() else "❌"
            table.add_row("Locale",
                         self.spoofed_state['locale'],
                         self.original_state['locale'],
                         status)
        
        self.console.print(table)
        
        # Clear the spoofed state
        self.spoofed_state = {}
        self.console.print("\n[green]Restore complete![/green]")

    def run(self):
        """Main execution function"""
        self.show_banner()
        
        while True:
            action = self.main_menu()
            
            if action == 'Exit':
                break
                
            elif action == 'Spoof This Device':
                self.backup_current_state()
                options = self.spoofing_menu()
                
                for option in options:
                    if option == 'MAC Address':
                        self.spoof_mac()
                    elif option == 'Hostname':
                        self.spoof_hostname()
                    elif option == 'DNS Servers':
                        self.spoof_dns()
                    elif option == 'Locale':
                        self.spoof_locale()
                    elif option == 'Show WebRTC Info':
                        self.show_webrtc_info()
                
                self.show_spoofing_summary()
                
            elif action == 'Restore Original State':
                if not self.spoofed_state:
                    self.console.print("[yellow]No spoofed settings found. Nothing to restore.[/yellow]")
                    continue
                    
                if Confirm.ask("Are you sure you want to restore all settings to their original state?"):
                    self.restore_state()
                else:
                    self.console.print("[yellow]Restore cancelled.[/yellow]")
                    
            elif action == 'Check Device Status':
                self.check_device_status()

if __name__ == "__main__":
    try:
        tool = Doppelganger()
        tool.run()
    except KeyboardInterrupt:
        print("\nExiting Doppelgänger...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1) 