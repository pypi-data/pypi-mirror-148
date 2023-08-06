import sys
import os
from pycocotools import mask
import numpy as np
import cv2
import json
from collections import defaultdict
import unittest
import torch

sys.path.insert(0, os.path.abspath('')) # Test files from current path rather than installed module
from pymlutil.s3 import *

test_config = 'test.yaml'

class Test(unittest.TestCase):
    #  PutDir(self, bucket, path, setname)
    def test_PutDir(self):

        parameters = ReadDict(test_config)
        if 's3' not in parameters:
            raise ValueError('s3 not in {}'.format(test_config))

        s3, _, s3def = Connect(parameters['s3']['credentials'])

        set = None
        if parameters['s3']['testset'] in s3def['sets']:
            set = s3def['sets'][parameters['s3']['testset']]
        else:
            raise ValueError('{} {} clone set undefined {}'.format(__file__, __name__, parameters['s3']['testset']))

        destobjpath = set['prefix']
        if destobjpath is not None and len(destobjpath) > 0:
            destobjpath += '/'
        destobjpath += parameters['s3']['objectpath']

        if not (s3.PutDir(set['bucket'], parameters['s3']['sourcepath'], destobjpath)):
             raise ValueError('{} {} failed'.format(__file__, __name__))

        #  RemoveObjects(self, bucket, setname=None, pattern='**', recursive=False):
        if not s3.RemoveObjects(set['bucket'], destobjpath, recursive=True):
            raise ValueError('{} {} RemoveObjects({}, {}, recursive={}) failed'.format(__file__, __name__, set['bucket'], destobjpath, recursive=True))

    # def CloneObjects(self, destbucket, destsetname, srcS3, srcbucket, srcsetname):
    def test_CloneObjects(self):
        parameters = ReadDict(test_config)
        if 's3' not in parameters:
            raise ValueError('s3 not in {}'.format(test_config))

        s3, _, s3def = Connect(parameters['s3']['credentials'])

        set = None
        if parameters['s3']['testset'] in s3def['sets']:
            set = s3def['sets'][parameters['s3']['testset']]
        else:
            raise ValueError('{} {} clone set undefined {}'.format(__file__, __name__, parameters['s3']['testset']))
        srcobjepath = set['prefix']
        if srcobjepath is not None and len(srcobjepath) > 0:
            srcobjepath += '/'
        srcobjepath += parameters['s3']['objectpath']

        if not (s3.PutDir(set['bucket'], parameters['s3']['sourcepath'], srcobjepath)):
            raise ValueError('{} {} PutDir failed'.format(__file__, __name__))

        destobjpath = set['prefix']
        if destobjpath is not None and len(destobjpath) > 0:
            destobjpath += '/'
        destobjpath += parameters['s3']['objectpath'] + '_dest'
        if not s3.CloneObjects(set['bucket'], destobjpath , s3, set['bucket'], srcobjepath):
            raise ValueError('{} {} CloneObjects failed'.format(__file__, __name__))

        #  RemoveObjects(self, bucket, setname=None, pattern='**', recursive=False):
        if not s3.RemoveObjects(set['bucket'], srcobjepath, recursive=True):
            raise ValueError('{} {} RemoveObjects({}, {}, recursive={}) failed'.format(__file__, __name__, set['bucket'], srcobjepath, recursive=True))

        if not s3.RemoveObjects(set['bucket'], destobjpath, recursive=True):
            raise ValueError('{} {} RemoveObjects({}, {}, recursive={}) failed'.format(__file__, __name__, set['bucket'], destobjpath, recursive=True))

if __name__ == '__main__':
    unittest.main()