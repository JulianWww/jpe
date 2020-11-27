from jpe.Jfloat import Jfloat as jfloat
import warnings
import jpe.errors.warnings
import jpe.utils.unicode.unicode
import copy

class _utils:
        def swapEquasions(arr, idxA, idxB):
                "swaps the positions of 2 equasions aka 1st guasean operator"
                temp = arr[idxA]
                arr[idxA] = arr[idxB]
                arr[idxB] = temp

        def scanColumb(arr, x, y):
                for idx in range(y, len(arr)):
                        if arr[idx][x] != 0:
                                return idx
                return None

        def _setValsTo0(arr, x, y):
                currantVal = arr[y][x]
                subEquasion = arr[y]
                for yidx in range(y+1, len(arr)):
                        equasion = arr[yidx]
                        curratEquasionVal = arr[yidx][x]
                        for xidx in range(len(arr[0])):
                                arr[yidx][xidx] -= subEquasion[xidx] * curratEquasionVal/currantVal


        def refine(system):
                x, y = 0, 0
                while x < len(system._arr[1])-1 and y < len(system._arr):
                        if x not in system.freeVariables:
                                for xidx in range(len(system._arr[y])):
                                    system._arr[y][xidx] /= system._arr[y][x]
                                    
                                if y != 0:
                                    for equasionIdx in range(0, y):
                                        for elementIdx in range(len(system._arr[0])):
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
                if isinstance(vals[0], linearEquasionSystemJfloat): self._arr = copy.copy(vals[0]._arr)
                # else generate jflowt sysstem
                elif isinstance(vals[0][0], list):
                    self._arr = linearEquasionSystemJfloat._init_arr(vals[0])
                else:self._arr = linearEquasionSystemJfloat._init_arr(vals)

    def __str__(self):
                "temp Function aka convet to string"
                warnings.warn(jpe.errors.warnings.jpeDevFuncWarning("this function is still in development sry i u are a dev plz get to work"))
                outStirng = ""
                for eqasn in self._arr:
                        outStirng += str(eqasn) + "\n"
                return outStirng[:-1]

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key)>2:
                raise IndexError(f"key is not a valid index for linearEquason system do many dimentions")
            if key[0] >= len(self._arr) or key[1] >= len(self._arr[0]) :
                raise IndexError(f"key is not a valid index for linearEquason system value out of bounds")
            return self_arr[key[0]][key[1]]
        return self._arr[key]


    def __getstate__(self):
        raise jpe.errors.warnings.jpeDevFuncWarning("this function is still in development sry i u are a dev plz get to work")

    
    def _init_arr(vals):
                "initiate jfloat matrix it crates a 2d arrac containing the extended coefficient matrix containing jfloat objects see jpe.jfloat for more detail"
                
                size = len(vals[0])
                arr = []
                for sys in vals:
                        arr.append([])
                        if len(sys) != size: raise jpeInvalidSystemError("input dims dont match")

                        for koeffizeint in sys:
                                arr[-1].append(jfloat(koeffizeint))
                return arr

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
                arr = copy.copy(system._arr)
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

        def refine(self):
            """refine the system"""
            _utils.refine(self)
            return self

        def _refine(self):
            """refine and complaine"""
            warnings.warn(jpe.errors.warnings.jpeClassDataChange("call RowEtulants.getMathPrintSolution has refined the system data loss posible\n"))
            return self.refine()

        def _hassolution(self):
            """retuns bool value for is a solution exists"""
            # if any equasion is 0+0+..+0 != 0 ist is Fasle
            for equasion in self._arr:
                NonZero=False
                for element in equasion[:-1]:
                    if element != 0:
                        nonZero=True
                        break
                if equasion[-1] == 0 and not NonZero:
                    return False
            return True

        def getMathprinsSolution(self):
            # if the system is not in refied form we have to do that
            if not self.isRefined:
                    self._refine()
            # if it dosnt have a solution we cant print it and complain
            if not self._hassolution():
                raise ValueError(f"linear Equasion system has no valis solution")

            
            def getSide(x, y):
                """ put all the operants togather"""
                string = str(self._arr[y][-1])
                for idx in range(len(self._arr)):
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

s = linearEquasionSystemJfloat([1,2,1,3], [4,5,0,6])
r = rowEtulantSystemJfloat(s).refine()
print(r.getMathprinsSolution())
