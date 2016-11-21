import json
import re
import base64
import hashlib
import tempfile
import os

from pymisp.tools import stix

misperrors = {'error': 'Error'}
userConfig = {}
inputSource = ['file']

moduleinfo = {'version': '0.2', 'author': 'Hannah Ward',
              'description': 'Import some stix stuff',
              'module-type': ['import']}

moduleconfig = []


def handler(q=False):
    # Just in case we have no data
    if q is False:
        return False

    # The return value
    r = {'results': []}

    # Load up that JSON
    q = json.loads(q)

    # It's b64 encoded, so decode that stuff
    package = base64.b64decode(q.get("data")).decode('utf-8')

    # If something really weird happened
    if not package:
        return json.dumps({"success": 0})

    tfile = tempfile.NamedTemporaryFile(mode="w", prefix="STIX", delete=False)
    tfile.write(package)
    tfile.close()

    pkg = stix.load_stix(tfile.name)

    for attrib in pkg.attributes:
        r["results"].append({ "values" : [attrib.value] , "types": [attrib.type], "categories": [attrib.category]})

    os.unlink(tfile.name)
    return r

def introspection():
    modulesetup = {}
    try:
        userConfig
        modulesetup['userConfig'] = userConfig
    except NameError:
        pass
    try:
        inputSource
        modulesetup['inputSource'] = inputSource
    except NameError:
        pass
    return modulesetup


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo