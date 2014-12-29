# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2014

@author: GRUPO 3
"""

# TRABALHO DE GRUPO
# GRUPO 3


import os
from Bio import Entrez
from Bio import SeqIO

# aceder ao NCBI e guarda o ficheiro correspondente a zona do genoma
def zona_genoma(filename):
    Entrez.email = "pg27658@alunos.uminho.pt"
    if not os.path.isfile(filename):
        # Inicio da zona de interesse 468401 e fim 727400.
        net_handle = Entrez.efetch(db="nucleotide",id="59800473", rettype="gb", retmode="text", seq_start="468401", seq_stop="727400")
        out_handle = open(filename, "w")
        out_handle.write(net_handle.read())
        out_handle.close()
        net_handle.close()
    
    record = SeqIO.read(filename, "genbank")
    
    return record


def anotacoes(filename):
    print ""
    print "Verificacao das anotacoes correspondentes a zona do genoma: "
    print ""
    records = SeqIO.parse(filename, "genbank")
    for seq_record in records:
        print "ID: %s" % seq_record.id
        print "Name: %s" % seq_record.name
        print "Description: %s" % seq_record.description
        print "Sequence length: %i" % len(seq_record)
        print "Number of features: %i" % len(seq_record.features)    
        print "Organism %s" % seq_record.annotations["organism"]
        print "Accessions zone: %s" % seq_record.annotations["accessions"]
        print ""

def anotacoes_features(record,filename):
    features = record.features
    f = open(filename,'w')
    f.write("Anotações\n\n\n")
    for aux in features:
            if aux.type=='CDS':
                print "Tipo: %s " % aux.type
                f.write("Tipo: %s\n" % aux.type)
                print "Localização: %s" % aux.location
                f.write("Localização: %s\n" % aux.location)
                print "Proteina codificada: %s" % aux.qualifiers['protein_id']
                f.write("Proteina codificada: %s\n" % aux.qualifiers['protein_id'])
                print "db_xref: %s" % aux.qualifiers['db_xref']
                f.write("db_xref: %s\n" % aux.qualifiers['db_xref'])
                print "Locus_tag: %s" % aux.qualifiers['locus_tag']
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                print "Produto: %s" % aux.qualifiers['product']
                f.write("Produto: %s\n" % aux.qualifiers['product'])
                f.write("\n")
                #print aux
                print ""
            elif aux.type=='gene':
                print "Tipo: %s " % aux.type
                f.write("Tipo: %s\n" % aux.type)
                print "Localização: %s" % aux.location
                f.write("Localização: %s\n" % aux.location)
                print "db_xref: %s" % aux.qualifiers['db_xref']
                f.write("db_xref: %s\n" % aux.qualifiers['db_xref'])
                print "Locus_tag: %s" % aux.qualifiers['locus_tag']
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                f.write("\n")
                #print aux
                print ""
    
            
if __name__ == "__main__":
    filename = "gi_59800473.gbk"
    # aceder ao NCBI e guarda o ficheiro correspondente a zona do genoma
    record = zona_genoma(filename)
    # verificar as anotacoes correspondentes a zona definida
    anotacoes(filename)
    anotacoes_features(record,"Anotacoes.txt")
    
    