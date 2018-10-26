#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

class ResourceDepletionError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return  repr('The proxy source is exhausted.')

class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy pool is empty.')