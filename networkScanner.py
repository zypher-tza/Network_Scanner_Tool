import socket
import os
import time
import threading
import sy


class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def banner():
    os.system("clear")
    print(Color.CYAN + r"""
███████╗██╗   ██╗██████╗ ██╗  ██╗███████╗██████╗
╚══███╔╝╚██╗ ██╔╝██╔══██╗██║  ██║██╔════╝██╔══██╗
  ███╔╝  ╚████╔╝ ██████╔╝███████║█████╗  ██████╔╝
 ███╔╝    ╚██╔╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
███████╗   ██║   ██║     ██║  ██║███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

    NETWORK SCANNER TOOL by Zypher
""" + Color.RESET)

def progress_bar(task, total):
    print(Color.YELLOW + f"\n[{task}]" + Color.RESET)
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = "█" * (percent // 5)
        print(f"\r{Color.GREEN}{bar:<20}{Color.RESET} {percent}%", end="")
        time.sleep(0.02)
    print("\n")

def ping_host(host):
    progress_bar("Pinging Host", 50)
    response = os.system(f"ping -c 1 {host} > /dev/null 2>&1")

    if response == 0:
        print(Color.GREEN + f"[+] {host} is ONLINE\n" + Color.RESET)
    else:
        print(Color.RED + f"[-] {host} is OFFLINE\n" + Color.RESET)

def scan_port(host, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

def port_scan(host):
    print(Color.BLUE + f"\n[+] Scanning {host}...\n" + Color.RESET)

    progress_bar("Scanning Ports", 100)

    open_ports = []
    threads = []

    for port in range(1, 1025):
        t = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if open_ports:
        print(Color.GREEN + "[OPEN PORTS FOUND]" + Color.RESET)
        for p in sorted(open_ports):
            print(Color.YELLOW + f"  - Port {p}" + Color.RESET)
    else:
        print(Color.RED + "No open ports found." + Color.RESET)

def menu():
    while True:
        print(Color.BOLD + Color.CYAN + """
================ MENU ================
1. Ping Host
2. Port Scan (1–1024)
3. Exit
======================================
""" + Color.RESET)

        choice = input(Color.YELLOW + "Select option: " + Color.RESET)

        if choice == "1":
            host = input("Enter host/IP: ")
            ping_host(host)

        elif choice == "2":
            host = input("Enter host/IP: ")
            port_scan(host)

        elif choice == "3":
            print(Color.GREEN + "Exiting..." + Color.RESET)
            break

        else:
            print(Color.RED + "Invalid option!\n" + Color.RESET)

if __name__ == "__main__":
    try:
        banner()
        menu()
    except KeyboardInterrupt:
        print("\033[91m Thanks by zypher.\033[0m")
        sys.exit(0)
