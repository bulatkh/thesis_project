import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def create_nn_and_train(size, out_size, conv_size, pool_size, learn_rate, train_x, train_y, test_x, test_y, val_x, val_y):
    with tf.name_scope('input_layer'):
        x = tf.placeholder(tf.float32, [None, size, size], name='x')
        y = tf.placeholder(tf.float32, [None, out_size], name='y')
        x_image = tf.reshape(x, [-1, size, size, 1], name='image')

    with tf.name_scope('convolutional_layer-1'):
        with tf.name_scope('params'):
            W_conv_0 = tf.Variable(tf.truncated_normal([conv_size, conv_size, 1, 32], stddev=0.1), name='W')
            b_conv_0 = tf.Variable(tf.constant(0.1, shape=[32]), name='b')
        conv_0_logit = tf.add(tf.nn.conv2d(x_image, W_conv_0, strides=[1, 1, 1, 1], padding='SAME'), b_conv_0, name='logit')
        h_conv_0 = tf.nn.relu(conv_0_logit, name='relu')

    with tf.name_scope('pool_layer-1'):
        h_pool_0 = tf.nn.max_pool(h_conv_0, ksize=[1, pool_size, pool_size, 1], strides=[1,pool_size,pool_size,1], padding='SAME')

    with tf.name_scope('convolutional_layer-2'):
        with tf.name_scope('params'):
            W_conv_1 = tf.Variable(tf.truncated_normal([conv_size, conv_size, 32, 64], stddev=0.1), name='W')
            b_conv_1 = tf.Variable(tf.constant(0.1, shape=[64]), name='b')
        conv_1_logit = tf.add(tf.nn.conv2d(h_pool_0, W_conv_1, strides=[1, 1, 1, 1], padding='SAME'), b_conv_1, name='logit')
        h_conv_1 = tf.nn.relu(conv_1_logit, name='relu')

    with tf.name_scope('pool_layer-2'):
        h_pool_1 = tf.nn.max_pool(h_conv_1, ksize=[1,pool_size,pool_size,1], strides=[1,pool_size,pool_size,1], padding='SAME')

    with tf.name_scope('convolutional-layer-3'):
        with tf.name_scope('params'):
            W_conv_2 = tf.Variable(tf.truncated_normal([conv_size, conv_size, 64, 128], stddev=0.1), name='W')
            b_conv_2 = tf.Variable(tf.constant(0.1, shape=[128]), name='b')
        conv_2_logit = tf.add(tf.nn.conv2d(h_pool_1, W_conv_2, strides=[1, 1, 1, 1], padding='SAME'), b_conv_2, name='logit')
        h_conv_2 = tf.nn.relu(conv_2_logit, name='relu')

    with tf.name_scope('pool_layer-3'):
        h_pool_2 = tf.nn.max_pool(h_conv_2, ksize=[1, pool_size, pool_size, 1], strides=[1, pool_size, pool_size, 1], padding='SAME')

    with tf.name_scope('fc-1'):
        h_pool_2_flat = tf.reshape(h_pool_2, [-1, 7*7*128], name='flatten')
        with tf.name_scope('params'):
            W_fc_0 = tf.Variable(tf.truncated_normal([7*7*128, 256], stddev=0.1), name='W')
            b_fc_0 = tf.Variable(tf.constant(0.1, shape=[256]), name='b')
        fc_0_logit = tf.add(tf.matmul(h_pool_2_flat, W_fc_0), b_fc_0, name='logit')
        h_fc_0 = tf.nn.relu(fc_0_logit, name='relu')

    with tf.name_scope('fc-2'):
        with tf.name_scope('params'):
            W_fc_1 = tf.Variable(tf.truncated_normal([256, out_size], stddev=0.1), name='W')
            b_fc_1 = tf.Variable(tf.constant(0.1, shape=[out_size]), name='b')
        logit_out = tf.add(tf.matmul(h_fc_0, W_fc_1), b_fc_1, name='logit')

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=logit_out))
    loss_summary = tf.summary.scalar('loss', loss)

    with tf.name_scope('accuracy'):
        correct_prediction = tf.equal(tf.argmax(logit_out, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    accuracy_summary = tf.summary.scalar('accuracy', accuracy)

    train_step = tf.train.AdamOptimizer(learning_rate=learn_rate).minimize(loss)

    init = tf.global_variables_initializer()

    config = tf.ConfigProto(log_device_placement=False)
    config.gpu_options.allow_growth = True
    config.gpu_options.allocator_type = 'BFC'

    sess = tf.Session(config=config)

    sess.run(init)

    summary_writer = tf.summary.FileWriter('../neural_network/logs/adam', sess.graph)

    for i in range(round(len(train_x) / 256) - 1):
        test_count = 0
        batch_xs = train_x[i: i + 256]
        batch_ys = train_y[i: i + 256]

        _, loss_s = sess.run([train_step, loss_summary], feed_dict={x: batch_xs, y: batch_ys})

        if i % 10 == 0:
            summary_writer.add_summary(loss_s, i)

        if i % 100 == 0:
            test_xs = test_x[test_count: test_count + 256]
            test_ys = test_y[test_count: test_count + 256]
            test_count += 1
            acc, acc_s = sess.run([accuracy, accuracy_summary], feed_dict={x: test_xs, y: test_ys})
            print("[%s] Точность распознавания %s" % (i, acc))

    print('Финальная точность : %s' % sess.run(accuracy, feed_dict={
        x: val_x[:100],
        y: val_y[:100]
    }))

    tf.add_to_collection('weights', W_conv_0)
    tf.add_to_collection('weights', W_conv_1)
    tf.add_to_collection('weights', W_conv_2)
    tf.add_to_collection('weights', W_fc_0)
    tf.add_to_collection('weights', W_fc_1)

    tf.add_to_collection('biases', b_conv_0)
    tf.add_to_collection('biases', b_conv_1)
    tf.add_to_collection('biases', b_conv_2)
    tf.add_to_collection('biases', b_fc_0)
    tf.add_to_collection('biases', b_fc_1)

    saver = tf.train.Saver(max_to_keep=1)
    nn_name = input("Имя нейросети:")
    os.mkdir('C:\\Users\\User\\Desktop\\\\Thesis\\trained_nn\\' + nn_name)
    saver.save(sess, 'C:\\Users\\User\\Desktop\\\\Thesis\\trained_nn\\' + nn_name + "\\" + nn_name + ".ckpt",
               global_step=round(len(train_x) / 64))