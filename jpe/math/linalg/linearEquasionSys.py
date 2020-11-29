import numpy as np
import warnings
import jpe.errors
import jpe.utils.unicode.unicode
from jpe import Jfloat as jfloatMod
import jpe.utils.copy 

class gausean:
        """ this is a utils class contining the operations or tha gaussean eliminination as well as the rifinement methode"""
        def swapEquasions(system, idxA, idxB):
            arr = np.copy(system._arr)
            temp = np.copy(arr[idxA])
            arr[idxA] = arr[idxB]
            arr[idxB] = temp
            return arr
        
        def scanColumb(system, idx):
            arr = np.copy(system._arr)[:, idx]
            pos = np.where(arr != 0)
            if len(pos[0])> 0:
                return pos[0]
            return None

        def ZeroSetVals(system, var, topColum):
            arr = np.copy(system._arr).astype("float64")
            toChange = arr [topColum+1:,:]
            # the actuall calculation according to R3
            toChange -= (np.ones((arr.shape[1], toChange.shape[0])) * arr[topColum].reshape(arr.shape[1], 1) * (toChange[:, var])).T / arr[topColum, var]
            return arr

        def setPivotTo1(system):
            "set the pivo Elements of a RowEdulants system to 1"
            x, y = 0, 0
            while x < system._arr.shape[1]-1 and y < system._arr.shape[0]:
                if x not in system.freeVariables:
                    system._arr[y] /= system._arr[y, x]
                    if len(system._arr[:y]) != 0:
                        system._arr[:y] -= system._arr[y] * system._arr[:y,x].reshape(y, 1)
                    y+=1
                x+=1
#depricated
        def setElementsAbovePivosTo0(system):
            warnings.warn(DeprecationWarning("depricated Function (not needed(ops moved to setPivotTo1))"))
            x, y = 0, 0
            while x < system._arr.shape[1]-1 and y < system._arr.shape[0]:
                if x not in system.freeVariables:
                    if len(system._arr[:y]) != 0:
                        system._arr[:y] -= system._arr[y] * system._arr[:y,x].reshape(y, 1)
                    y+=1
                x+=1


class linearEquasionSystem:
    def __init__(self, *val, acc=10):
        self.sublcassInit(val, acc)
        
    def sublcassInit(self, val, acc = 10):
        # used for printout rounding donst affect calculations
        self.acc = acc
        # if input is a np array just save it
        if isinstance(val[0], linearEquasionSystem):
            self.acc = val[0].acc
            val = val[0]._arr, 0
        if isinstance(val[0], np.ndarray):
            self._arr = val[0]
            return
        #convert val to np array
        self._arr = np.array(val)
        # if its not a valid system raise error
        if len(self._arr.shape) != 2:
            raise InvalidSystem(f"could not calculate system from input {val}")

    def __str__(self):
        out = ""
        #iterate over eqasions for line by line printout
        for equasion in self._arr:
            isEmpty = True
            # add each value to printout
            for idx, val in enumerate(equasion[:-1]):
                # igrnore o valued variables
                if round(val, self.acc) != 0:
                    # add the sign if its not the first
                    if not isEmpty: out += (" + " if val>0 else " - ")
                    # add a - if its the first but negative
                    elif val<0: out +=('-')
                    # get variable index
                    # add variable to printout
                    if round(abs(val), self.acc) != 1:
                        out += (f"{round(abs(val), self.acc)} X{linearEquasionSystem._getPrettyIndex(idx)}")
                    else:
                        out += (f"X{linearEquasionSystem._getPrettyIndex(idx)}")
                    isEmpty = False
            #if no val in printout add a zero
            if isEmpty:
                out += ("0")
            # add the = part
            out += (f" \u2245 {equasion[-1]}\n")
        return out[:-1]

    def copy(self):
        "coppy the system"
        return linearEquasionSystem(np.copy(self._arr), acc = self.acc)
#depricated
    def __rowEdulents__(self):
        return rowEdulants(self)
    
    def getRowEdulants(self):
        """wandelt system in zeilenstufenform um"""
        # copy sys and get the current turning value position (x, y)
        
        new_sys = rowEdulants(self.copy(), _convert = False, acc = self.acc)
        freeVars = []
        y = 0
        x = 0
        # build stairs untill done aka hit a rim of the Matrix
        while x < new_sys._arr.shape[1]-1 and y < new_sys._arr.shape[0]:
            #get non zeros
            scanedColumData = gausean.scanColumb(new_sys, x)
            #if all zeros make Free Variable and move on
            if scanedColumData is None or not len(np.where(scanedColumData>=y)[0]):
                freeVars.append(x);x+=1;continue
        #else get any non zero koeficient below or on y
            nonZero_loc = scanedColumData[np.where(scanedColumData>=y)[0][0]]
            # if ist all zeros move on
##            print(f"at loc{x, y} the non zeros where {nonZero_loc} while out was {gausean.scanColumb(new_sys, x)}")
##            print(new_sys._arr)
            # so that _arr[y,x] != 0 aka swap equasions
            if y != nonZero_loc:
                new_sys._arr = gausean.swapEquasions(new_sys, y, nonZero_loc)
            # set every in the colum x under y to 0
            new_sys._arr = gausean.ZeroSetVals(new_sys, x, y); x+=1; y+=1
        # add last values to freeVars
        while x < new_sys._arr.shape[1]-1:
            freeVars.append(x)
            x+=1
        return new_sys, freeVars

    def test(self, *vals):
        "test a solution"
        #calculate solution ov every equasion with example values
        inVars = np.array(vals)
        reses = np.sum(self._arr[:, :-1] * inVars, axis=1)
        return reses
    
    def _getPrettyIndex(var):
        "get subscript index"
        #print indexes as subscript
        strIdx = ""
        for i in str(var+1):strIdx += str(chr(0x2080 + (int(i))))
        return strIdx

    def _getPrettyPower(var):
        "get superscript chars (broken)"
        #ptettely print out powers as superscript
        return jpe.utils.unicode.unicode.superscript(str(var))
        def getPower(i):
            if i == 2 or i == 3:
                return chr(0x1071)
            return chr(0x2070+ (int(i)-1))
        strIdx = ""
        for i in str(var+1):strIdx += str(getPower(i))
        return strIdx

    def getMatrix(self, acc=None):
        "returns the extended coeffizient matrix of the system"
        # use stand acc
        if acc is None:
            acc = self.acc
        return np.round_(self._arr, acc)
        


class rowEdulants(linearEquasionSystem):
    def __init__(self,*val, acc = 10, _convert=True):
        #state that sys not in refiend form
        self.isRefined = False
        #init superclass
        linearEquasionSystem.sublcassInit(self,val, acc = acc)
        #set printout accuracy
        self.acc = acc
        #this is needed becouse the calculation of the row etdulants uses this class as a storage so we would get into inf recoursions
        if _convert:
            #convert to rowEdulants
            SystemInRowEdulants, self.freeVariables = self.getRowEdulants()
            self._arr = SystemInRowEdulants._arr
        else:
            # keep system du to recursion
            self.freeVariables = None

    def copy(self):
        "copy sys"
        return rowEdulants(np.copy(self._arr), acc = self.acc, _convert = False)

#depricated
    def _sort(self):
        "sort the system because the row Edulants building functin (getRowEdulants in LinearEquasionSystem) will not return the rowEtulants in the right order"   
        warnings.warn(DeprecationWarning("depricated not needed"))
        warnings.warn(RuntimeWarning("call unneaded if it is its a bug"))
        y = 0
        x = 0
        # run stairs untill done aka hit a rim of the Matrix
        while x < self._arr.shape[1]-1 and y < self._arr.shape[0]:
            #get non zeros
            nonZero_loc = gausean.scanColumb(self, x)
            if nonZero_loc is None: x+=1; continue
            #if found a solution
            if len(np.where(nonZero_loc>=y)[0]) > 0:
                #swap equasions
                self._arr = gausean.swapEquasions(self, y, nonZero_loc[np.where(nonZero_loc>=y)[0][0]])
                y+=1
            x+=1

    def refine(self):
        "convert the system into refined row etulant form"
        if self.isRefined:
            warnings.warn(jpe.errors.jpeRedundantCall("rowEtulants.refine call redundent, system already refined call unneaded"))
        ##new_sys = rowEdulants(self.copy(), _convert = False)
        # sort the system so its in an actual row Edulants form as the building process can mess stuf up
##        self._sort()
        # set pivo elements to 1 and sets the elemets obove to 0
        gausean.setPivotTo1(self)
        # set elements above pivos to 0
##        gausean.setElementsAbovePivosTo0(self)
        self.isRefined = True
        return self

    def getSolutionFromFreeVals(self, *vals):
        "enter eg free vals under *vals and get the other variables calculated"
        # if system has not jet been refined refine it
        if not self.isRefined:
            warnings.warn(jpe.errors.jpeClassDataChange("call rowEtulants.getSolutionFromFreeVals has refined the system data loss posible"))
            self.refine()
        # get input matrix
        inVals = np.zeros(self._arr.shape[1]-1)
        inVals[np.array(self.freeVariables)] = np.array(vals)
        #calculate diferance
        return self._arr[: , -1] - self.test(inVals)

    def getFreeVarString(self):
        "string of Free Variables"
        #self explanetory
        out = "freeVars are: "
        for var in self.freeVariables:
            out += f" X{linearEquasionSystem._getPrettyIndex(var)},"
        return out[:-1]

    def getMathPrintSolution(self):
        "returns the solution Quantity as i matprintisch form"
        # if system hasn't been refined jet refine it
        if not self.isRefined:
            warnings.warn(jpe.errors.jpeClassDataChange("call RowEtulants.getMathPrintSolution has refined the system data loss posible"))
            self.refine()
        #calculate the linear side thingy
        def getSide(x, y):
            string = str(round(self._arr[y,-1],self.acc))
            for idx in range(self._arr.shape[1]-1):
                if idx != x and self._arr[y, idx] !=0: string += f" {'-' if self._arr[y, idx]>0 else '+'} {round(abs(self._arr[y,idx]), self.acc)} X{linearEquasionSystem._getPrettyIndex(idx)}"
            return string
        #put Quantyty togather
        out = "{("
        x, y = 0, 0
        while x < self._arr.shape[1]-1:
            #not free add it as a func of the free ones
            if not x in self.freeVariables:
                out += getSide(x, y) + ", "; y+=1
            #else just add it
            else:
                out += f"X{linearEquasionSystem._getPrettyIndex(x)}, "
            x+=1
        # do some cleaning ad a the vec room
        out = out[:-2]
        return out + f")\u03B5R{linearEquasionSystem._getPrettyPower(self._arr.shape[1]-1)}"+"}"
    

# error raised when system is not valid
class InvalidSystem(Exception):
    "raised when an invalid system is passed"
    pass

class _utils:
        def swapEquasions(arr, idxA, idxB):
                "swaps the positions of 2 equasions aka 1st guasean operator"
                temp = arr[idxA]
                arr[idxA] = arr[idxB]
                arr[idxB] = temp
        
        def scanColumb(arr, x, y):
                "scan colum for non hiest non zero above y"
                for idx in range(y, len(arr)):
                        if arr[idx][x] != 0:
                                return idx
                return None

        def _setValsTo0(arr, x, y):
                "set all values below y on x to 0"
                currantVal = arr[y][x]
                subEquasion = arr[y]
                # go over every equasion
                for yidx in range(y+1, len(arr)):
                        equasion = arr[yidx]
                        curratEquasionVal = arr[yidx][x]
                        # substect y quasion from yidx equasion so that everything beloy x is 0
                        for xidx in range(len(arr[0])):
                                arr[yidx][xidx] -= subEquasion[xidx] * curratEquasionVal/currantVal


        def refine(system):
                x, y = 0, 0
                while x < len(system._arr[1])-1 and y < len(system._arr):
                        if x not in system.freeVariables:
                                for xidx in reversed(range(len(system._arr[y]))):
                                    # set value to x, y to 1
                                    system._arr[y][xidx] /= system._arr[y][x]
                                
                                #sett every value above y to 0    
                                if y != 0:
                                    for equasionIdx in range(0, y):
                                        for elementIdx in reversed(range(len(system._arr[0]))):
                                            system._arr[equasionIdx][elementIdx] -= system._arr[y][elementIdx] * system._arr[equasionIdx][x]
                                y+=1
                        x+=1

class linearEquasionSystemJfloat:
    def __init__(self, *vals, acc=10):
        "a container for linear equasion systems using jfloats for extream acc"
        self._init(vals)
        self.acc=acc
                
    def _init(self, vals):
                "subinit"
                # is system input copy system
                if isinstance(vals[0], linearEquasionSystemJfloat): self._arr = jpe.utils.copy.copyLists.copy(vals[0]._arr)
                # else generate jflowt sysstem
                elif isinstance(vals[0][0], list):
                    self._arr = linearEquasionSystemJfloat._init_arr(vals[0])
                else:self._arr = linearEquasionSystemJfloat._init_arr(vals)

    def __str__(self):
            "temp Function aka convet to string"
            return self.getMatrix()

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key)>2:
                raise IndexError(f"key is not a valid index for linearEquason system do many dimentions")
            if key[0] >= len(self._arr) or key[1] >= len(self._arr[0]) :
                raise IndexError(f"key is not a valid index for linearEquason system value out of bounds")
            return self._arr[key[0]][key[1]]
        return self._arr[key]


    def __getstate__(self):
        raise jpe.errors.jpeDevFuncWarning("this function is still in development sry i u are a dev plz get to work")

            
    def _init_arr(vals):
                "initiate jfloat matrix it crates a 2d arrac containing the extended coefficient matrix containing jfloat objects see jpe.jfloat for more detail"
                
                size = len(vals[0])
                arr = []
                for sys in vals:
                        arr.append([])
                        if len(sys) != size: raise jpeInvalidSystemError("input dims dont match")

                        for koeffizeint in sys:
                                arr[-1].append(jfloatMod.Jfloat(koeffizeint))
                return arr

    def __copy__(self):
        return linearEquasionSystemJfloat(jpe.utils.copy.copyLists.copy(self._arr))

    def test(self, *args):
        "retusn eg solution for input variables"
        reses = []
        # iterate over every equesion
        for equasion in self._arr:
            # add 0 t element -1 idx
            reses.append(0)
            #iterate over every value and add ti to the solution
            for element, value in zip(equasion[:-1], args):
                reses[-1]+=element* value
        return reses


    def getMatrix(self):
        "get a matrix pintout"
        outStirng = ""
        for eqasn in self._arr:
                outStirng += str(eqasn) + "\n"
        return outStirng[:-1]
        
        

class rowEtulantSystemJfloat(linearEquasionSystemJfloat):
        def __init__(self, *vals, acc=10):
                " container conainting a linear equasion system in row etulant form aswll as the conversion algorythem"
                # init superclass
                linearEquasionSystemJfloat._init(self, vals)
                # convert system into row Etulant form
                self._arr, self.freeVariables = rowEtulantSystemJfloat._generateRowEtulants(self)
                # say sys is not refined
                self.isRefined = False
                # depricated acc variable for printout maybe il find a use
                self.acc=acc

        def _generateRowEtulants(system):
                #copy the sys to prevent messups
                arr = jpe.utils.copy.copyLists.copy(system._arr)
                #init scan vars
                x, y = 0,0
                #conains the free vars so we can keept tack of them as i dont move them to avoid the hassel of correcting the bijunction
                freeVars= []
                #run algorythem untill we hit the rim of the koefficient matrix
                while x < len(arr[1])-1 and y < len(arr):
                        #look for higerst non zero koeffeicient under or on y
                        scaned = _utils.scanColumb(arr, x, y)
                        # if none found its free and and we proceede with next run
                        if scaned is None:
                                freeVars.append(x); x+=1; continue
                        #swape equasons so arr[y,x] != 0
                        _utils.swapEquasions(arr, scaned, y)
                        # third gausean operator on all values under y to set arr[y:,x] = zero array
                        _utils._setValsTo0(arr, x,y )
                        x+=1; y+=1

                #after hitting bottom set all vars to be frees
                while x < len(arr[1])-1:
                        freeVars.append(x);x+=1

                return arr, freeVars

        def __copy__(self):
            return rowEtulantSystemJfloat(jpe.utils.copy.copyLists.copy(self._arr))

        def refine(self):
            """refine the system"""
            _utils.refine(self)
            self.isRefined = True
            return self

        def _refine(self):
            """refine and complaine"""
            warnings.warn(jpe.errors.jpeClassDataChange("call RowEtulants.getMathPrintSolution has refined the system data loss posible\n"))
            return self.refine()

        def _hassolution(self):
            """retuns bool value for is a solution exists"""
            # if any equasion is 0+0+..+0 != 0 ist is Fasle
            for equasion in self._arr:
                isZero=True
                for element in equasion[:-1]:
                    if element != 0:
                        isZero=False
                        break
                if equasion[-1] != 0 and isZero:
                    return False
            return True

        def getSolutionFromFreeVals(self,*vals):
            "gets a solution eg from free variable input"
            # crates list for solution
            reses = []
            #go throw each equasion and get the variable it defines
            for equasion in self._arr:
                # add a new solution
                reses.append(equasion[-1])
                # iterate over every free value and calculate the solution
                for value, idx in zip(vals,self.freeVariables ):
                    reses[-1]-= equasion[idx] * value
            return reses

        def getFreeVarString(self):
            "returns the free variables as a string"
            out = "free vars: "
            for idx in self.freeVariables:
                out += f"X{ jpe.utils.unicode.unicode.prettyIndex(idx)}"
            return out

        def getMathPrintSolution(self):
            # if the system is not in refied form we have to do that
            if not self.isRefined:
                    self._refine()
            # if it dosnt have a solution we cant print it and complain
            if not self._hassolution():
                raise ValueError(f"linear Equasion system has no valis solution")

            
            def getSide(x, y):
                """ put all the operants togather"""
                string = str(self._arr[y][-1])
                for idx in range(len(self._arr[0])-1):
                    if idx != x and self._arr[y][idx] !=0: string += f" {'-' if self._arr[y][idx]>0 else '+'} {abs(self._arr[y][idx])} X{jpe.utils.unicode.unicode.prettyIndex(idx)}"
                return string

            output = "{("
            x, y = 0, 0
            #go throw all variables
            while x < len(self._arr[0])-1:
                # if free ad xidx to res set
                if x in self.freeVariables:
                    output += f"X{jpe.utils.unicode.unicode.prettyIndex(x)}, "
                #add the computation to set
                else:
                    output += getSide(x, y) + ", "; y+=1
                x+=1
            return output[:-2]+")}"
        
            
                
                                
                
class jpeInvalidSystemError(Exception):pass

if __name__ == "__main__":
    js = linearEquasionSystemJfloat([1,2,1,3], [4,5,0,6])
    jr = rowEtulantSystemJfloat(js)
    print(jr)
    print(jr.getMathprinsSolution())
    #eingabe eines algemeine gleichungsystems als erweiterte koeffizientenmatrixs
    s = linearEquasionSystem([26,5, 10],
                             [4,5, 11],
                             [7,8,  12])
    print("input Sys matrix")
    print(s.getMatrix(1))
    
    r = rowEdulants(s, acc=10)
    print("row etulant matrix")
    print(r.getMatrix(1))
    r.refine()
    print("refined matrix")
    print(r.getMatrix(1))
    #print(r.getSolutionFromFreeVals(34))
    #print(s.test(1, -324.55844156, 25.31168831, -21.68831169, 10))
    print(r.getFreeVarString())
    print(r.getMathPrintSolution())
    
