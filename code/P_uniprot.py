# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 18:36:57 2015

@author: Diana
"""
import urllib
from Bio.SeqIO import UniprotIO
import urllib2

######UNIPROT######

#Vai buscar os ids das proteinas ao Uniprot - parte do codigo baseado no codigo do grupo 5
def uniprot_ID(proteins):
    listaIDs = []
    for i in range(len(proteins)):
        handler = urllib.urlopen("http://www.uniprot.org/uniprot/?query="+proteins[i]+"&sort=score")        
        data = str(handler.read())
        try:
            start = data.index('<tbody>')
        except ValueError:
            start = len(data)
        
        if start != len(data):
            ids = data[start+15:start+21]
            listaIDs.append(ids)
    return listaIDs

#Pesquisa determinada proteina no uniprot e devolde informaçao
def uniprot_xml(ids):
    for i in range(len(ids)):
        url = 'http://www.uniprot.org/uniprot/' + ids[i] + '.xml' 
        data = urllib2.urlopen(url).read()
        records = UniprotIO.UniprotIterator(data)
        for i in records:
            print i.annotations
            print ""

#Devolve lista das proteinas reviewed e lista das unreviewed
#No menu este codigo apenas recebe uma proteina e diz se é reviewed ou unreviewed
def uniprot_Info(ids):
    l_unrev, l_rev = [], []
    tag = 'reviewed'
    s, e = '>', '<'
    for i in range(len(ids)):
        url = 'http://www.uniprot.org/uniprot/' + ids[i] + '.rdf' 
        data = urllib2.urlopen(url).read()
        try: 
            start = data.index(tag)
            start = start + data[start:].index(s) + 1
            end = start + data[start:].index(e)
            value = data[start:end].lower()
            value = data[start:end]
            if value == 'false':
                print "%s - unreviewed protein\n" % ids[i]
                l_unrev.append(ids[i])
            else:
                print "%s - reviewed protein\n" % ids[i]
                l_rev.append(ids[i])
        except ValueError:
            l_unrev.append('NA')
            l_rev.append('NA')
    
    return l_unrev,l_rev
                              