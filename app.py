# Small app to forward Plex webhooks to Hue bulbs.
#
# Hue API information https://developers.meethue.com/develop/hue-api/groupds-api/
# Plex Webhooks information https://support.plex.tv/articles/115002267687-webhooks/
import json
import requests
from flask import Flask, request
import logging
from logutils import logformat as lf

# Create the app
app = Flask(__name__)

# Setup logging
infoLogFile = 'C:/hosted_python_apps/logs/PlexClient/debug.log'
errorLogFile = 'C:/hosted_python_apps/logs/PlexClient/error.log'
logging.basicConfig(filename=infoLogFile, format='%(asctime)s %(message)s', level=logging.INFO)
logging.basicConfig(filename=errorLogFile, level=logging.ERROR)

local_phone_uuid = '013b038c87a5cd67-com-plexapp-android'
urlGroup = 'http://192.168.1.95/api/rmnxM5hTeDs-3Oyot-zfpeC6bnd4Nog0sSkbRkJe/groups/1/action'


# General GET
@app.route('/', methods=['GET'])
def hello():
    return 'HELLO'


# Main home route that Plex posts webhooks to
@app.route('/', methods=['POST'])
def ingestPlexWebhook():
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
    elif not player.get('uuid') == local_phone_uuid:
        return ''

    # Probably don't need to always log local plays
    logging.info(lf.formatLog(player, metaData))

    # Lot more to do if we're local and on my phone
    # Only change the bulbs for movies
    if not metaData.get('type') == 'movie':
        return ''

    # Only act on play/resume/pause/stop
    if event == 'media.play' or event == 'media.resume':
        # {"on":true,"bri":254, "hue":39392}
        requests.put(urlGroup, json={'on': True, 'bri': 30})

    elif event == 'media.stop' or event == 'media.pause':
        requests.put(urlGroup, json={'on': True, 'bri': 254})

    # Required
    return ''


if __name__ == '__main__':
    app.run(debug=True)
