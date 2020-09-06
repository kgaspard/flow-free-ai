import tensorflow as tf
def limit_gpu():
  gpus = tf.config.experimental.list_physical_devices('GPU')
  tf.config.experimental.set_visible_devices([], 'GPU')