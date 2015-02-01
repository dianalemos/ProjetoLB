# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 14:29:42 2015

@author: Diana
"""

import xlwt
#import leitura

def tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('My Genes',cell_overwrite_ok=True)
    
    #Titulos das colunas
    titles = ['LOCUS_TAG','GENE_ID','LOCATION','PROTEIN','PRODUCT']
    
    # Escrevendo titulos na primeira linha do arquivo
    for i in range(len(titles)):
        ws.write(0, i, titles[i])
        
    # Definindo largura das celulas das sequencia
#    for i in range(1,len(titles)):
#        ws.col(i).width = len(titles)
    
    
    i=1
    
    for x in range(len(l_locus)):
    
        # Escrevendo o identificar na 1ª coluna da linha i
        ws.write(i, 0, l_locus[x])   
        ws.write(i,1,l_geneID[x])
        ws.write(i,2,str(l_local[x]))
        ws.write(i,3,l_proteinas[x])
        ws.write(i,4,l_produto[x])
        i +=1
            
    wb.save('My_Genes.xls')