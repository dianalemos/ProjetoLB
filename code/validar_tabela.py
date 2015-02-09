# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 17:21:30 2015

@author: Diana
"""

#################################Codigo grupo 5#############################################
###VALIDA INFORMAÇAO TABELA### 
# verify if information in the feature is the same as the one present in the line
def verify(line, feature, ltstart, ltend):
    check = False
    #print "LINE %s" % line
    start, end, strand = feature.location.start + 1, feature.location.end, feature.location.strand
    #print "START %s" % start
    #As zonas de start e end nao correspondem as da tabela
    if start == int(line[2]) and end == int(line[3]) and strand == int(line[4] + '1'):
        check = True
    return check

def valida(record):
    ltstart, ltend = "NGO0487", "NGO0727"
    # open log file to record validation
    with open('validacao.log', 'w') as f:
    
        # open comparison table
        with open('ProteinTable864_169534.tsv') as table:
            for line in table:
                if line[0] != '#':
                    line = line[:-1].split('\t')
                    
                    # if current locus_tag is between target locus_tag's
                    if line[7] >= ltstart and line[7] <= ltend:
                        ngos = []
        
                    
                        # fetch features with identical locus_tag
                        for feature in record.features:
                            if feature.type == 'gene' or feature.type == 'CDS':
                                if feature.qualifiers['locus_tag'][0] == line[7]:
                                    ngos.append(feature)
                                
                        
                        # compare if information in each feature is the same as the one present in the comparison table and write to file
                        for ngo in ngos:
                            if verify(line, ngo, ltstart, ltend):
                                f.write('Check! ' + line[7] + ' ' + str(ngo.qualifiers['locus_tag'][0]) + ' ' + str(ngo.type) + ' ' + str(ngo.location) +'\n')
                            else:
                                f.write('Not check...\n' + str(ngo) + str(line) + '\n')
                                                
##############################################################################