#!/usr/bin/env python3

import socket
import ipaddress
import concurrent.futures
import subprocess
import os

'''
remove duplicated entries in authorized_keys:
$ awk '!a[$0]++' ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp && mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys
'''

START_IP = ipaddress.IPv4Address('10.1.41.10')
END_IP = ipaddress.IPv4Address('10.1.41.20')
DEFAULT_USER = 'zhlx'
USER_DICT = {
    '10.1.41.12': 'zhanglx',
    '10.1.41.15': 'zhanglx',
    '10.1.41.20': 'zhanglx',
}

def scan_host(ip, port=22, timeout=5.0):
    """
    尝试连接指定 IP 的指定端口，判断端口是否开放。
    """
    try:
        # 尝试建立 TCP 连接
        with socket.create_connection((str(ip), port), timeout=timeout):
            return True
    except Exception:
        return False

def scan_subnet(subnet):
    """
    遍历指定子网内的所有主机，扫描开放22端口的主机，返回 IP 地址列表。
    """
    open_hosts = []
    network = ipaddress.ip_network(subnet, strict=False)
    # Filter IP addresses within the specified range
    filtered_network = [ip for ip in network.hosts() 
        if ip.version == 4 and START_IP <= ip <= END_IP]
    network = filtered_network  # Replace the original network with filtered IPs
    print(f"地址列表 {network} ...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # 对每个主机提交扫描任务
        future_to_ip = {executor.submit(scan_host, ip): ip for ip in network}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    open_hosts.append(str(ip))
            except Exception:
                pass
    return open_hosts

def push_key_to_host(host, username, pubkey_path):
    """
    调用 ssh-copy-id 命令将公钥推送到目标主机。
    """
    print(f"正在向 {username}@{host} 推送公钥...")
    cmd = ["ssh-copy-id", "-i", pubkey_path, "-o", "PreferredAuthentications=publickey", f"{username}@{host}"]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{host} 推送成功：\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{host} 推送失败：\n{e.stderr}")

def main():
    # 指定要扫描的子网（10.1.41.0/24 表示10.1.41.x网段）
    subnet = "10.1.41.0/24"
    hosts = scan_subnet(subnet)
    
    if not hosts:
        print("在指定子网内未发现开放 SSH 端口的主机。")
        return
    print(f"扫描完成，发现以下主机：\n{hosts}\n")

    # 指定本地公钥文件路径，默认使用 ~/.ssh/id_rsa.pub
    pubkey_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    if not os.path.exists(pubkey_path):
        print(f"公钥文件 {pubkey_path} 不存在，请先生成 SSH 密钥对。")
        return

    # 对每台扫描到的主机，调用 ssh-copy-id 推送公钥
    for host in hosts:
        # Get username from global dictionary or use default
        host_user = USER_DICT.get(host, DEFAULT_USER)
        push_key_to_host(host, host_user, pubkey_path)

if __name__ == "__main__":
    if os.name != 'posix':
        raise OSError("This script only runs on Linux/Unix platforms")
    main()
