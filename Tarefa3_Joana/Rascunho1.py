# -*- coding: utf-8 -*-
"""
Created on Sat Jan 03 01:16:38 2015

@author: Joana
"""

from Bio import Entrez

ids = (59801002, 59801019)
stream = Entrez.efetch(db='protein', rettype='fasta', id='YP_207668.1')
data = stream.read()

out = file('output.fasta', 'wt')
out.write(data)
out.close()