import random
import uuid
from pyelasticsearch import ElasticSearch

es = ElasticSearch('http://localhost:9202/')

def readPlan(planName):
    #This function read de plan
    #return a array with all posible door points
    archivo = open(planName)
    #save positions and objects
    positions = {}
    linea = archivo.readline()
    while linea != '':
        ind1 = linea.index(' ')
        posx = linea[:ind1]
        ind2 = linea.index(' ',ind1+1)
        posy = linea[ind1+1:ind2]
        ind3 = linea.index('\n',ind1+1)
        value = linea[ind2+1:ind3]
        positions[posx,posy] = value

        linea = archivo.readline()

    #save points where can door ubicated
    canDoor = []
    for px,py in positions:
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
    #print canDoor #to test readPlan function
    return canDoor

def generatePoblation(n,universe):
    #This function generate a poblation with n random individuals of five doors
    #save individuals in ElasticSearch
    poblation = {}
    rangeRandom = len(universe)
    for i in range(n):
        poblation[i] = {'adn':[]}
        for j in range(5):
            poblation[i]['adn'].append(universe[random.randint(0, rangeRandom-1)])
        try:
            responseElastic = es.index('ia',
                                'individual',
                                poblation[i])
        except Exception as e:
            print e
    #print poblation #to test generatePoblation
    return poblation

def simulate():
    #simulate all individuals in poblation pobl
    #agregate time for each individual in pobl
    #query = {'sort':[{'art_date':{'order':'asc'}}],'query':{'match_all':{}},}
    query = {'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        allIndividuals = es.search(query,size=totalInd['count'], index='ia')
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    #print allIndividuals
    data = allIndividuals['hits']['hits']
    for key in data:
        print key['_source']['adn']
        #print i
        #print pobl[i]
        #por ahora esto tiempos son aleatorios
        #Quienes se quieren encargar de mezclar python con netlogo?
        #se puede hacer por medio de archivos
        #tambien existe un codigo java que los une directamente
        #key['_source']['time'] = random.randint(10,100)

def evaluate(pobl):
    #evaluate result of simulate
    #asigned points a each individual depend lower
    bestTime = 999999999999999999999999999999
    worstTime = 0
    for i in pobl:
        if pobl[i]['time'] <= bestTime:
            bestTime = pobl[i]['time']
        if pobl[i]['time'] >= worstTime:
            worstTime = pobl[i]['time']
    #asigned point depend lower individual
    for i in pobl:
        pobl[i]['points'] = 1 - pobl[i]['time']/float(worstTime)

def pair(pobl):
    #this function pair poblation pobl
    return pobl
    #return a object with the news individuals

def selectBest(pobl,npar):
    #select npar best points individuals
    for i in pobl:
        print i
    #return npar best individuals


#main AlgoritmoEvolutivo
class AlgoritmoEvolutivo():
    #all points where can door ubicated
    allCanDoor = readPlan('plan.plan')
    #generate n poblations of combinated five random points with doors
    #poblation = generatePoblation(100, allCanDoor)
    #evaluate all individuals in poblation
    simulate()
    #evaluate results
    #evaluate(poblation)
    #selectBest(poblation,10)
    #pair poblation
    #childrens = pair(poblation)
    #print poblation
    query = {'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        allIndividuals = es.search(query,size=totalInd['count'], index='ia')
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    print allIndividuals





if __name__ == "__main__":
    app = AlgoritmoEvolutivo()

