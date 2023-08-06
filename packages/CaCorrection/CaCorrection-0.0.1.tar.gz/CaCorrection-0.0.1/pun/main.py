from nemo.utils.exp_manager import exp_manager
from nemo.collections import nlp as nemo_nlp

import os
import wget 
import torch
import pytorch_lightning as pl
from omegaconf import OmegaConf


os.system('gdown https://drive.google.com/uc?id=1-5-7Sy5fOcDM9a5ay7H87fN_WlNRpDd9')
os.system('gdown https://drive.google.com/uc?id=1-4PDopoWmBFsFwm-N8Pvcc284Si_2rZ0')
global checkpoint_path 
global pretrained_model 

checkpoint_path = ''
pretrained_model = None

cmd = os.getcwd()
print("Weights downloaded and located in {}".format(cmd))

def setpath(path):
  global checkpoint_path 
  checkpoint_path = path
  


def init_model():
  global pretrained_model 
  pretrained_model = nemo_nlp.models.PunctuationCapitalizationModel.restore_from(checkpoint_path)

def correct(text):  
  inference_results = pretrained_model.add_punctuation_capitalization(text)
  return inference_results
