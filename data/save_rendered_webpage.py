import sys
import pickle
import requests

error_count = 0

link = sys.argv[1]
page = sys.argv[2]
i = sys.argv[3]

if page != '0':
    link += "&pg=" + page

try:
    html_doc = requests.get(link)
    with open("saved_files/saved" + i + "_" + page + ".html", "wb") as fw:
        fw.write(html_doc.content)

    if html_doc.status_code != requests.codes.ok:
        print("Error")

    time.sleep(20)
except:
    error_count += 1
    

