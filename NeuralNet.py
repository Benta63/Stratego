import numpy as np
import random
import tensorflow as tf
import scipy.misc
import os
import csv
import time
import itertools

class Trainer(object):
	def __init__(self):
		#Setting training parameters
		self.batch_size = 4 #Number of experience traces per training step
		self.updaes = 5 #How often to perform a training set
		self.path = "./Models" #Where the saved models are
		self.num_episodes = 5 #How many game environments to train with
		self.pre_steps = 50 #Number of random actions before training begins
		self.startE = 1 #Starting chance of random action
		self.endE = 0.1 #Final chance of random action
		self.loadModel = False #Should we load a saved model?
		self.timePerStep = 1 #Length of each step used
		self.tau = 0.001
		tf.reset_default_graph()

		#Here we create the networks

		## Add networks after you create them
		self.rewardPath = "data/rewards"
		#Define this function lower

		#self.clearFile(self.rewardPath)
	
	def updateTargetGraph(self, tfVars, tau):
		total_vars = len(tfVars)
		op_holder = []
		for ids, var in enumerate(tfvars[0:total_vars//2]):
			op_holder.append(tfvars[ids:total_vars//2].assign((var.value()*tau) + ((1-tau)*tfvars[ids+total_vars//2].value)))
		return op_holder	

	def updateTarget(self, op_holder):
		for op in op_holder:
			self.sess.run(op)

	def close_sess(self):
		self.ses.close()

	def writeToFile(self, path, data):
		f = open(path, 'a')
		f.write(data)
		f.close()
	def clearFile(self, path):
		f = open(path, 'w')
		f.write('')
		f.close()

	def init_episode(self, vec84, epnum, steps):
		if epnum == 0:
			self.init = tf.global_variables_initializer()
			self.targetOps = self.updateTargetGraph(tf.trainable_variables(),self.tau)
			#self.myBuffer = #NEED TO MAKE A BUFFER CLASS
			#TODO: Need to decrease rate of random actions

			self.sess = tf.Session()
			self.sess.run(self.init)
		else: #The end of an episode update
			#Write to file
			#Buffer stuff
			#Need to make some lists
			print("Placeholder")
		self.s = vec84
		self.rAll = 0

	def makeMove(self):
		print ("Placeholder")

	def trainReward(self):
		print("Placeholder")
