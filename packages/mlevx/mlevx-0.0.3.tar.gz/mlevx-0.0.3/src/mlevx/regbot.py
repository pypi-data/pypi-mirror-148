#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire


class Regbot:
  reg_model_path = resource_filename(__name__, 'finalized_model.h5') 
  model_scaler_path = resource_filename(__name__, 'logscaler.gz') 


  def __init__(self,*args):
  	pass



  @classmethod  
  def loadmodel(cls):
    loaded_model = joblib.load(open(f'{cls.reg_model_path}', 'rb'))
    return loaded_model


  @classmethod  
  def prepareInput(cls,opening,closing):
    avr = closing/(opening + closing)
    bvr = opening/(opening + closing)
    alpha = (closing/opening) - 1
    testdata = np.array([[avr,bvr,alpha]])
    scaler = joblib.load(f'{cls.model_scaler_path}')
    testdata = scaler.transform(testdata)

    return testdata


  @classmethod
  def enterSignalGenerator(cls,opening,closing,lthr):
    scalledInput = cls.prepareInput(opening,closing)
    result = (cls.loadmodel().predict_proba(scalledInput)[:,1] > lthr <= 0.9)
    return int(result==True)
    #return (cls.loadmodel().predict(scalledInput) > 0).astype(int)[0]

  @classmethod
  def exitSignalGenerator(cls,opening,closing,lthr):
    scalledInput = cls.prepareInput(opening,closing)
    result = (cls.loadmodel().predict_proba(scalledInput)[:,1] <= lthr)
    return int(result==False)
    #return (cls.loadmodel().predict(scalledInput) > 0).astype(int)[0]





def signal(opening,closing,lthr,sig):
  if sig.lower() == 'enter':
    try:
      return Regbot.enterSignalGenerator(opening,closing,lthr)
    except Exception as e:
      print(e)
  if sig.lower() == 'exit':
    try:
      return Regbot.exitSignalGenerator(opening,closing,lthr)
    except Exception as e:
      print(e)
  else:
    print(f'{sig} is not a valid option!')
    return 


if __name__ == '__main__':
  fire.Fire(signal)
