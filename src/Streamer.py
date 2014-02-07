'''
Created on 2014Äê2ÔÂ7ÈÕ

@author: fengjian
'''

class configLoader():
    
    EXT_X_VERSION = 3
    EXT_X_TARGETDURATION = 10

class Streamer(configLoader):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        pass

    def genSegment(self, name, content):
        
        '''
        '''
        try:
            segment_file = open(name, "w")
            segment_file.write(content)
            return 1
        except IOError, e:
            print e
            return 0
        finally:
            segment_file.close()
            
    def getVERSION(self):
        
        return "#EXT-X-VERSION:%d" % self.EXT_X_VERSION
        
    def getTARGETDURATION(self):
        
        return "#EXT-X-TARGETDURATION:%d" % self.EXT_X_TARGETDURATION
    
    def getM3U(self):
        
        return "#EXTM3U"
    
    def getINF(self, dur, segurl):
        
        return "#EXTINF:%d\n%s" % (dur, segurl)
    
    def getENDLIST(self):
        
        return "#EXT-X-ENDLIST"
    
    def genM3U8(self, name, content):
        
        try:
            m3u8_file = open(name, "w")
            m3u8_file.write(content)
            return 1
        except IOError, e:
            print e
            return 0
        finally:
            m3u8_file.close()
            
class VOD(Streamer):
    
    def __init__(self):
        
        pass
    
    def findVOD(self):
        
        pass