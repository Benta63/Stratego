import numpy as np
import random
import tensorflow as tf
import scipy.misc
import os
#Make Environments later


import time
import itertools
class PlaceNetwork(object):
	def __init__(self):
		self.X = tf.placeholder("float", [None, 64])
		self.B1 = tf.Variable(tf.zeros([1]))
		self.W1 = tf.Variable(tf.truncated_normal([64, 44], stddev=0.1))
		self.B2A = tf.Variable(tf.zeros([1]))
		self.W2A = tf.Variable(tf.truncated_normal([44, 22], stddev=0.1))
		self.B2V = tf.Variable(tf.zeros([1]))
		self.W2V = tf.Variable(tf.truncated_normal([44,22], stddev=0.1))

		#May have to switch the B's to the end for this. I don't remember
		self.Y1 = tf.nn.relu(self.B1 + tf.matmul(self.X, self.W1))
		self.Y2A = tf.nn.relu(self.B2A + tf.matmul(self.Y1, self.W2A))
		self.Y2V = tf.nn.relu(self.B2V + tf.matmul(self.Y1, self.W2V))

		self.AW = tf.Variable(tf.truncated_normal([22,32]))
		self.VW = tf.Variable(tf.truncated_normal([22, 1]))

		self.Advantage = tf.matmul(self.Y2A, self.AW)
		self.Value = tf.matmul(self.Y2V, self.VW)

		self.salience = tf.gradients(self.Advantage, self.X)

		self.Qout = self.Value + tf.subtract(self.Advantage, tf.reduce_mean(self.Advantage, axis=1, keep_dims=True))
		self.predict = tf.argmax(self.Qout, 1)

		#Getting the loss by getting the difference in squares between the target and the predicted Qs
		self.targetQ = tf.placeholder(shape=[None], dtype=tf.float32)
		self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
		self.actions_onehot = tf.onehot(self.actions, 32, dtype=tf.float32)

		self.Q = tf.reduce_sum(tf.end_multiply(self.Qout, self.actions_onehot), axis=1)

		self.td_error = tf.square(self.targetQ - self.Q)
		self.loss = tf.reduce_mean(self.td_error)
		self.trainer = tf.train.AdamOptimizer(learning_rate= 0.00001)
		self.updateModel = self.trainer.minimize(self.loss)

#Should I make a dueling NN?? Would be literally the same in all but name of the place network

class experience_buffer(object):
	def __init__(self, buffer_size= 100000):
		self.buffer = []
		self.buffer_size = buffer_size

	def add(self, experience):
		if len(self.buffer) + len(experience) >= self.buffer_size:
			self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
		self.buffer.extend(experience)

	def sample(self, size):
		return np.reshape(np.array(random.sample(self.buffer, size)), [size, 5])

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
		self.load_model = False



		self.tau = 0.001

		tf.reset_default_graph()

		#Here we create the networks

		## Add networks after you create them
		self.rewardPath = "data/rewards"
		self.clearFile(self.rewardPath)
		#Define this function lower
		self.mainPN = PlaceNetwork()
		self.targetPN = PlaceNetwork()

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

	def init_episode(self, vec100, epnum, steps):
		if epnum == 0:
			self.init = tf.global_variables_initializer()
			self.targetOps = self.updateTargetGraph(tf.trainable_variables(),self.tau)
			self.myBuffer = experience_buffer()


			#self.myBuffer = #NEED TO MAKE A BUFFER CLASS
			#Setting the random action decrease
			self.e = self.startE
			self.stepDrop = (self.startE - self.endE)/self.annealing_steps
			self.jList = {}
			self.rList = {}

			self.sess = tf.Session()
			self.sess.run(self.init)
		else: #The end of an episode update
			#self.writeToFile(self.rewardPath, '{}|{}|{}|{}\n'.format(self.))
			self.myBuffer.add(self.episodeBuffer.buffer)
			self.jList.append(steps)
			self.rList.append(self.rAll)
		self.episodeBuffer = experience_buffer()
		self.s = vec100 #The whole board
		return
	def get_moves(self, turn):
		total_steps = turn
		#Choose a greedy action with an e chance of randomness
		if np.random.rand(1) < self.e or total_steps < self.pre_steps:
			self.a1 = np.random.randint(0, 100) #100
			self.place = np.random.rand(1,100)[0]
		else:
			self.a1 = self.sess.run(self.mainPN.predict,food_dict={self.mainPN.X:[self.s]})[0]
			self.place = self.sess.run(self.mainPN.Qout,fend_dict={self.mainPN.X:[self.s]})[0]
		return self.place

	def trainReward(self, vec100, r, total_steps):
		print("T steps: {} -- pt steps: {}".format(total_steps, self.pre_train_steps))
		s1 = vec_100
		self.episodeBuffer.add(np.reshape(np.array([self.s, self.a1, self.a2, r, s1]), [1,6]))

		if total+steps > self.pre_steps:
			if self.e > self.endE:
				self.e -= self.stepDrop

			if total_steps % (self.update_freq) == 0:
				#Get some randomness
				trainBatch = self.myBuffer.sample(self.batch_size)
				 #Below we operate the neural network
				P1 = self.sess.run(self.mainPN.predict,feed_dict={self.mainPN.X:np.vstack(trainBatch[:,4])})
				P2 = self.sess.run(self.targetPN.predict,feed_dict={self.targetPN.X:np.vstack(trainBatch[:,4])})

				end_multiplier = - (trainBatch[:,5] - 1)
				 
				sizeP = P2[rand(batch_size), P1]

				targetP = trainBatch[:,3] + (y*doubleP * end_multiplier)
				#Update neural network with new target values
				up = self.sess.run(self.mainPN.updateModel, feed_dict={self.mainPN.X:np.vstack(trainBatch[:,0]),
				 					self.mainPN.targetQ:targetP,
				 					self.mainPN.action:trainBatch[:, 1]})


				self.updateTarget(self.targetOps)

		self.rAll += r
		self.s = s1

	def first_game(self, vec100, r):
		s1 = vec100
		self.episodeBuffer.add(np.reshape(np.array([self.s, self.a1, self.a2, r, s1]),[1,5]))
		self.rAll += r
		self.s = s1

