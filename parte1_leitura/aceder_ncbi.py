# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 18:23:25 2015

@author: Diana
"""

from Bio import Entrez
from Bio import SeqIO

#Genoma completo
def genoma(filename):
    Entrez.email = "pg27658@alunos.uminho.pt"
    net_handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id="59800473")
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    record = SeqIO.read(filename, "gb")
    print record
    net_handle.close()
    return record

#Zona do genoma correspondente
def zona_genoma(filename):
    Entrez.email = "pg27658@alunos.uminho.pt"
    # Inicio da zona de interesse 468401 e fim 727400
    net_handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id="59800473", seq_start = "468401", seq_stop = "727400")
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    record = SeqIO.read(filename, "gb")
    print record
    net_handle.close()
    return record
    
if __name__ == "__main__":
    filename = "genoma_completo.gb"
    filename2 = "zona_genoma.gb"
    # acede ao NCBI e guarda o ficheiro correspondente ao genoma
    record = genoma(filename)    
    # acede ao NCBI e guarda o ficheiro correspondente a zona do genoma
    record2 = zona_genoma(filename2)