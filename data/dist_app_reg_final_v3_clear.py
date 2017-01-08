# -*- coding: utf-8 -*-
import tensorflow as tf
import happybase as hb
import random as rd
import numpy as np
import hbForApp as hbfa
import sys
import time

#graph define
__node__(0) { #with tf.device('/job:worker/task:0/gpu:0'):
	with tf.name_scope('input_m_0'):
		x = tf.placeholder(tf.float32,[None, 7], name='input_x')
}
__node__(1) { #with tf.device('/job:worker/task:1/gpu:0'):
	with tf.name_scope('hidden_1_m_1'):
		y1 = tf.Variable(tf.random_uniform([7,200]), name='hidden_layer_y1')
		y_1 = tf.nn.relu(tf.matmul(x,y1))
#tf.histogram_summary('h1m1', y_1)
}
__node__(2) { #with tf.device('/job:worker/task:2/gpu:0'):
	with tf.name_scope('hidden_2_m_2'):
		y2 = tf.Variable(tf.random_uniform([200, 400]), name='hidden_layer_y2')
		y_2 = tf.nn.relu(tf.matmul(y_1,y2))
#tf.histogram_summary('h2m2', y_2)
}
__node__(3) { #with tf.device('/job:worker/task:1/gpu:0'):
	with tf.name_scope('hidden_3_m_1'):
		y3 = tf.Variable(tf.random_uniform([400,500]), name='hidden_layer_y3')
		y_3 = tf.nn.tanh(tf.matmul(y_2, y3))
#tf.histogram_summary('h3m1', y_3)
}
__node__(4) { #with tf.device('/job:worker/task:2/gpu:0'):
	with tf.name_scope('hidden_4_m_2'):
		y4 = tf.Variable(tf.random_uniform([500,378]), name='hidden_layer_y4')
		y_4 = tf.nn.relu(tf.matmul(y_3, y4))
#tf.histogram_summary('h4m2', y_4)
}
__node__(5) { #with tf.device('/job:worker/task:0/gpu:0'):
	with tf.name_scope('output_m_0'):
		y = tf.placeholder(tf.float32, [None,378], name='output_y')
}
__node__(6) { #with tf.device('/job:worker/task:0/gpu:0'):
	cross_entropy = -tf.reduce_sum(y*tf.log(y_4))
	train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
	print ">>> Graph construction done."
}

__execute__(){
#happyBase specification
fa = hbfa.hbAccess()
fa.connOpen()
batchSize = 100
#cluster specification without parameterServer
print(">>> Setting TensorFlow cluster specification...")

#other setting
if len(sys.argv) is 1:
	iteration = 1000
elif len(sys.argv) is 2:
	iteration = sys.argv[1]
elif len(sys.argv) is 3:
	iteration = sys.argv[1]
	batchSize = sys.argv[2]



#setting session
print ">>> Start session configuration..."
sess = tf.Session("grpc://localhost:2222", config=tf.ConfigProto(log_device_placement=True))
init = tf.initialize_all_variables()

'''
timestamp start here
'''
tStart = time.time()

print(">>> TensorFlow Session initiation:")
sess.run(init)
print ">>> Initialtion done."

# Start to run iteration times wtih batchSize datas each iteration
print ">>> Session run..."
for i in range(int(iteration)):
	#writer = tf.train.SummaryWriter("/home/mcas/tensorflow/tb_output", sess.graph)
	#trainData, trainLabel = fa.fetchData(batchSize,0)
	trainData, trainLabel = fa.fetchData_no_buyYear(batchSize,0)
	#result = sess.run(train_step, feed_dict={x: x2_, y: tmp2Y})
	if(i%10 == 0):
		correct = tf.equal(tf.argmax(y_4,1), tf.argmax(y,1))
		accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
		#result = sess.run(accuracy, feed_dict={x: x2_, y: tmp2Y})
		#print("Accuracy rate:" + "{0:.2f}".format(result) + "%")
		#testData, testLabel = fa.fetchData(batchSize,1)
		testData, testLabel = fa.fetchData_no_buyYear(batchSize,1)
		#testData, testLabel = fa.fetchData_no_buyYear(1,1)
		print "*********\n>>>>> Accuracy:", (sess.run(accuracy, feed_dict={x: testData, y: testLabel})), "\n*********"
	else:
		result = sess.run(train_step, feed_dict={x: trainData, y: trainLabel})
	print(">>>>> Progress: "+ "{0:.2f}".format((i+1)/float(iteration)*100) +"%")
testDataFinal, testLabelFinal = fa.fetchData_no_buyYear(1,1)
print "*********\n>>>>> [Final] Accuracy:", (sess.run(accuracy, feed_dict={x: testDataFinal, y: testLabelFinal})), "\n*********"
sess.close()
fa.connClose()

'''
timestamp stop here
'''
tEnd = time.time()
print "It cost %f sec" % (tEnd - tStart)

costTime = tEnd - tStart
}
