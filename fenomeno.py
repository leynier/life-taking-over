class Fenomeno():
    def __init__(self, nombre, grado):
        self.nombre = nombre
        self.grado = grado
<<<<<<< Updated upstream
        
class Ciclon(Fenomeno):
    def __init__(self, nombre, grado):
        super().__init__(nombre, grado)
        
    def Efectuar_Ciclon(mapas,criatura,pos):
        pass
=======
        self.Recorrido = MyQueue()
        self.pos = 0
        self.cor = cor
        self.count_maxDistance = randint(0,10)
        self.vecmov = []
        self.map = mapa
        
        #cambiar por probabilidad
        duracion = randint(1,7)
        self.Recorrido.put((duracion, None))

    
    def GenerarRecorrido(self,corulti):
        duracion = randint(0,7)
        if corulti[2] == self.count_maxDistance:
            return []
        
        elif corulti[1] == None:
            return [(duracion,self.cor,0)]
        
        elif self.vecmov == "Random":
            ult_pos = corulti
            
            x = randint(-1,1)
            y = randint(-1,1)
            
            cornew = (ult_pos[1][0] + x, ult_pos[1][1] + y)
            if cornew[0] < self.map.SizeX and cornew[1] < self.map.SizeY:
                return [(duracion,cornew,corulti[2]+ 1)]
            
        return []
                
    
    def GenerateVector(self):
        self.vecmov.append("Random")
    
    def Refresc(self,time):
        queueCom = MyQueue()
        lenrecorrido = len(self.Recorrido)
        for i in range(0,lenrecorrido):
            posrecorrido = self.Recorrido.get()
            queueCom.put((posrecorrido[0],posrecorrido[1],time))
            
            while len(queueCom) != 0:
                posrecorrido = queueCom.get()
                move = (posrecorrido[0],posrecorrido[1],posrecorrido[2])
                duracion = posrecorrido[0]
                rest = posrecorrido[2]
                if duracion > rest:
                    posrecorrido = (duracion - time,posrecorrido[1],posrecorrido[2])
                    self.EfectuarFenomeno(move)
                    self.Recorrido.put(posrecorrido)
        
                elif duracion == rest:
                    duracion = duracion - time
                    self.EfectuarFenomeno(move)
                    listmove = self.GenerarRecorrido(move)
                    self.CambiarZona(posrecorrido,listmove)
                    for i in range(0,len(listmove) - 1):
                        self.Recorrido.append(listmove[i])
        
                elif duracion < rest:
                    rest = rest - duracion
                    self.EfectuarFenomeno(move)
                    duracion = 0
                    self.CambiarZona(time,move)
                    listmove = self.GenerarRecorrido(move)
                    for i in range(0,len(listmove)):
                        queueCom.put((listmove[i][0],listmove[i][1],rest))
                
            
    def EfectuarFenomeno(self,move):
        print("Efectuando Fenomeno")
        return
    
    def CambiarZona(self,corulti,listmove):
        i = 0
        for zone in self.map.Zones:
            for tile in zone.TileList:
                if tile.Coordinates == corulti:
                   i += 1
                   #eliminar fenomeno
                
                for j in range(0,len(listmove)):
                    if tile.Coordinates == listmove[j]:
                        i += 1
                        #añadir fenomeno
                    
                if i == 1 + len(listmove):
                    return
                    
                    
        
class Ciclon(Fenomeno):
    def __init__(self, nombre, grado, cor, mapa):
        super().__init__(nombre,grado,cor,mapa)
        
    def Rand_Mov_CC(self,cor_ciclon, poder_ciclon):
        cor_EjeX_low = cor_ciclon[1]
        cor_EjeX_up = self.map.SizeY-cor_ciclon[1]
        
        cor_EjeY_low = cor_ciclon[0]
        cor_EjeY_up = cor_ciclon[0]
        
        cord_rand_move = misc.randCord(-cor_EjeY_low, cor_EjeY_up, -cor_EjeX_low, cor_EjeX_up)
        cor_new = (cor_ciclon[0] + cord_rand_move[0]*poder_ciclon, cor_ciclon[1] + cord_rand_move[1]*poder_ciclon)
        return cor_new
    
    def EfectuarFenomeno(self,cor):
        if cor[1] == None:
            return
        
        ListaCriaturas = self.DetectarCriaturas(cor)
        self.MoverCriaturas(ListaCriaturas)
    
    def DetectarCriaturas(self,cor):
        creaturesMoves = []
        if cor != None: 
            for zone in self.map.Zones:
                for tile in zone.TileList:
                    if tile.Coordinates == cor:
                        while tile.CreatureList > 0:
                            cordnew = self.Rand_Mov_CC(cor,1)
                            creature = tile.CreatureList.pop()
                            creaturesMoves.append((creature,cordnew))
                        return creaturesMoves
        return creaturesMoves

    def MoverCriaturas(self,ListCreature):
        while len(ListCreature) > 0:
            t = ListCreature.pop()
            for zone in self.map:
                for tile in zone.TileList:
                    if tile.Coordinates == t[1]:
                        #Cambiar las coordenadas de la ubicacion de la especie
                        tile.CreatureList.append(t[0])
>>>>>>> Stashed changes

class ErupcionVolcánica(Fenomeno):
    def __init__(self, nombre, grado, posicion):
        super().__init__(nombre, grado)
        
<<<<<<< Updated upstream
        
    def Erupcion(mapas,especies):
        pass
        
class Subnami(Fenomeno):
    def __init__(self, nombre, grado):
        super().__init__(nombre, grado)
        
    def Efectuar_Subnami(mapas,especies,pos):
        pass
    


def General_Nombre_Random():
    
=======
    def EfectuarFenomeno(self,cor):
        if cor[1] == None:
            return
        
        if cor == self.cor:
            list_caida_rocas = self.PosCaida_Rocas(self.corvolcan)
            self.Lluvia_De_Rocas(list_caida_rocas)
        
        self.LavaRecorrido()
        
    def PosCaida_Rocas(self):
        for zone in self.map.Zones:
            for tile in zone.TileList:
                if tile.Coordinates == self.cor_volcan:
                    cantidad_rocas = randint(0,20)
                    Lpos_caida_rocas = self.Coordenadas_Caida_Rocas(cantidad_rocas)
                    return Lpos_caida_rocas
    

    def Lluvia_De_Rocas(self,list_rocas):
        for roca_cor in range(0,len(list_rocas)):
            for zone in self.map.Zones:
                for tile in zone.TileList:
                    if tile.Coordinates == roca_cor:
                        i = 0
                        while i < len(tile.CreatureList):
                            #Cambiar por probabilidades:
                            creature = tile.CreatureList[i]
                            death = randint(0,1)
                            if death == 1:
                                tile.CreatureList.pop(i)
                            else: 
                                i += 1
                                 
        
    def LavaRecorrido(self,cor):
        if self.Recorrido[self.pos] != None: 
            for zone in self.map.Zones:
                for tile in zone.TileList:
                    if tile.Coordinates == self.Recorrido[self.pos]:
                        self.DamageLava(tile)
    
    def DamageLava(self,tile):
        i = 0
        while i < len(tile.CreatureList):
            creature = tile.CreatureList[i]
            death = randint(0,1)
            if death == 1:
                tile.CreatureList.pop(i)
            else: 
                i += 1
            
    
        
class Terremoto(Fenomeno):
    def __init__(self, nombre, grado, cor, mapa):
        super().__init__(nombre, grado, cor, mapa)
        
    def EfectuarFenomeno(self,cor):
        if cor[1] == None:
            return
        
        for zone in self.map.Zones:
            for tile in zone.TileList:
                if tile.Coordinates == self.corini:
                    return
                
    def Agrietar():
        pass
>>>>>>> Stashed changes
