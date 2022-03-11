import json
import urllib.request

"""
Usage: Gets and prepares poll data from a json file. The format used should be similar to :
https://github.com/nsppolls/nsppolls
"""


class PollData:
    def __init__(self):
        self.Data = []
        self.PInstitute = set()
    """
    Loads the data from the provided source
    :param source: URL for the data. http://, https://, ftp://, ftps://. Filepaths should be prefixed with file://.

    """
    def load(self, source: str):
        with urllib.request.urlopen(source) as s:
            self.Data = json.load(s)
        self.PInstitute = set([x['nom_institut'] for x in self.Data])


if __name__ == '__main__':
    foo = PollData()
    foo.load('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json')
    print(foo.PInstitute)
