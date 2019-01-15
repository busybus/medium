# RA, 2019-01-15
# Download an OpenStreetMap file based on a lat-lon bounding box

# License: CC0 -- "No rights reserved"

# IMPORTS:

import os
import json
import inspect
import logging
import datetime as dt
import urllib.request, urllib.error

# INPUT FILES:

pass

# OUTPUT FILES:

OFILE = {
    # Put the downloaded *.osm files here
    'OSM': "OUTPUT/maps/UV/{region}.osm",

    # Record meta-info here
    'OSM-meta': "OUTPUT/maps/{region}_meta.txt",
}

for fn in OFILE.values():
    os.makedirs(os.path.dirname(fn).format(), exist_ok=True)

# PARAMETERS:

PARAM = {
    # Bounding box to download [left, bottom, right, top]
    # https://wiki.openstreetmap.org/wiki/API_v0.6
    'regions': {
        'kaohsiung_small': [120.2206, 22.4827, 120.4308, 22.7578],
        'kaohsiung_large': [119.9377, 22.1645, 120.8084, 23.3347],
    },

    # Download URL
    'API-URL': "zhttps://overpass-api.de/api/map?bbox={bbox}",
}

# AUXILIARY:

# https://stackoverflow.com/questions/34491808/how-to-get-the-current-scripts-code-in-python
THIS = inspect.getsource(inspect.getmodule(inspect.currentframe()))

# Set logger verbosity and output format
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s [%(asctime)s] : %(message)s",
    datefmt="%Y%m%d %H:%M:%S %Z"
)


# Log which files are opened
def logged_open(filename, mode='r', *argv, **kwargs):
    from builtins import open as builtin_open
    logging.info("({}):\t{}".format(mode, filename))
    return builtin_open(filename, mode, *argv, **kwargs)


open = logged_open


# SLAVES:

def download(region):
    bbox = PARAM['regions'][region]

    url = PARAM['API-URL'].format(bbox="{0},{1},{2},{3}".format(*bbox))
    out = OFILE['OSM'].format(region=region)

    meta = {
        'Region': region,
        'File location': out,
        'Bounding box': bbox,
        'Source': url,
        'Retrieval (UTC)': dt.datetime.utcnow().isoformat(),
        'Script': THIS,
    }

    with urllib.request.urlopen(url) as response:
        with open(out, 'wb') as fd:
            fd.write(response.read())

    with open(OFILE['OSM-meta'].format(region=region), 'w') as fd:
        json.dump(meta, fd, indent=2)


# MASTER:

def download_all():
    for region in PARAM['regions']:
        try:
            logging.info("Downloading region '{}'...".format(region))
            download(region)
            logging.info("Download OK!")
        except urllib.error.URLError:
            logging.exception("Download failed (no connection or wrong URL?).")
        except:
            logging.exception("Download failed.")


# ENTRY:

if __name__ == "__main__":
    download_all()
