from PollData import PollData
from datetime import date

foo = PollData()
foo.Settings['Instituts'] = {'Opinion Way', 'Odoxa', 'Ifop', 'Ipsos',
                             'Harris Interactive', 'BVA', 'Elabe', 'Kantar Public'}

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
foo.Settings['Source'] = 'https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.json'

foo.load(foo.Settings['Source'])
foo.formatdata('Premier tour', '*')

foo.getimage(['Emmanuel Macron', 'Marine Le Pen', 'Jean-Luc Mélenchon', 'Valérie Pécresse', 'Eric Zemmour',
              'Fabien Roussel', 'Yannick Jadot', 'Jean Lassalle', 'Nathalie Arthaud', 'Nicolas Dupont-Aignan',
              'Philippe Poutou', 'Anne Hidalgo'])

foo.formatdata('Deuxième tour', 'Hypothèse Macron / Le Pen')

foo.getimage(['Emmanuel Macron', 'Marine Le Pen'])
