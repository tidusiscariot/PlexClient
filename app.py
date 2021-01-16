# Small app to forward Plex webhooks to Hue bulbs.
import json
import requests
from flask import Flask, request
import logging
import os
from logutils import logformat as lf

# Create the app
app = Flask(__name__)

# Setup logging
# logFile = os.path.relpath('.') + '/logs/debug.log'
logFile = 'C:/hosted_python_apps/logs/PlexClient/debug.log'
logging.basicConfig(filename=logFile, format='%(asctime)s %(message)s', level=logging.INFO)


# General GET
@app.route('/', methods=['GET'])
def hello():
    return 'HELLO'


# Main home route that Plex posts webhooks to
@app.route('/', methods=['POST'])
def ingestPlexWebhook():
    urlBulb1 = 'http://192.168.1.95/api/rmnxM5hTeDs-3Oyot-zfpeC6bnd4Nog0sSkbRkJe/lights/1/state'
    urlBulb2 = 'http://192.168.1.95/api/rmnxM5hTeDs-3Oyot-zfpeC6bnd4Nog0sSkbRkJe/lights/2/state'
    urlBulb3 = 'http://192.168.1.95/api/rmnxM5hTeDs-3Oyot-zfpeC6bnd4Nog0sSkbRkJe/lights/3/state'

    # Encode to a useful json obj
    jsonReq = json.loads(request.values.get('payload'))

    # Get  the metadata to see what type of media is playing
    metaData = jsonReq.get('Metadata')

    # Get event data
    event = jsonReq.get('event')

    # Get the player data
    player = jsonReq.get('Player')

    # Log and exit if remote user
    if not player.get('local'):
        logging.info(lf.formatLog(player, metaData))
        return ''
    # Exit if not my phone uuid
    elif not player.get('uuid') == '013b038c87a5cd67-com-plexapp-android':
        return ''

    # Lot more to do if we're local and on my phone
    # Only change the bulbs for movies
    if not metaData.get('type') == 'movie':
        return ''

    # Only act on play/resume/pause/stop
    if event == 'media.play' or event == 'media.resume':
        requests.put(urlBulb1, json={'on': True, 'bri': 30})
        requests.put(urlBulb2, json={'on': True, 'bri': 30})
        requests.put(urlBulb3, json={'on': True, 'bri': 30})

    elif event == 'media.stop' or event == 'media.pause':
        requests.put(urlBulb1, json={'on': True, 'bri': 254})
        requests.put(urlBulb2, json={'on': True, 'bri': 254})
        requests.put(urlBulb3, json={'on': True, 'bri': 254})

    # Required
    return ''


if __name__ == '__main__':
    app.run(debug=True)
