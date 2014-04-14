import pylab

def proteinCleavage(protein):
    
    """
    >>> proteinCleavage('ABCDKEFGHRIKPJLMNROPQ')
    {'ABCDK', 'EFGHR', 'IKPJLMNR'}
    >>> proteinCleavage('MVPPPPSRGGAAKPGQLGRSLGPLLLLLRPEEPEDGDREICSESK')
    {'EICSESK', 'MVPPPPSR', 'SLGPLLLLLRPEEPEDGDR', 'GGAAKPGQLGR'}
    >>> protein = 'MLRLPAVLRQIRPVSRALTPHLTRAYAKDVKFGADARTLMLQGVDLLADAVAVTMGPKGRTVIIEQSWGSPKVTKDGVTVAKSIDLKDKYKNIGAKLVQDVANNTNEEAGDGTTTATVLARSIAKEGFEKISKGANPVEIRRESGVMLAVDAVIAELKRQSKPVTTPEEIAQVATISANGDKEIGNIISDAMKKVGRKGVITVKDGKTLNDELEIIEGMKFDRGYISPYFINTSKGQKCEFQDAYVLLSEKKISSVQSIVPALEIANAHRKPLVIIAEDVDGEALSTLVLNRLKVGLQVVAVKAPGFGDNRKNQLKDMAIATGGAVFGEEGLTLNLEDVQPHDLGKVGEVIVTKDDAMLLKGKGDKAQIEKRIQEIIEQLDITTSEYEKEKLNERLAKLSDGVAVLKVGGTSDVEVNEKKDRVTDALNATRAAVEEGIVLGGGCALLRCIPALDSLTPANEDQKIGIEIIKRTLKIPAMTIAKNAGVEGSLIVEKIMQSSSEVGYDAMLGDFVNMVEKGIIDPTKVVRTALLDAAGVVSLLTTAEVVVTEIPKEEKDPGMGGMGGMGGGMGGGMF'
    >>> proteinCleavage(protein)
    {'VGGTSDVEVNEK', 'IQEIIEQLDITTSEYEK', 'IMQSSSEVGYDAMLGDFVNMVEK', 'DMAIATGGAVFGEEGLTLNLEDVQPHDLGK', 'EIGNIISDAMK', 'IGIEIIK', 'LSDGVAVLK', 'ISSVQSIVPALEIANAHR', 'AQIEK', 'SIDLK', 'CEFQDAYVLLSEK', 'QIRPVSR', 'FGADAR', 'TLMLQGVDLLADAVAVTMGPK', 'GANPVEIR', 'NIGAK', 'IPAMTIAK', 'TLNDELEIIEGMK', 'VGEVIVTK', 'KPLVIIAEDVDGEALSTLVLNR', 'LPAVLR', 'GIIDPTK', 'LVQDVANNTNEEAGDGTTTATVLAR', 'DDAMLLK', 'APGFGDNR', 'EGFEK', 'CIPALDSLTPANEDQK', 'NAGVEGSLIVEK', 'TVIIEQSWGSPK', 'TALLDAAGVVSLLTTAEVVVTEIPK', 'AAVEEGIVLGGGCALLR', 'DGVTVAK', 'ESGVMLAVDAVIAELK', 'VGLQVVAVK', 'GYISPYFINTSK', 'VTDALNATR', 'GVITVK', 'ALTPHLTR', 'QSKPVTTPEEIAQVATISANGDK'}
    """
    
    result, start = set(), 0
    for stop in range(len(protein)):
        if protein[stop] in 'KR' and (stop == (len(protein) - 1) or protein[stop + 1] != 'P'):
            if 5 <= (stop - start + 1) <= 50:
                result.add(protein[start:stop + 1])
            start = stop + 1
    return result

def genomeCleavage(accession):
    
    """
    >>> peptides = genomeCleavage('L42023')
    >>> len(peptides)
    32424
    """
    
    from genome_data import getGenBank    # download genomes from GenBank

    # download the genome
    genome = getGenBank(accession, fmt='gb', storageLocation='')
    
    # extract peptides from all protein sequences
    peptides = set()
    for feature in genome.features:
        if feature.type == 'CDS' and 'translation' in feature.qualifiers:
            protein = feature.qualifiers['translation'][0]
            peptides.update(proteinCleavage(protein))
    return peptides

def draftGenomeCleavage(filename):
    
    """
    >>> peptides = draftGenomeCleavage('LMG26808.gb')
    >>> len(peptides)
    56127
    >>> peptides = draftGenomeCleavage('LMG26811.gb')
    >>> len(peptides)
    56189
    """
    
    from Bio import SeqIO

    # extract peptides from all protein sequences
    peptides = set()
    for record in SeqIO.parse(filename, 'genbank'):    
        for feature in record.features:
            if feature.type == 'CDS' and 'translation' in feature.qualifiers:
                protein = feature.qualifiers['translation'][0]
                peptides.update(proteinCleavage(protein))
    return peptides

#Genomes must be provided in genbank format (CDS - Proteins)
genomes = [
    ('CP000422', 'Pediococcus pentosaceus ATCC 25745'),
    ('CP003137', 'Pediococcus clausennii ATCC BAA-344'), ('wz37', 'Pediococcus damnosus')
    
]

# download genomes
peptides = []
for acc, organism in genomes:
    if acc.startswith('wz'):
        peptides.append(draftGenomeCleavage(acc + ".gbk"))
    else:
        peptides.append(genomeCleavage(acc))
        
# compute pan and core genomes
panpeptides, corepeptides = set(), set()
pan, core = [], []
for peptideset in peptides:
    
    # extend pan and core genomes
    if not panpeptides:
        panpeptides = peptideset
        corepeptides = peptideset
    else:
        panpeptides = panpeptides.union(peptideset)
        corepeptides = corepeptides.intersection(peptideset)
        
    # add sizes of pan and core genomes
    pan.append(len(panpeptides))
    core.append(len(corepeptides))
    
print(pan)
print(core)

pylab.plot(
    range(len(pan)), pan, 'bo-', linewidth=2, 
    markersize=8, markeredgecolor='blue', markeredgewidth=3, markerfacecolor='white'
)
pylab.plot(
    range(len(core)), core, 'ro-', linewidth=2,
    markersize=8, markeredgecolor='red', markeredgewidth=3, markerfacecolor='white'
)
pylab.xticks(range(len(core)), [g[0] for g in genomes], rotation=45, fontsize=8)
pylab.legend(('pan', 'core'), loc=2)
pylab.show()
'''    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
'''
