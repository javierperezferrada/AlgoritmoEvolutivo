import random
import uuid
from pyelasticsearch import ElasticSearch
import os
import time
import json

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
        poblation = {'adn':[],'simulated':False}
        for j in range(5):
            poblation['adn'].append(universe[random.randint(0, rangeRandom-1)])
        try:
            responseElastic = es.index('ia',
                                'individual',
                                poblation)
        except Exception as e:
            print e
        print "individuo %s creado" % i

def simulate():
    print "Esperando"
    time.sleep(5)
    #simulate all individuals in poblation pobl
    #agregate time for each individual in pobl
    #query = {'sort':[{'art_date':{'order':'asc'}}],'query':{'match_all':{}},}
    query = {'query':{'bool':{
                'filter':[
                {'term':{'simulated':False}}
                ]
    }},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        allIndividuals = es.search(query, size=totalInd['count'], index='ia')
        print "no simulados: "+str(totalInd['count'])
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    #print allIndividuals
    data = allIndividuals['hits']['hits']
    #print data
    i=0
    for key in data:
        print i
        #print key
        #print len(key['_source']['adn'])
        #CREAR ARCHIVO Y METER key['_source']['adn'][cesar]
        combi_puertas = open("doors.plan", "w+")
        for cesar in range(len(key['_source']['adn'])):
            #print key['_source']['adn'][cesar]
            combi_puertas.write(key['_source']['adn'][cesar]+" \n")
            #combi_puertas.write("\n")
        combi_puertas.close()
        time.sleep(1)
        os.system("java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model escape4.nlogo --experiment simulation")
        segundos = open("seconds.output", "r")
        for linea in segundos:
            linea = linea.rstrip("\n")
            print "segundos: %s" % (linea)
            queryDoc = {'time':int(linea),'simulated':True}

        try:
            es.update('ia','individual',key['_id'],doc=queryDoc)
        except Exception as e:
            print e
        i+=1

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
    query = {'sort':[{'time':{'order':'desc'}}],'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        print "total:"+str(totalInd)
        bestIndividuals = es.search(query,size=nPar, index='ia')
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    #print bestIndividuals
    data = bestIndividuals['hits']['hits']
    i=0
    while i<nPar:
        print i
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
        newIndividual = {'adn':new,'simulated':False}
        try:
            responseElastic = es.index('ia',
                                'individual',
                                newIndividual)
            print "hijo agregado"
        except Exception as e:
            print e
        i+=2

    simulate()



def summary():
    #evaluate result of simulate
    total = {'query':{'match_all':{}},}
    query = {'aggs': { 'avg_time' : {'avg': { 'field': 'time'}}}}
    query2 = {'aggs': { 'min_time' : {'min': { 'field': 'time'}}}}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(total,index='ia')
        average = es.search(query, index='ia')
        minimum = es.search(query2, index='ia')
        print average['aggregations']['avg_time']['value']
        print minimum['aggregations']['min_time']['value']
        #f = open("grafico.csv", "a")
        #f.write(str(totalInd['count'])+","+str(average['aggregations']['avg_time']['value'])+","+str(minimum['aggregations']['min_time']['value'])+","+minimumComb['hits']['hits'][len(minimumComb['hits']['hits'])-1]['_source']['adn']+"\n")
        query3 = {"query" : {"constant_score" : { "filter" : {"term" : { "time" : minimum['aggregations']['min_time']['value']}}}}}
        minimumComb = es.search(query3, index='ia')
        print minimumComb['hits']['hits'][len(minimumComb['hits']['hits'])-1]['_source']['adn'] #se imprime la ultima combinacion de puertas de menor tiempo
        f = open("grafico.csv", "a")
        f.write(str(totalInd['count'])+","+str(average['aggregations']['avg_time']['value'])+","+str(minimum['aggregations']['min_time']['value'])+","+str(minimumComb['hits']['hits'][len(minimumComb['hits']['hits'])-1]['_source']['adn'])+"\n")
        
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    
    newPoblationResult = {'minimum':minimum['aggregations']['min_time']['value'],'average':average['aggregations']['avg_time']['value'],'poblation':totalInd['count']}
    try:
        es.index('results',
                'results',
                newPoblationResult)
    except Exception as e:
        print e

def mutation(nPar,allCanDoor):
    print len(allCanDoor)
    #evaluate result of simulate
    query = {'sort':[{'time':{'order':'desc'}}],'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        print "total:"+str(totalInd)
        bestIndividuals = es.search(query,size=nPar, index='ia')
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    #print bestIndividuals
    data = bestIndividuals['hits']['hits']
    #print data
    aux2 = [-1,1]
    i=0
    while i<nPar:
        #print i
        ind1 = bestIndividuals['hits']['hits'][i]['_source']['adn']
        ind2 = bestIndividuals['hits']['hits'][i+1]['_source']['adn']
        #print ind1
        #print ind2
        new = []
        for j in range(5):
            rand = random.randint(0,10)
            if rand<=5:
                mut = random.choice(aux2) #se suma o resta un valor a una coordenada aleatoriamente
                esp = ind1[j].index(' ')
                x=int(ind1[j][0:esp])
                #print x                
                y=int(ind1[j][esp+1:len(ind1[j])])
                #print y
                if allCanDoor.count(str(x+mut)+" "+str(y)) > 0: 
                    print str(x+mut)+" "+str(y)
                    new.append(str(x+mut)+" "+str(y)) #si le sumamos uno a X y es puerta, se crea el hijo
                if allCanDoor.count(str(x)+" "+str(y+mut)) > 0: 
                    print str(x)+" "+str(y+mut)
                    new.append(str(x)+" "+str(y+mut))#si le sumamos uno a Y y es puerta, se crea el hijo
                
            else:
                mut = random.choice(aux2)
                esp = ind2[j].index(' ')
                x=int(ind2[j][0:esp])
                #print x                
                y=int(ind2[j][esp+1:len(ind2[j])])
                #print y
                if allCanDoor.count(str(x+mut)+" "+str(y)) > 0:
                    print str(x+mut)+" "+str(y)
                    new.append(str(x+mut)+" "+str(y))
                if allCanDoor.count(str(x)+" "+str(y+mut)) > 0:
                    print str(x)+" "+str(y+mut)
                    new.append(str(x)+" "+str(y+mut))
                #print allCanDoor.count(ind2[j])
        print new
        newIndividual = {'adn':new,'simulated':False}
        try:
            responseElastic = es.index('ia',
                                'individual',
                                newIndividual)
            print "hijo agregado"
        except Exception as e:
            print e
        i+=2
    simulate()
    summary()


#main AlgoritmoEvolutivo
class AlgoritmoEvolutivo():

    aux=0
    query = {'query':{'match_all':{}},}
    try:
        #request all articles to ElasticSearch
        totalInd = es.count(query,index='ia')
        allIndividuals = es.search(query,size=totalInd['count'], index='ia')
        print totalInd
        aux=totalInd['count']
    except Exception as e:
        #if fail conection to ElasticSearch
        print e
    allCanDoor = readPlan('plan.plan')
    if aux<500: #se crea poblacion de padres e hijos
        i=0
        while aux<500:
            #all points where can door ubicated
            #allCanDoor = readPlan('plan.plan')
            #generate n poblations of combinated five random points with doors
            generatePoblation(20, allCanDoor)
            #evaluate all individuals in poblation
            simulate()
            #evaluate results
            selection(10)
            summary()
            '''query = {'query':{'bool':{
                        'filter':[
                        {'term':{'simulated':False}}
                        ]
            }},}'''
            query = {'query':{'match_all':{}},}
            try:
                #request all articles to ElasticSearch
                totalInd = es.count(query,index='ia')
                print totalInd['count']
                aux=totalInd['count']
                #allIndividuals = es.search(query,size=totalInd['count'], index='ia')
            except Exception as e:
                #if fail conection to ElasticSearch
                print e
            #print allIndividuals
            #print allIndividuals
            i+=1
    else: #se crean hijos y se mutan
        #mutaciones
        while aux<2125:
            mutation(50,allCanDoor)
            query = {'query':{'match_all':{}},}
            try:
                #request all articles to ElasticSearch
                totalInd = es.count(query,index='ia')
                print totalInd['count']
                aux=totalInd['count']
                #allIndividuals = es.search(query,size=totalInd['count'], index='ia')
            except Exception as e:
                #if fail conection to ElasticSearch
                print e
    #f = open("10peores-apareamientoAleatorio.json", "a")
    #f.write(json.dumps(allIndividuals))
    #f.close()





if __name__ == "__main__":
    app = AlgoritmoEvolutivo()