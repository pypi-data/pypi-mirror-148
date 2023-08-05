import sys
import os

from .s3 import *
from .jsonutil import *
from pymlutil.imutil import ImUtil, ImTransform

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments')

    parser.add_argument('-d', '--debug', action='store_true',help='Wait for debuggee attach')   
    parser.add_argument('-debug_port', type=int, default=3000, help='Debug port')
    parser.add_argument('-debug_address', type=str, default='0.0.0.0', help='Debug port')

    parser.add_argument('-credentials', type=str, default='creds.yaml', help='Credentials file.')


    parser.add_argument('--PutDir', '-p', action='store_true',help='Get coco dataset') 
    parser.add_argument('-src', type=str, default=None, help='path to source directory')
    parser.add_argument('-set', type=str, default='dataset', help='set defined in credentials file')
    parser.add_argument('-dest', type=str, default=None, help='destindation in s3')

    parser.add_argument('-cocourl', type=json.loads, default=None, 
                        help='List of coco dataset URLs to load.  If none, coco 2017 datafiles are loaded from https://cocodataset.org/#download')

    args = parser.parse_args()
    return args

def main(args):

    s3, creds, s3def = Connect(args.credentials)

    if args.PutDir:
        if args.set not in s3def['sets']:
            print('PutDir failed: args.set {} not found in credentials file'.format(args.set))
        elif args.src is None:
            print('PutDir failed: args.src is None')
        elif args.dest is None:
            print('PutDir failed: args.dest is None')
        else:
            dest = '{}/{}'.format(s3def['sets'][args.set]['prefix'], args.dest)
            s3.PutDir(s3def['sets'][args.set]['bucket'], args.src, dest)


    print('pymluitil complete')

    
if __name__ == '__main__':
    import argparse
    args = parse_arguments()

    if args.debug:
        print("Wait for debugger attach on {}:{}".format(args.debug_address, args.debug_port))
        import debugpy

        debugpy.listen(address=(args.debug_address, args.debug_port)) # Pause the program until a remote debugger is attached
        debugpy.wait_for_client()  # Pause the program until a remote debugger is attached
        print("Debugger attached")

    main(args)