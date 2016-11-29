#!env/python3
# coding: utf-8






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Stand alone tools
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def normalize_chr(chrm):
    chrm = chrm.upper()
    if (chrm.startswith("CHROM")):
        chrm = chrm[5:]
    if (chrm.startswith("CHRM")):
        chrm = chrm[4:]
    if (chrm.startswith("CHR")):
        chrm = chrm[3:]
    return chrm


def get_alt(alt):
    if ('|' in alt):
        return alt.split('|')
    else:
        return alt.split('/')


def normalize(pos, ref, alt):
    if (ref == alt):
        return None,None,None
    if ref is None:
        ref = ''
    if alt is None:
        alt = ''

    while len(ref) > 0 and len(alt) > 0 and ref[0]==alt[0] :
        ref = ref[1:]
        alt = alt[1:]
        pos += 1
    if len(ref) == len(alt):
        while ref[-1:]==alt[-1:]:
            ref = ref[0:-1]
            alt = alt[0:-1]

    return pos, ref, alt


def is_transition(ref, alt):
    tr = ref+alt
    if len(ref) == 1 and tr in ('AG', 'GA', 'CT', 'TC'):
        return True
    return False


