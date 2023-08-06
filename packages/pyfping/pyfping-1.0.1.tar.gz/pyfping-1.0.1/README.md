# pyfping 

ping-like pythonic pinger, works for multiple hosts

```
usage: ping.py [-h] [-f FILENAME] [-c COUNT] [-i INTERVAL] [-s SIZE] [host]

python ping script similar to fping

positional arguments:
  host                  single target host

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        file contains host list
  -c COUNT, --count COUNT
                        icmp packet count to a destination
  -i INTERVAL, --interval INTERVAL
                        icmp packet interval to a destination
  -s SIZE, --size SIZE  icmp packet size
```

Result is like below:
```
admin$ pyfping -f some_file_contain_target_hosts
Ping www.baidu.com (110.242.68.3): 98 data bytes
Ping www.taobao.com (121.29.9.227): 98 data bytes
106 bytes from www.baidu.com(110.242.68.3): icmp_seq=0 ttl=44 time=44.3398 ms
106 bytes from www.taobao.com(121.29.9.227): icmp_seq=0 ttl=46 time=38.8643 ms
106 bytes from www.baidu.com(110.242.68.3): icmp_seq=1 ttl=44 time=44.9580 ms
106 bytes from www.taobao.com(121.29.9.227): icmp_seq=1 ttl=46 time=38.3545 ms
106 bytes from www.baidu.com(110.242.68.3): icmp_seq=2 ttl=44 time=44.3999 ms
106 bytes from www.taobao.com(121.29.9.227): icmp_seq=2 ttl=46 time=38.4810 ms
106 bytes from www.baidu.com(110.242.68.3): icmp_seq=3 ttl=44 time=44.8110 ms
106 bytes from www.taobao.com(121.29.9.227): icmp_seq=3 ttl=46 time=39.9470 ms

--- www.baidu.com ping statistics ---
4 packets transmitted, 4 packets received, 0.00% packet loss
round-trip min/avg/max/stddev = 44.34/44.63/44.96/0.26 ms

--- www.taobao.com ping statistics ---
4 packets transmitted, 4 packets received, 0.00% packet loss
round-trip min/avg/max/stddev = 38.35/38.91/39.95/0.63 ms
```