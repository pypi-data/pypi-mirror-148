import sys
import os
from pycocotools import mask
import numpy as np
import cv2
import json
from collections import defaultdict
import unittest
import torch

from pymlutil.functions import *



class Test(unittest.TestCase):
    def test_GaussianBasis(self):
        self.assertEqual(GaussianBasis(torch.tensor(0.0), zero=0.0, sigma=0.33), 1.0)