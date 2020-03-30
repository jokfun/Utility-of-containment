from random import uniform
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import os
import shutil
import tqdm

#Delete the file in which the images will be stored, otherwise create it.
folder = "output"
try:
	shutil.rmtree(folder)
except Exception as e:
	print(e)
if not os.path.exists(folder):
    os.makedirs(folder)

def save():
	"""
		Convert the generated images of the simulation into a .mp4 video
	"""
	os.system("ffmpeg -r 120 -i output/%01d_save.png -vcodec mpeg4 -y movie.mp4")

class Dot:
	def __init__(self,maxX,maxY,infected=False):
		"""
			A dot is an individual in the population

			Required parameters : 
			maxX : length of of the area
			maxY : width of the area

			Optionnal parameters : 
			infected : if the dot is infected, default : False
		"""

		#Generate a position for the dot
		self.x = round(uniform(0,maxX),2)
		self.y = round(uniform(0,maxY),2)

		#Fix var
		self.infected = infected
		self.maxX = maxX
		self.maxY = maxY

	def update(self,chance_to_move=0.5,length_move=0.8):
		"""
			Update the position of the dot

			Optionnal parameters :
			chance_to_move : the probability for the dot to move, default : 0.5
			length_move : maximum distance the point can travel on the x or y axis, default : 0.8
		"""
		if uniform(0,1)<=chance_to_move:
			newX = self.x + round(uniform(-length_move,length_move),2)
			newY = self.y + round(uniform(-length_move,length_move),2)
			#If the position escapes the map, create a new one
			while newX<0 or newY<0 or newX>self.maxX or newY>self.maxY:
				newX = self.x + round(uniform(-length_move,length_move),2)
				newY = self.y + round(uniform(-length_move,length_move),2)
			self.x = newX
			self.y = newY

class Population:
	def __init__(self,quantity,maxX,maxY,chance_to_move=0.1,length_move=0.5,infected_rate=0.01):
		"""
			Create a population of individuals

			Required parameters : 
			quantity : number of individuals in the population
			maxX : length of of the area
			maxY : width of the area

			Optionnal parameters :
			chance_to_move : the probability for the dot to move, default : 0.5
			length_move : maximum distance the point can travel on the x or y axis, default : 0.8
			infected_rate : probability of an individual being infected at its creation

		"""

		#Fix var
		self.maxX = maxX
		self.maxY = maxY
		self.chance_to_move = chance_to_move
		self.length_move = length_move

		#Part of the population will be infected, the other not
		isInfected = int(quantity*infected_rate)
		if isInfected==0:
			isInfected=1

		#Create the population
		self.population = []
		for count in range(quantity):
			dot = Dot(maxX,maxY)
			if count<isInfected:
				dot.infected = True
			self.population.append(dot)

	def rateInfected(self):
		"""
			Calculate the rate of infection in the population
		"""
		rate = 0
		for dot in self.population:
			if dot.infected==True:
				rate+=1
		self.areInfected = rate
		return rate/len(self.population)

	def whoIsInfected(self,episode=None):
		"""
			Display the rate of infection in the population

			Optional parameters :
			episode : episode in the simulation
		"""
		rate = self.rateInfected()
		add=""
		if episode!=None:
			add="Episode : "+str(episode)+","
		print(add+"Population infected : ",rate)

	def updateInfected(self):
		"""
			Updating infected people in the population
			Be careful, the larger the population and the higher the rate of infected people. 
		"""
		for i in range(len(self.population)-1):
			dot = self.population[i]
			if dot.infected == True:
				for j in range(i+1,len(self.population)):
					neighboor = self.population[j]
					"""
						The distance to a neighbour is calculated with an Euclidean distance
						The max value == 1. was determined after several tests.
					"""
					if neighboor.infected==False and sqrt((dot.x-neighboor.x)**2 + (dot.y-neighboor.y)**2)<=1.:
						neighboor.infected=True

	def drawPopulation(self,episode):
		"""
			Draw on a figure the evolution of the population

			There will be three charts:
			- the simulation with all individuals according to their infection status at time t
			- the evolution of the infection rate
			- the variables used to generate the population

			Required parameters :
			- episode : time t during the simulation
		"""
		fig = plt.figure(1)
		gridspec.GridSpec(2,2,wspace=3.,hspace=3.)

		#First plot, the simulation
		plt.subplot2grid((2,2), (0,0), colspan=1, rowspan=2)
		plt.xlim(0,self.maxX)
		plt.ylim(0,self.maxY)

		xRed = [dot.x for dot in self.population if dot.infected==True]
		yRed = [dot.y for dot in self.population if dot.infected==True]
		plt.scatter(xRed, yRed, s=6,c="r")

		xBlue = [dot.x for dot in self.population if dot.infected!=True]
		yBlue = [dot.y for dot in self.population if dot.infected!=True]
		plt.scatter(xBlue, yBlue, s=6,c="b")

		plt.yticks([])
		plt.xticks([])

		plt.title("Simulation of population movements")

		#Second plot, the evolution of the infected rate
		plt.subplot2grid((2,2), (0,1))
		plt.xlim(0,self.episodes)
		plt.ylim(0,1)
		plt.plot(self.cases)
		plt.title("Evolution of cases")

		#Third plot, the cars used of the simulation
		plt.subplot2grid((2,2), (1,1))
		plt.yticks([])
		plt.xticks([])
		plt.axis('off')
		plt.ylim(0,3)
		plt.text(0,0,"Chance to move : "+str(self.chance_to_move))
		plt.text(0,1,"Length of a move : "+str(self.length_move))
		plt.text(0,2,"Number infected : "+str(self.areInfected))
		plt.text(0,3,"Size of the population : "+str(len(self.population)))

		fig.savefig("output/"+str(episode)+'_save.png')
		plt.close(fig)

	def run(self,episodes=50):
		"""
			Main loop creating the simulation

			Optionnal parameters :
			episodes : number of episodes for the simulation
		"""
		self.cases = []
		self.episodes = episodes
		print("Creating the simulation..")
		for episode in tqdm.trange(self.episodes):
			for dot in self.population:
				dot.update(self.chance_to_move,self.length_move)
			self.updateInfected()
			self.cases.append(self.rateInfected())
			self.drawPopulation(episode)
		#At the end of the simulation we create the video of the simulation
		save()

if __name__ == "__main__":

	"""
		CUSTOM THE HYPERPARAMETERS HERE
	"""
	size_population = 150
	borderX = 20
	borderY = 20
	episodes = 3000
	chance_to_move = 0.01
	length_move = 0.2

	population = Population(size_population,borderX,borderY,chance_to_move,length_move)
	population.run(episodes)
