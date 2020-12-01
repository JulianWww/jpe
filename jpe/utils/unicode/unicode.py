"unicode aid functions"

def superscript(txt):
    """put txt in superscript

    a function to convert a text to supersript using unicode
    @param txt: a string of the values to be turned into supersript
    @type txt: string

    @return: txt in superscript
    """
    chars = {"0": "\u2070",
             "1": "\u00B9",
             "2": "\u00B2",
             "3": "\u00B3",
             "4": "\u2074",
             "5": "\u2075",
             "6": "\u2076",
             "7": "\u2077",
             "8": "\u2078",
             "9": "\u2079",
             "+": "\u207A",
             "-": "\u207B",
             "=": "\u207C",
             "(": "\u207D",
             ")": "\u207E",
             "n": "\u207F",
             "i": "\u2071"}
    out = ""
    for char in txt:
        out += chars[char]
    return out

def prettyIndex(var):
    """put txt in subscript

    a function to convert a text to subscript using unicode
    @param txt: a string of the values to be turned into subscript
    @type txt: string

    @return: txt in subscript
    """
    #print indexes as subscript
    strIdx = ""
    for i in str(var+1):strIdx += str(chr(0x2080 + (int(i))))
    return strIdx

def nroot(n):
    """nth root print
    
    its ugly"""
    return superscript(n) + "\u221A"

             
             
             
