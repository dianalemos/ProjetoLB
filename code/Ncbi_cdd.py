# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 18:32:06 2015

@author: Diana
"""

from Bio import Entrez
from Bio import SeqIO

#pesquisa determinado termo no ncbi cdd
def ncbi_cdd(filename,termo):
    Entrez.email = "pg27658@alunos.uminho.pt"
    net_handle = Entrez.esearch(db = "cdd", term = termo)
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    print net_handle.read()
    #record = SeqIO.read(filename, "xml")
    #print record
    net_handle.close()
    #return record
    
def cdd():
    Entrez.email = "pg27658@alunos.uminho.pt"
    net_handle = Entrez.efetch(db="cdd", id="59800982")
#    out_handle = open(filename, "w")
#    out_handle.write(net_handle.read())
#    out_handle.close()
#    record = SeqIO.read(filename, "gb")
#    net_handle.close()
#    return record
    print net_handle.read()

cdd()
