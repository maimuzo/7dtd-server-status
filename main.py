from telnetlib import Telnet
import csv
import time
import re

telnet_port = 8081
timeout_sec = 30

# target line
# 2020-11-14T08:37:35 883.129 INF Time: 14.68m FPS: 20.00 Heap: 1095.0MB Max: 1117.5MB Chunks: 240 CGO: 54 Ply: 1 Zom: 4 Ent: 9 (13) Items: 1 CO: 1 RSS: 2171.2MB

target_pattern = r'^(2\d{3})-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])T(\d+?):(\d+?):(\d+?)\s(.+?)\sINF\sTime:\s([\d\.]+?)m\sFPS:\s([\d\.]+?)\sHeap:\s([\d\.]+?)MB\sMax:\s([\d\.]+?)MB\sChunks:\s(\d+?)\sCGO:\s(\d+?)\sPly:\s(\d+?)\sZom:\s(\d+?)\sEnt:\s(\d+?)\s\((\d+?)\)\sItems:\s(\d+?)\sCO:\s(\d+?)\sRSS:\s([\d\.]+?)MB'
repatter = re.compile(target_pattern)

with open('server-status.csv', 'w') as f:
    writer = csv.writer(f)
    # CSV header
    writer.writerow(['datetime', 'time from boot(min)', 'FPS', 'Heap memory(MB)', 'Max memory(MB)', 'chunks', 'CGO', 'Players', 'Zombie', 'Entity', 'Total Entity', 'Items', 'CO', 'RSS(MB)'])

    # retry loop
    while True:
        try:
            # connect telnet server of 7dtd
            with Telnet('localhost', telnet_port, timeout_sec) as tn:

                # parse and write loop
                while True:

                    # read line and match test
                    line = tn.read_until(b"\n", timeout=timeout_sec).decode('utf-8')
                    result = repatter.match(line)

                    if result is not None:
                        # pickup and write
                        toCSV = []
                        toCSV[0] = f"{groups(1)}/{groups(2)}/{groups(3)}T{groups(4)}:{groups(5)}:{groups(6) {groups(7)}}/{groups(2)}"
                        toCSV[1] = groups(8) # time from boot(min)
                        toCSV[2] = groups(9) # FPS
                        toCSV[3] = groups(10) # Heap memory(MB)
                        toCSV[4] = groups(11) # Max memory(MB)
                        toCSV[5] = groups(12) # chunks
                        toCSV[6] = groups(13) # CGO
                        toCSV[7] = groups(14) # Players
                        toCSV[8] = groups(15) # Zombie
                        toCSV[9] = groups(16) # Entity
                        toCSV[10] = groups(17) # Total Entity
                        toCSV[11] = groups(18) # Items
                        toCSV[12] = groups(19) # CO
                        toCSV[13] = groups(20) # RSS(MB)

                        writer.writerow(toCSV)
        except:
            print("detect exception")
            # wait network recovery
            time.sleep(10)
        