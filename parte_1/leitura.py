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


def anotacoes_geral(filename):
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

def anotacoes_type(record,filename):
    features = record.features
    genes_id = []
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
                print "Gene ID: %s" % aux.qualifiers['db_xref']
                genes_id.append(aux.qualifiers['db_xref'])
                f.write("Gene ID: %s\n" % aux.qualifiers['db_xref'])
                print "Locus_tag: %s" % aux.qualifiers['locus_tag']
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                if "product" in aux.qualifiers:
                    print "Produto: %s" % aux.qualifiers['product']
                    f.write("Produto: %s\n" % aux.qualifiers['product'])
                else: 
                    print "Nao tem produto"
                f.write("\n")
                #print aux
                print ""
            elif aux.type=='gene':
                print "Tipo: %s " % aux.type
                f.write("Tipo: %s\n" % aux.type)
                print "Localização: %s" % aux.location
                f.write("Localização: %s\n" % aux.location)
                print "Gene ID: %s" % aux.qualifiers['db_xref']
                f.write("Gene ID: %s\n" % aux.qualifiers['db_xref'])
                print "Locus_tag: %s" % aux.qualifiers['locus_tag']
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                f.write("\n")
                #print aux
                print ""
    
    f.close()
    
            
if __name__ == "__main__":
    filename = "gi_59800473.gbk"
    # aceder ao NCBI e guarda o ficheiro correspondente a zona do genoma
    record = zona_genoma(filename)
    # verificar as anotacoes correspondentes a zona definida
    anotacoes_geral(filename)
    # verificar as features correspondentes a zona definida
    anotacoes_type(record,"Anotacoes.txt")
    
    
    