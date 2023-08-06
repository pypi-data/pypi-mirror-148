#===============================================================================
# export_bedgraph.py
#===============================================================================

"""Export methylation data in bedgraph format"""

from pybedtools import BedTool

def export_bedgraph(bedmethyl, chromosomes=None):
    """Convert methylation results to bedgraph format and print to stdout

    Parameters
    ----------
    bedmethyl
        path to a bedmethyl formatted file of methylation results
    chromosomes
        iterable of chromosomes to include in output
    """

    bedtool = BedTool(bedmethyl).sort()
    if chromosomes:
        for chrom, start, stop, *_, methyl in (i.fields for i in bedtool):
            c = set(chromosomes)
            if (chromosomes is None) or (chrom in  c):
                print(chrom, start, stop, methyl, sep='\t')
    else:
        for chrom, start, stop, *_, methyl in (tuple(i) for i in bedtool):
            print(chrom, start, stop, methyl, sep='\t')
