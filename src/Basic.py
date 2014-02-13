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
import urlparse
import os

class Basic(object):
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
        self.urlparse = urlparse
        
    def log(self):
        
        self.logger = logging.getLogger("easystream")  
        self.logger.setLevel(logging.DEBUG)  
        # create file handler which logs even debug messages  
        fh = logging.FileHandler("log/easystream.log")  
        fh.setLevel(logging.DEBUG)  
        # create console handler with a higher log level  
        ch = logging.StreamHandler()  
        ch.setLevel(logging.ERROR)  
        # create formatter and add it to the handlers  
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  
        ch.setFormatter(formatter)  
        fh.setFormatter(formatter)  
        # add the handlers to logger  
        self.logger.addHandler(ch)  
        self.logger.addHandler(fh)  
        # "application" code

    def live(self):
        import SocketServer
        self.socketserver = SocketServer.SocketServer()
        
    def hls(self):
       
        self.SEGMENT_NUMBER = 3 
        self.EXT_X_VERSION = 3
        self.EXT_X_TARGETDURATION = 10
        self.HTTPROOT = "httproot"
        self.VODROOT = "vod"
