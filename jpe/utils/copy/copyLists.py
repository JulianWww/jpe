import copy as copyLib
    

def copy(val):
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
    
