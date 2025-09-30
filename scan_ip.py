import socket
import subprocess
import ipaddress

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个外部地址，获取本地IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    print(f"本地IP: {ip}")
    return ip

def scan_network(network):
    used = []
    unused = []
    for ip in network.hosts():
        print(f"正在扫描: {ip}")
        result = subprocess.run(['ping', '-n', '1', '-w', '100', str(ip)],
                               stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            used.append(str(ip))
        else:
            unused.append(str(ip))
    return used, unused

if __name__ == '__main__':
    local_ip = get_local_ip()
    # 假设子网掩码为24位
    net = ipaddress.ip_network(local_ip + '/24', strict=False)
    used, unused = scan_network(net)
    print(f'已使用IP: {len(used)}')
    print('\n'.join(used))
    print(f'未使用IP: {len(unused)}')
    print('\n'.join(unused))