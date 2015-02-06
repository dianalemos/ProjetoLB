# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 14:29:42 2015

@author: Diana
"""

import xlwt
import xlrd

def keep_info(filename):
    l_unrev = []
    l_rev = []
    data = xlrd.open_workbook(filename)
    worksheet = data.sheet_by_name('My Genes')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        print 'Row:', curr_row
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
         # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)
         #Guarda lista das proteinas UNREVIEWED
            if cell_value == 'Unreviewed': 
                l_unrev.append(worksheet.cell_value(curr_row, curr_cell-2))
            elif cell_value == 'Reviewed': 
                l_rev.append(worksheet.cell_value(curr_row, curr_cell-2))
            print '	', cell_type, ':', cell_value
#    print l_rev
#    print l_unrev

def tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('My Genes',cell_overwrite_ok=True)
    
    #Titulos das colunas
    titles = ['LOCUS_TAG','GENE_ID','LOCATION','PROTEIN','PRODUCT']
    
    # Escrevendo titulos na primeira linha do arquivo
    for i in range(len(titles)):
        ws.write(0, i, titles[i])
        
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
    
if __name__ == "__main__":
    keep_info("My_Genes.xls")