import os
import numpy as np 
import pyautogui
import socket
from socket import SHUT_RDWR
import sys
import time
import shutil
import cv2
from PIL import Image
import threading

MAX_BUFFER_SIZE = 5000*5000
HOST = "127.0.0.1"
PORT  = 8008

from enum import Enum

class MODE_SENT(Enum):
    STRING = 1
    IMAGE = 2
    STRING_IMAGE = 3

MODE_DATE_SENT  = MODE_SENT.IMAGE 

class BIT(Enum):
    MODE =0
    WIDTH =1
    HEIGHT =2
    SHAPE =3
    DATALENGHT =4

    def __repr__(self):
      return int(self.value)

      


