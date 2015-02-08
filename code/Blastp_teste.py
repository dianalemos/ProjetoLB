# -*- coding: utf-8 -*-
"""
Created on Sat Jan 03 01:16:38 2015

@author: Joana
"""

from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


def get_locustag(record,locus): 
    gi = []
    #Codigo baseado no codigo do grupo 5
    for feature in record.features:
        if feature.type == 'CDS':
            if 'locus_tag' in feature.qualifiers:
                aux = feature.qualifiers['locus_tag'][0]
                if locus == aux:
                    gi.append(feature.qualifiers['db_xref'][0][3:])
    return gi

def blast(gene):
    result_handle = NCBIWWW.qblast("blastp", "swissprot", gene)
    save_file = open(gene, "w")
    save_file.write(result_handle.read())
    save_file.close()
    result_handle.close()

def analise(filename):
    for record in NCBIXML.parse(open(filename)):
        print "QUERY: %s" % record.query
        for align in record.alignments :
            print " MATCH: %s" % align.title
            for hsp in align.hsps :
                print " Evalue = %f, from position %i to %i" % (hsp.expect, hsp.query_start, hsp.query_end)
                #if hsp.align_length < 60 :
                print "  Query: %s" % hsp.query
                print "  Match: %s" % hsp.match
                print "  Sbjct: %s" % hsp.sbjct
                
                print ""