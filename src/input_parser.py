import argparse
import logging
import os
import sys

def validate_args(conf):
    conf.in_file = conf.in_file[0]
    if not os.path.exists(conf.in_file):
        logging.error('Input file does not exist')
        sys.exit()
    else:
        if not os.access(conf.in_file, 4):
            logging.error('Dont have permissions to read input file.')
            sys.exit()

    if os.path.exists(conf.out_file):
        if conf.force_overwrite:
            logging.warning('Output file exists - overwriting.')
            if not os.access(conf.out_file, 2):
                logging.error('Dont have permissions to write in output file.')
                sys.exit()
        else:
            logging.error('Output file already exists. Please change name, of add -F')
            sys.exit()
    
    if conf.bad_file:
        if not os.path.exists(conf.bad_file):
            logging.error('Features file does not exist')
            sys.exit()
        else:
            if not os.access(conf.bad_file, 4):
                logging.error('Dont have permissions to read features file.')
                sys.exit()

def _get():
    parser = argparse.ArgumentParser()
 #   sp = parser.add_subparsers()
    method = parser.add_mutually_exclusive_group(required=True)    

    method.add_argument('-c', action='store', dest='mincount',
                                help='Min count of occurences',
                                default=250)

    parser.add_argument(action='store', dest='in_file',
                                help='Input file in Vopal Wabbit input format',
                                nargs=1,
                                )

    parser.add_argument('-o', action='store', dest='out_file',
                                help='Output file in matrix format',
                                default='output.txt')


    parser.add_argument('-b', action='store', dest='bad_file',
                                help='Bad features file from liftmatrix',
                                )

    parser.add_argument('-F', action='store_true', default=False,
                                dest='force_overwrite',
                                                    help='Overwrite output file.')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    out =  parser.parse_args()
    validate_args(out)
    return out
