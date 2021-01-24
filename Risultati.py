from Conti import *
from Extract_Values import *
import pandas as pd
import csv
import xlsxwriter

def Risultati(Giorni, permutazioni, Combinazioni_portata,na, nb, A, Ap, Hnet, Hnetp, Fattore, Fattorep, Potenza_giorn, Potenza_scelta, Energia_annua, NPV):
    dw = None
    df = open("Output/Risultati.csv", mode='w')
    dw = csv.writer(df, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #Write headers
    dw.writerow(['Giorno', 'Tipo A', 'Tipo B', 'Portata config.', 'Q disponibile', 'Portata passante', 'Portata_parziale',
                 'Hnet', 'Hnet parz.', 'Fattore n.', 'Fattore n.p', 'Potenza della config.'])

    g = [[k for c in range(0, 1) for i in range(0, (Nb+1)*(Na+1))] for k in range(1, giorni+1)]
    comb = [Combinazioni_portata for i in range(0, giorni)]
    #Write rows
    for i in Giorni:
        for p in permutazioni:
            dw.writerow([g[i][p], na[i][p], nb[i][p], comb[i][p], Vettore_Qavailable[i], A[i][p], Ap[i][p], Hnet[i][p], Hnetp[i][p],
                         Fattore[i][p], Fattorep[i][p], Potenza_giorn[i][p]*1e-6])

    df.close()

    #Faccio csv per secondo foglio di excel con la potenza massimizzata in quel giorno
    dww = None
    dfw = open("Output/Potenza massimizzata.csv", mode='w')
    dww = csv.writer(dfw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dww.writerow(['Giorno', 'Potenza max [MWh]'])
    for i in Giorni:
        dww.writerow([i+1, Potenza_scelta[i]*1e-6])
    dfw.close()

    #Scrivo l'excel
    excel_name = "Output/Risultati.xlsx"
    read_file = pd.read_csv("Output/Risultati.csv")
    df = pd.DataFrame(read_file)
    writer = pd.ExcelWriter(excel_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Foglio1', startrow=1, index=None, header=False)
    workbook = writer.book
    worksheet1 = writer.sheets['Foglio1']

    read_file2 = pd.read_csv("Output/Potenza massimizzata.csv")
    dfw = pd.DataFrame(read_file2)
    dfw.to_excel(writer, sheet_name='Foglio2', startrow=1, index=None, header=False)
    worksheet2 = writer.sheets['Foglio2']

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': False,
        'valign': 'vcenter',
        'fg_color': '#7FFFD4',
        'center_across': True,
        'shrink': False,
        'border_color': '#F9966B', 
        'border': 2})

    worksheet1.set_row(0, 17)
    worksheet1.set_column('A:D', 8)
    worksheet1.set_column('D:K', 17)
    worksheet1.set_column('L:L', 19)
    for col_num, value in enumerate(df.columns.values):
        worksheet1.write(0, col_num, value, header_format)

    worksheet2.set_row(0, 17)
    worksheet2.set_column('A:A', 8)
    worksheet2.set_column('B:B', 19)
    for col_num, value in enumerate(dfw.columns.values):
        worksheet2.write(0, col_num, value, header_format)
    writer.save()

    return
