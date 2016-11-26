class MyApplication():
    #read plan
    archivo = open('plan.plan')
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

    #print positions
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
    print canDoor

if __name__ == "__main__":
    app = MyApplication()
