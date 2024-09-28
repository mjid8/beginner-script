from scapy.all import ARP, Ether, srp
import subprocess
import re
ascii_art = """
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
█░░║║║╠─║─║─║║║║║╠─░░█
█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█"""

print(ascii_art)

# Function to validate IP addresses
def is_valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

# Function to get connected devices (IP & MAC)
def get_connected_devices():
    print("Connected Devices (IP & MAC):")
    target_ip = "192.168.1.1/24"  # Replace with your network's IP range
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")

# Function to ping an IP address
def ping(ip):
    try:
        # Using subprocess to run the ping command
        output = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)

        # Check if 'Request timed out' or 'unreachable' or non-zero return code
        if output.returncode != 0 or "Request timed out" in output.stdout or "unreachable" in output.stdout:
            return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to ping default IPs and specific IPs
def ping_ips():
    default_ips = ["8.8.8.8", "8.8.4.4"]
    print("\nPinging Default IPs:")
    for ip in default_ips:
        if ping(ip):
            print(f"{ip} is reachable")
        else:
            print(f"{ip} is unreachable")

    while True:
        user_input = input("\nDo you want to ping a specific IP? (type 'yes' to ping /type 'no' to exit): ").strip().lower()
        if user_input == "no":
            print("Exiting pinging section.")
            break
        elif user_input == "yes":
            user_ip = input("Enter the IP address to ping: ").strip()
            if is_valid_ip(user_ip):
                if ping(user_ip):
                    print(f"{user_ip} is reachable")
                else:
                    print(f"{user_ip} is unreachable")
            else:
                print("Invalid IP address. Please enter a valid IP.")
        else:
            print("Invalid input, please type 'yes' or 'no'.")

# Main function for steps 1 and 2
def main():
    get_connected_devices()
    ping_ips()

if __name__ == "__main__":
    main()
