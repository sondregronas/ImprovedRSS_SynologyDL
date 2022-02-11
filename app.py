from flask import Flask, request, Response
import subprocess
import time

import tempfile
import json

hostip = "192.168.1.5"
host_port = 5000
searchURL = "http://127.0.0.1:4444/search/"

app = Flask(__name__)

@app.route('/')
def queryrss():
    json = request.args.get('j', default="empty")
    active = str(request.args.get('active', default='yes'))

    if active != "yes":
        return "Query inactive"

    # If JSON is empty, treat it like a search
    if json == "empty":
        return querysearch(request)

    inv = 'python3 rssmerge.py ' + json + ' -l 0'

    i = 0
    while i < 10:
        try:
            response = subprocess.check_output(inv, shell=True)
            return Response(response, mimetype='application/rss+xml')
        except:
            print('Error loading RSS, retrying..')
            time.sleep(2)
            continue

    return 'Error loading RSS'


def querysearch(request):
    query = request.args.get('search')
    amount = str(request.args.get('limit', default=50))
    category = str(request.args.get('category', default=41))
    link = str(f"{searchURL}{query}?category={category}&limit={amount}")

    data = {"title": "RSS Search",
            "size": int(amount),
            "feeds": [{"name": "Search",
                       "source": link,
                       "size": int(amount)
                     }]
           }

    path = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(data, path)
    path.flush()

    inv = 'python3 rssmerge.py ' + path.name + ' -l 0'

    i = 0
    while i < 10:
        try:
            response = subprocess.check_output(inv, shell=True)
            return Response(response, mimetype='application/rss+xml')
        except:
            print('Error loading RSS, trying again in 2 seconds')
            time.sleep(2)
            continue

    return 'Error loading RSS'

if __name__ == "__main__":
    app.run(host=hostip, port=host_port)