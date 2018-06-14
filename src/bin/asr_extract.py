#!/usr/bin/env python

# Copyright 2018 Nagoya University (Tomoki Hayashi)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import argparse
import logging
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    # general configuration
    parser.add_argument('--gpu', default=None, type=int, nargs='?',
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--ngpu', default=0, type=int,
                        help='Number of GPUs')
    parser.add_argument('--backend', default='pytorch', type=str,
                        choices=['chainer', 'pytorch'],
                        help='Backend library')
    parser.add_argument('--out', type=str, required=True,
                        help='Output basename')
    parser.add_argument('--verbose', '-V', default=0, type=int,
                        help='Verbose option')
    # task related
    parser.add_argument('--feat', type=str, required=True,
                        help='Filename of train feature data (Kaldi scp)')
    parser.add_argument('--model', type=str, required=True,
                        help='Model file parameters to read')
    parser.add_argument('--model-conf', type=str, required=True,
                        help='Model config file')
    parser.add_argument('--extract-layer-idx', type=int, default=-1,
                        help='Index of hidden layer to extract the states')
    args = parser.parse_args()

    # logging info
    if args.verbose > 0:
        logging.basicConfig(
            level=logging.INFO, format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s')
    else:
        logging.basicConfig(
            level=logging.WARN, format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s')
        logging.warning('Skip DEBUG/INFO messages')

    # check gpu argument
    if args.gpu is not None:
        logging.warn("--gpu option will be deprecated, please use --ngpu option.")
        if args.gpu == -1:
            args.ngpu = 0
        else:
            args.ngpu = 1

    # check CUDA_VISIBLE_DEVICES
    if args.ngpu > 0:
        if "clsp.jhu.edu" in subprocess.check_output(["hostname", "-f"]):
            cvd = subprocess.check_output(["/usr/local/bin/free-gpu", "-n", str(args.ngpu)]).strip()
            logging.info('CLSP: use gpu' + cvd)
            os.environ['CUDA_VISIBLE_DEVICES'] = cvd

        cvd = os.environ.get("CUDA_VISIBLE_DEVICES")
        if cvd is None:
            logging.warn("CUDA_VISIBLE_DEVICES is not set.")
        elif args.ngpu != len(cvd.split(",")):
            logging.error("#gpus is not matched with CUDA_VISIBLE_DEVICES.")
            sys.exit(1)

    # display PYTHONPATH
    logging.info('python path = ' + os.environ['PYTHONPATH'])

    # extract
    logging.info('backend = ' + args.backend)
    if args.backend == "chainer":
        raise NotImplementedError
    elif args.backend == "pytorch":
        from asr_pytorch import extract
        extract(args)
    else:
        raise ValueError("chainer and pytorch are only supported.")


if __name__ == '__main__':
    main()
