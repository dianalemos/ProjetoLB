# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 18:58:26 2014

@author: SONY
"""

# TRABALHO DE GRUPO
# GRUPO 3


import os
from Bio import Entrez
from Bio import SeqIO

# aceder ao NCBI e guardar o ficheiro
Entrez.email = "pg27658@alunos.uminho.pt"     # dizer ao NCBI quem somos
filename = "gi_59800473.gbk"
if not os.path.isfile(filename):
    # Downloading...
    net_handle = Entrez.efetch(db="nucleotide",id="59800473", rettype="gb", retmode="text")
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    net_handle.close()
    print("Saved")

print("Parsing...")
record = SeqIO.read(filename, "genbank")
print(record)
print ""
print ""


# verificar as anotações correspondentes à zona definida
print "Verificacao das anotações correspondentes à zona definida: "
print ""

Entrez.email = "pg27658@alunos.uminho.pt"
handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id = "59800473")
for seq_record in SeqIO.parse(handle, "gb"):
    print seq_record.id, seq_record.description[:50] + "..."
    print "Sequence length %i," % len(seq_record),
    print "%i features," % len(seq_record.features),    
    print "from: %s" % seq_record.annotations["source"]
    print ""
handle.close()