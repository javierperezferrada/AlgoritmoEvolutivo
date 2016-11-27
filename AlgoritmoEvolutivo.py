import random

def readPlan(planName):
    #This function read de plan
    #return a array with all posible door points
    archivo = open(planName)
    #save positions and objects
    positions = {}
    linea = archivo.readline()
    while linea != '':
        #print linea
        ind1 = linea.index(' ')
        posx = linea[:ind1]
        #print posx
        ind2 = linea.index(' ',ind1+1)
        posy = linea[ind1+1:ind2]
        #print posy
        ind3 = linea.index('\n',ind1+1)
        value = linea[ind2+1:ind3]
        #print value
        positions[posx,posy] = value

        linea = archivo.readline()

    #save points where can door ubicated
    canDoor = []
    for px,py in positions:
        #print 'px'
        #print px
        #print 'py'
        #print py
        #print 'value'
        #print positions[px,py]
        if positions[px,py] == '64':
            #if is wall check around
            arround = [positions[str(int(px)+1),py],positions[px,str(int(py)-1)],
                    positions[str(int(px)-1),py],positions[px,str(int(py)+1)]]
            #print arround
            interior = False
            exterior = False
            for a in arround:
                if a == '0':
                    interior = True
                if a == '2':
                    exterior = True
            if interior == True and exterior == True:
                #can ubicated Door in the point px py
                canDoor.append(px+' '+py)
    #print canDoor #observate to test readPlan function
    return canDoor

def generatePoblation(n,universe):
    #This function generate a poblation with n random individuals of five doors
    #return a object with n individuals
    print 'This function generate a poblation with n random individuals'
    poblation = {}
    rangeRandom = len(universe)
    for i in range(n):
        poblation[i] = []
        for j in range(5):
            poblation[i].append(universe[random.randint(0, rangeRandom)])
    #print poblation to test generatePoblation
    return poblation

#main AlgoritmoEvolutivo
class AlgoritmoEvolutivo():
    #all points where can door ubicated
    allCanDoor = readPlan('plan.plan')
    #generate n poblations of combinated five random points with doors
    poblation = generatePoblation(10, allCanDoor)
    print poblation




if __name__ == "__main__":
    app = AlgoritmoEvolutivo()
