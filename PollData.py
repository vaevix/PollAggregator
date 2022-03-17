import json
import urllib.request
from datetime import date
import matplotlib.pyplot as plt
from Kfilter import KalmanFilter

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
        for sondage in [x for x in self.Data if (x['nom_institut'] in self.Settings['Instituts'])]:
            for t in [x for x in sondage['tours'] if x['tour'] == tour]:
                for hypo in t['hypotheses']:
                    for result in [x for x in hypo['candidats'] if x['candidat'] in self.FormattedData.keys()]:
                        self.FormattedData[result['candidat']].append({'candidat': result['candidat'],
                                                                       'date': date.fromisoformat(sondage['fin_enquete']),
                                                                       'score': float(result['intentions']),
                                                                       'err_inf': float(result['erreur_inf']),
                                                                       'err_sup': float(result['erreur_sup']),
                                                                       'rolling': sondage['rolling'] == 'true'})

    @staticmethod
    def setchartsettings(fig, ax):
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
        ax.vlines(x=[date(2022, 4, 10), '2022-04-10'], ymin=0, ymax=1, transform=ax.get_xaxis_transform(),
                  color='#036ffcF0', label='1er tour de l\'élection présidentielle', linewidth=1)
        for line in fig.legend(loc='lower center', facecolor='#25354C', edgecolor='#121A26', labelcolor=axcolor) \
                .get_lines():
            line.set_linewidth(2)
            line.set_alpha(1)

        ax.text(0, 0, '@VaeVix', transform=ax.transAxes, fontsize=60, color='white',
                alpha=0.2, ha='left', va='bottom', rotation='0')

    def getimage(self, candidatA):
        fig, ax = plt.subplots(nrows=1, ncols=1)
        tf = {'family': 'serif', 'color':  'white', 'weight': 'normal'}
        fig.suptitle('Intentions de vote à l\'élection présidentielle de 2022', fontsize=22, fontdict=tf)
        ax.set_title('Instituts pris en compte : '+', '.join(foo.Settings['Instituts']), fontsize=10, color='white')
        for candidat in candidatA:
            couleur = [x[1] for x in self.Settings['Candidats'] if x[0] == candidat].pop() +\
                      [x[2] for x in self.Settings['Candidats'] if x[0] == candidat].pop()
            ckline = [x[1] for x in self.Settings['Candidats'] if x[0] == candidat].pop() + 'FF'
            cerror = [x[1] for x in self.Settings['Candidats'] if x[0] == candidat].pop() + '20'
            data = [x for x in self.FormattedData[candidat] if self.Settings['From'] <= x['date'] <= self.Settings['To']]
            data.sort(key=lambda x: x['date'])

            KF = KalmanFilter(data[0]['score'])
            dates, scores, Kscores = [x['date'] for x in data], [x['score'] for x in data],\
                                     [KF.filter(x['score']) for x in data]

            ax.plot_date(dates, scores, color=couleur)

            ax.plot_date(dates, [x[0][0] for x in Kscores], color=ckline, ls='-', marker=None)
            ax.annotate('   '+str(round(Kscores[-1][0][0], 0)) + '% - '+candidat, (dates[-1], Kscores[-1][0][0]),
                        color=ckline)

            # Marges d'erreur
            plt.fill_between(dates, [x[2][0] for x in Kscores], [x[3][0] for x in Kscores], color=cerror)

        self.setchartsettings(fig, ax)
        plt.show()

## TODO : Replace with proper script / argsparse
if __name__ == '__main__':
    foo = PollData()
    foo.Settings['Instituts'] = {'Opinion Way', 'Odoxa', 'Ifop', 'Ipsos',
                                 'Harris Interactive', 'BVA', 'Elabe', 'Kantar Public'}

    # foo.Settings['Instituts'] = {'Elabe'}


    foo.Settings['Candidats'] = {('Jean Lassalle', '#26c4ec', '30'), ('Emmanuel Macron', '#ffeb00', '30'),
                                 ('Valérie Pécresse', '#007FFF', '50'), ('Nathalie Arthaud', '#bb0000', '30'),
                                 ('Fabien Roussel', '#dd0000', '30'), ('Nicolas Dupont-Aignan', '#0082C4', '40'),
                                 ('Philippe Poutou', '#bb0000', '30'), ('Anne Hidalgo', '#FF8080', '40'),
                                 ('Jean-Luc Mélenchon', '#FF8080', '40'), ('Eric Zemmour', '#909090', '50'),
                                 ('Yannick Jadot', '#00c000', '30'), ('Marine Le Pen', '#A775FF', '40')}
    # Base codes couleurs : https://fr.wikipedia.org/wiki/Mod%C3%A8le:Infobox_Parti_politique_fran%C3%A7ais/couleurs
    # Le canal alpha est utilisé pour assurer la visibilité, en particulier pour les partis de droite.
    # Exception : gris de Zemmour, bleu de Pécresse, éclaircis pour être mieux visible.
    # Teinte Le Pen modifiée même raison.

    foo.Settings['From'] = date(2022, 1, 1)
    foo.Settings['To'] = date(2099, 1, 1)
    foo.load('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json')
    foo.formatdata('Premier tour')

    foo.getimage(['Marine Le Pen', 'Jean-Luc Mélenchon'])
