import random
import uuid
from pyelasticsearch import ElasticSearch
import os

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
    rangeRandom = len(universe)
    for i in range(n):
        poblation = {'adn':[],'simulated':'not'}
        for j in range(5):
            poblation['adn'].append(universe[random.randint(0, rangeRandom-1)])
        try:
            responseElastic = es.index('ia',
                                'individual',
                                poblation)
        except Exception as e:
            print e

def simulate():
    #simulate all individuals in poblation pobl
    #agregate time for each individual in pobl
    #query = {'sort':[{'art_date':{'order':'asc'}}],'query':{'match_all':{}},}
    query = {'query':{'bool':{
                'filter':[
                {'term':{'simulated':'not'}}
                ]
    }},}
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
        #print key
        #print len(key['_source']['adn'])
        #CREAR ARCHIVO Y METER key['_source']['adn'][cesar]
        combi_puertas = open("doors.plan", "w+")
        for cesar in range(len(key['_source']['adn'])):
            #print key['_source']['adn'][cesar]
            combi_puertas.write(key['_source']['adn'][cesar]+" \n")
            #combi_puertas.write("\n")
        os.system("java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model escape4.nlogo --experiment simulation")
        segundos = open("seconds.output", "r")
        for linea in segundos:
            linea = linea.rstrip("\n")
            print "segundos: %s" % (linea)
            queryDoc = {'time':int(linea),'simulated':'yes'}

        try:
            es.update('ia','individual',key['_id'],doc=queryDoc)
        except Exception as e:
            print e
        #EN VEZ DE IMPRIMIR, CREAR ARCHIVO 
        #
        #
        #
        #
        #
        #
        #print i
        #print pobl[i]
        #por ahora esto tiempos son aleatorios
        #Quienes se quieren encargar de mezclar python con netlogo?
        #se puede hacer por medio de archivos
        #tambien existe un codigo java que los une directamente
        #key['_source']['time'] = random.randint(10,100)

def selection(nPar):
    #evaluate result of simulate
    query = {'sort':[{'time':{'order':'asc'}}],'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        bestIndividuals = es.search(query,size=nPar, index='ia')
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    #print bestIndividuals
    data = bestIndividuals['hits']['hits']
    for i in range(nPar/2):
        ind1 = bestIndividuals['hits']['hits'][i]['_source']['adn']
        ind2 = bestIndividuals['hits']['hits'][i+1]['_source']['adn']
        #print ind1
        #print ind2
        new = []
        for j in range(5):
            rand = random.randint(0,10)
            if rand<=5:
                new.append(ind1[j])
            else:
                new.append(ind2[j])
        newIndividual = {'adn':new}
        try:
            responseElastic = es.index('ia',
                                'individual',
                                newIndividual)
        except Exception as e:
            print e
    simulate()

def pair(pobl):
    #this function pair poblation pobl
    return pobl
    #return a object with the news individuals

def selectBest(pobl,npar):
    #select npar best points individuals
    for i in pobl:
        print i
    #return npar best individuals


def summary():
    #evaluate result of simulate
    query = {'aggs': { 'avg_time' : {'avg': { 'field': 'time'}}}}
    query2 = {'aggs': { 'min_time' : {'min': { 'field': 'time'}}}}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        #print totalInd
        average = es.search(query, index='ia')
        minimum = es.search(query2, index='ia')
        print average['aggregations']['avg_time']['value']
        print minimum['aggregations']['min_time']['value']
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    newPoblationResult = {'minimum':minimum['aggregations']['min_time']['value'],'average':average['aggregations']['avg_time']['value']}
    try:
        es.index('ia',
                'results',
                newPoblationResult)
    except Exception as e:
        print e


#main AlgoritmoEvolutivo
class AlgoritmoEvolutivo():
    #all points where can door ubicated
    #allCanDoor = readPlan('plan.plan')
    #generate n poblations of combinated five random points with doors
    #generatePoblation(20, allCanDoor)
    #evaluate all individuals in poblation
    #simulate()
    #evaluate results
    #selection(10)
    #selectBest(poblation,10)
    #pair poblation
    #childrens = pair(poblation)
    #print poblation
    #summary()
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