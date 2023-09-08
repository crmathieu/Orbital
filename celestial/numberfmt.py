""" module handling number formatting """

# will remove trailing 0 if the result is a float
def trim(svalue):

    exp = svalue.find('e')
    if exp <> -1:
        preExp = svalue[0:exp]
        postExp = svalue[exp+1: ]
        return trim(preExp)+"e"+postExp

    else:
        if "." in svalue:
            while True:
                ch = svalue[-1]
                if ch == '0' or ch == '.':
                    svalue = svalue[:-1] # will remove the last character
                    if ch == ".":
                        break
        return svalue


def normalizeNumber(snumber):

    dot = snumber.find(".")
    if dot <> -1:
        # the dot exists, hence we have a decimal
        wholeValue = snumber[0:dot]
        decimals = snumber[dot+1:]
    else:
        wholeValue = snumber
        decimals = ""

    normed = insertCommas(wholeValue)
    if len(decimals) > 0:
        normed += "."+decimals

    return normed


def setPrecision(svalue, iprecision):

    wholeValue = svalue
    decimals = ""

    # figure out if there is a decimal part
    dot = svalue.find(".")
    if dot <> -1:
        # the dot exists, hence we have a decimal
        wholeValue = svalue[0:dot]
        decimals = svalue[dot+1:]

        if "e" in svalue:
            # we have an exponent: find it
            exp = decimals.find("e")
            preExp = decimals[0:exp]
            postExp = decimals[exp+1:]
            n = len(preExp)
            if n > iprecision: # adjust number of digits to precision
                preExp = preExp[0:iprecision]
            svalue = formatWithExponent(insertCommas(wholeValue), preExp+"e"+postExp)

        else:
            if int(wholeValue) == 0:
                # case 0.XXXX our result is less than 1: let's eliminate
                # decimals heading zeros
                nzeros = 0
                if decimals <> "0":
                    d = decimals
                    while d[0] == "0":
                        d = d[1:]
                        nzeros += 1
                    exp = nzeros
                    if exp > 2:
                        decimals = d
                    else:
                        exp = 0

                    n = len(decimals)

                    if exp > 2:
                        # since the whole part is 0, we can take the first digit of the
                        # decimal part and push it to the whole part, as long as we add
                        # an extra negative exponent
                        if n >= 1:
                            wholeValue = decimals[0]
                            decimals = decimal[1:]
                            exp += 1
                            n -= 1

                    # then truncate where our precision wants it to be
                    if n > iprecision:
                        # .. #
                        if nzeros >= iprecision:
                            iprecision = nzeros+1

                        decimals = decimals[0:iprecision]

                    # finally concatenate exponent value
                    if exp > 0:
                        sexp = "e-"+ "{0<2}".format(exp)
                        decimals = decimals+sexp

            else:
                # case XXX.XXXXX
                n = len(decimals)
                if n > iprecision:
                    decimals = decimals[0:iprecision]

            svalue = formatWithExponent(insertCommas(wholeValue), decimals)

    else:
        # there is no decimal point
        exp = svalue.find("e")
        if e <> -1:
            # we have an exponent
            wholeValue = svalue[0:exp]
            expvalue = svalue[exp+1:]
            svalue = formatWithExponent(wholeValue, "e"+expvalue)

        svalue = insertCommas(svalue)

    return svalue #, iprecision

def formatWithExponent(wholeValue, decimal):
    if decimal[0] == "e":
        return wholeValue + decimal
    return wholeValue + "." + decimal


def insertCommas(wholeValue):
    # let's take care of signs and exponent
    # first signs....
    fc = wholeValue[0]
    sign = False
    if fc == "-" or fc == "+":
        sign = True
        wholeValue = wholeValue[1:]

    # now exponent....
    if "e" in wholeValue:
        return wholeValue

    n = len(wholeValue)
    i = 1
    strWithCommas = ""

    while i <= n:
        strWithCommas = wholeValue[-1] + strWithCommas # add from the right
        if i % 3 == 0:
            strWithCommas = ','+strWithCommas
        i += 1
        wholeValue = wholeValue[:-1] # remove last character and let's keep going

    if strWithCommas[0] == ",":
        strWithCommas = strWithCommas[1:]

    if sign == True:
        strWithCommas = fc + strWithCommas

    return strWithCommas
