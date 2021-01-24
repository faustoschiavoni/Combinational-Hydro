from Conti import *
from Risultati import Risultati


Optimization_Goal = 'NPV'


# Invoco la funzione che calcola la più grande Potenza_annua [MWh] --> se il numero di turbine A e B è fissato implice un maggiore NPV 
Giorni, permutazioni, Combinazioni_portata, na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV = Conti(Optimization_Goal)

# Risultati
Risultati(Giorni, permutazioni, Combinazioni_portata, na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV)
