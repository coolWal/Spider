#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import argparse

parse = argparse.ArgumentParser()

parse.add_argument('echo',help='echo string you use here')
parse.add_argument('square',help='display a  square of a given number',type=int)
args = parse.parse_args()

print args.echo
print '========================================'
print args.square**2








