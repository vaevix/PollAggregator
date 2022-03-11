import json
import urllib.request


class PollData:
    def __init__(self):
        self.Data = []

    """
        Loads the data from the provided source
    :param source: URL for the data. http://, https://, ftp://, ftps://. Filepaths should be prefixed with file://.

    """
    def load(self, source: str):
        with urllib.request.urlopen(source) as s:
            self.Data = json.load(s)


if __name__ == '__main__':
    foo = PollData()
    foo.load('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json')
    