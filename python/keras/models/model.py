# import tensorflow as tf
# from keras.models import Model
# from keras.layers.merge import concatenate
# from keras.layers.core import Lambda
#
#
# def parallelize(model, parallelism):
#     def get_slice(data, idx, parts):
#         shape = tf.shape(data)
#         size = tf.concat([shape[:1] // parts, shape[1:]], axis=0)
#         stride = tf.concat([shape[:1] // parts, shape[1:]*0], axis=0)
#         start = stride * idx
#         return tf.slice(data, start, size)
#
#     outputs_all = []
#     for i in range(len(model.outputs)):
#         outputs_all.append([])
#
#     # Place a copy of the model on each GPU, each getting a slice of the batch
#     for i in range(parallelism):
#         with tf.device('/gpu:%d' % i):
#             with tf.name_scope('tower_%d' % i) as scope:
#                 print(scope)
#
#                 inputs = []
#                 # Slice each input into a piece for processing on this GPU
#                 for x in model.inputs:
#                     input_shape = tuple(x.get_shape().as_list())[1:]
#                     slice_n = Lambda(get_slice, output_shape=input_shape, arguments={'idx': i, 'parts': parallelism})(x)
#                     inputs.append(slice_n)
#
#                 outputs = model(inputs)
#
#                 if not isinstance(outputs, list):
#                     outputs = [outputs]
#
#                 # Save all the outputs for merging back together later
#                 for l in range(len(outputs)):
#                     outputs_all[l].append(outputs[l])
#
#     # merge outputs on CPU
#     with tf.device('/cpu:0'):
#         merged = []
#         for outputs in outputs_all:
#             merged.append(concatenate(outputs, axis=0))
#
#         return Model(inputs=model.inputs, outputs=merged)
