from telnetlib import Telnet
import csv
import time
import re

telnet_port = 8081
timeout_sec = 60

# target line
# 2020-11-14T08:37:35 883.129 INF Time: 14.68m FPS: 20.00 Heap: 1095.0MB Max: 1117.5MB Chunks: 240 CGO: 54 Ply: 1 Zom: 4 Ent: 9 (13) Items: 1 CO: 1 RSS: 2171.2MB

target_pattern = r'^(2\d{3})-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])T(\d+?):(\d+?):(\d+?)\s(.+?)\sINF\sTime:\s([\d\.]+?)m\sFPS:\s([\d\.]+?)\sHeap:\s([\d\.]+?)MB\sMax:\s([\d\.]+?)MB\sChunks:\s(\d+?)\sCGO:\s(\d+?)\sPly:\s(\d+?)\sZom:\s(\d+?)\sEnt:\s(\d+?)\s\((\d+?)\)\sItems:\s(\d+?)\sCO:\s(\d+?)\sRSS:\s([\d\.]+?)MB'
repatter = re.compile(target_pattern)

with open('server-status.csv', 'w') as f:
    writer = csv.writer(f)
    # CSV header
    writer.writerow(['timestamp', 'time from boot(min)', 'FPS', 'Heap memory(MB)', 'Max memory(MB)', 'chunks', 'CGO', 'Players', 'Zombie', 'Entity', 'Total Entity', 'Items', 'CO', 'RSS(MB)'])

    # retry loop
    while True:
        try:
            # connect telnet server of 7dtd
            with Telnet('localhost', telnet_port, timeout_sec) as tn:

                # parse and write loop
                while True:

                    # read line and match test
                    line = tn.read_until(b"\n", timeout=timeout_sec).decode('utf-8')
                    print(line)
                    result = repatter.match(line)

                    if result is not None:
                        # pickup and write
                        g = result.groups()
                        toCSV = [
                            f"{g[0]}/{g[1]}/{g[2]}T{g[3]}:{g[4]}:{g[5]}",
                            g[7], # time from boot(min)
                            g[8], # FPS
                            g[9], # Heap memory(MB)
                            g[10], # Max memory(MB)
                            g[11], # chunks
                            g[12], # CGO
                            g[13], # Players
                            g[14], # Zombie
                            g[15], # Entity
                            g[16], # Total Entity
                            g[17], # Items
                            g[18], # CO
                            g[19], # RSS(MB)
                        ]

                        writer.writerow(toCSV)
                        f.flush()
        except Exception as e:
            print("detect exception. so disconnect telnet server.")
            print(e)
            # wait network recovery
            time.sleep(10)
        