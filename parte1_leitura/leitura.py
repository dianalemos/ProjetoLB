# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2014

@author: GRUPO 3
"""

# TRABALHO DE GRUPO
# GRUPO 3

from Bio import SeqIO
import criar_tabela

def anotacoes_geral(filename,f):
    print ""
    print "Verificacao das anotacoes correspondentes a zona do genoma: "
    f.write("#######ANOTAÇÕES GERAIS#######\n\n\n")
    print ""
    records = SeqIO.parse(filename, "genbank")
    for seq_record in records:
        print "ID: %s" % seq_record.id
        f.write("ID: %s\n" % seq_record.id)
        print "Name: %s" % seq_record.name
        f.write("Name: %s\n" % seq_record.name)
        print "Description: %s" % seq_record.description
        f.write("Description: %s\n" % seq_record.description)
        print "Sequence length: %i" % len(seq_record)
        f.write("Sequence length: %i\n" % len(seq_record))
        print "Number of features: %i" % len(seq_record.features)  
        f.write("Number of features: %i\n" % len(seq_record.features))  
        print "Organism %s" % seq_record.annotations["organism"]
        f.write("Organism: %s\n" % seq_record.annotations["organism"]) 
        print "Accessions zone: %s" % seq_record.annotations["accessions"]
        f.write("Accessions zone: %s\n" % seq_record.annotations["accessions"]) 
        print ""

###Anotaçoes individuais###
#anotação do locus_tag
def anotacao_locus_tag(record):
    f = record.features
    locus = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "locus_tag" in x.qualifiers:
                locus.append(x.qualifiers["locus_tag"][0])
            else: locus.append("NA")
    return locus

#Anotação devolve GENE ID
def anotacao_geneID(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "db_xref" in x.qualifiers:
                id.append(x.qualifiers["db_xref"])
            else: id.append("NA")
    return id

#Anotação devolve localizaçao
def anotacao_local(record):
    f = record.features
    id = []
    for i in f:
        if i.type == "CDS":
            id.append(i.location)
    return id
    
#Anotação devolve proteina codificada
def anotacao_proteina(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "protein_id" in x.qualifiers:
                id.append(x.qualifiers["protein_id"][0])
            else: id.append("NA")
    return id

#Anotação devolve produto
def anotacao_produto(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "product" in x.qualifiers:
                id.append(x.qualifiers["product"])
            else: id.append("NA")
    return id
    
    
######


#Escreve num ficheiro as informações para cada gene e CDS
#Anotações todas ao mesmo tempo - separar
def anotacoes_type(record,f):
    features = record.features
    genes_id = []
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
                print ""
            elif aux.type=='gene':
                print "Tipo: %s " % aux.type
                f.write("Tipo: %s\n" % aux.type)
                print "Localização: %s" % aux.location
                f.write("Localização: %s\n" % aux.location)
                if "db_xref" in aux.qualifiers:
                    print "Gene ID: %s" % aux.qualifiers['db_xref']
                    f.write("Gene ID: %s\n" % aux.qualifiers['db_xref'])
                else:
                    print "Não tem Gene ID\n"
                    f.write("Não tem Gene ID\n")
                print "Locus_tag: %s" % aux.qualifiers['locus_tag']
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                f.write("\n")
                print ""
                
##############################################################################
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
                                                
##############MENU####################
def menu(record,filename,f,f2):
    while True:
        x = input ("""
    1 - Global Annotations
    2 - Get all the genes
    3 - Locus_tag
    4 - Genes ID
    5 - Protein
    6 - Get table
    7 - Exit
    """)
        if x == "1":
            a = anotacoes_geral(filename,f)
            print a
        elif x == "2":
            anotacoes_type(record,f,f2)
        elif x == "3":
            l_locus = anotacao_locus_tag(record)
            print l_locus
        elif x == "4":
            l_geneID = anotacao_geneID(record)
            print l_geneID
        elif x == "5":
            l_proteinas = anotacao_proteina(record)
            print l_proteinas
        elif x == "6":
                l_local = anotacao_local(record)
                l_produto = anotacao_produto(record)
                #Cria tabela informaçao      
                criar_tabela.tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto)
                print "Tabela criada\n"
        else:
            print("\nNot Valid\n")
                                             
     
if __name__ == "__main__":
    #Ficheiro correspondente a zona do genoma em estudo - 468401 a 727400
    filename = "zone.gb"
    # aceder ao NCBI e guarda o ficheiro correspondente a zona do genoma
    #record_zona = aceder_ncbi.zona_genoma(filename)

    #Abre ficheiro onde vao ser escritas algumas anotaçoes
    f = open("Anotacoes.txt",'w')
       
    # verificar as anotacoes gerais correspondentes a zona definida
    anotacoes_geral(filename,f)
    
    f.write("\n##########Anotações#########\n\n\n")
    # verificar as features correspondentes a zona definida
    record = SeqIO.read(filename, "genbank") 
    anotacoes_type(record,f)
    #menu(record,filename,f,f2)
    #devolve locus_tag de cada gene    
    l_locus = anotacao_locus_tag(record)
    l_geneID = anotacao_geneID(record)
    l_local = anotacao_local(record)
    l_proteinas = anotacao_proteina(record)
    l_produto = anotacao_produto(record)
    #Cria tabela informaçao      
    criar_tabela.tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto)
    f.close() 
    
    #valida com a informaçao da tabela
    #valida(record)
    
    