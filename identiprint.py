import socket
import threading
import ipaddress

printer_ips = []

# Function to check if a specific IP is a printer
def is_printer(ip):
    try:
        # Connect to the printer port (e.g., 9100)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, 9100))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error occurred while checking {ip}: {str(e)}")
        return False

# Function to scan IP range for printers
def scan_range(start_ip, end_ip):
    start_octets = list(map(int, start_ip.split(".")))
    end_octets = list(map(int, end_ip.split(".")))

    for octet_1 in range(start_octets[0], end_octets[0] + 1):
        for octet_2 in range(start_octets[1], end_octets[1] + 1):
            for octet_3 in range(start_octets[2], end_octets[2] + 1):
                for octet_4 in range(start_octets[3], end_octets[3] + 1):
                    ip = f"{octet_1}.{octet_2}.{octet_3}.{octet_4}"
                    # print("\n ~~~~~~~~~~~~~~  Checked: " + ip + "~~~~~~~~~~~~~~~~~~~~~ \n")
                    if is_printer(ip):
                        printer_ips.append(ip)
                        print(f"Printer found: {ip}")

# Ask the user to choose the scanning mode
mode = int(input("Enter 0 to use the hardcoded IP ranges, or 1 to enter custom IP ranges: "))

if mode == 0:
    # Hardcoded IP ranges
    ip_ranges = [("xx.xx.xx.xx", "xx.xx.xx.xx"), ("xx.xx.xx.xx", "xx.xx.xx.xx")]
else:
    # Custom IP ranges
    ip_ranges = []
    while True:
        start_ip = input("Enter the start IP of the range (or 'done' to finish): ")
        if start_ip.lower() == "done":
            break
        end_ip = input("Enter the end IP of the range: ")
        ip_ranges.append((start_ip, end_ip))

# Create threads for scanning each IP range
threads = []
for start_ip, end_ip in ip_ranges:
    thread = threading.Thread(target=scan_range, args=(start_ip, end_ip))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("Printer discovery complete.")
