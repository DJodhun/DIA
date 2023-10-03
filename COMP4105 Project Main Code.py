import tkinter as tk
from tkinter import *
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
#Error handling
from tkinter.messagebox import showerror
from contextlib import suppress
from scipy.spatial import cKDTree
import time
#Array handling
import copy
import itertools
#For stats
import pandas as pd
from scipy.stats import ttest_ind
#Files to import
from aStarFinal import *
from GeneticAlgorithmFinal import *

#In canvas.after(N, ...), set N to 0 for no graphics + instant numbers 

#%%
global success
success = [] #multiply fitness[i] by success[i], so fitness = 0 if failed. Success = 1, faliure = 0
np.array(success)

class Counter:
    def __init__(self,canvas):
        self.dirtCollected = 0
        self.canvas = canvas
        self.canvas.create_text(70,50,text="Dirt collected: "+str(self.dirtCollected),tags="counter")
        
    def itemCollected(self, canvas):
        self.dirtCollected +=1
        self.canvas.itemconfigure("counter",text="Dirt collected: "+str(self.dirtCollected))

class Bot:

    def __init__(self,namep,canvasp):
        # self.x = random.randint(100,900)
        # self.y = random.randint(100,900)
        # self.theta = random.uniform(0.0,2.0*math.pi)
        self.x = 900
        self.y = 900
        self.theta = random.uniform(0.0, 2*np.pi) #(-3.0*math.pi)/4 # self.theta = 0 IS FACING RIGHT, NOT UP, pi is left, pi/2 is down, 3pi/2 is up
        #self.theta = 0
        self.name = namep
        self.ll = 60 #axle width
        self.vl = 0.0
        self.vr = 0.0
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.canvas = canvasp
        #self.movement = 50

    def draw(self,canvas):
        points = [ (self.x + 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                ]
        canvas.create_polygon(points, fill="blue", tags=self.name)
        

        self.sensorPositions = [ (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                                 (self.x - 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y + 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta),  \
                                 (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta) \
                            ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        canvas.create_oval(centre1PosX-15,centre1PosY-15,\
                           centre1PosX+15,centre1PosY+15,\
                           fill="gold",tags=self.name)

        wheel1PosX = self.x - 30*math.sin(self.theta)
        wheel1PosY = self.y + 30*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,\
                                         wheel1PosX+3,wheel1PosY+3,\
                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 30*math.sin(self.theta)
        wheel2PosY = self.y - 30*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,\
                                         wheel2PosX+3,wheel2PosY+3,\
                                         fill="green",tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        sensor3PosX = self.sensorPositions[4]
        sensor3PosY = self.sensorPositions[5]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3, \
                           sensor1PosX+3,sensor1PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3, \
                           sensor2PosX+3,sensor2PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor3PosX-3, sensor3PosY-3, \
                          sensor3PosX+3,sensor3PosY+3,
                          fill="yellow",tags=self.name)
        
        #coords = canvas.coords(self.name)
        
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self,canvas,registryPassives,dt, safeXPosition2 = [], safeYPosition2 = []):
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0], \
                        [math.sin(omega*dt), math.cos(omega*dt), 0],  \
                        [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: # straight line movement
            self.x += self.vr*math.cos(self.theta) #vr wlog
            self.y += self.vr*math.sin(self.theta)
        
        if self.x >= 10 and self.x <= 990:
            currentXPosition2 = self.x
            
            safeXPosition2.append(currentXPosition2)
        if self.y >= 10 and self.y <= 990:
            currentYPosition2 = self.y
            safeYPosition2.append(currentYPosition2)
        #toroidal movement
        # if self.x<0.0:
        #     self.x=999.0
        # if self.x>1000.0:
        #     self.x = 0.0
        # if self.y<0.0:
        #     self.y=1000.0
        # if self.y>1000.0:
        #     self.y = 0.0
            
        #bounce off edges
        if self.x<=0.0:
            print("Hit Wall")
            self.theta = abs(self.theta + np.pi * np.random.uniform(0.1, 0.9))
            self.x = safeXPosition2[-10]
            #self.vr = -2.0
            #self.vr = 2.0
            # self.theta = abs(self.theta - np.pi)
            
        if self.x>=1000.0:
            print("Hit Wall")
            #self.x = 999.0
            self.theta = abs(self.theta + np.pi * np.random.uniform(0.1, 0.9))
            self.x = safeXPosition2[-10]
            #self.vr = -2.0
            #self.vr = 2.0
            #self.currentlyTurning == True
        if self.y<=0.0:
            print("Hit Wall")
            #self.y = 1.0
            #self.vr = -2.0
            #self.vr = 2.0
            self.theta = abs(self.theta + np.pi * np.random.uniform(0.1, 0.9))
            self.y = safeYPosition2[-10]
            #self.currentlyTurning == True
        if self.y>=1000.0:
            print("Hit Wall")
            #self.y = 999.0
            self.theta = abs(self.theta + np.pi * np.random.uniform(0.1, 0.9))
            self.y = safeYPosition2[-10]
            #self.vr = -2.0
            #self.vr = 2.0
            #self.currentlyTurning == True
        
        #hardcoding the furniture for each room 
        #if self.x in range
        canvas.delete(self.name)
        self.draw(canvas)
        
    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )
    
    def distanceToRightSensor(self,lx,ly):
        return abs(math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                          (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) ))

    def distanceToLeftSensor(self,lx,ly):
        return abs(math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                            (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) ))
    
    def distanceToRearSensor(self, lx, ly):
        return         
    
    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                if self.distanceTo(rr)<30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives

    def brain(self, path, count, window, mode ="True"):
        #Wandering Mode
        
        # if self.currentlyTurning==True:
        #     self.vl = -2.0
        #     self.vr = 2.0
        #     self.turning -= 1
        # else:
        #     self.vl = 5.0
        #     self.vr = 5.0
        #     self.moving -= 1
        # if self.moving==0 and not self.currentlyTurning:
        #     self.turning = np.random.randint(0, 100)
        #     self.currentlyTurning = True
        # if self.turning==0 and self.currentlyTurning:
        #     self.moving = 50
        #     self.currentlyTurning = False
                        
        #map behaviour
        if mode == "True":
            #If list index is out of range causes a fatal error, it is because path is empty from the get go. This happens due to popping the path variable, and not reading in the backup save each time.
            #print(path)
            maptarget = (((path[0])[0]*100) + 50, ((path[0])[1]*100) + 50) #+ 50 to both if this does not work 
            if abs(self.distanceToRightSensor(maptarget[0], maptarget[1]))>abs(self.distanceToLeftSensor(maptarget[0], maptarget[1])):
                 self.vl = 2.0
                 self.vr = -2.0
            elif abs(self.distanceToRightSensor(maptarget[0], maptarget[1]))<abs(self.distanceToLeftSensor(maptarget[0], maptarget[1])):
                 self.vl = -2.0
                 self.vr = 2.0
            if abs(self.distanceToRightSensor(maptarget[0], maptarget[1])-self.distanceToLeftSensor(maptarget[0], maptarget[1]))<self.distanceToLeftSensor(maptarget[0], maptarget[1])*0.1:
                 self.vl = 5.0
                 self.vr = 5.0
            # if abs(self.distanceToLeftSensor(maptarget[0], maptarget[1])-self.distanceToRightSensor(maptarget[0], maptarget[1]))<self.distanceToRightSensor(maptarget[0], maptarget[1])*0.1:
            #      self.vl = 5.0
            #      self.vr = 5.0     
            if self.distanceToRightSensor(maptarget[0], maptarget[1]) < 50 and self.distanceToLeftSensor(maptarget[0], maptarget[1]) < 50:
                 self.vl = 0.0
                 self.vr = 0.0 
                 path.pop(0)
                 print("Checkpoint")
                 
                 if len(path) == 0:
                     self.vl = 0.0
                     self.vr = 0.
                    
    def collision(self, registryPassives, canvas, safeXPosition = [], safeYPosition = [], stuck = []):#print Hit Object and Hit Wall to see where its at 
        botCoords = canvas.coords(self.name)
        colls = canvas.find_overlapping(botCoords[0], botCoords[1], botCoords[2], botCoords[3])
        colls = list(colls)
        currentXPosition = self.x
        currentYPosition = self.y
        collision = False
        # dummypos = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # safeXPosition.append(dummypos)
        # safeYPosition.append(dummypos)
        if collision == False:
            safeXPosition.append(currentXPosition)
            safeYPosition.append(currentYPosition)
        if len(colls) > 1:
            if colls[0] < 10:
                collision = True
                #print("Hit Object")
                self.x = safeXPosition[-15]
                self.y = safeYPosition[-15]
                while collision == True:
                    stuck.append(1)
                    #print(stuck)
                    if len(stuck) > 10:
                        for i in range(len(stuck)):
                            stuck.pop(0)
                        if safeXPosition[-15] - safeXPosition[-5] < 20 and safeYPosition[-15] - safeYPosition[-5] < 20:
                            print("Well and Truly stuck")
                            self.x = safeXPosition[-20]
                            self.y = safeYPosition[-20]
                            self.theta = self.theta - np.pi
                            # self.vr = 0.0
                            # self.vl = 0.0
                        #print("Stuck")
                        self.theta = self.theta - np.pi
                        collision = False
            elif colls[0] > 10:
                #print("Dirt Collected")
                pass    
        if self.x<=0.0:
            collision = True
            #print("Hit Wall")
            #self.x = safeXPosition[-15]
            self.theta = self.theta + np.pi
        if self.x>=1000.0:
            #self.x = safeXPosition[-15]
            self.theta = self.theta - np.pi
            #self.currentlyTurning == True
        if self.y<=0.0:
            #self.y = safeYPosition[-15]
            self.theta = self.theta - np.pi
            #self.currentlyTurning == True
        if self.y>=1000.0:
            self.y = safeYPosition[-15]
            self.theta = self.theta - np.pi
                
    def bump(self):
        self.theta = self.theta - np.pi
        if self.x<0.0:
            self.x = 1.0
            self.theta = self.theta + np.pi
        if self.x>1000.0:
            self.x = 999.0
            self.theta = self.theta - np.pi
        if self.y<0.0:
            self.y = 1.0
            self.theta = self.theta - np.pi
        if self.y>1000.0:
            self.y = 999.0
            self.theta = self.theta - np.pi
        #self.updateMap()
        self.canvas.delete(self.name)
        self.draw(self.canvas)

class Sofa:
    def __init__(self, namep, xx, yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep
    
    def draw(self, canvas):
        body = canvas.create_rectangle(self.centreX-350,self.centreY-200, \
                                  self.centreX+350,self.centreY+200, \
                                  fill="black",tags=self.name)
        bbox = canvas.bbox("Sofa")
        canvas.create_rectangle(bbox, outline="red")
        
        coords = canvas.coords("Sofa")
        print(coords)


    def getLocation(self):
        return self.centreX, self.centreY              

class SmallTable:
    def __init__(self, namep, xx, yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep
    
    def draw(self, canvas):
        body = canvas.create_rectangle(self.centreX-200,self.centreY-100, \
                                  self.centreX+200,self.centreY+100, \
                                  fill="brown",tags=self.name)
            
        bbox = canvas.bbox("SmallTable")
        canvas.create_rectangle(bbox, outline="red")
        
        coords = canvas.coords("SmallTable")
        print(coords)

    def getLocation(self):
        return self.centreX, self.centreY  
    
    def brain(self):
        pass

class Bed:
    def __init__(self, namep, xx, yy): #centre = 500, 50
        self.centreX = xx
        self.centreY = yy
        self.name = namep
        self.x = np.arange(200, 800, 15)
        self.y = np.arange(50, 500, 15)
        self.xedges = np.linspace(200, 800, 15)
        #self.yedges = np.arange()
        self.edge2 = xx + 300
        self.edge3 = yy
        self.edge4 = yy + 500
    
    def draw(self, canvas):
        body = canvas.create_rectangle(200,0,800,500,\
                                  fill="black",tags=self.name)
        bbox = canvas.bbox("Bed")
        canvas.create_rectangle(bbox, outline="red")
        
        coords = canvas.coords("Bed")
        print(coords)

    def getLocation(self):
        return self.centreX, self.centreY
    
    def brain(self):
        pass

class Table:
    def __init__(self, namep, xx, yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep
    
    def draw(self, canvas):
        body = canvas.create_rectangle(self.centreX-200,self.centreY-150, \
                                  self.centreX+200,self.centreY+150, \
                                  fill="brown",tags=self.name)
        
        bbox = canvas.bbox("Table")
        canvas.create_rectangle(bbox, outline="red")
        
        coords = canvas.coords("Table")
        print(coords)


    def getLocation(self):
        return self.centreX, self.centreY  
    
    def brain(self):
        pass
    
class Dirt:
    def __init__(self,namep,xx,yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep

    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-1,self.centreY-1, \
                                  self.centreX+1,self.centreY+1, \
                                  fill="grey",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY

def buttonClicked(x,y,registryActives):
    for rr in registryActives:
        if isinstance(rr,Bot):
            rr.x = x
            rr.y = y

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def placeDirt(registryPassives,canvas):
    #places dirt in a specific configuration
    map = np.zeros( (10,10), dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                map[xx][yy] = random.randrange(1,5)
    # for yy in range(0,10):
    #     map[8][yy] = 10
    # for xx in range(1,8):
    #     map[xx][0] = 10
    map[0][0] = 3
    map[9][9] = 0
    i = 0
    for xx in range(10):
        for yy in range(10):
            for _ in range(map[xx][yy]):
                dirtX = xx*100 + random.randrange(0,99)
                dirtY = yy*100 + random.randrange(0,99)
                dirt = Dirt("Dirt"+str(i),dirtX,dirtY)
                registryPassives.append(dirt)
                dirt.draw(canvas)
                i += 1
    #print(np.transpose(map))
    return map

def register(canvas, population):
    registryActives = []
    registryPassives = []
    noOfBots = 1
    # smalltable1 = SmallTable("SmallTable", 0, 50) #Bedroom
    # smalltable2 = SmallTable("SmallTable", 800, 50) #Bedroom
    # registryPassives.append(smalltable1) #Bedroom
    # registryPassives.append(smalltable2) #Bedroom
    # smalltable1.draw(canvas) #Bedroom
    # smalltable2.draw(canvas) #Bedroom
    # bed = Bed("Bed", 500, 50) #Bedroom
    # registryPassives.append(bed) #Bedroom
    # bed.draw(canvas) #Bedroom
    # sofa = Sofa("Sofa",500,50)
    # table = Table("Table", 500, 950) 
    # registryPassives.append(sofa) #Living Room
    # sofa.draw(canvas)
    # table.draw(canvas)
    # registryPassives.append(table) 
    # table.draw(canvas) 
    for i in range(0,noOfBots):
        bot = Bot("Bot"+str(i),canvas)
        registryActives.append(bot)
        bot.draw(canvas)
    map = placeDirt(registryPassives,canvas)
    #path = aStarSearch(map)
    #path = makeRandomPath1step(20) #This now outputs path and choices
    path = choicesToPath(population)
    count = Counter(canvas)
    canvas.bind( "<Button-1>", lambda event: buttonClicked(event.x,event.y,registryActives) )
    return registryActives, registryPassives, count, map, path

def moveIt(canvas,registryActives,registryPassives,count,moves,window, path):
    moves += 1
    for rr in registryActives:
        if isinstance(rr, Bot):
            rr.brain(path, count, window)
            rr.move(canvas,registryPassives,1.0)
            #rr.directionMove(count, window, newdir)
            registryPassives = rr.collectDirt(canvas,registryPassives, count)
            #registryPassives = rr.collectDirt(canvas,registryPassives, count)
            #rr.checkForDanger(dangerThreshold, registryActives)
            collision = rr.collision(registryPassives, canvas)
#            collision = rr.coliision()
        if path == False:
            numberOfMoves = 2000
        #print(moves)
            if moves>numberOfMoves:
                print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
                window.destroy()
        if path != False:
            numberOfMoves = 2000
            if moves>numberOfMoves:
                print("Path Failure")
                print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
                success.append(0)
                #print(success)
                window.destroy()
            if len(path) == 0:
                print("Path Successful")
                print("Total dirt collected in path is", count.dirtCollected, ". Moves = ", moves)
                success.append(1)
                #print(success)
                window.destroy()
    canvas.after(100,moveIt,canvas,registryActives,registryPassives,count,moves,window, path) #Set to 0 for no graphics -> Quiet mode

def main(mode, population):
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map, path = register(canvas, population)
    moves = 0
    if mode == "GA":
        path, choices = makeRandomPath1step(20)
    elif mode == "A":
        path = aStarSearch(map)
        choices = 0
    #path = choicesToPath(population)
    path1 = copy.deepcopy(path)
    moveIt(canvas,registryActives,registryPassives, count, moves, window, path)
    window.mainloop()
    return count.dirtCollected, path1, choices

def main2():
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map, path = register(canvas, population)
    moves = 0
    #path = aStarSearch(map)
    pathdefaults, choices = makeRandomPath1step(20)
    path = choicesToPath(choices)
    #path = choicesToPath(population)
    path1 = copy.deepcopy(path)
    moveIt(canvas,registryActives,registryPassives, count, moves, window, path)
    window.mainloop()
    return count.dirtCollected, path1

def runSetOfExperiments(numberOfRuns, mode, initalpop):
    dirtCollectedList = []
    pop = []
    for _ in range(numberOfRuns):
        dirt, path, choices = main(mode, initialpop)
        dirtCollectedList.append(dirt)
        pop.append(path)
    return dirtCollectedList, path

start_time = time.time()
avsSS, avsS, choices = main("A", initialpop)
print("--- %s seconds ---" % (time.time() - start_time))

#%%
#Run A* Code
def aStarAvs(runs):
    avsS = []
    for i in range(400):
        dirt, path = runSetOfExperiments(1,"A")
        aStarAverage = np.average(dirt)
        avsS.append(aStarAverage)
        
    starstd = np.std(avsSS)
    megaaverageA = np.average(avsS)
    return avsS, aStarAverage, starstd, megaaverageA

start_time = time.time()
avsSS, avsS, starstd, megaaverageA = aStarAvs(30)
print("--- %s seconds ---" % (time.time() - start_time))

#%%
global success
success = [] #multiply fitness[i] by success[i], so fitness = 0 if failed. Success = 1, faliure = 0
np.array(success)

def geneticMain(population):
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, map, path = register(canvas, population)
    moves = 0
    path = choicesToPath(population)
    #path = aStarSearch(map)
    path1 = copy.deepcopy(path)
    moveIt(canvas,registryActives,registryPassives, count, moves, window, path)
    window.mainloop()
    return count.dirtCollected#,path1

def popFitPairs3(initialpop):
    fitness22 = []
    success = []
    averages2 = []
    bests2 = []
    population1 = copy.deepcopy(initialpop)
    count = 0
    
    for i in range(len(initialpop)):
        count += 1
        fitness22.append(geneticMain(initialpop[i]))
        #fitnessnorm2 = [fitness22*success for fitness22, success in zip(fitness22, success)]
        # print(fitnessnorm22)
        averages2.append(sum(fitness22)/count)
        print("av ",sum(fitness22)/count)
        bests2.append(max(fitness22))
        print("max ",max(fitness22))
    
    pairs = list(zip(population1,fitness22))
    
    return pairs, fitness22, averages2, bests2

def runGA3(numberInGeneration, tournamentSize, popSiz, numberOfGenerations):
    totalfitness = []
    totalavs = []
    totalbests = []
    bestGenestotal = []
    count = 0
    avs2g = []
    bests2g = []
    poptot = []
    
    population1 = initialPopulation(20)
    poptot.append(population1)
    
    for i in range(numberOfGenerations):
        count += 1
        print("Generation: ", count)
        pairs, fitness, averages, bests = popFitPairs3(population1)
        # if pairs[i]*success[i] == 0:
        #     fitness[i] = 0
        totalfitness.append(fitness)
        totalavs.append(averages)
        avs2g.append(averages)
        bests2g.append(bests)
        totalbests.append(bests)
        parent1, parent2, population1, bestGene, bestGenes, tourney = tournament(pairs, tournamentSize, popSiz)
        population2 = copy.deepcopy(population1)
        poptot.append(population1)
        
    return totalfitness, totalavs, totalbests, parent1, parent2, poptot, bestGene, bestGenes, tourney


start_time = time.time()
fitness, avs, bests, p1, p2, popList, bestGene, bestGenes, tourney = runGA3(4, 4, 4, 4) #734.5447750091553 seconds for 10,4,10,100
print("--- %s seconds ---" % (time.time() - start_time))

#Takes 1622.1312 seconds for 20,8,20,100
#432.415 seconds for 10,4,10,60
#207.18511176109314 seconds for 10,4,10,30

#%%

def GAStatistics(avs, bests, fitness, popList):
    avsU = [] #U denotes unwrapping the list of lists 
    bestsU = []
    fitnessU = []
    popListU = []
    sumavs = []
    sumbests = []
    sumfits = []
    
    for i in range(len(avs)):
        sumi = sum(avs[i])
        sumavs.append(sumi)
    
    for i in range(len(bests)):
        sumj = sum(bests[i])
        sumbests.append(sumj)

    for i in range(len(fitness)):
        sumk = sum(avs[i])
        sumfits.append(sumk)

    for i in range(len(avs)):
        for j in range(len(avs[i])):
            avsU.append(avs[i][j])
    
    for i in range(len(bests)):
        for j in range(len(bests[i])):
            bestsU.append(bests[i][j])
            
    for i in range(len(fitness)):
        for j in range(len(fitness[i])):
            fitnessU.append(fitness[i][j])
    
    for i in range(len(popList)):
        for j in range(len(popList[i])):
            popListU.append(popList[i][j])
    
    maxpos = fitnessU.index(max(fitnessU))
    maxpathdirt = popListU[maxpos]
    
    megaaverageGA = np.average(avsU)
    stdGA = np.std(avsU)
    
    # normavs = [avsU*success for avsU,success in zip(avsU,success)]
    # normavsNon0 = [i for i in normavs if i != 0]

    return sumavs, sumbests, sumfits, avsU, bestsU, fitnessU, popListU, maxpathdirt, megaaverageGA, stdGA#,normavs, normavsNon0

#%%
avsSS = 0
def comparativeStats(avsU, avsSS, fitnessU, bestsU, sumavs, sumbests, sumfits):
    fig1 = plt.subplot(121)
    
    plt.plot(sumavs)
    plt.plot(sumbests)
    plt.xlabel("Generation")
    plt.ylabel("Averages")
    
    fig1 = plt.subplot(121)
    plt.plot(sumavs)
    plt.plot(sumbests)
    plt.xlabel("Generation")
    plt.ylabel("Averages")
    
    fig2 = plt.subplot(122)
    plt.plot(sumfits)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    
    # plt.plot(normavsNon0)
    # plt.xlabel("Iteration")
    # plt.ylabel("Average Value")
    
    fig3 = plt.figure()
    data = {"A*": [avsSS], "GA":[avsU]}
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data = pd.DataFrame({"A*": avsSS, "GA": avsU})
    ax = data[['A*', 'GA']].plot(kind='box', title='Map 1')
    plt.show()
        

    sample1 = avsU
    sample2 = avsSS
    t_stat, p_value = ttest_ind(sample1, sample2)
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)
    
    return fig1, fig2, fig3, t_stat, p_value

#%%
sumavs, sumbests, sumfits, avsU, bestsU, fitnessU, popListU, maxpathdirt, megaaverageGA, stdGA = GAStatistics(avs, bests, fitness, popList)
comparativeStats(avsU, avsSS, fitnessU, bestsU, sumavs, sumbests, sumfits)
