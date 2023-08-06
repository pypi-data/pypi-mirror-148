#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys
import argparse
import math
import socket
import struct
import select
import signal
import time
import threading


class PingStats():
    """stats for a pinger"""

    def __init__(self, host):
        self._sent = 0
        self._received = 0
        self._rtt = []
        self._sum = 0
        self._sumsq = 0
        self._min = 999999999
        self._max = 0
        self._avg = 0
        self._stddev = 0
        self._current = 0
        self._ts = []
        self._last = -1
        self._host = host


    def append_sent(self, timestamp, seq):
        self._sent += 1
        self._current = seq
        self._ts.append(timestamp)


    def append_received(self, timestamp, seq):
        self._received += 1
        popn = seq - self._last
        for _ in range(popn):
            delta = self._ts.pop(0)
        self._last = seq
        rtt = timestamp - delta
        self._min = min(self._min, rtt)
        self._max = max(self._max, rtt)
        self._sum += rtt
        self._sumsq += rtt*rtt
        return popn

    def get_last_received(self):
        return self._last


    def get_last_sent(self):
        return self._sent


    def get_stats(self):
        if self._received == 0:
            return 0,0,0,0,0,0
        mean = self._sum / self._received
        stddev = math.sqrt(self._sumsq/self._received - mean * mean)
        return self._sent, self._received, self._min, self._max, mean, stddev

class FPinger():
    """ fping-like: pinger for multihost """

    def __init__(self, single_host, filename, count=4, interval=1, timeout=3, pktlen=98):
        pid = os.getpid() & 0xFFFF
        self._id = pid
        self._hosts = []
        self._ipaddr = []
        self._stats = []
        self._dict = {}
        self._total = 0
        self._signal = True
        if single_host is not None:
            self._hosts.append(single_host)
            self._ipaddr.append(socket.gethostbyname(single_host))
            self._stats.append(PingStats(single_host))
            self._dict[single_host] = self._total
            self._total += 1
        if filename is not None:
            with open(filename) as f:
                for line in f:
                    host = line.rstrip('\n')
                    if len(host) > 0:
                        self._hosts.append(host)
                        self._ipaddr.append(socket.gethostbyname(host))
                        self._stats.append(PingStats(host))
                        self._dict[host] = self._total
                        self._total += 1
        self._count = count
        self._timeout = timeout
        self._pktlen = pktlen
        self._interval = interval
        try:
            # use SOCK_DGRAM so avoid root privileged
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
            # sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            if e.errno == 1:
                e.msg +=  "ICMP messages need privileged"
            raise socket.error(e.msg)
        except Exception as e:
            print ("Exception: %s" %(e))
        # use non block mode
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        self._rx_thread = threading.Thread(target=self._rx_pongs, args=())
        self._rx_thread.start()


    def _checksum(self, data):
        """  Verify the packet integritity """
        csum = 0
        data += b'\x00'

        for i in range(0, len(data) - 1, 2):
            csum += (int(data[i]) << 8) + int(data[i + 1])
            csum = (csum & 0xffff) + (csum >> 16)

        csum = ~csum & 0xffff
        return csum


    def _rx_pongs(self):
        """
        Receive ping from the socket.
        """
        while self._signal:
            readable = select.select([self.sock], [], [], self._timeout)
            if readable[0] == []: # Timeout
                for host, ipsrc, stat in zip(self._hosts, self._ipaddr, self._stats):
                    if stat.get_last_received() < stat.get_last_sent():
                        for miss in range(stat.get_last_received() + 1, stat.get_last_sent()):
                            print("Request timeout for {}({}): icmp_seq {:d}".format(host, ipsrc, miss))
                return

            time_received = time.time() * 1000
            recv_packet, addr = self.sock.recvfrom(self._pktlen + 40)
            ip_header = recv_packet[:20]
            icmp_len = len(recv_packet) - 20
            icmp_header = recv_packet[20:28]
            ipv, tos, iplen, ipid, ipoff, ttl, ipproto, ipsum, ipsrc, \
                ipdst = struct.unpack("!BBHHHBBH4s4s", ip_header)
            ipsrc = socket.inet_ntoa(ipsrc)
            if ipsrc in self._ipaddr:
                index = self._ipaddr.index(ipsrc)
                host = self._hosts[index]
            else:
                continue
            # ipdst = socket.inet_ntoa(ipdst)
            ptype, code, checksum, packet_id, seq = struct.unpack("bbHHh", icmp_header)
            if packet_id == self._id:
                time_bytes = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28:28 + time_bytes])[0] * 1000
                time_diff = time_received - time_sent
                idx = self._dict[host]
                popn = self._stats[idx].append_received(time_received, seq)
                if popn > 1:
                    for miss in range(seq - popn + 1, seq):
                        print("Request timeout for {}({}): icmp_seq {:d}".format(host, ipsrc, miss))
                if time_diff < 1000:
                    print("{:d} bytes from {}({}): icmp_seq={:d} ttl={:d} time={:.4f} ms".format(icmp_len, host, ipsrc, seq, ttl, time_diff))
                else:
                    print("{:d} bytes from {}({}): icmp_seq={:d} ttl={:d} time={:.4f} s".format(icmp_len, host, ipsrc, seq, ttl, (time_diff/1000.0)))
                continue
            else:
                print("unecpect icmp packet for {:d}".format(packet_id))
                continue


    def send_ping(self, host, ipaddr, sequence=1):
        """
        Send ping to the target host
        """
        ECHO_REQUEST = 8
        content = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        checksum = 0

        # Create a dummy heder with a 0 checksum.
        header = struct.pack("bbHHh", ECHO_REQUEST, 0, checksum, self._id, sequence)
        time_bytes = struct.calcsize("d")
        if self._pktlen < len(content):
            data = content[:(self._pktlen - time_bytes)]
        else:
            ntimes = (self._pktlen - time_bytes) / len(content)
            padding = (self._pktlen - time_bytes) % len(content)
            data = content * int(ntimes) + content[:padding]

        ts = time.time()
        data = struct.pack("d", ts) + bytes(data.encode('utf-8'))
        # Get the checksum on the data and the dummy header.
        checksum = self._checksum(header + data)
        header = struct.pack("bbHHh", ECHO_REQUEST, 0, socket.htons(checksum), self._id, sequence)
        packet = header + data
        n = self.sock.sendto(packet, (ipaddr, 1))
        if n < 0:
            print("fail to send")
        else:
            idx = self._dict[host]
            self._stats[idx].append_sent(ts * 1000, sequence)


    def ping_all(self):
        """
        ping hosts
        """
        for host, ip in zip(self._hosts, self._ipaddr):
            print ("Ping %s (%s): %d data bytes" % (host, ip, self._pktlen))
        for i in range(self._count):
            for host, ip in zip(self._hosts, self._ipaddr):
                try:
                    # delay = self.ping_pong(host, ip, i)
                    self.send_ping(host, ip, sequence=i)
                except socket.gaierror as e:
                    print ("Ping failed. (socket error: '%s')" % e[1])
                    break
            try:
                time.sleep(self._interval)
            except KeyboardInterrupt:
                break


    def print_icmp_stats(self):
        print("")
        for host in self._hosts:
            idx = self._dict[host]
            tx_pkts, rx_pkts, min_lat, max_lat, mean_lat, stddev = self._stats[idx].get_stats()
            print("--- %s ping statistics ---" % host)
            print("{:d} packets transmitted, {:d} packets received, {:.2f}%% packet loss".format(tx_pkts, rx_pkts, (100* (tx_pkts - rx_pkts)/ tx_pkts)))
            print("round-trip min/avg/max/stddev = {:.2f}/{:.2f}/{:.2f}/{:.2f} ms".format(min_lat, mean_lat, max_lat, stddev))
            print("")


    def __del__(self):
        if self.sock is not None:
            self.sock.close()


    def signal_handler(self):
        self._signal = False
        self._rx_thread.join()
        self.print_icmp_stats()
        sys.exit()


def main():
    """main functions with argparse"""
    parser = argparse.ArgumentParser(description='python ping script similar to fping')
    parser.add_argument(dest='host', nargs="?", action="store", help='single target host')
    parser.add_argument('-f', '--file', dest='filename', action="store", type=str,
                        help='file contains host list')
    parser.add_argument('-c', '--count', dest='count', action="store", type=int, default=4,
                        help='icmp packet count to a destination')
    parser.add_argument('-i', '--interval', dest='interval', action="store", type=float,
                        default=1, help='icmp packet interval to a destination')
    parser.add_argument('-s', '--size', dest='size', action="store", type=int, default=98,
                        help='icmp packet size')

    args = parser.parse_args()
    if args.host is None and args.filename is None:
        print("specify a host or host file")
        sys.exit(0)
    pinger = FPinger(single_host=args.host, filename=args.filename, count=args.count, interval=args.interval, pktlen=args.size)

    signal.signal(signal.SIGINT, lambda signal, frame: pinger.signal_handler())
    pinger.ping_all()
    signal.raise_signal(signal.SIGINT)


if __name__ == '__main__':
    main()
