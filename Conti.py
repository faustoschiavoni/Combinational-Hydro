from Extract_Values import *

def Conti(Optimization_Goal):
    if Optimization_Goal == 'NPV':
        Combinazioni_portata = [Qa*i + Qb*tt for i in range(0, Na+1) for tt in range(0, Nb+1)] #si parte da 0 turbine per tipo fino ad arrivare alle volute
        Giorni = range(0, giorni)
        permutazioni = range(0, len(Combinazioni_portata))
        comb_a = [Qa * c for c in range(0, Na + 1) for k in range(0, Nb + 1)]
        comb_b = [Qb * k for c in range(0, Na + 1) for k in range(0, Nb + 1)]

        A = []
        Ap = []
        Hnet = []
        Hnetp = []
        Fattore = []
        Fattorep = []
        Potenza_giorn = []
        for i in Giorni:
            A += [[]]
            Ap += [[]]
            Hnet += [[]]
            Hnetp += [[]]
            Fattore += [[]]
            Fattorep += [[]]
            Potenza_giorn += [[]]

        for i in Giorni:
            list = []
            listina = []
            for ii in permutazioni:
                if Combinazioni_portata[ii] <= Vettore_Qavailable[i]: #and comb_a[ii] >= Pa and comb_b[ii] >= Pb non c'è bisogno di questo controllo tanto le portate sono multiple di quelle nominali: quindi o sono 0 o sono superiori alla portata minima
                    Q = float(Combinazioni_portata[ii])
                    list += [Q]
                    Delta = Vettore_Qavailable[i] - Combinazioni_portata[ii]
                    controllino = [len(Combinazioni_portata) - j for j in range(0, Nb+1)]
                    if Pa < Delta > Pb and Qa > Delta < Qb and ii not in controllino: #così sono certo che la portata parzializzata sia maggiore della minima di tutte e due le turbine e comunque minore della nominale--> sicura parzializzazione su una sola turbina. in più così sono certo che non sia l'ultima combinazione (in cui non potrei comunque aggiungere altre turbine)
                        listina += [Delta]
                    else:
                        listina += [0]
                else:
                    list += [0]
                    listina += [0]
            A[i] = list
            Ap[i] = listina

        for k in Giorni:
            lista = []
            listina = []
            for j in permutazioni:
                lista += [Vettore_Hg[k] - Coeff*(A[k][j]**2)]
                listina += [Vettore_Hg[k] - Coeff*(Ap[k][j]**2)]
            Hnet[k] = lista
            Hnetp[k] = listina

        na = [[c for c in range(0, Na + 1) for i in range(0, Nb + 1)] for k in range(0, giorni)]
        nb = [[i for c in range(0, Na + 1) for i in range(0, Nb + 1)] for k in range(0, giorni)]

        for f in Giorni:
            bo = []
            for p in permutazioni:
                if A[f][p] != 0:
                    bo += [(10 ** 3) * 9.81 * (Eta_a*comb_a[p] + Eta_b*comb_b[p])]
                else:
                    bo += [0]
            Fattore[f] = bo

        for f in Giorni:
            bop = []
            for p in permutazioni:
                if Ap[f][p] == 0:
                    Eta_p = 0
                else:
                    Lista = [Lista_Qp[i] * Qa for i in range(0, len(Lista_Qp))]
                    Q_vicino = min(Lista, key=lambda x: abs(x - Ap[f][p]))
                    for m in range(0, len(df3)):
                        if Lista[m] == Q_vicino:
                            Eta_p = Lista_Etap[m]/100
                bop += [(10 ** 3) * 9.81 * Eta_p]
            Fattorep[f] = bop

        for i in Giorni:
            listatt = []
            for p in permutazioni:
                listatt += [Fattore[i][p]*Hnet[i][p] + Fattorep[i][p]*Ap[i][p]*Hnetp[i][p]]
            Potenza_giorn[i] = listatt

        Potenza_scelta = []
        Potenza_scelta += [max(Potenza_giorn[i][p] for p in permutazioni) for i in Giorni]

        Energia_annua = sum(Potenza_scelta)*24*Eta_aux*1e-6 #[MWh]

        #Energia_annua = 5931.67293033924 #valore energia preciso presp da excel

        INV_COST = Inv_Cost + Na*Ca + Nb*Cb
        Revenues = Energia_annua*Revenues_specific #all'anno
        Costs_perTasse = INV_COST*(Perc_OM + (1/Ammortization)) #cambia per l'ammortamento
        Costs_perCF = INV_COST*Perc_OM
        Taxes_1_20 = (Revenues - Costs_perTasse)*Taxes
        Taxes_21_30 = (Revenues - Costs_perCF)*Taxes
        CF_1_20 = Revenues - Costs_perCF - Taxes_1_20
        CF_21_30 = Revenues - Costs_perCF - Taxes_21_30

        Attual_amm = sum(1/((1+Discount_Rate)**i) for i in range(1, Ammortization+1))
        Attual_senza = sum(1/((1+Discount_Rate)**i) for i in range(Ammortization+1, Lifetime+1))

        NPV = -INV_COST + Attual_amm*CF_1_20 + Attual_senza*CF_21_30

        print('\n', 'Yearly Energy Maximized: ', round(Energia_annua, 2), 'MWh', '\n', 'NPV Maximized:',
              round(NPV, 2), '€')

    return Giorni, permutazioni, Combinazioni_portata, na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV
