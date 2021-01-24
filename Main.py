from Conti import *
from Risultati import Risultati


Optimization_Goal = 'NPV'


# Invoco la funzione che massimizza il NPV
Giorni, permutazioni, Combinazioni_portata, na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV = Conti(Optimization_Goal)

# Risultati
Risultati(Giorni, permutazioni, Combinazioni_portata, na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV)
