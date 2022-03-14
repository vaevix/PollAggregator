import json
import urllib.request
from datetime import date
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from pykalman import KalmanFilter

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
        self.FormattedData = dict(zip([x[0] for x in self.Settings['Candidats']], [[] for _ in self.Settings['Candidats']]))
        for sondage in self.Data:
            for t in [x for x in sondage['tours'] if x['tour'] == tour]:
                for hypo in t['hypotheses']:
                    for result in [x for x in hypo['candidats'] if x['candidat'] in self.FormattedData.keys()]:
                        self.FormattedData[result['candidat']].append({'candidat': result['candidat'],
                                                                       'date': date.fromisoformat(sondage['fin_enquete']),
                                                                       'score': float(result['intentions']),
                                                                       'err_inf': float(result['erreur_inf']),
                                                                       'err_sup': float(result['erreur_sup']),
                                                                       'rolling': sondage['rolling'] == 'true'})
    def setChartSettings(self, fig, ax):



        facecolor, axcolor = '#384f75', '#ffffffC0'
        ax.tick_params(color=axcolor, labelcolor=axcolor)
        for spine in ax.spines.values():
            spine.set_edgecolor(axcolor)
        fig.set_facecolor(facecolor)


        ax.set_ylim([0, None])
        ax.set_facecolor(facecolor)
        ax.grid(color=axcolor, alpha=0.1)
        ax.vlines(x=[date(2022, 2, 24), '2022-02-24'], ymin=0, ymax=1, transform=ax.get_xaxis_transform(),
                  color='#FF000070', label='Invasion de l\'Ukraine', linewidth=1)
        ax.vlines(x=[date(2022, 3, 7), '2022-03-07'], ymin=0, ymax=1, transform=ax.get_xaxis_transform(),
                  color='#00FF0040', label='Publication de la liste des candidats', linewidth=1)

        for line in fig.legend(loc='lower center', facecolor='#25354C', edgecolor='#121A26', labelcolor=axcolor) \
                .get_lines():
            line.set_linewidth(2)
            line.set_alpha(1)


    def getimage(self):
        candidat = 'Eric Zemmour'
        couleur = [x[1] for x in self.Settings['Candidats'] if x[0] == candidat].pop() + \
                  [x[2] for x in self.Settings['Candidats'] if x[0] == candidat].pop()
        data = [x for x in self.FormattedData[candidat]
                if self.Settings['From'] <= x['date'] <= self.Settings['To']]
        fig, ax = plt.subplots(nrows=1, ncols=1)


        dates, scores =[x['date'] for x in data], [x['score'] for x in data]
        ax.plot_date(dates, scores, color=couleur)

        self.setChartSettings(fig, ax)
        plt.show()


if __name__ == '__main__':
    foo = PollData()
    foo.Settings['Instituts'] = {'Opinion Way', 'Odoxa', 'Ifop', 'Ipsos',
                                 'Harris Interactive', 'BVA', 'Elabe', 'Kantar Public'}

    foo.Settings['Candidats'] = {('Jean Lassalle', '#26c4ec', '20'), ('Emmanuel Macron', '#ffeb00', '20'),
                                 ('Valérie Pécresse', '#0066cc', '50'), ('Nathalie Arthaud', '#bb0000', '20'),
                                 ('Fabien Roussel', '#dd0000', '20'), ('Nicolas Dupont-Aignan', '#0082C4', '30'),
                                 ('Philippe Poutou', '#bb0000', '20'), ('Anne Hidalgo', '#FF8080', '30'),
                                 ('Jean-Luc Mélenchon', '#FF8080', '20'), ('Eric Zemmour', '#909090', '40'),
                                 ('Yannick Jadot', '#00c000', '20'), ('Marine Le Pen', '#0D378A', '90')}
    # Codes couleurs : https://fr.wikipedia.org/wiki/Mod%C3%A8le:Infobox_Parti_politique_fran%C3%A7ais/couleurs
    # Le canal alpha est utilisé pour assurer la visibilité, en particulier pour les partis de droite.
    # Exception : gris de Zemmour éclairci pour être mieux visible.
    foo.Settings['From'] = date(2022, 1, 1)
    foo.Settings['To'] = date(2099, 12, 31)
    foo.load('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json')
    foo.formatdata('Premier tour')
    foo.getimage()
    print(foo.Candidates)
