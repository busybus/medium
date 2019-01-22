# RA, 2019-01-22
# Compress and decompress a JSON object

# License: CC0 -- "No rights reserved"

# For zlib license, see https://docs.python.org/3/license.html
import zlib

import json, base64

ZIPJSON_KEY = 'base64(zip(o))'

def json_zip(j):
    j = {
        ZIPJSON_KEY: base64.b64encode(
            zlib.compress(
                json.dumps(j).encode('utf-8')
            )
        ).decode('ascii')
    }

    return j


def json_unzip(j, insist=True):
    try:
        assert (j[ZIPJSON_KEY])
        assert (set(j.keys()) == {ZIPJSON_KEY})
    except:
        if insist:
            raise RuntimeError("JSON not in the expected format {" + str(ZIPJSON_KEY) + ": zipstring}")
        else:
            return j

    try:
        j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
    except:
        raise RuntimeError("Could not decode/unzip the contents")

    try:
        j = json.loads(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents")

    return j


import unittest

class TestJsonZipMethods(unittest.TestCase):
    # Unzipped
    unzipped = {'a': "A", 'b': "B"}

    # Zipped
    zipped = {ZIPJSON_KEY: "eJyrVkpUslJQclTSUVBKArGclGoBLeoETw=="}

    # List of items
    items = [123, "123", unzipped]

    def test_json_zip(self):
        self.assertEqual(self.zipped, json_zip(self.unzipped))

    def test_json_unzip(self):
        self.assertEqual(self.unzipped, json_unzip(self.zipped))

    def test_json_zipunzip(self):
        for item in self.items:
            self.assertEqual(item, json_unzip(json_zip(item)))

    def test_json_unzip_insist_failure(self):
        for item in self.items:
            with self.assertRaises(RuntimeError):
                json_unzip(item, insist=True)

    def test_json_unzip_noinsist_justified(self):
        for item in self.items:
            self.assertEqual(item, json_unzip(item, insist=False))

    def test_json_unzip_noinsist_unjustified(self):
        self.assertEqual(self.unzipped, json_unzip(self.zipped, insist=False))


if __name__ == '__main__':
    unittest.main()
