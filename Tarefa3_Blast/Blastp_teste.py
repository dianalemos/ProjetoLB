# -*- coding: utf-8 -*-
"""
Created on Sat Jan 03 01:16:38 2015

@author: Joana
"""

from Bio import SeqIO
from Bio.Blast import NCBIWWW

def get_locustag(record):
    gis = []
    lcs = {}
    
    #Codigo do grupo 5
    # selects our relevant locus tags, between NGO0487 and NGO0727, and adds them to 'gis'
    for feature in record.features:
        if feature.type == 'CDS':
            locus_tag = feature.qualifiers['locus_tag'][0]
            if locus_tag >= 'NGO0487' and locus_tag <= 'NGO0727':
                gis.append(feature.qualifiers['db_xref'][0][3:])
                lcs[gis[-1]] = locus_tag
    
    # fetches all the records according to the selected 'gis'
    #request = Entrez.efetch(db="nucleotide", rettype='gb', retmode='text', id=gis)
    #records1 = SeqIO.parse(request, 'gb')
    #
    ## saves each individual SeqRecord to a 'gb' file, with its locus_tag as filename
    #for rec in records1:
    #    with open(lcs[rec.annotations['gi']] + '.gb', 'w') as f:
    #        SeqIO.write(rec, f, 'gb')
    
    print lcs
    return (lcs,gis)

def blast(lcs, gis):
    for gix in gis:
        print gix
        result_handle = NCBIWWW.qblast("blastp", "swissprot", gix)
        save_file = open(lcs[gix], "w")
        save_file.write(result_handle.read())
        save_file.close()
        result_handle.close()
    
if __name__ == "__main__":
    #Ficheiro correspondente a zona do genoma em estudo - 468401 a 727400
    filename = "zone.gb"
    record = SeqIO.read(filename, "genbank") 
    lcs, gis = get_locustag(record)
    blast(lcs, gis)