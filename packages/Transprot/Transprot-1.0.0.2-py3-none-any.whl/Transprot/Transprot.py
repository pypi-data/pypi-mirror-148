def Translate(DNA):
    codon=['AAA', 'AAT', 'AAG', 'AAC', 'ATA', 'ATT', 'ATG', 'ATC', 'AGA', 'AGT', 'AGG', 'AGC', 'ACA', 'ACT', 'ACG', 'ACC', 'TAA', 'TAT', 'TAG', 'TAC', 'TTA', 'TTT', 'TTG', 'TTC', 'TGA', 'TGT', 'TGG', 'TGC', 'TCA', 'TCT', 'TCG', 'TCC', 'GAA', 'GAT', 'GAG', 'GAC', 'GTA', 'GTT', 'GTG', 'GTC', 'GGA', 'GGT', 'GGG', 'GGC', 'GCA', 'GCT', 'GCG', 'GCC', 'CAA', 'CAT', 'CAG', 'CAC', 'CTA', 'CTT', 'CTG', 'CTC', 'CGA', 'CGT', 'CGG', 'CGC', 'CCA', 'CCT', 'CCG', 'CCC']
    protein=['K', 'N', 'K', 'N', 'I', 'I', 'M', 'I', 'R', 'S', 'R', 'S', 'T', 'T', 'T', 'T', '.', 'Y', '.', 'Y', 'L', 'F', 'L', 'F', '.', 'C', 'W', 'C', 'S', 'S', 'S', 'S', 'E', 'D', 'E', 'D', 'V', 'V', 'V', 'V', 'G', 'G', 'G', 'G', 'A', 'A', 'A', 'A', 'Q', 'H', 'Q', 'H', 'L', 'L', 'L', 'L', 'R', 'R', 'R', 'R', 'P', 'P', 'P', 'P']
    trans=dict(zip(codon,protein))
    result_trans=[]
    for i in range(0,len(DNA),3):
        result_trans.append(trans[DNA[i:i+3]])
    rawprot=''.join(result_trans)
    output=''.join(rawprot[rawprot.index('M'):rawprot.index('.')])
    return output




