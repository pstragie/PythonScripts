"""
Genome statistics

This module contains useful functions for computing basic statistics
about the DNA content of a genome (especially counts and frequencies), 
and for displaying the results.
"""

import numpy
from Bio.Seq import Seq

def nt2int(nt):
    """
    Maps a given nucleotide to its corresponding integer index.
    """
    return {'A':0, 'C':1, 'G':2, 'T':3, 'a':0, 'c':1, 'g':2, 't':3}[nt]

def int2nt(i):
    """
    Maps a given integer index to its corresponding nucleotide.
    """
    return {0:'A', 1:'C', 2:'G', 3:'T'}[i]
  
def nmer2int(nmer):
    """
    Maps a given n-mer to its corresponding integer index. Note that
    this mapping is only unique for n-mers with the same length. For
    example, both 'TT' and 'ATT' are mapped to the index 15.
    """
    return sum([(4 ** i) * nt2int(nmer[len(nmer) - i - 1]) for i in range(len(nmer))])

def int2nmer(i, size):
    """
    Maps a given integer index to its corresponding n-mer. Given the 
    fact that multiple n-mers of different lengths can be mapped to the
    same n-mer (e.g. both 'TT' and 'ATT' are mapped to the integer index
    15), this function requires the size of the n-mer as a mandatory
    parameter.
    """
    nmer = ''
    for j in range(size):
        nmer = int2nt(i % 4) + nmer
        i //= 4
    return nmer
  
def nmerdict2array(d):
    """
    Converts a dictionary of values that uses n-mers as keys into a list
    of values, where the n-mers are mapped to their corresponding index 
    positions.
    
    See also: nmer2int
    """  
    
    # build list from dictionary by mapping nmers to indexes
    l = None
    for key in d:
        if l is None:
            size = len(key)
            l = numpy.zeros(4 ** size)
        try:
            l[nmer2int(key)] = d[key]
        except:
            # nmers containing non-base characters are not taken into
            # account as they cannot be mapped to an index
            pass
    
    return l

def randomSequence(n, alphabet=None, weights=None, uppercase=True):
    """
    Generates a random sequence of length n with symbols taken from the 
    given alphabet. The default alphabet is Bio.Alphabet.generic_dna. 
    The alphabets Bio.Alphabet.generic_rna and 
    Bio.Alphabet.generic_protein create sequences of RNA and proteins 
    respectively.
    
    If weights are assigned to the different symbols in the alphabet 
    (passed as a mapping with symbols as keys and weights as their 
    corresponding values) a weighted random sequence is generated where 
    each symbol is selected at random based on its weight. The weights 
    usually represent probabilities or frequencies.
    
    The uppercase parameter determines whether the randomly generated 
    sequence uses uppercase (True) or not (False).
    
    >>> randomSequence(40)
    Seq('TCAGCGAGCTATATATAATAGTCAACGGCACCGAGCAGCC', DNAAlphabet())
    >>> randomSequence(40, weights = {'A':0.1, 'C':0.4, 'G':0.4, 'T':0.1})
    Seq('CGGACGCACCGCGTGCCCAATCGGGCGCTGGGCGCCGGGG', DNAAlphabet())
    """
    
    # initialize the alphabet to the generic DNA alphabet
    if alphabet is None:
        from Bio.Alphabet import generic_dna
        alphabet = generic_dna
    
    # if no probabilities are given, equal probabilities are considered
    import random
    if weights:
        import numpy.random
        # create list of probabilities and corresponding symbols
        symbols = ''.join(weights.keys())
        frequencies = weights.values()
        if uppercase:
            symbols = symbols.upper()
        else:
            symbols = symbols.lower()
        # generate random sequence based on multinomial model with given probabilities
        seq = ''.join([x * y for x, y in zip(numpy.random.multinomial(n, frequencies), symbols)])
        seq = list(seq)
        random.shuffle(seq)
        seq = ''.join(seq)
    else:
        # generate random sequence based on multinomial model with equal probabilities
        symbols = 'ACGT'
        if not uppercase:
            symbols = symbols.lower()
        seq = ''.join([random.choice(symbols) for symbol in xrange(n)])
    return Seq(seq, alphabet)
      
def randomMarkovSequence(n, transition_weights, alphabet=None, initial_state_weights=None, uppercase=True):
    """
    Generates a random sequence of length n with symbols taken from the 
    given alphabet. The default alphabet is Bio.Alphabet.generic_dna. 
    The alphabets Bio.Alphabet.generic_rna and 
    Bio.Alphabet.generic_protein create sequences of RNA and proteins 
    respectively.
    
    The sequence is generated under a Markov model with given transition 
    weights between states corresponding to the different symbols in the 
    alphabet. These transition weights are given as a two dimensional 
    matrix, with rows and columns corresponding to the order of the 
    symbols in the alphabet. The weights in the transition matrix 
    usually represent probabilities or frequencies.
    
    The uppercase parameter determines whether the randomly generated 
    sequence uses uppercase (True) or not (False).
    
    >>> tm = [[.6, .2, .1, .1], 
              [.1, .1, .8, .0], 
              [.2, .2, .3, .3], 
              [.1, .8, .0, .1]]
    >>> randomMarkovSequence(200, tm, 'ACGT')
    Seq('TCGGCGTCGTTCGAAATAAAAAAAAAAAAAGTTCGCGTCGAAACGGGTCGGGCG...GGG', DNAAlphabet())
    """
    
    # initialize the alphabet to the generic DNA alphabet
    if alphabet is None:
        from Bio.Alphabet import generic_dna
        alphabet = generic_dna
    
    # all initial states have equal probabilities if no probabilities are given
    seq, l = [], len(transition_weights[0])
    if not initial_state_weights:
        initial_state_weights = [1.0 / l] * l
    
    # helper function: generate random state under given multinomial model 
    def random(probabilities):
        import random
        total, p = 0.0, random.uniform(0, 1)
        for i in range(len(probabilities)):
            total += probabilities[i]
            if p <= total:
                return i
    
    # determine case of alphabet
    symbols = 'ACGT'
    if not uppercase:
        symbols = symbols.lower()
    
    # add state symbol to sequence and go to next state
    state = random(initial_state_weights)
    for i in xrange(n):
        seq.append(symbols[state])
        state = random(transition_weights[state])
      
    return Seq(''.join(seq), alphabet)

def permutedSequence(seq):
    """
    Returns a new sequence that is a permutation of the bases in the
    original sequences.
    
    >>> seq = randomSequence(40)
    >>> seq
    Seq('TCAGCGAGCTATATATAATAGTCAACGGCACCGAGCAGCC', DNAAlphabet())
    >>> permutedSequence(seq)
    Seq('CGGACGCACCGCGTGCCCAATCGGGCGCTGGGCGCCGGGG', DNAAlphabet())
    
    See also: randomSequence
    """
    
    from random import shuffle
    from Bio.Seq import Seq, MutableSeq
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # permute given sequence
    newseq = list(str(seq))
    shuffle(newseq)
    newseq = ''.join(newseq)
    
    # return appropriate object type
    if isinstance(seq, Seq):
        return Seq(newseq, seq.alphabet)
    elif isinstance(seq, MutableSeq):
        return MutableSeq(newseq, seq.alphabet)
    else:
        return newseq

def baseCount(seq, bundleOther=False, warning=False):
    """
    Counts the number of occurrences of each nucleotide in the given 
    sequence and returns these numbers as the values of a dictionary 
    with keys A, C, G and T. If non-base characters are present in the 
    sequence, their individual counts are added to the dictionary as 
    well. If the parameter bundleOthers is set to True, the count of all 
    non-base characters is bundled into a single dictionary entry with 
    key "other". If the warning parameter is set to True, a warning is 
    given if other characters are present in the given sequence.
    
    >>> baseCount('AGCTGCTCGTGATCGT')
    {'A':2, 'C':4, 'T':5, 'G':5}
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # compute histogram of symbols used in seq
    seq2int = map(ord, seq)
    hist = dict((chr(key),val) for key, val in enumerate(numpy.bincount(seq2int)) if val)
    
    # bundle non-base symbols into other and issue warning if other sequences are found
    if warning or bundleOther:
        other, otherSymbols = 0, ''
        for base in hist.keys():
            if base not in 'AGCT':
                otherSymbols += base
                other += hist[base]
                if bundleOther:
                    del hist[base]
            if bundleOther and other > 0:
                hist['other'] = other
            if warning and otherSymbols:
                print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
    
    return hist
  
def aaCount(seq, bundleOther=False, warning=False):
    """
    Counts the number of occurrences of each amino acid in the given 
    sequence and returns these numbers as the values of a dictionary 
    with amino acid symbols as keys. If non-amino acid symbols are 
    present in the sequence, their individual counts are added to the 
    dictionary as well. If the parameter bundleOthers is set to True, 
    the count of all non-amino acid symbols is bundled into a single 
    dictionary entry with key "other". If the warning parameter is set 
    to True, a warning is given if other characters are present in the 
    given sequence.
    
    >>> aaCount('AGCTGCTCGTGATCGT')
    {'A':2, 'C':4, 'T':5, 'G':5}
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # compute histogram of symbols used in seq
    seq2int = map(ord, seq)
    hist = dict((chr(key),val) for key, val in enumerate(numpy.bincount(seq2int)) if val)
    
    # bundle non-base symbols into other and issue warning if other sequences are found
    # TODO: needs implementation
    #  if warning or bundleOther:
    #    other, otherSymbols = 0, ''
    #    for base in hist.keys():
    #      if base not in 'AGCT':
    #        otherSymbols += base
    #        other += hist[base]
    #        if bundleOther:
    #          del hist[base]
    #    if bundleOther and other > 0:
    #      hist['other'] = other
    #    if warning and otherSymbols:
    #      print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
    
    return hist
  
def percentageGC(seq):
    """
    Calculates G+C content, returns the percentage (float between 0 and 
    100). Copes with mixed case sequences and with the ambiguous 
    nucleotide S (represents either G or C) when counting the G and C 
    content. The percentage is calculated against the full length, e.g.:
    
    >>> percentageGC('ACTGN')
    40.0
    
    Note that this will return zero for an empty sequence.
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    try:
        gc = sum(map(seq.count,['G','C','g','c','S','s']))
        return 100.0 * gc / len(seq)
    except ZeroDivisionError:
        return 0.0

def baseCountFrequency(seq, bundleOther=False, warning=False):
    """
    Counts the number of occurrences and the frequency of each 
    nucleotide in the given sequence and returns both numbers as the 
    tuple-values of a dictionary with keys A, C, G and T. If non-base 
    characters are present in the sequence, their individual counts and 
    frequencies are added to the dictionary as well. If the parameter 
    bundleOthers is set to True, the count of all non-base characters is 
    bundled into a single dictionary entry with key "other". If the 
    warning parameter is set to True, a warning is given if non-base 
    characters are present in the given sequence.
    
    >>> baseCountFrequency('AGCTGCTCGTGATCGT')
    {'A':(2, 0.125), 'C':(4, 0.25), 'T':(5, 0.3125), 'G':(5, 0.3125)}
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # compute histogram of symbols used in seq
    seq2int = map(ord, seq)
    hist = dict((chr(key),val) for key, val in enumerate(numpy.bincount(seq2int)) if val)
    
    # bundle non-base symbols into other and issue warning if other sequences are found
    if warning or bundleOther:
        other, otherSymbols = 0, ''
        for base in hist.keys():
            if base not in 'AGCT':
                otherSymbols += base
                other += hist[base]
                if bundleOther:
                    del hist[base]
        if bundleOther and other > 0:
            hist['other'] = other
        if warning and otherSymbols:
            print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
    
    # add frequencies to the histogram
    for base in hist:
        hist[base] = (hist[base], float(hist[base]) / len(seq))
    
    return hist
  
def dimerCount(seq, bundleOther=False, warning=False):
    """
    Counts the number of nucleotide dimers in the given sequence and 
    returns these numbers in a dictionary with keys AA, AC, AG,..., GT, 
    TT. Gaps (-) are removed from the input sequence. If non-base 
    characters are present in the sequence, the corresponding dimers are 
    added to the dictionary as well. If the parameter bundleOthers is 
    set to True, the count of all dimers with non-base characters is 
    bundled into a single dictionary entry with key "other". If the 
    warning parameter is set to True, a warning message is displayed if 
    non-base characters are present in the given sequence.
    
    >>> dimerCount('AGCAGAGGCGCGT')
    {'GT':1, 'AG':3, 'CA':1, 'CG':2, 'GG':1, 'GC':3, 'GA':1}
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # remove gaps from the sequence
    if seq.find('-') >= 0:
        seq = seq.replace('-', '')
    
    # compute histogram of symbols used in seq
    dimer2int = [ord(seq[i]) + 256 * ord(seq[i + 1]) for i in xrange(len(seq) - 1)]
    hist = dict((chr(key % 256) + chr(key // 256), val) for key, val in enumerate(numpy.bincount(dimer2int)) if val)
    
    # bundle non-base symbols into other and issue warning if other sequences are found
    if warning or bundleOther:
        other, otherSymbols = 0, set()
        for dimer in hist.keys():
            if dimer[0] not in 'AGCT' or dimer[1] not in 'AGCT':
                if dimer[0] not in 'AGCT':
                    otherSymbols.add(dimer[0]) 
                if dimer[1] not in 'AGCT':
                    otherSymbols.add(dimer[1])
                other += hist[dimer]
                if bundleOther:
                    del hist[dimer]
        if bundleOther and other > 0:
            hist['other'] = other
        if warning and otherSymbols:
            print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
    
    return hist

def genomicSignature(seq, warning=False):
    """  
    Computes the genome signature for a given sequence (i.e. the ratio
    between the frequency of the dinucleotide (say AT) and the product 
    of the frequencies of its components (say A, and T) and returns 
    these numbers in a dictionary with keys AA, AC, AG,..., GT, TT. Gaps 
    (-) are removed from the input sequence. If the warning parameter is 
    set to True, a warning message is displayed if non-base characters 
    are present in the given sequence.
    
    >>> seq = randomSequence(240)
    >>> gs = genomicSignature(seq)
    >>> showDimerMatrix(gs, fmt='%10.4f')
        0.8580    1.1193    1.2468    0.7579
        1.3292    0.7416    1.1362    0.8651
        0.9535    0.8970    0.9404    1.2309
        0.7579    1.2977    0.7126    1.1381
    
    Reference:
    
      S.Karlin, A.M.Campbell, J. Mrazek, "Annu. Rev. Genet.", 32:185-225,
      (1998).
      
    See also: dnDensity, dimerCount, ntDensity, baseCountFrequency
    """
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # compute frequencies
    bases = baseCount(seq, warning=warning)
    dimers = dimerCount(seq)
    for kmer in bases:
        bases[kmer] /= float(len(seq))
    for kmer in dimers:
        dimers[kmer] /= float(len(seq)-1)
    
    # return odds ratios
    return dict((base1 + base2, dimers[base1 + base2] / float(bases[base1] * bases[base2])) for base1 in 'ACGT' for base2 in 'ACGT')

def codonCount(seq, frame=0, warning=False):
    """
    Counts the number of occurrences of each codon in the given sequence 
    and returns these numbers in a dictionary with keys AAA, AAC, AAG, 
    ..., TTG, TTT. Gaps (-) are removed from the input sequence. Codons 
    with ambiguous nucleotide symbols are not counted. If the warning 
    parameter is set to True, a warning message is displayed if non-base 
    characters are present in the given sequence. Codons are counted for
    the reading frame 0, 1 or 2. Default is 0.
    
    >>> codonCount('AGCCCCACCCCCTAT')
    {'ACC':1, 'ATG':0, 'AAG':0, 'AAA':0, ..., 'TGG':0, 'TCT':0}
    """
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # remove gaps from the sequence
    if seq.find('-') >= 0:
        seq = seq.replace('-', '')
    
    # initialize codon histogram
    hist = dict((base1 + base2 + base3, 0) for base1 in 'ACGT' for base2 in 'ACGT' for base3 in 'ACGT')
    
    # compute histogram of symbols used in seq
    other, otherSymbols = 0, set()
    for codon in (seq[i:i + 3] for i in xrange(frame,len(seq) - 2, 3)):
        try:
            hist[codon] += 1
        except:
            other += 1
            for base in xrange(3):
                if codon[base] not in 'ACGT':
                    otherSymbols.add(codon[base])
    if other>0:
        hist['other']=other
    if warning and otherSymbols:
        print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
    
    return hist

def nmerCount(seq, n, threshold=-1, warning=False):
    """
    Counts the number of occurrences of each n-mer (pattern with length 
    n) in the given sequence and returns these numbers in a dictionary.
    Gaps (-) are removed from the input sequence. Only n-mers that occur
    at least threshold times are included in the dictionary. If the 
    warning parameter is set to True, a warning message is displayed if 
    non-base characters are present in the given sequence.
    
    >>> nmerCount('AGCCCCACCCCC', 10)
    {'AGCCCCACCC':1, 'CCCCACCCCC':1, 'GCCCCACCCC':1}
    """
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # remove gaps from the sequence
    if seq.find('-') >= 0:
        seq = seq.replace('-', '')
    
    # compute histogram of symbols used in seq
    hist = {}
    for nmer in (seq[i:i + n] for i in xrange(len(seq) - n + 1)):
        try:
            hist[nmer] += 1
        except:
            hist[nmer] = 1  
    
    # remove n-mers with cardinality below threshold
    if threshold >= 0:
        for key in hist.keys():
            if hist[key] < threshold:
                del hist[key]
          
    # issue warning message if non-base symbols occur in the sequence
    if warning:
        otherSymbols = set.difference(set(seq), set('ACGT'))
        if otherSymbols:
            print 'Unknown symbols \'%s\' appear in the sequence.' % ''.join(sorted(otherSymbols))
          
    return hist

def ntDensity(seq, window=None, stepSize=1, showIndividual=True, showCombined=True):
    """
    Generates a sliding window density plot of the nucleotides A,T,C,G 
    in a given sequence. The window length must be an odd integer >= 5 
    and has a default value of len(seq)/20 (unacceptable values are 
    adjusted accordingly). The stepsize must be an integer >= 1 and has 
    a default value of 1.
    
    If the showIndividual parameter is set to True, the frequency is
    plotted for all four nucleotides individually. If the showCombined
    parameter is set to True, the combined AT and GC frequencies are
    plotted. At least on of these parameters must be set True.
    
    >>> seq = randomSequence(240)
    >>> ntDensity(seq)
    
    See also: baseCount, dimerCount, codonCount
    """
    
    assert (showIndividual or showCombined), 'Function ntDensity must generate at least one type of plot.'
    
    # convert Bio.SeqRecord.SeqRecord objects to Bio.Seq.Seq objects if
    # needed
    try:
        seq = seq.seq
    except:
        pass
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # set default values
    w = int(window) if window else len(seq) // 20
    s = int(stepSize) if stepSize else 1
    
    if w < 5:                # window has a minimum length of 5
        w = 5
    elif w % 2 == 0:         # window must be odd
        w += 1
      
    # calculate nucleotide densities with a sliding window
    l = len(seq)
    sa, sc, sg, st = [], [], [], []
    for i in xrange(0, l-w+2, s):
        sa.append(sum(map(seq[i:i + w].count,['A','a'])) / float(w))
        sc.append(sum(map(seq[i:i + w].count,['C','c'])) / float(w))
        sg.append(sum(map(seq[i:i + w].count,['G','g'])) / float(w))
        st.append(sum(map(seq[i:i + w].count,['T','t'])) / float(w))
      
    # create two plots: one for density of every base, and one for AT and GC
    import pylab
    import operator
    
    pylab.figure()  
    if showIndividual:
        if showCombined:
            pylab.subplot(2, 1, 1)
        pylab.title('nucleotide density (window=%d)' % w)
        pylab.plot(range(w // 2, l - w // 2 + 1, s), sa,  label='A')    
        pylab.plot(range(w // 2, l - w // 2 + 1, s), sc,  label='C')    
        pylab.plot(range(w // 2, l - w // 2 + 1, s), sg,  label='G')    
        pylab.plot(range(w // 2, l - w // 2 + 1, s), st,  label='T')    
        pylab.legend()
        pylab.xlim(0, len(seq))
        pylab.ylim(0, 1)
    
    if showCombined:
        if showIndividual:
            pylab.subplot(2, 1, 2)
        pylab.title('AT and GC density (window=%d)' % w)
        sat = map(operator.add, sa, st)
        scg = map(operator.add, sc, sg)
        pylab.plot(range(w // 2, l - w // 2 + 1, s), sat,  label='AT')    
        pylab.plot(range(w // 2, l - w // 2 + 1, s), scg,  label='GC')    
        pylab.legend()
        pylab.xlim(0, len(seq))
        pylab.ylim(0, 1)
  
def dnDensity(seq, window=None, stepSize=None, dimers=None):
    """
    Generates a sliding window density plot for a selection of the 16
    dinucleotides in a given sequence. The window length must be an odd 
    integer >= 5 and has a default value of len(seq)/20 (unacceptable 
    values are adjusted accordingly). The stepsize must be an integer >= 
    1 and has a default value of 1. By default, only the dinucleotides
    AT and CG are plotted. Alternatively, a Python sequence of the 
    dinucleotides to be plotted can be passed as the parameter dimers.
    
    >>> seq = randomSequence(240)
    >>> dnDensity(seq)
    
    See also: baseCount, dimerCount, codonCount
    """
    
    # convert Bio.Seq object to string object if needed
    try:
        seq = str(seq)
    except:
        pass
    
    # set default values
    w = int(window) if window else len(seq) // 20
    s = int(stepSize) if stepSize else 1
    d = dimers if dimers else ['AT', 'CG']
    
    if w < 5:                # window has a minimum length of 5
        w = 5
    elif w % 2 == 0:         # window must be odd
        w += 1
      
    # calculate dinucleotide densities with a sliding window
    l = len(seq)
    densities = []
    dim = [seq[k:k + 2] for k in xrange(l - 1)]
    for dimer in d:
        densities.append([])
    for i in xrange(0, l - w + 2, s):
        wdim = dim[i:i + w - 1]
        for j in xrange(len(d)):
            densities[j].append(wdim.count(d[j]) / float(w - 1))
      
    # create one densityplot for each dimer
    import pylab
    
    pylab.figure()
    pylab.title('dinucleotide density')
    for i in xrange(len(d)):
        pylab.plot(range(w // 2, l - w // 2 + 1, s), densities[i], label=d[i])
    pylab.legend()

def showDimerTable(hist, fmt='%10d'):
    """
    Prints a two-column table to standard output for a given mapping 
    from dinucleotides (as keys) to corresponding measures (as values).
    Usually, the mapping is passed as a dictionary. The first column of
    the output contains the dinocleotide, the second column the 
    corresponding measure. The measures are printed in the given format 
    ('%10d' by default).
    
    >>> dimers = dimerCount(randomSequence(200))
    >>> showDimerTable(dimers, fmt='%3d')
       AA: 16
       AC: 13
       AG: 15
       AT: 11
       ...
    
    See also: randomSequence, dimerCount
    """
    
    for base1 in 'ACGT':
        for base2 in 'ACGT':
            print ('%5s:' + fmt) % (base1 + base2, hist.get(base1 + base2, 0))
    if 'other' in hist:
        print ('other:' + fmt) % hist['other']

def showDimerMatrix(hist, fmt='%10d'):
    """
    Prints a two-dimensional matrix to standard output for a given 
    mapping from dinucleotides (as keys) to corresponding measures 
    (as values). Usually, the mapping is passed as a dictionary. The
    rows correspond to the first base of the dinucleotides in the
    order A*, C*, G*, T* and the columns correspond to the second base
    in the order *A, *C, *G, *T. The measures are printed in the given 
    format ('%10d' by default).
    
    >>> dimers = dimerCount(randomSequence(200))
    >>> showDimerMatrix(dimers, fmt='%5d')
       13    7   15   16
       12   11   13    9
       12   12   13   15
       14   15   11   11
    
    See also: randomSequence, dimerCount
    """
    
    # GS=GENSIGN(SEQ) calculate the genome signature of a sequence. In the
    # results raws are A*, C*, G*, T*, columns are *A, *C, *G, *T
    for base1 in 'ACGT':
        row = ''
        for base2 in 'ACGT':
            row += fmt % hist[base1+base2]
        print row
    if 'other' in hist:
        print ('other: ' + fmt) % hist['other']

def showCodonTable(hist, fmt='%10d'):
    """
    Prints a two-column table to standard output for a given mapping 
    from codons (as keys) to corresponding measures (as values). Usually, 
    the mapping is passed as a dictionary. The first column of the output 
    contains the codons, the second column the corresponding measure. 
    The measures are printed in the given format ('%10d' by default).
    
    >>> codons = codonCount(randomSequence(2000))
    >>> showCodonTable(codons, fmt='%2d')
      AAA -  7    AAC -  9    AAG - 11    AAT -  9  
      ACA -  9    ACC -  7    ACG - 16    ACT - 15  
      AGA - 13    AGC -  9    AGG - 10    AGT - 11  
      ATA -  8    ATC -  9    ATG - 10    ATT - 12  
      ...
    
    See also: randomSequence, codonCount
    """
    
    for base1 in 'ACGT':
        for base2 in 'ACGT':
            row = ''
        for base3 in 'ACGT':
            row += ('%5s - ' + fmt + '  ') % (base1 + base2 + base3, hist.get(base1 + base2 + base3, 0))
        print row
    if 'other' in hist:
        print ('other:' + fmt) % hist['other']
    
def showCodonHeatmap(hist, title=None):
    """
    Generates a heat map for a given mapping from codons (as keys) to 
    corresponding measures (as values). Usually, the mapping is passed 
    as a dictionary. The heatmap is labeled with the codons.
    
    >>> codons = codonCount(randomSequence(2000))
    >>> showCodonTable(codons, fmt='%2d')
    
    See also: randomSequence, codonCount
    """
    
    # construct array
    import pylab
    
    # construct matrix
    matrix = numpy.zeros((8, 8),  dtype=numpy.int)
    pos = [[0, 0], [4,0], [0, 4], [4, 4]]
    base = 'ACGT'
    for i in xrange(4):
        for j in xrange(4):
            for k in xrange(4):
                matrix[7 - (pos[i][1] + k), pos[i][0] + j] = hist[base[i] + base[k] + base[j]]
    
    # plot matrix as heatmap
    pylab.figure()
    pylab.pcolormesh(matrix)
    pylab.bone()
    pylab.colorbar()
    pylab.axis('off')
    if title:
        pylab.title(title)
    
    # plot codons on heatmap
    pos = [[0, 0], [4,0], [0, 4], [4, 4]]
    base = 'ACGT'
    for i in xrange(4):
        for j in xrange(4):
            for k in xrange(4):
                pylab.text(
                    pos[i][0] + j + .5, 8 - (pos[i][1] + k + .5), 
                    base[i] + base[k] + base[j], 
                    horizontalalignment='center', 
                    verticalalignment='center', 
                    color='red'
                )
