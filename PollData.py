import json
import urllib.request
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

"""
Usage: Gets and prepares poll data from a json file. The format used should be similar to :
https://github.com/nsppolls/nsppolls
"""


class PollData:
    def __init__(self):
        self.Data = []
        self.FormattedData = dict()
        self.PInstitute = set()
        self.Candidates = set()
        self.Settings = dict()
    """
    Loads the data from the provided source
    :param source: URL for the data. http://, https://, ftp://, ftps://. Filepaths should be prefixed with file://.

    """
    def load(self, source: str):
        with urllib.request.urlopen(source) as s:
            self.Data = json.load(s)
        self.PInstitute = set([x['nom_institut'] for x in self.Data])
        for sondage in self.Data:
            for tour in sondage['tours']:
                for hypothese in tour['hypotheses']:
                    for candidat in hypothese['candidats']:
                        if candidat['candidat'] not in self.Candidates:
                            self.Candidates.add(candidat['candidat'])

    def formatdata(self, tour: str):
        self.FormattedData = dict(zip(self.Settings['Candidats'], [[] for x in self.Settings['Candidats']]))
        for sondage in self.Data:
            for t in [x for x in sondage['tours'] if x['tour'] == tour]:
                for hypo in t['hypotheses']:
                    for result in [x for x in hypo['candidats'] if x['candidat'] in self.FormattedData.keys()]:
                        self.FormattedData[result['candidat']].append({'candidat': result['candidat'],
                                                                  'date': date.fromisoformat(sondage['fin_enquete']),
                                                                  'score': float(result['intentions']),
                                                                  'err_inf': float(result['erreur_inf']),
                                                                  'err_sup': float(result['erreur_sup']),
                                                                  'rolling': sondage['rolling'] == 'true'
                                                                  })


    def getimage(self, width: int, height: int, minscore: float):
        data = cbook.get_sample_data('goog.npz', np_load=True)['price_data']
        ax = plt.plot('date', 'adj_close', data=data)[0].axes
        # common to all three:

        # Major ticks every half year, minor ticks every month,
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.grid(True)
        ax.set_ylabel(r'Price [\$]')

        # different formats:


        ax.set_title('ConciseFormatter', loc='left', y=0.85, x=0.02, fontsize='medium')
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        plt.show()


if __name__ == '__main__':
    foo = PollData()
    foo.Settings['Instituts'] = {'Opinion Way', 'Odoxa', 'Ifop', 'Ipsos',
                                 'Harris Interactive', 'BVA', 'Elabe', 'Kantar Public'}

    foo.Settings['Candidats'] = {'Jean Lassalle', 'Emmanuel Macron', 'Valérie Pécresse', 'Nathalie Arthaud',
                                 'Fabien Roussel', 'Nicolas Dupont-Aignan', 'Philippe Poutou', 'Anne Hidalgo',
                                 'Jean-Luc Mélenchon', 'Eric Zemmour', 'Yannick Jadot', 'Marine Le Pen'}
    foo.Settings['From'] = date(2022, 2, 4)
    foo.Settings['To'] = date(2099, 12, 31)
    foo.load('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json')
    bar = foo.formatdata('Premier tour')
    foo.getimage(800, 600, 1.0)
    print(foo.Candidates)
