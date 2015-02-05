# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 23:42:03 2015

@author: Diana
"""

from Bio.Blast import NCBIXML

def analise(filename):
    for record in NCBIXML.parse(open(filename)):
        print "QUERY: %s" % record.query
        for align in record.alignments :
            print " MATCH: %s" % align.title
            for hsp in align.hsps :
                print " HSP, e=%f, from position %i to %i" % (hsp.expect, hsp.query_start, hsp.query_end)
                #if hsp.align_length < 60 :
                print "  Query: %s" % hsp.query
                print "  Match: %s" % hsp.match
                print "  Sbjct: %s" % hsp.sbjct
                
                print ""

