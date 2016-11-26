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
    for px,py in positions:
        print 'px'
        print px
        print 'py'
        print py


if __name__ == "__main__":
    app = MyApplication()
