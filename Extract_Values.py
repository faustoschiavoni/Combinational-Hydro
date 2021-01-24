import pandas as pd
import configparser

# Leggo e rendo attivo il file di configurazione
config = configparser.ConfigParser()
config.read_file(open("Config.conf"))
#Leggo tutte le variabili in Config.conf

giorni = int(config['Parametri']['giorni'])
DMV = float(config['Parametri']['DMV'])
Coeff = float(config['Parametri']['Coeff'])
Eta_aux = float(config['Parametri']['Eta_aux'])
Revenues_specific = float(config['Parametri']['Revenues_specific'])
Perc_OM = float(config['Parametri']['Perc_OM'])
Inv_Cost = float(config['Parametri']['Inv_Cost'])
Ammortization = int(config['Parametri']['Ammortization'])
Taxes = float(config['Parametri']['Taxes'])
Discount_Rate = float(config['Parametri']['Discount_Rate'])
Lifetime = int(config['Parametri']['Lifetime'])

t = int(config['Numero tipi diversi di turbine']['t'])

Qa = float(config['Portata nominale per tipo di turbina']['Qa'])
Qb = float(config['Portata nominale per tipo di turbina']['Qb'])

Na = int(config['Numero di turbine per tipo di turbina']['Na'])
Nb = int(config['Numero di turbine per tipo di turbina']['Nb'])

Pa = float(config['Portata minima per tipo di turbina']['Pa'])
Pb = float(config['Portata minima per tipo di turbina']['Pb'])

Ma = float(config['Portata massima per tipo di turbina']['Ma'])
Mb = float(config['Portata massima per tipo di turbina']['Mb'])

Eta_a = float(config['Rendimenti nominali per tipo di turbina']['Eta_a'])
Eta_b = float(config['Rendimenti nominali per tipo di turbina']['Eta_b'])

Ca = float(config['Costo turbina']['Ca'])
Cb = float(config['Costo turbina']['Cb'])
#Leggo Excel vari
def Iniz_D():
    xls = pd.ExcelFile('Inputs/Excel.xls')
    df1 = pd.read_excel(xls, 'Duration_Curve')
    serie_portate = []
    for i in range(0, giorni):
        serie_portate += [df1.loc[i][1] - DMV]  # così ho direttamente la Q_available

    return serie_portate

def Iniz_Hg(): 
    xls = pd.ExcelFile('Inputs/Excel.xls')
    df2 = pd.read_excel(xls, 'Hgross')
    serie_Hgross = []
    for i in range(0, giorni):
        serie_Hgross += [df2.loc[i][1]]

    return serie_Hgross

Vettore_Hg = Iniz_Hg() #indicizzati da 0 a 364
Vettore_Qavailable = Iniz_D() #print(Vettore_Qavailable[0], Vettore_Qavailable[364])

def Iniz_Eta_parziali():
    xls = pd.ExcelFile('Inputs/Excel.xls')
    df3 = pd.read_excel(xls, 'Efficiency_1')
    serie_Etap = []
    serie_Qp = []
    for i in range(0, len(df3)):
        serie_Qp += [df3.loc[i][0]]
        serie_Etap += [df3.loc[i][1]]
    return serie_Qp, serie_Etap, df3

Lista_Qp, Lista_Etap, df3 = Iniz_Eta_parziali()


