import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_forward
import mnist_backward
TEST_INTERVAL_SECS = 5

def test(minst):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
        y_ = tf.placeholder(tf.float32, [None, mnist_forward.ONPUT_NODE])
        y = mnist_forward.forward(x, None)

        ema = tf.train.ExponentialMovingAverage(mnist_backward.MOVING_AVERAGE_DECAY)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)

        correct_prediction = tf.equal(tf.arg_max(y, 1), tf.arg_max(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        while True:
            with tf.Session() as sess:
                ckpt = tf.train.get_checkpoint_state(mnist_backward.MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    global_step = ckpt.model_checkpoint_path.split("/")[-1].split('-')[-1]
                    accuracy_score = sess.run(accuracy, feed_dict={x: minst.test.images, y_: minst.test.labels})
                    print("After %s training step(s), test accuracy = %g" % (global_step, accuracy_score))
                else:
                    print('No checkpoint file found')
            time.sleep(TEST_INTERVAL_SECS)

def main():
    minst = input_data.read_data_sets("./data", one_hot=True)
    test(minst)

if   __name__ == '__main__':
  main()