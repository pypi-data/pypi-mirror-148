import sys, os

from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Lambda, Dropout, Concatenate, Reshape
import tensorflow.keras.backend as K
from mechanoChemML.src.transform_layer import Transform
import tensorflow as tf

import numpy as np


class IDNN(tf.keras.Model):
  
  """
  Integrable deep neural network (idnn)
  Keras model class.

  :param input_dim: Size of input vector
  :type input_dim: int

  :param hidden_units: List containing the number of neurons in each hidden layer
  :type hidden_units: [int]

  :param dropout: Dropout parameter applied after each hidden layer (default is None)
  :type dropout: float

  :param transforms: List of functions to transform the input vector, applied before the first hidden layer (default is None)
  :type transforms: [function]

  :param unique_inputs: if True, requires separate input vectors for the function, its gradient, and its Hessian; if False, assumes the same input vector will be used for function and all derivatives
  :type unique_inputs: bool

  :param final_bias: if True, a bias is applied to the output layer (this cannot be used if only derivative data is used in training); if False, no bias is applied to the output layer (default is False)
  :type final_bias: bool

  The idnn can be trained with first derivative (gradient) data, second derivative (Hessian) data, and/or data from the function itself. (If only derivative data is used then the ``final_bias`` parameter must be ``False``.) The training data for the function and its derivatives can be given at the same input values (in which case, ``unique_inputs`` should be ``False``), or at different input values, e.g. providing the function values at :math:`x \in \{0,1,2,3\}` and the derivative values at :math:`x \in \{0.5,1.5,2.5,3.5\}` (requiring ``unique_inputs`` to be ``True``). Even when ``unique_inputs`` is ``True``, however, the same number of data points must be given for the derivatives and function, even though the input values themselves are different. So, for example, if one had first derivative values at :math:`x \in \{0,1,2,3\}` and second derivative values only at :math:`x \in \{0.5,1.5,2.5\}`, then some of the second derivative data would need to be repeated to that the number of data points are equal, e.g. :math:`x \in \{0.5,1.5,2.5,2.5\}`. Currently, the IDNN structure assumes the function output is a scalar, the gradient is a vector, and the Hessian is a matrix.

  The following is an example where values for the function and the first derivative are used for training, but they are known at different input values. Note that the loss and loss_weights are defined only for the given data (function data and first derivatative data), but fictitious data has to be given for the second derivative or an error will be thrown:

  .. code-block:: python 

     idnn = IDNN(1,
            [20,20],
            unique_inputs=True,
            final_bias=True)

     idnn.compile(loss=['mse','mse',None],
             loss_weights=[0.01,1,None],
             optimizer=keras.optimizers.RMSprop(lr=0.01))

     idnn.fit([c_train0,c_train,0*c_train],
              [g_train0,mu_train,0*mu_train],
              epochs=50000,
              batch_size=20)

  """

  def __init__(self, input_dim,hidden_units,activation='softplus',dropout=None,transforms=None,unique_inputs=False,final_bias=False):
    super().__init__()
    
    self.transforms = transforms
    self.unique_inputs = unique_inputs
    
    # Define dense layers
    self.dnn_layers = []
    self.dnn_layers.append(Dense(hidden_units[0], activation=activation, input_dim=input_dim))
    for i in range(1,len(hidden_units)):
      self.dnn_layers.append(Dense(hidden_units[i], activation=activation))
      if dropout:
        self.dnn_layers.append(Dropout(dropout))
    self.dnn_layers.append(Dense(1,use_bias=final_bias))
        
  @tf.function(autograph=False)
  def call(self, inputs):

    def DNN(y):
      if self.transforms:
        y = Transform(self.transforms)(y)
      for layer in self.dnn_layers:
        y = layer(y)
      return y

    if self.unique_inputs:
      x1 = inputs[0]
      x2 = inputs[1]
      x3 = inputs[2]
      
      y = DNN(x1)
      
      with tf.GradientTape() as g:
        g.watch(x2)
        y2 = DNN(x2)
      dy = g.gradient(y2,x2)
      
      with tf.GradientTape() as g2:
        g2.watch(x3)
        with tf.GradientTape() as g1:
          g1.watch(x3)
          y3 = DNN(x3)
        dy3 = g1.gradient(y3,x3)
      ddy = g2.batch_jacobian(dy3,x3)
      
    else:
      x1 = inputs
      with tf.GradientTape() as g2:
        g2.watch(x1)
        with tf.GradientTape() as g1:
          g1.watch(x1)
          y = DNN(x1)
        dy = g1.gradient(y,x1)
      ddy = g2.batch_jacobian(dy,x1)

    return [y,dy,ddy]  


def convex(M):

    # Check if positive definite
    try:
        np.linalg.cholesky(0.5*(M+M.T))
        return 1
    except np.linalg.LinAlgError:
        return 0

def convexMult(Ms):

    ind = np.zeros(Ms.shape[0],dtype=np.bool)
    for i in range(Ms.shape[0]):
        ind[i] = convex(Ms[i])

    return ind

def find_wells(idnn,x,dim=4,bounds=[0,0.25],rereference=True):

    # Find "wells" (regions of convexity, with low gradient norm)

    # First, rereference the free energy
    if idnn.unique_inputs:
        pred = idnn.predict([x,x,x])
    else:
        pred = idnn.predict(x)
    mu_test = 0.01*pred[1]
    if rereference:
        eta_test = np.array([bounds[0]*np.ones(dim),
                             bounds[1]*np.ones(dim)])
        if idnn.unique_inputs:
            y = 0.01*idnn.predict([eta_test,eta_test,eta_test])[0]
        else:
            y = 0.01*idnn.predict(eta_test)[0]
        g0 = y[0,0]
        g1 = y[1,0]
        mu_test[:,0] = mu_test[:,0] - 1./bounds[1]*(g1 - g0)
    gradNorm = np.sqrt(np.sum(mu_test**2,axis=-1))

    H = pred[2] # get the list of Hessian matrices
    ind2 = convexMult(H) # indices of points with local convexity
    eta = x[ind2]
    gradNorm = gradNorm[ind2]

    ind3 = np.argsort(gradNorm)
    
    # Return eta values with local convexity, sorted by gradient norm (low to high)

    return eta[ind3]
