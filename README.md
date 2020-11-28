
jpe

jpe is a libray for python 3.6 contining utils functons that make my life easyser if u want to use them go ahead.
jfloat()

    jfloats are a datatype for python for rational number used for other code mostly

crono.timer(acc)

    acc ist the rounding fore printout timer will start emediatly
    start()
        start the timer
    lap(msg)/endLap(msg)
        adds a lap to the timer with msg msg
    clear()
        remove all laps from memory
    print(timer)
        printsout the timer result

math.linalg.vector(*vars)

    vector container
    str(vector)
        converts to vector
    vec+vec2
        adds to vector togather
    vec-vec2
        substact 2 vecor from each others
    vec * int or vec*float
        scale vector
    vec/int or vec/float
        scale veector by 1/int bzw 1/float
    abs(vec)
        |vec| or absolute value of vector
    vec.unit()
        unit vector in same direction
    vec.dot(vec2)
        vector dot product
    vec.cross(vec2)
        vector cross product
    vec.angle(vec2)
        angle betwean vectors
    vec.det()
        determinant of the vector
    vec[key]
        vector index on dimention key

math.linalg.linearEquasionSystem(*val, acc=10)

    liear equasion system container
    print(sys)
        equasion system render function
    copy():
        copys the system
    getRowEtulants()
        returns a tupple containing the linear equasion system in row etulant form as well as a list fo free variables
        #test(*vals)
        returns the results of each equasion based on the variable vector
    getMatrix(self, acc=None)
    -returns the sysems extendend coeffiecent matrix rounded to acc post comma digits or system.acc if None

maht.linalg.rowEtulants(*vals, acc=10)

    subclass of math.linalg.linearEquasionSystem
    and is the container for linear equasion system in row etulant form
    copy()
        crates copy of system
    refine():
        converts sytem into refined row etulant form
    getSolutionFromFreeVals(*vals)
        calculates eg solution by stetting the free vals to what is specifeid py *vals
    getFreeVarString()
        user output for free variables not computer sutable for computer output see maht.linalg.rowEtulants.freeVariables
    freeVariables
        list of free variable indexes
    getMathPrintSolution():
        return user Friedly solution quantity according.

math.linalg.linearEquasionSystemJfloat

    liear equasion system container
    sys[x]/sys[x,y]
        index the sytems matrix
    print(sys)
        equasion system render function
    copy():
        copys the system
    getRowEtulants()
        returns a tupple containing the linear equasion system in row etulant form as well as a list fo free variables
        #test(*vals)
        returns the results of each equasion based on the variable vector
    getMatrix(self, acc=None)
    -returns the sysems extendend coeffiecent matrix rounded to acc post comma digits or system.acc if None

math.linalg.rowEtulantSystemJfloat(*vals)

    subclass of math.linalg.linearEquasionSystem
    and is the container for linear equasion system in row etulant form
    copy()
        crates copy of system
    refine():
        converts sytem into refined row etulant form
    getSolutionFromFreeVals(*vals)
        calculates eg solution by stetting the free vals to what is specifeid py *vals
    getFreeVarString()
        user output for free variables not computer sutable for computer output see maht.linalg.rowEtulants.freeVariables
    freeVariables
        list of free variable indexes
    getMathPrintSolution():
        return user Friedly solution quantity according.

