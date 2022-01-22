import math
from unittest import result
import globals
import queue
import random


dir1Row=[0,-1,-1,-1, 0, 1,1,1]
dir2Col=[1,1,  0,-1,-1,-1,0,1]

def dictMergeSum(dict1, dict2):
    tempdict ={}
    
    #Llenando el dict2 en caso de que sea vacío
    if len(dict2.keys()) == 0:
        for i in dict1.keys():
            dict2[i] = 0
    
    
    for i in dict1.keys():
        tempdict[i] = int(dict1[i])+ int(dict2[i])
        
    return tempdict

def dictMergeSubstract(dict1, dict2):
    tempdict ={}
    
    #Llenando el dict2 en caso de que sea vacío
    if len(dict2.keys()) == 0:
        for i in dict1.keys():
            dict2[i] = 0
    
    for i in dict1.keys():
        tempdict[i] = int(dict1[i])- int(dict2[i])
        
    return tempdict

def dictPromed(dict1, dict2):
    tempdict ={}
    
    
    for i in dict1.keys():
        if (int(dict1[i])+ int(dict2[i]))%2==1:
            tempdict[i] =1+ (int(dict1[i])+ int(dict2[i]))/2
        else:
            tempdict[i] = (int(dict1[i])+ int(dict2[i]))/2
        
    return tempdict

def dieList():
    for item in globals.deadIndividuals:
        if item in globals.worldIndividuals.keys():
            del globals.worldIndividuals[item]
    globals.deadIndividuals=[]

def bornList():
    for item in globals.bornIndividuals:
        globals.worldIndividuals[item[0]]=item[1]
    globals.bornIndividuals=[]

def mapMaker(myMap,matrix):
    i=0
    while i < len(matrix):
        myMap.append([])
        j=0
        while j < len(matrix[i]):
            if matrix[i][j]==globals.voidValue:
                myMap[i].append(globals.voidValue)    
            else:
                myMap[i].append(0)
            j+=1
        i+=1
def sumMatrix(myMap,matrix):
    i=0
    while i < len(matrix):
        j=0
        while j < len(matrix[i]):
            myMap[i][j]+=matrix[i][j]
            j+=1
        i+=1
        
def mulMatrix(matrix,value):
    i=0
    while i < len(matrix):
        j=0
        while j < len(matrix[i]):
            if matrix[i][j]!=globals.voidValue: 
                matrix[i][j]*=value
            j+=1
        i+=1    
    return matrix
            
            
def pathFinder(currentIndividual,mapa):
    
    previusX,previusY=currentIndividual.xMundo,currentIndividual.yMundo
    #mapa para trabajar
    myFixMap=[]    
    #mapa para la matrix de adyacencia
    myMap=[]
    foodMatrix=mapa["Comida"]
    dangerMatrix=mapa["Peligro"]
    mateMatrix=mapa["Pareja"]
    especiesMatrix=mapa["Especie"]
    mapMaker(myMap,mapa["Tile"])
    mapMaker(myFixMap,mapa["Tile"])
    if currentIndividual.naturalDefenseInd["Inteligencia"]>=2:
        sumMatrix(myMap,mulMatrix(foodMatrix,currentIndividual.priorities['hambre']) )
    if currentIndividual.naturalDefenseInd["Inteligencia"]>5:
        sumMatrix(myMap,mulMatrix(dangerMatrix,currentIndividual.priorities['danger']) )
    if currentIndividual.naturalDefenseInd["Inteligencia"]>8:
        sumMatrix(myMap,mulMatrix( mateMatrix,currentIndividual.priorities['mate']))
    if currentIndividual.naturalDefenseInd["Inteligencia"]>11:
        sumMatrix(myMap,mulMatrix(especiesMatrix,currentIndividual.priorities["imanEspecie"]))
        
    destination=bestLocationFinder(myMap)
    adyacencyList=adyacencyMatrizBuilder(myMap)
    
    myPosition=(int((len(foodMatrix)-1)/2),int((len(foodMatrix)-1)/2))
    
    if destination==None:
        print("a")
    
    
    road= ucsSmart(myFixMap,adyacencyList,myPosition,destination)
    
    #borrar 
    a=globals.worldMap
     
    i=1
    temp=fixRoad(road,destination,myPosition)
    currentPosition=None
    lastPosition=temp[0]
    while(currentIndividual.naturalDefenseInd["Velocidad_agua"]>i):
        if  len(temp)>i:
            currentPosition=temp[i]
            currentIndividual.xMundo+=currentPosition[0] - lastPosition[0] 
            currentIndividual.yMundo+=currentPosition[1] - lastPosition[1] 
            if not indexChecker((currentIndividual.xMundo,currentIndividual.yMundo),globals.worldMap.SizeX):
                print("a")
            if chanceToDie(dangerMatrix[currentPosition[0]][currentPosition[1]]):
                globals.worldMap.udpdateIndividual(currentIndividual,previusX,previusY)
                print("Yo "+currentIndividual.name+" me movi hacia "+str(currentIndividual.xMundo) +","+str(currentIndividual.yMundo)+"")
                currentIndividual.die()
                return False    

            previusX,previusY=currentIndividual.xMundo,currentIndividual.yMundo
            lastPosition=currentPosition                
        i+=1
    return True
    print("3")

def chanceToDie(risk,index=10):
    tempInt=random.randint(0,100)
    if tempInt<risk*index:
        return True
    return False

def bestLocationFinder(myMap):
    i=0
    temp=globals.voidValue
    result=None
    while i<len(myMap):
        j=0
        while j < len(myMap[i]):
            if temp>myMap[i][j] and myMap[i][j]!=globals.voidValue:
                temp=myMap[i][j]
                result=(i,j)
            j+=1
        i+=1        
    return result

#revisar que no se salga de los indices de la matrix
def indexChecker(tup,size):
    for i in range(len(tup)):
        if int(tup[i])<0 or int(tup[i])>=int(size):
            return False
    return True

def fixRoad(mapa,destination,origin):
    road=[]
    road.append(destination)
    currentPosition=destination
    if  abs(destination[0]-origin[0])>1 and abs(destination[1]-origin[1])>1:
        print('a')
    
    while mapa[currentPosition[0]][currentPosition[1]].padre!=None:
        road.append(mapa[currentPosition[0]][currentPosition[1]].padre)
        currentPosition=mapa[currentPosition[0]][currentPosition[1]].padre
    return listInversor(road)

def listInversor(lista):
    result=[]
    i=len(lista)-1
    while i>=0:
        result.append(lista[i])
        i-=1
    return result

#dijstra con euristica    
def ucsSmart(mapa,adyacencyList,myPosition,destination):
    myMap=mapZone(mapa)
    x1=myPosition[0]
    y1=myPosition[1]
    myMap[x1][y1]=simpleNode(0,None,False)
    
    myQueue=queue.PriorityQueue()
    
    #if myPosition[0]!=destination[0] or destination[1]!=myPosition[1]:
        #print("asdf")
    #aqui insertamos euristica
    myQueue.put((calcularDistancia(myPosition[0],myPosition[1],destination[0],destination[1]),myPosition))
    while myQueue.qsize()>0:
        temp=myQueue.get()
        #if temp==20000000:
            #print("a")
        if myMap[temp[1][0]][temp[1][1]].visitado:
            continue
        myMap[temp[1][0]][temp[1][1]].visitado=True
        if temp[1][0]==destination[0] and temp[1][1]==destination[1]:
            break
        i=0
        while i < len(dir1Row):
            adyacentNode=(temp[1][0]+dir1Row[i],temp[1][1]+dir2Col[i])
            #revisando q no este visitado y q sea una posicion valida
            valid=indexChecker(adyacentNode,len(mapa))
            
            if valid  and not myMap[adyacentNode[0]][adyacentNode[1]].visitado  and mapa[adyacentNode[0]][adyacentNode[1]]!=globals.voidValue:
                #preguntando si la distancia euristica G es menor x este camino 
                if  myMap[adyacentNode[0]][adyacentNode[1]].distanciaEuristica> myMap[temp[1][0]][temp[1][1]].distancia+calcularDistancia(temp[1][0],temp[1][1],adyacentNode[0],adyacentNode[1]): #adyacencyList[(temp[1][0],temp[1][1],adyacentNode[0],adyacentNode[1])]
                    #actualizando la distancia y la distancia euristica y padre
                    myMap[adyacentNode[0]][adyacentNode[1]].distancia=myMap[temp[1][0]][temp[1][1]].distancia+adyacencyList[(temp[1][0],temp[1][1],adyacentNode[0],adyacentNode[1])]
                    myMap[adyacentNode[0]][adyacentNode[1]].distanciaEuristica=myMap[temp[1][0]][temp[1][1]].distancia+calcularDistancia(destination[0],destination[1],adyacentNode[0],adyacentNode[1])+adyacencyList[(temp[1][0],temp[1][1],adyacentNode[0],adyacentNode[1])]
                    myMap[adyacentNode[0]][adyacentNode[1]].padre=(temp[1][0],temp[1][1])
                    #poniendo en la cola con el valor de la distancia euristica G
                    myQueue.put((myMap[adyacentNode[0]][adyacentNode[1]].distanciaEuristica,(adyacentNode[0],adyacentNode[1])))
                    #tester= myQueue.get()
                    #if tester==20000000:
                    #    print("a")
                    #myQueue.put((myMap[adyacentNode[0]][adyacentNode[1]].distanciaEuristica,(adyacentNode[0],adyacentNode[1])))
            i+=1
    return myMap
    

def calcularDistancia(x1,y1,x2,y2):
    temp =math.sqrt(pow(abs(x1-x2),2)+pow(abs(y1-y2),2))
    return temp

def adyacencyMatrizBuilder(mapa):
    adyacencyList={}
    x=0
    while x < len(mapa):
        y=0
        while y < len(mapa[x]):
            k=0
            while k < len(dir1Row):
                if x+dir1Row[k] >=0 and x+dir1Row[k]< len(mapa) and y+dir2Col[k]>=0 and y+dir2Col[k]<len(mapa[x]):
                    adyacencyList[(x,y,x+dir1Row[k],y+dir2Col[k])]=mapa[x+dir1Row[k]][y+dir2Col[k]]
                k+=1
            y+=1
        x+=1   
    return adyacencyList                        

    

class Coordinates:
    X = -1
    Y = -1

    def __init__(self, x, y):
        self.X = x
        self.Y = y



class Element:
    def __init__(self,atmoicValue, name):
        self.AtomicValue = atmoicValue
        self.Name = name

class simpleNode():
    def __init__(self,distancia,padre,visitado):
        self.distancia=distancia
        self.distanciaEuristica=globals.voidValue
        self.padre=padre
        self.visitado=visitado

def mapZone(myMap):
    newMap=[]
    i=0
    while i < len(myMap):
        j=0
        newMap.append([])
        while j < len(myMap[i]):
            #distancia=infinita,padre=none,visto=false
            newMap[i].append(simpleNode(globals.voidValue,None,False))
            j+=1
        i+=1
    return newMap
                
                
    ##################################################combate##########################################
    
    #tipos de accion se recibe una accion de lucha y una cantidad de pasos para escapar
    #1-caminar hacia alguna casilla 
    #2-atacar con golpe normal que hace daño normal
    #3-atacar con ataque debil, este tiene mas chance de critico
    #4-atacar a bajar velocidad (bajo daño bajo critico alto chance de lenteo)
    #5-atacar para buscar daño de sangrado
    #dir= countPredictionsFirst,countPredictionsSecond,moves,atacks,debuffs,mapa,firstIndividualPos,SecondIndividualPos,firstIndividualVit,SecondIndividualVit 
def combatTurnPredator(predator,prey,battleLogPredator,battleLogPrey,myMap,whosPredicting,iteration):
    #(value,tuple) tuple is a tuple with las position and which attack
    fullResult=None
    result4=None
    
    
    posX=battleLogPredator["xPosition"]
    posY=battleLogPredator["yPosition"]
    
    if battleLogPrey["life"]<=0: return (1000000,(posX,posY,battleLogPredator["action"]))
    if battleLogPredator["life"]<=0: return (-1000000,(posX,posY,battleLogPredator["action"]))
    if checkBorderEscape((posX,posY),myMap): return (-1000000,(posX,posY,battleLogPredator["action"]))
    
    if iteration<0:
        action=battleLogPredator["action"]
        return (euristicaHunt(battleLogPredator,battleLogPrey,myMap),(posX,posY,action))
        
    moves=battleLogPredator["movements"]-battleLogPredator["debuffSlow"]
    if moves > 0:
        for i in range(len(dir1Row)+1):
            if indexChecker((posX+dir1Row[i],posY+dir2Col[i]),len(myMap)):
                newDiccPredator=copyBattleLog(battleLogPredator)
                newDiccPrey=copyBattleLog(battleLogPrey)
                newDiccPredator["movements"]==newDiccPredator["movements"]-1
                tempresult=combatTurnPrey(predator,prey,newDiccPredator,newDiccPrey,myMap,iteration)
                if result4==None:
                    result4=tempresult
                if whosPredicting == "Predator":
                    if result4[0]>tempresult[0]:
                        fullResult=tempresult[0]
                else:
                    if result4[0]<tempresult[0]:
                        result4=tempresult
                        
                        
    if battleLogPredator["action"]==None and hitRange((posX,posY),(battleLogPrey["xPosition"],battleLogPrey["yPosition"])):
        newDiccPredator1=copyBattleLog(battleLogPredator),
        newDiccPrey1=copyBattleLog(battleLogPrey)
        newDiccPredator1["action"]=="normalHit"
        standarAttack(predator,prey,newDiccPredator1,(2,1,1))
        result1=combatTurnPredator(predator,prey,newDiccPredator1,newDiccPrey1,myMap,whosPredicting,iteration)
        
        newDiccPredator2=copyBattleLog(battleLogPredator)
        newDiccPrey2=copyBattleLog(battleLogPrey)
        newDiccPredator2["action"]=="critHit"
        standarAttack(predator,prey,newDiccPredator2,(1,2,1))
        result2=combatTurnPredator(predator,prey,newDiccPredator2,newDiccPrey2,myMap,whosPredicting,iteration)
        
        newDiccPredator3=copyBattleLog(battleLogPredator)
        newDiccPrey3=copyBattleLog(battleLogPrey)
        newDiccPredator3["action"]=="slowHit"
        standarAttack(predator,prey,newDiccPredator1,(1,1,2))
        result3=combatTurnPredator(predator,prey,newDiccPredator3,newDiccPrey3,myMap,whosPredicting,iteration)

        fullResult=bestResult([result1,result2,result3,result4])
        return fullResult
        
        
def bestResult(listRes):
    if listRes!=None:
        tempMax=listRes[0]
    for i in range(len(listRes)):
        if listRes[i]!=None and listRes[i][0]>tempMax[0]:
            tempMax=listRes[i]
    
    return tempMax
    

def hitRange(predatorPos,preyPos):
    if abs(predatorPos[0]-preyPos[0])<=1 and abs(predatorPos[1]-preyPos[1])<=1:
        return True
    return False

def combatTurnPrey(predator,prey,battleLogPredator,battleLogPrey,myMap,iteration):
    #(value,tuple) tuple is a tuple with las position and which attack
    result=None
    if iteration<=0:
        posX=battleLogPrey["xPosition"]
        posY=battleLogPrey["yPosition"]
        action=battleLogPrey["action"]
        return (euristicaHuir(battleLogPrey,battleLogPredator,myMap),(posX,posY,action))
        
    moves=battleLogPrey["movements"]-battleLogPrey[""]
    if True:
        for i in range(len(dir1Row)):
            pass
    

def mapCreator():
    result=[]
    for i in range(21):
        result.append([])
    
    return result



#este es el metodo a invocar para que ocurra el combate
def fullCombat(predator,prey):
    
    mapLentgh=max(int(predator.naturalDefenseInd["Velocidad_agua"]),int(predator.naturalDefenseInd["Velocidad_agua"]))
    #parche por si la matrix se hace muy grande
    if mapLentgh>100 :
        mapLentgh=100
    myMap=mapCreator(mapLentgh*10+1)
    
    predatorBattleLog=battleLogGenerator(predator)
    preyBattleLog=battleLogGenerator(prey)
    prey["xPosition"]=len(myMap)//2
    prey["yPosition"]=len(myMap)//2
    
    sneakWalk(predator,prey,predatorBattleLog,preyBattleLog,myMap)
    
    
    
    i=0
    move=None
    #llamado a combatTurn
    while True:
        if i%2==0:
            futureSigth=(predator.naturalDefenseInd["Inteligencia"]+predator.naturalDefenseInd["Percepcion_de_mundo"])//2
            move= combatTurnPredator(predator,prey,predatorBattleLog,preyBattleLog,myMap,0,futureSigth)
            predatorBattleLog["xPosition"]=move[1][0]
            predatorBattleLog["yPosition"]=move[1][1]
            if(move[1][2])==0:
                standarAttack(predator,prey,preyBattleLog,(2,1,1))
            elif (move[1][2])==0:
                standarAttack(predator,prey,preyBattleLog,(1,2,1))
            elif (move[1][2])==0:
                standarAttack(predator,prey,preyBattleLog,(1,1,2))
        else : 
            futureSigth=(prey.naturalDefenseInd["Inteligencia"]+prey.naturalDefenseInd["Percepcion_de_mundo"])//2
            combatTurnPrey(predator,prey,predatorBattleLog,preyBattleLog,myMap,futureSigth)
            preyBattleLog["xPosition"]=move[1][0]
            preyBattleLog["yPosition"]=move[1][1]
            if(move[1][2])==0:
                standarAttack(prey,predator,predatorBattleLog,(2,1,1))
            elif (move[1][2])==0:
                standarAttack(prey,predator,predatorBattleLog,(1,2,1))
            elif (move[1][2])==0:
                standarAttack(prey,predator,predatorBattleLog,(1,1,2))
        if preyBattleLog["life"]<=0: return 0
        if predatorBattleLog["life"]<=0: return 1
        if checkBorderEscape((preyBattleLog["xPosition"],preyBattleLog["yPosition"])):
            return 2
        
        i+=1

def checkBorderEscape(pos,map):
    if (pos[0]==0 or pos[0]==len(map) and pos[1]==0 or pos[1]==len(map[0])):
        return True
    return False    

#esto se puede mejorar
def euristicaHuir(firstIndividualBattlelog,secondIndividualBattlelog,mapa,peso=1):
    distXPredator=abs(firstIndividualBattlelog["xPosition"]-secondIndividualBattlelog["xPosition"])
    distYPredator=abs(firstIndividualBattlelog["yPosition"]-secondIndividualBattlelog["yPosition"])
    distXEdge= max(len(mapa)-firstIndividualBattlelog["xPosition"],firstIndividualBattlelog["xPosition"])//2
    distYEdge=max(len(mapa[0])-firstIndividualBattlelog["yPosition"],firstIndividualBattlelog["yPosition"])//2
    
    
    return (distXEdge+distYEdge+distXPredator+distYPredator+firstIndividualBattlelog["currentlife"]-firstIndividualBattlelog["currentlife"])*peso
    
def euristicaHunt(firstIndividualBattlelog,secondIndividualBattlelog,mapa,peso=1):
    distXPredator=len(mapa)-abs( firstIndividualBattlelog["xPosition"]-secondIndividualBattlelog["xPosition"])
    distYPredator=len(mapa)-abs(firstIndividualBattlelog["yPosition"]-secondIndividualBattlelog["yPosition"])
    distXEdge=min(len(mapa)-secondIndividualBattlelog.BattleLog["xPosition"],secondIndividualBattlelog["xPosition"])
    distYEdge=min(len(mapa[0])-secondIndividualBattlelog.BattleLog["xPosition"],secondIndividualBattlelog["yPosition"])   
    
    
    return (distXEdge+distYEdge+distXPredator+distYPredator+firstIndividualBattlelog["currentlife"]-secondIndividualBattlelog.BattleLog["currentlife"])*peso

#realiza un ataque recibe un peso para ver que tipo de ataque sera
#weithgs=(min%attack,max%attack,critIncrease,slowIncrease,)
def standarAttack(currentIndividual, secondIndividual,battleLogSecond,weithgs):
    attack=calculatePercent(currentIndividual.naturalDefenseInd["Vida"],random.randint(15,20))*weithgs[0]
    
    armorChance=random.randint(0,100)
    defense=0
    if armorChance>secondIndividual.naturalDefenseInd["Armadura_fuerte_porciento"]:
        defense=calculatePercent(secondIndividual.naturalDefenseInd["Armadura"],random.randint(10,20))
    else:
        defense=calculatePercent(secondIndividual.naturalDefenseInd["Armadura"],random.randint(0,10))
    
    critChance=random.randint(0,100)*weithgs[1]
    if critChance>100-currentIndividual.naturalDefenseInd["Crit_chance_increase"]:
        attack*=3
        
    slowChance=random.randint(0,100)*weithgs[2]
    slowDone=0
    if slowChance>100-currentIndividual.naturalDefenseInd["Slow_chance"]:
        slowDone=calculatePercent(currentIndividual.naturalDefenseInd["Slow_done"],random.randint(25,40))
        battleLogSecond["Slow"]=battleLogSecond["Slow"]+slowDone
        
    bleedChance=random.randint(0,100)
    bleedDone=0
    if bleedChance>100-currentIndividual.naturalDefenseInd["Bleed_chance"]:
        bleedDone=calculatePercent(secondIndividual.naturalDefenseInd["Vida"],currentIndividual.naturalDefenseInd["Bleed_damage"])
        battleLogSecond["Bleed"]=battleLogSecond["Bleed"]+bleedDone
            
    result=0
    if defense<attack: 
        result=attack-defense
    
    battleLogSecond["life"]-=result

#el depredador se acerca sigilosamente
def sneakWalk(predator,prey,battleLogPredator,battleLogPrey,mapa):
    
    tempX,tempY=0,0
    if battleLogPredator["xPosition"]==battleLogPrey["xPosition"]:
        dirX=0
    else:
        dirX=battleLogPredator["xPosition"]-battleLogPrey["xPosition"]//abs(battleLogPredator["xPosition"]-battleLogPrey["xPosition"])*-1
    
    if battleLogPredator["yPosition"]==battleLogPrey["yPosition"]:
        dirY=0
    else:
        dirY=battleLogPredator["yPosition"]-battleLogPrey["yPosition"]//abs(battleLogPredator["yPosition"]-battleLogPrey["yPosition"])*-1
    
    while True:
        if indexChecker((dirX+battleLogPredator["xPosition"],dirY+battleLogPredator["yPosition"]),len(mapa)):
            if dirX+battleLogPredator["xPosition"]== battleLogPrey["xPosition"] and dirY+battleLogPredator["yPosition"]==battleLogPrey["yPosition"]:
                standarAttack(predator,prey,battleLogPrey,(2,2,2))
                return
        else:
            predatorChance=20*(int(predator.naturalDefenseInd["Sigilo"])-(int(prey.naturalDefenseInd["Intelgencia"])+(int(prey.naturalDefenseInd["Intelgencia"])))//2)
            sneakChance=random.randint(0,100)
            if predatorChance>sneakChance:
                battleLogPredator["xPosition"]=dirX+battleLogPredator["xPosition"]
                battleLogPredator["yPosition"]=dirY+battleLogPredator["yPosition"]
            else:
                return    
    
    
def calculatePercent(number,percent):
    return number*percent//100 


def battleLogGenerator(individuo):
    battleLog={}
    battleLog["life"]=int(individuo.naturalDefenseInd["Vida"])
    battleLog["currentLife"] =int(individuo.naturalDefenseInd["Vida"])
    battleLog["movements"] =int(individuo.naturalDefenseInd["Velocidad_agua"])
    battleLog["xPosition"] =0
    battleLog["xPosition"] =0
    
    battleLog["action"] =None
    
    battleLog["turnsLeft"] =(int(individuo.naturalDefenseInd["Percepcion_de_mundo"])+int(individuo.naturalDefenseInd["Inteligencia"]))//2
    
    battleLog["debuffSlow"]=0
    battleLog["debuffBleed"]=0
    return battleLog

def resetBattleLog(individuo,battleLog):
    battleLog["currentMovements"]=int(individuo.naturalDefenseInd["Velocidad_agua"])
    battleLog["action"] =None
    
def copyBattleLog(firstBattleLog):
    newBattleLog={}
    for key in firstBattleLog:
        newBattleLog[key]=firstBattleLog[key]
        
    return newBattleLog