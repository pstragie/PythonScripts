"""
Genome data

This module contains useful functions for downloading genome sequences
from online databases, and basic manipulations of genomic data.
"""

def concatenateContigs(storageLocation, fmt='fasta', separator=''):
    """
    Reads a series of contigs from file and returns a concatenated
    sequence containing all contigs in the same order as they were 
    stored in the file. The individual contigs are parsed from a file 
    with the format specified by the fmt parameter. The storageLocation
    parameter indicates the location of the file on the local file 
    system. Acceptable values for the fmt parameter are 'gb' (for 
    GenBank format) and 'fasta' (for FASTA format).
    
    By default, the contigs are concatenated into a single string,
    that contains no traces of the boundaries in between contigs. If
    the separator parameter is set to a string, that string will be 
    used in the concatenated sequence to indicate positions where two
    contigs were concatenated. 
    """
    from Bio import SeqIO
    handle = open(storageLocation, 'rU')
    return separator.join([str(seq.seq).strip() for seq in SeqIO.parse(handle, fmt)])

def longestContig(storageLocation, fmt='fasta'):
    """
    Returns the SeqRecord that is the longest contig from file. The 
    individual contigs are parsed from a file with the format specified 
    by the fmt parameter. The storageLocation parameter indicates the 
    location of the file on the local file system. Acceptable values 
    for the fmt parameter are 'gb' (for GenBank format) and 'fasta' 
    (for FASTA format).
    """
    from Bio import SeqIO
    handle = open(storageLocation, 'rU')
    longest = None
    for contig in SeqIO.parse(handle, fmt):
        if longest is None or len(longest.seq) < len(contig.seq):
            longest = contig
    return longest

def getGenBank(acc, fmt='fasta', mode='text', storageLocation=None, location=None):
    """
    Searches for the accession number in the GenBank database and 
    returns a Bio.SeqRecord.SeqRecord object containing information for
    the sequence. The sequence information is parsed from a file with
    the format specified by the fmt parameter. Acceptable values are
    'gb' (for GenBank format) and 'fasta' (for FASTA format).
    
    By default, the complete GenBank sequence is downloaded. If a tuple 
    of two integers is passed to the location parameter, they are 
    considered to indicate the start and stop location to retrieve a 
    specified subsequence from the selected GenBank file. Take into 
    account that sequence location are indexed starting from 1 (not 0).
    
    If the path name of a directory is passed to the storageLocation
    parameter, the original sequence file downloaded from GenBank is
    stored locally in that directory with file name <acc>.<format>. If a
    file was already available with that name in indicated directory,
    that file is taken instead of downloading the file anew from GenBank.
    
    If an error occurs while retrieving the formatted information from
    GenBank, try to run the query again at a later time. Errors can 
    occur due to internet connectivity issues that are unrelated to the 
    GenBank record.
    
    >>> acc, fmt, storageLocation = 'L42023', 'fasta', '/tmp/'
    >>> Hflu = getGenbank(acc, fmt, storageLocation)
    >>> print Hflu
    ID: gi|6626252|gb|L42023.1|
    Name: gi|6626252|gb|L42023.1|
    Description: gi|6626252|gb|L42023.1| Haemophilus influenzae Rd KW20, complete genome
    Number of features: 0
    Seq('TATGGCAATTAAAATTGGTATCAATGGTTTTGGTCGTATCGGCCGTATCGTATT...TCT', SingleLetterAlphabet())
    
    See http://www.ncbi.nlm.nih.gov/About/disclaimer.html for more 
    information on GenBank data.
    
    See http://www.ncbi.nlm.nih.gov/corehtml/query/static/efetch_help.html
    for a complete description of the Efetch Entrez web service that allows
    to retrieves records in the requested format from one of the databases
    maintained by the National Center for Biotechnology Information (NCBI).
    """
  
    # REMARK:
    # If file is downloaded once with given efetch parameters (e.g. 
    # start and stop location), it will not be downloaded anew if other 
    # parameters are passed to the getGenBank function. In that case, it 
    # is not safe to rely on a local copy of the GenBank file.
    
    import os
    from Bio import Entrez
    from Bio import SeqIO
    
    # Adjust storage directory to make sure it ends with the pathname 
    # separator used by the local file system. By default the downloaded
    # file is stored in the current working directory.
    localDir=storageLocation if storageLocation else ''
    if localDir and localDir[-1]!=os.sep:
        localDir+=os.sep
  
    # process additional parameters for the EFetch web service
    efetch_params = {}
    if location:
        efetch_params['seq_start'], efetch_params['seq_stop'] = location

    # open source as either local or remote
    if storageLocation!=None:
        localFile = localDir+'%s.%s' % (acc, fmt)
    if storageLocation is None or not os.path.exists(localFile):
        # download GenBank file if no local storage location is wanted or 
        # if file is not locally available from the given storage location
        print 'Downloading sequence %s in %s format from GenBank ...' % (acc, fmt)
        Entrez.email = 'Peter.Dawyndt@UGent.be'
        source = Entrez.efetch(db='nucleotide', rettype=fmt, retmode=mode, id=acc, **efetch_params)
    else:
        source = open(localFile) 
    if not(storageLocation is None) and not os.path.exists(localFile):
        # make local copy from GenBank file and read from local copy
        destination = open(localFile, 'w')
        for line in source:
            destination.write(line)
        source.close()
        destination.close()
        source = open(localFile)
  
    # parse GenBank file
    seq = SeqIO.read(source, format=fmt)
    source.close()

    return seq
  
def getEntrezProtein(acc, fmt='fasta', mode='text', storageLocation=None, location=None):
    """
    Searches for the record corresponding with accession number in the 
    Entrez Protein database, which is a translation of the nucleotide
    sequences in the GenBank database and is maintained by the National
    Center for Biotechnology Information. The function returns an object
    with type Bio.SeqRecord.SeqRecord, containing information for the 
    protein sequence (amino acids). The sequence information is parsed 
    from a file with the format specified by the fmt parameter. 
    Acceptable values are 'gb' (for GenBank format) and 'fasta' (for 
    FASTA format).
    
    By default, the complete Entrez Protein sequence is downloaded. If a 
    tuple of two integers is passed to the location parameter, they are 
    considered to indicate the start and stop location to retrieve a 
    specified subsequence from the selected GenBank file. Take into 
    account that sequence location are indexed starting from 1 (not 0).
    
    If the path name of a directory is passed to the storageLocation
    parameter, the original sequence file downloaded from Entrez Protein 
    is stored locally in that directory with file name <acc>.<format>. 
    If a file was already available with that name in indicated 
    directory, that file is taken instead of downloading the file anew 
    from Entrez Protein.
    
    If an error occurs while retrieving the formatted information from
    Entrez Protein, try to run the query again at a later time. Errors 
    can occur due to internet connectivity issues that are unrelated to 
    the Entrez Protein record.
    
    >>> acc, fmt, storageLocation = 'L42023', 'fasta', '/tmp/'
    >>> Hflu = getGenbank(acc, fmt, storageLocation)
    >>> print Hflu
    ID: gi|6626252|gb|L42023.1|
    Name: gi|6626252|gb|L42023.1|
    Description: gi|6626252|gb|L42023.1| Haemophilus influenzae Rd KW20, complete genome
    Number of features: 0
    Seq('TATGGCAATTAAAATTGGTATCAATGGTTTTGGTCGTATCGGCCGTATCGTATT...TCT', SingleLetterAlphabet())
    
    See http://www.ncbi.nlm.nih.gov/About/disclaimer.html for more 
    information on GenBank data.
    
    See http://www.ncbi.nlm.nih.gov/corehtml/query/static/efetch_help.html
    for a complete description of the Efetch Entrez web service that allows
    to retrieves records in the requested format from one of the databases
    maintained by the National Center for Biotechnology Information (NCBI).
    """
  
    # REMARK:
    # If file is downloaded once with given efetch parameters (e.g. 
    # start and stop location), it will not be downloaded anew if other 
    # parameters are passed to the getGenBank function. In that case, it 
    # is not safe to rely on a local copy of the GenBank file.
  
    import os
    from Bio import Entrez
    from Bio import SeqIO
  
    # Adjust storage directory to make sure it ends with the pathname 
    # separator used by the local file system. By default the downloaded
    # file is stored in the current working directory.
    localDir=storageLocation if storageLocation else ''
    if localDir and localDir[-1]!=os.sep:
        localDir+=os.sep
  
    # process additional parameters for the EFetch web service
    efetch_params = {}
    if location:
        efetch_params['seq_start'], efetch_params['seq_stop'] = location

    # open source as either local or remote
    if storageLocation!=None:
        localFile = localDir+'%s.%s' % (acc, fmt)
    if storageLocation is None or not os.path.exists(localFile):
        # download GenBank file if no local storage location is wanted or 
        # if file is not locally available from the given storage location
        print 'Downloading sequence %s in %s format from Entrez Protein ...' % (acc, fmt)
        Entrez.email = 'Peter.Dawyndt@UGent.be'
        source = Entrez.efetch(db='protein', rettype=('gp' if fmt=='gb' else fmt), retmode=mode, id=acc, **efetch_params)
    else:
        source = open(localFile) 
    if not(storageLocation is None) and not os.path.exists(localFile):
        # make local copy from Entrez Proteun file and read from local copy
        destination = open(localFile, 'w')
        for line in source:
            destination.write(line)
        source.close()
        destination.close()
        source = open(localFile)
  
    # parse GenBank file
    seq = SeqIO.read(source, format=fmt)
    source.close()

    return seq
  
def accession2gi(acc, db='nucleotide', speed='quick'):
    """
    Perform an egquery, esearch and esummary to check whether a given
    accession number can be found in the protein or nucleotide sequence
    databases of the NCBI. A tuple containing the accession number and
    the appropriate databse is returned.
    
    The db parameter can be either nucleotide (the default) or protein.
    
    The speed parameter can be either quick (the default) or slow. Slow
    lookups will possibly retrieve more accurate information.
    
    TODO: this function needs further elaboration, and if finished it
          may be used in the getGenBank and getEntrezProtein functions
          to check the validity of the accession numbers passed to these
          functions. In particular, Biopython has already implemented
          parsers for all NCBI Entrez web services. So, no need to parse
          the information here ourselves.
    """

    import urllib
  
    # Perform a query of all Entrez databases using egquery to get a 
    # count of the number of hits for the given accession number in
    # nucleotide and protein. This information is used to throw an error
    # if the users used the wrong function to retrieve the sequence file
    # (e.g. used getGenBank to retrieve a peptide sequence). After the
    # query, esearch is used to retrieve the gi number that corresponds
    # with the given accession number.
    if speed=='quick':
        # using the [Accession] key word accelerates the query
        queryURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=%s[Accession]' % acc
    else:
        # not using the [Accession] slows down the query, but allows dead
        # suppressed and replaced files to be found.
        queryURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=%s' % acc
    
    queryXML = urllib.urlopen(queryURL)
  
    # Parse out the number of hits in each database, based on the DbName
    # tag (personal communication with Tao Tao at NCBI suggested that
    # the DbName element would be more meaningful (and potentially more 
    # stable) than the MenuName element. CoreNucleotide database is now
    # named nucleotide.
    dbCount={}
    from xml.dom.minidom import parse
    dom = parse(queryXML)
    for node in dom.getElementsByTagName('ResultItem'):  # visit every ResultItem node
        newdb = node.getElementsByTagName('DbName')[0].firstChild.toxml()
        count = int(node.getElementsByTagName('Count')[0].firstChild.toxml())
        dbCount[newdb]=count
    queryXML.close()
  
    # if db is specified as nucleotide, we need to determine which 
    # specific nucleotide database must be used
    proteinCount = dbCount.get('protein', 0)
    nucleotideCount = 0
    for newdb in ['nuccore', 'nucgss', 'nucest']:
        nucleotideCount += dbCount.get(newdb, 0)
        if db.lower()=='nucleotide' and dbCount.get(newdb, 0) > 0:
            db=newdb
        
    if nucleotideCount == 0 and proteinCount == 0:
        print 'here'
        return None
    elif ((nucleotideCount > 1 and db[:3].lower() == 'nuc')
          and (proteinCount > 1 and db.lower() == 'protein')):
        # given an error if more than one GenBank identifier is found for
        # the given accession number
        print 'The key %s has more than one sequence file associated with it in the %s database.' % (acc, db)
        return None
    elif proteinCount == 0 and db.lower() == 'protein':
        # given an error if the sequence was found in the other database
        print 'The key %s was not found in the %s database, but it is in the %s database.' % (acc, db, 'nucleotide')
        return None    
    elif nucleotideCount == 0 and db[:3].lower() == 'nuc':
        # given an error if the sequence was found in the other database
        print 'The key %s was not found in the %s database, but it is in the %s database.' % (acc, db, 'protein')
        return None
    else:
        # build esearch URL
        if speed == 'quick':
            # using the [Accession] key word accelerates the query
            queryURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=%s&term=%s[Accession]' % (db, acc)
        else:
            # not using the [Accession] slows down the query, but allows dead
            # suppressed and replaced files to be found.
            queryURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=%s&term=%s' % (db, acc)

        # parse out the unique GenBank identifier
        queryXML = urllib.urlopen(queryURL)
        dom = parse(queryXML)
        gid = int(dom.getElementsByTagName('Id')[0].firstChild.toxml())
        queryXML.close()
    
        # TODO: we might use esummary here to get the DocSum for the 
        #       record and parse the XML to get record status, replacement
        #       record and comments, and warn the user appropriately
        
        return gid
    
def getEMBL(acc, fmt='fasta', storageLocation=None, location=None):
    """
    Searches for the accession number in the EMBL database and 
    returns a Bio.SeqRecord.SeqRecord object containing information for
    the sequence. The sequence information is parsed from a file with
    the format specified by the fmt parameter. Acceptable values are
    'embl' (for EMBL format) and 'fasta' (for FASTA format). The full
    record is always downloaded
    
    By default, the complete EMBL sequence is downloaded. If a tuple of 
    two integers is passed to the location parameter, they are 
    considered to indicate the start and stop location to retrieve a 
    specified subsequence from the selected EMBL file. Take into 
    account that sequence location are indexed starting from 1 (not 0).
    
    If the path name of a directory is passed to the storageLocation
    parameter, the original sequence file downloaded from EMBL is
    stored locally in that directory with file name <acc>.<format>. If a
    file was already available with that name in indicated directory,
    that file is taken instead of downloading the file anew from EMBL.
    
    If an error occurs while retrieving the formatted information from
    EMBL, try to run the query again at a later time. Errors can occur 
    due to internet connectivity issues that are unrelated to the EMBL
    record.
    
    >>> acc, fmt, storageLocation = 'L42023', 'fasta', '/tmp'
    >>> Hflu = getEMBL(acc, fmt, storageLocation)
    >>> print Hflu
    ID: ENA|L42023|L42023.1
    Name: ENA|L42023|L42023.1
    Description: ENA|L42023|L42023.1 Haemophilus influenzae Rd KW20, complete genome.
    Number of features: 0
    Seq('TATGGCAATTAAAATTGGTATCAATGGTTTTGGTCGTATCGGCCGTATCGTATT...GCA', SingleLetterAlphabet())
    
    See http://www.ebi.ac.uk/Information/termsofuse.html for more 
    information on EMBL data.  
    """
    
    import os
    import urllib
    from Bio import SeqIO
    
    # Adjust storage directory to make sure it ends with the pathname 
    # separator used by the local file system. By default the downloaded
    # file is stored in the current working directory.
    localDir=storageLocation if storageLocation else ''
    if localDir and localDir[-1] != os.sep:
        localDir+=os.sep
  
    # open source as either local or remote
    if storageLocation != None:
        localFile = localDir+'%s.%s' % (acc, fmt)
    if storageLocation is None or not os.path.exists(localFile):
        # download EMBL file if no local storage location is wanted or 
        # if file is not locally available from the given storage location
        print 'Downloading sequence %s in %s format from EMBL ...' % (acc, fmt)
        url='http://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=EMBL&id=%s&format=%s&style=raw' % (acc, fmt)
        source = urllib.urlopen(url)
    else:
        source = open(localFile) 
    if not(storageLocation is None) and not os.path.exists(localFile):
        # make local copy from EMBL file and read from local copy
        destination = open(localFile, 'w')
        for line in source:
            destination.write(line)
        source.close()
        destination.close()
        source = open(localFile)
  
        # parse EMBL file
        seq = SeqIO.read(source, format=fmt)
        source.close()
    else:
        return

    # extract sequence fragment
    if location:
        start, end = location
        seq = seq[start:end]

    return seq