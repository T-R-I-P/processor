import tensorflow as tf
import numpy as np

  x = tf.placeholder(tf.float32,[None, 8])
sess = tf.Session("grpc://localhost:2222", config=tf.ConfigProto(log_device_placement=True))
#timestamp1 here
init = tf.initialize_all_variables()
print(">>> TensorFlow Session Run:")
sess.run(init)

for i in range(int(rangeCount)):
  # Fetch data from HBase (code deleted)
  x_ = [x0,x1,x2,x3,x4,x5,x6,x7]
  x_ = np.reshape(x_, (-1, 8))
  tmpY = [0]*600
  tmpY[rd.randint(0,600-1)] = 1
  tmpY = np.reshape(tmpY, (-1,600))
  result = sess.run(train_step, feed_dict={x: x_, y_4_:tmpY}) # input feed here
sess.close()
# timestamp2 here
