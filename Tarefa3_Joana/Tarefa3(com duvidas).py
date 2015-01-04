# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 11:09:44 2014

@author: Joana
"""

### Tarefa 3 ###

from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW


 # Zona do genoma
Entrez.email = "pg24094@alunos.uminho.pt"
net_handle = Entrez.efetch(db="nucleotide",id="59800473", rettype="gb", retmode="text", seq_start="468401", seq_stop="727400")
out_handle = open("gi_59800473.gbk", "w")
out_handle.write(net_handle.read())
out_handle.close()
net_handle.close()
record = SeqIO.read("gi_59800473.gbk", "genbank")


#Download das sequencias proteicas da zona (duvidas)
features = record.features
lst = []
for aux in features:
    if aux.type=='CDS':
        prot_seq = aux.qualifiers['protein_id']
        lst.append(prot_seq)
        [num for elem in lst for num in elem]        
        stream = Entrez.efetch(db='protein', rettype='fasta', id=str(num))
        data = stream.read()
        out = file('output.fasta', 'wt')
        out.write(data)    
        

record = SeqIO.read(open('output.fasta'),format = 'fasta')
print 'A sequencia tem ' + str(len(record.seq)) + ' aminoacidos'

# Similaridade apartir de Blast
result_handle = NCBIWWW.qblast('blastp', 'swissprot', record.format('fasta'))
save_file = open('interl-blast.xml','w')
save_file.write(result_handle.read())	
save_file.close()	
result_handle.close()



#Informação obtida

from Bio.Blast import NCBIXML
result_handle = open('interl-blast.xml')
blast_records = NCBIXML.parse(result_handle)
print 'Parametros:'
first_record = blast_records.next()
print ' - Database: ' + first_record.database
print ' - Matriz: ' + first_record.matrix
print ' - Gap Penalties: ' +str(first_record.gap_penalties)
print ''



result_handle=open('interl-blast.xml', 'r+')
from Bio.Blast import NCBIXML
blast_records=NCBIXML.parse(result_handle)
first_record=blast_records.next()
print 'Parametros dos alinhamentos'
alinhamentos=first_record.alignments
tamanho_alinhamentos=len(alinhamentos)
for i in range(tamanho_alinhamentos):
    print 'Alinhamento '+str(i+1)
    align=first_record.alignments[i]
    access=align.accession
    print ' - Accession: ' + access
    organismo=align.hit_def
    print ' - Organismo: ' + organismo
    evalue=align.hsps[0]
    valores=str(evalue.expect)
    print ' - E-value: ' + valores
    print ''