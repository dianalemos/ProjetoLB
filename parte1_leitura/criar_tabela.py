# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 14:29:42 2015

@author: Diana
"""

import xlwt
import leitura

wb = xlwt.Workbook()
ws = wb.add_sheet('My Genes',cell_overwrite_ok=True)

#Titulos das colunas
titles = ['Locus_tag','ID']

# Escrevendo titulos na primeira linha do arquivo
for i in range(len(titles)):
    ws.write(0, i, titles[i])
    
# Definindo largura das celulas das sequencia
#for i in range(1,len(titles)):
#    ws.col(i).width = 1024

record_zona = leitura.aceder_ncbi.zona_genoma("gi_59800473_zona.gbk")
locus = leitura.anotacao_locus_tag(record_zona)
geneID = leitura.anotacao_geneID(record_zona)

i=1

for x in range(len(locus)):

    # Escrevendo o identificar na 1ª coluna da linha i
    ws.write(i, 0, locus[x])   
    ws.write(i,1,geneID[x])
    i +=1
        
wb.save('My Genes.xls')
