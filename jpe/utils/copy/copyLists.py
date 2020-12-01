"patch fore coping problems"

import copy as copyLib
    

def copy(val):
    """crates a copy of a list or dict

    this is a fix for the problem that when coping a list it of a list it dosnt copy second dim list

        >>> a = [[1,2],[3,4]]
        >>> b = copy.copy(a)
        # std copy lib copy 

        >>> a[0] = 10
        # in this case b is [[1,2],[3,4]]
        # so it works 

    however

        >>> a[1][0] = 10
        # in this case b is [[1,2],[10,4]] but in a true copy it schould be [[1,2], [3,4]]
        # if we use this patch
        >>> a = [[1,2],[3,4]]
        >>> c = jpe.utils.copy.copy(a)
        >>> a[0][0] = 10
        >>> b
        [[1,2],[3,4]]

    @param val: object what we want to copy
    @type val: list, dict, anything else will be done via copy.copy

    @return: pyobject
            a true copy of val

    """
    if isinstance(val, list):
        output = []
        for element in val:
            output.append(copy(element))
        return output

    elif isinstance(val, dict):
        output ={}
        for element in val:
            print(element, val[element])
            output[copy(element)] = copy(val[element])
        return output

    return copyLib.copy(val)
    
