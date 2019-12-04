"""
HOW TO RUN:
tsp.py mapa250.txt

where 'mapa250.txt' is a input file with all coordinates that we need to read

"""

scriptpath = "/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/teste/"
import os
import sys 
sys.path.append(os.path.abspath(scriptpath))


# IMPORTANT STUFF --------------------------------------------------------------
import sys
import math
import random

# OUR METHODS ------------------------------------------------------------------
import entrada
# import graph
with open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/mapa250.txt", "r") as f:
        f.readline()
        data =  ([p.split() for p in f.read().strip().splitlines()])
data

# GET DATA FROM INPUT FILE AND SAVE IT -----------------------------------------


# FLAGS ------------------------------------------------------------------------
initialCity = True # PRINT FIRST CITY AGAIN AT THE END OF THE ROUTE

"""
--- GA CONCEPTS ---
* Gene: a city (represented as (x, y) coordinates)
* Individual (aka “chromosome”): a single route satisfying the conditions above
* Population: a collection of possible routes (i.e., collection of individuals)
* Parents: two routes that are combined to create a new route
* Mating pool: a collection of parents that are used to create our next population (thus creating the next generation of routes)
* Fitness: a function that tells us how good each route is (in our case, how short the distance is)
* Mutation: a way to introduce variation in our population by randomly swapping two cities in a route
* Elitism: a way to carry the best individuals into the next generation
"""


# SETTING UP OUR CLASSES AND METHODS -------------------------------------------
class City:
   def __init__(self, x=None, y=None):
      self.x = None
      self.y = None
      if x is not None:
         self.x = x
      else:
         self.x = int(random.random() * 200)
      if y is not None:
         self.y = y
      else:
         self.y = int(random.random() * 200)
   
   def getX(self):
      return self.x
   
   def getY(self):
      return self.y
   
   def distanceTo(self, city):
      xDistance = abs(self.getX() - city.getX())
      yDistance = abs(self.getY() - city.getY())
      distance = math.sqrt( (xDistance*xDistance) + (yDistance*yDistance) )
      return distance
   
   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class PathManager:
   destinationCities = []
   
   def addCity(self, city):
      self.destinationCities.append(city)
   
   def getCity(self, index):
      return self.destinationCities[index]
   
   def numberOfCities(self):
      return len(self.destinationCities)


class Path:
   def __init__(self, pathmanager, path=None):
      self.pathmanager = pathmanager
      self.path = []
      self.fitness = 0.0
      self.distance = 0
      if path is not None:
         self.path = path
      else:
         for index in range(0, self.pathmanager.numberOfCities()):
            self.path.append(None)
   
   def __len__(self):
      return len(self.path)
   
   def __getitem__(self, index):
      return self.path[index]
   
   def __setitem__(self, key, value):
      self.path[key] = value
   
   def __repr__(self):
      geneString = ""
      for i in range(0, self.pathSize()):
         geneString += "[" + str(self.getCity(i)) + "]"
      return geneString
   
   def generateIndividual(self):
      for cityIndex in range(0, self.pathmanager.numberOfCities()):
         self.setCity(cityIndex, self.pathmanager.getCity(cityIndex))
      random.shuffle(self.path)
   
   def getCity(self, pathPosition):
      return self.path[pathPosition]
   
   def setCity(self, pathPosition, city):
      self.path[pathPosition] = city
      self.fitness = 0.0
      self.distance = 0
   
   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         pathDistance = 0
         for cityIndex in range(0, self.pathSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex+1 < self.pathSize():
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            pathDistance += fromCity.distanceTo(destinationCity)
         self.distance = pathDistance
      return self.distance
   
   def pathSize(self):
      return len(self.path)
   
   def containsCity(self, city):
      return city in self.path

# GA POPULATION THEORY ---------------------------------------------------------
class Population:
   def __init__(self, pathmanager, populationSize, initialise):
      self.paths = []
      for i in range(0, populationSize):
         self.paths.append(None)
      
      if initialise:
         for i in range(0, populationSize):
            newPath = Path(pathmanager)
            newPath.generateIndividual()
            self.savePath(i, newPath)
      
   def __setitem__(self, key, value):
      self.paths[key] = value
   
   def __getitem__(self, index):
      return self.paths[index]
   
   def savePath(self, index, path):
      self.paths[index] = path
   
   def getPath(self, index):
      return self.paths[index]
   
   def getFittest(self):
      fittest = self.paths[0]
      for i in range(0, self.populationSize()):
         if fittest.getFitness() <= self.getPath(i).getFitness():
            fittest = self.getPath(i)
      return fittest
   
   def populationSize(self):
      return len(self.paths)

# GENETIC ALGORITHM THEORY -----------------------------------------------------
class GA:
   def __init__(self, pathmanager):
      self.pathmanager = pathmanager
      self.mutationRate = 0.015
      self.tournamentSize = 5
      self.elitism = True
   
   def evolvePopulation(self, pop):
      newPopulation = Population(self.pathmanager, pop.populationSize(), False)
      elitismOffset = 0
      if self.elitism:
         newPopulation.savePath(0, pop.getFittest())
         elitismOffset = 1
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         parent1 = self.tournamentSelection(pop)
         parent2 = self.tournamentSelection(pop)
         child = self.crossover(parent1, parent2)
         newPopulation.savePath(i, child)
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         self.mutate(newPopulation.getPath(i))
      
      return newPopulation
   
   def crossover(self, parent1, parent2):
      child = Path(self.pathmanager)
      
      startPos = int(random.random() * parent1.pathSize())
      endPos = int(random.random() * parent1.pathSize())
      
      for i in range(0, child.pathSize()):
         if startPos < endPos and i > startPos and i < endPos:
            child.setCity(i, parent1.getCity(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               child.setCity(i, parent1.getCity(i))
      
      for i in range(0, parent2.pathSize()):
         if not child.containsCity(parent2.getCity(i)):
            for ii in range(0, child.pathSize()):
               if child.getCity(ii) == None:
                  child.setCity(ii, parent2.getCity(i))
                  break
      
      return child
   
   def mutate(self, path):
      for pathPos1 in range(0, path.pathSize()):
         if random.random() < self.mutationRate:
            pathPos2 = int(path.pathSize() * random.random())
            
            city1 = path.getCity(pathPos1)
            city2 = path.getCity(pathPos2)
            
            path.setCity(pathPos2, city1)
            path.setCity(pathPos1, city2)
   
   def tournamentSelection(self, pop):
      tournament = Population(self.pathmanager, self.tournamentSize, False)
      for i in range(0, self.tournamentSize):
         randomId = int(random.random() * pop.populationSize())
         tournament.savePath(i, pop.getPath(randomId))
      fittest = tournament.getFittest()
      return fittest


# RUNNING PROJECT --------------------------------------------------------------
if __name__ == '__main__':
   
   pathmanager = PathManager()
   
   # FORMATING INPUT DATA ------------------------------------------------------
   for row in data:
      axisX = float(row[0])
      axisY = float(row[1])
      pathmanager.addCity(City(axisX, axisY))
      pass

   # INITIALIZE POPULATION -----------------------------------------------------
   pop = Population(pathmanager, len(data), True)
   print("Distancia Inicial: " + str(pop.getFittest().getDistance()))
   print("Realizando combinações")
   
   # EVOLVE POPULATION FOR N = 50 GENERATIONS ----------------------------------
   generations = 200
   dist0=[]
   for x in range(0,30):
       
   
       ga = GA(pathmanager)
       pop = ga.evolvePopulation(pop)
       for i in range(0, len(data) + generations):
          pop = ga.evolvePopulation(pop)
       
       # PRINT FINAL RESULTS -------------------------------------------------------
       result = pop.getFittest()
    
       print("Distancia Final: " + str(result.getDistance()))
       dist0.append(str(result.getDistance()))
       # WRITE OUTPUT DATA INTO .TXT FILE ------------------------------------------
       dataFile = open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/outputData.txt", "w")
       
       for item in result:
          dataFile.write(str(item.x) + " " + str(item.y) + "\n")
       dataFile.close()
    
    
    dataFile2 = open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/distancias.txt", "w")
    for x in range(0,30):
        dataFile2.write(str(dist0[x])+"\n")
    dataFile2.close()
    
    dist1=[]
    for x in range(0,30):
       
   
       ga = GA(pathmanager)
       pop = ga.evolvePopulation(pop)
       for i in range(0, len(data) + generations):
          pop = ga.evolvePopulation(pop)
       
       # PRINT FINAL RESULTS -------------------------------------------------------
       result = pop.getFittest()
    
       print("Distancia Final: " + str(result.getDistance()))
       dist1.append(str(result.getDistance()))
       # WRITE OUTPUT DATA INTO .TXT FILE ------------------------------------------
       dataFile3 = open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/outputDataM.txt", "w")
    
       for item in result:
          dataFile3.write(str(item.x) + " " + str(item.y) + "\n")
       dataFile3.close()
       
    dataFile4 = open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/distanciasM.txt", "w")
    for x in range(0,30):
        dataFile4.write(str(dist0[x])+"\n")
    dataFile4.close()
    