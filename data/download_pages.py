import pickle
import sys
import os
import subprocess
import time

start = int(sys.argv[1])
end = int(sys.argv[2])

processes = set()
max_processes = int(sys.argv[3])

main_links = pickle.load(open('./saved_files/saved_links.p', 'rb'))
extra_links = pickle.load(open('./extra_pages.p', 'rb'))

for i, link in enumerate(main_links[start:end+1]):
    num = extra_links[i+start]
    for j in range(0, num+1):
        print(i, link, num)
        processes.add(subprocess.Popen(["python3", "save_rendered_webpage.py",
            link, str(j), str(i + start)]))
        if len(processes) >= max_processes:
            print("============== Waiting")
            os.wait()
            print("============== Waiting Ends")
            processes.difference_update([p for p in processes if p.poll() is
                not None])
        time.sleep(1)

