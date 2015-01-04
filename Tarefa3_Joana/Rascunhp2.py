# -*- coding: utf-8 -*-
"""
Created on Fri Jan 02 12:06:54 2015

@author: Joana
"""
import os
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW

stream = Entrez.efetch(db = 'nucleotide', id='59800473', rettype='fasta', seq_start='468401', seq_stop='727400')

data = stream.read()
out = file ('seqs.gbk', 'wt')
out.write(data)
out.close()

prot = out.translate('seqs.gbk')
print prot



####################################

