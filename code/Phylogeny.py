# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 14:48:54 2015

@author: Diana
"""
from Bio import Phylo
from Bio import AlignIO

def alignments(filename):
        alignments = list(AlignIO.parse(filename, "phylip"))
        for alignment in alignments:
            AlignIO.write(alignment, "Multiple_alignments.fasta", "fasta")
            print alignment 

def phylogeny(filename):
        tree = Phylo.read(filename, "newick")
        print tree
        print Phylo.draw_ascii(tree)
        tree.rooted = True
        Phylo.draw(tree) 
        
alignments("alinhamentos.phy")
phylogeny("filogenia.dnd")