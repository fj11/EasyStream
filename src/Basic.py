#coding=utf-8
'''
Created on 2014年2月8日

@author: fengjian
'''
import logging
import TsParser
import threading
import socket
import time
import os

class Basci(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.time = time
        self.os = os
        self.socket = socket
        self.tsparser = TsParser.TSParser()
        self.threading = threading
        
        
    def log(self):
        
        logger = logging.getLogger("simple_example")  
        logger.setLevel(logging.DEBUG)  
        # create file handler which logs even debug messages  
        fh = logging.FileHandler("spam.log")  
        fh.setLevel(logging.DEBUG)  
        # create console handler with a higher log level  
        ch = logging.StreamHandler()  
        ch.setLevel(logging.ERROR)  
        # create formatter and add it to the handlers  
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  
        ch.setFormatter(formatter)  
        fh.setFormatter(formatter)  
        # add the handlers to logger  
        logger.addHandler(ch)  
        logger.addHandler(fh)  
        # "application" code  
        logger.debug("debug message")  
        logger.info("info message")  
        logger.warn("warn message")  
        logger.error("error message")  
        logger.critical("critical message") 
        
    def hls(self):
        
        self.EXT_X_VERSION = 3
        self.EXT_X_TARGETDURATION = 10
        self.HTTPROOT = "../httproot"
        self.VODROOT = "../vod"
