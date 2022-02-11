from random import randint
import globals
import misc
import especies
class Zone:

    def __init__(self, tileCount, ZoneType):
        self.TileCount = tileCount
        self.ZoneType = ZoneType
        self.Danger = globals.ZoneDanger[ZoneType]
        self.TileList = []



#El método recibe la especie con la que se trabajará    
    def startEvolving(self, especie):
        #Añadiedno la especie original al diccionario
        AllDictionary = {"EspeciePadre" : especie}

        #Contadores para saber cuantos evoluciono
        individualsInZone = 0
        MajorityOfindividuals = 0
        TileToEvolve = -1

        varianzaDictionary = {}


        #Dicionario donde guardaré el promedio de valores de todos los individuos de la especie
        promedDictionary = {}

        #Rellenando los valores promedios de los individuos con todos los que se encuentran en esa zona
        for i in self.TileList:
            temcount = 0
            for j in i.CreatureList:
                if j.especie == especie:
                    temcount += 1
                    individualsInZone +=1
                    #Añadiendo el individuo a la lista          
                    promedDictionary = misc.dictMergeSum(j.naturalDefenseInd, promedDictionary)

            if temcount > MajorityOfindividuals:
                MajorityOfindividuals = temcount
                TileToEvolve = i


        #Dividiendo cada valor entre la cantidad de individuos para hallar el promedio
        for i in promedDictionary.keys():
            promedDictionary[i] = promedDictionary[i]/individualsInZone


        #Añadiendo el promedio al diccionario
        AllDictionary["Promedio"]= promedDictionary


        #Rellenando todos los valores de varianza
        for i in self.TileList:
            for j in i.CreatureList:
                if j.especie == especie:
                    #Añadiendo el individuo a la lista        
                    tempdict = misc.dictMergeSubstract(j.naturalDefenseInd, promedDictionary)
                    varianzaDictionary = misc.dictMergeSum(tempdict,varianzaDictionary)

        #Terminando de hallar la varianza
        for i in varianzaDictionary.keys():
            varianzaDictionary[i] = varianzaDictionary[i]/individualsInZone

        AllDictionary["Varianza"] = varianzaDictionary



        if TileToEvolve == -1:
            return


        AllDictionary["x"] = TileToEvolve.Coordinates[0]
        AllDictionary["y"] = TileToEvolve.Coordinates[1]

        #Buscar la mejor comida para comer:
        AllDictionary["Elemento"] = self.SelectPopularElement(TileToEvolve)


        varianzaPromedio = -1 + sum(
            int(especie.naturalDefense[i]) - int(promedDictionary[i])
            for i in promedDictionary.keys()
        )

        #varianza = varianzaPromedio/individualsInZone
        varianza = varianzaPromedio



        #Si la varianza general es lo suficientemente grande entonces evoluciona
        if (varianza >= globals.EvolutionFrequency or varianza <= -1*(globals.EvolutionFrequency)) and MajorityOfindividuals>globals.minSizeOfNewEspecies:
            print("Una especie ha evolucionado en la casilla ( "+ str(TileToEvolve.Coordinates[0])+", " +str(TileToEvolve.Coordinates[1]) +")" )
            if MajorityOfindividuals <= (len(especie.individuos)/2):
                AllDictionary["Individuos"] = MajorityOfindividuals
                TileToEvolve.deleteCreaturesEspecies(MajorityOfindividuals, especie)
                especies.Especies(MajorityOfindividuals,TileToEvolve.Coordinates[0],TileToEvolve.Coordinates[1],AllDictionary)


            else:
                AllDictionary["Individuos"] = MajorityOfindividuals//2
                TileToEvolve.deleteCreaturesEspecies(MajorityOfindividuals//2, especie)
                especies.Especies(MajorityOfindividuals//2,TileToEvolve.Coordinates[0],TileToEvolve.Coordinates[1],AllDictionary)



        return AllDictionary

        

    
    def SelectPopularElement(self,Tile):
        ElementsPctTupleList = []
        count = 0
        for i in Tile.ComponentsDict.keys():
            if (
                i in ['Solar Light', 'Water'] or Tile.ComponentsDict[i] != 0
            ) and i not in ['Solar Light', 'Water']:
                if count == 0: 
                    ElementsPctTupleList.append((i,Tile.ComponentsDict[i]))
                else:
                    ElementsPctTupleList.append((i, Tile.ComponentsDict[i] + ElementsPctTupleList[-1][1]))

                count += 1

        ElementsPctTupleList.append(('Solar Light', ElementsPctTupleList[count - 1][1] + ElementsPctTupleList[count - 1][1]/10))

        ElementsPctTupleList.append(('Water', ElementsPctTupleList[count - 1][1] + ElementsPctTupleList[count - 1][1]/10))

        randomIndex = randint(0 , int(ElementsPctTupleList[-1][1]))

        return next(
            (i[0] for i in ElementsPctTupleList if i[1] >= randomIndex),
            'Solar Light',
        )
        
    
    def ChangeDanger(self, newDangerInt):
        self.Danger = newDangerInt
        
        
    def SelectPopularElement(self,Tile):
        ElementsPctTupleList = []
        count = 0
        for i in Tile.ComponentsDict.keys():
            if (
                i in ['Solar Light', 'Water'] or Tile.ComponentsDict[i] != 0
            ) and i not in ['Solar Light', 'Water']:
                if count == 0: 
                    ElementsPctTupleList.append((i,Tile.ComponentsDict[i]))
                else:
                    ElementsPctTupleList.append((i, Tile.ComponentsDict[i] + ElementsPctTupleList[-1][1]))

                count += 1

        ElementsPctTupleList.append(('Solar Light', ElementsPctTupleList[count - 1][1] + ElementsPctTupleList[count - 1][1]/10))

        ElementsPctTupleList.append(('Water', ElementsPctTupleList[count - 1][1] + ElementsPctTupleList[count - 1][1]/10))
        ElementsPctTupleList.append(('Cazador', ElementsPctTupleList[count - 1][1] + (ElementsPctTupleList[count - 1][1]/10)* globals.Hunting))

        randomIndex = randint(0 , int(ElementsPctTupleList[-1][1]))

        return next(
            (i[0] for i in ElementsPctTupleList if randomIndex <= i[1]),
            'Solar Light',
        )

