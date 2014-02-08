#coding=utf-8 
'''
Created on 2014年2月7日

@author: fengjian
'''
import Basic

class Streamer():
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__buffer = ""
        self.ENDSEGMENTFILE = ".old"
        self.CFG = Basic.Basci()
        self.CFG.hls()
        self.HLSROOTPATH = self.CFG.HTTPROOT

    def getVODRoot(self):
        
        return self.HTTPROOT

    def isNewStream(self, name):

        self.HLSROOTPATH = "%s/%s" % (self.CFG.HTTPROOT, name)
        if not self.CFG.os.path.exists(self.HLSROOTPATH):
            self.CFG.os.makedirs(self.HLSROOTPATH)
            return 1
        else:
            if self.CFG.os.path.exists("%s/%s" % (self.HLSROOTPATH, self.ENDSEGMENTFILE)):
                return 0
            else:
                return 1

    def genSeg(self, name, content):

        try:
            segment_file = None
            if self.CFG.os.path.isfile("%s/%s" %(self.HLSROOTPATH, name)):
                return 1
            segment_file = open("%s/%s" %(self.HLSROOTPATH, name), "w")
            segment_file.write(content)
            return 1
        except IOError, e:
            print e
            return 0
        finally:
            if segment_file:
                segment_file.close()
            
    def getVERSION(self):
        
        self.__buffer += "#EXT-X-VERSION:%d\n" % self.CFG.EXT_X_VERSION
        
    def getTARGETDURATION(self):
        
        self.__buffer += "#EXT-X-TARGETDURATION:%d\n" % self.CFG.EXT_X_TARGETDURATION
    
    def getM3U(self):

        self.__buffer += "#EXTM3U\n"
    
    def getINF(self, dur, segurl):
        
        self.__buffer += "#EXTINF:%.1f\n%s\n" % (dur, segurl)
    
    def getENDLIST(self):
        
        self.__buffer += "#EXT-X-ENDLIST\n"
    
    def genM3U8(self, name):
        
        try:
            m3u8_file = None
            if self.CFG.os.path.isfile("%s/%s" % (self.HLSROOTPATH, name)):
                return 1
            m3u8_file = open("%s/%s" % (self.HLSROOTPATH, name), "w")
            m3u8_file.write(self.__buffer)
            return 1
        except IOError, e:
            print e
            return 0
        finally:
            if m3u8_file:
                m3u8_file.close()

    def genFinish(self):

        try:
            seged = None
            seged = open("%s/%s" % (self.HLSROOTPATH, self.ENDSEGMENTFILE), "w")
            seged.write("")
            seged.close()
        except IOError, e:
            print e
        finally:
            if seged:
                seged.close()


class VOD():
    
    def __init__(self):

        self.BASIC = Basic.Basci()
        self.tsParser_object = self.BASIC.tsparser

    def vod2hls(self, filename):
        print self.BASIC.time.ctime(self.BASIC.time.time())
        segpackage = 0
        timer = 0
        count = 0
        timer_end = 0
        seg_number = 0
        vod_length = list()
        STREAMER = Streamer()
        if not STREAMER.isNewStream(self.BASIC.os.path.split(filename)[-1].split(".")[0]):
            return
        STREAMER.getM3U()
        STREAMER.getVERSION()
        STREAMER.getTARGETDURATION()
        file_object = self.openVOD("%s" % (filename))
        sec = file_object.read(188)
        while len(sec) == 188:
            segpackage += 1
            #print 1111
            self.tsParser_object.get_length(sec)
            timer = self.tsParser_object.get_clock()
            count = int(timer)/10
            #print time.ctime(time.time())
            if count > seg_number:
                seg_number = count
                dur = timer - timer_end
                timer_end = timer
                vod_length.append(segpackage * 188)
                segpackage = 0
                STREAMER.getINF(float(dur), "%d.ts" % seg_number)
            sec = file_object.read(188)
        seg_number += 1
        vod_length.append(segpackage * 188)
        STREAMER.getINF(float(timer-timer_end), "%d.ts" % (seg_number))
        STREAMER.getENDLIST()
        if not STREAMER.genM3U8("%s.m3u8" % "vod"):
            return
        file_object.seek(0)
        #print vod_length
        for length in range(len(vod_length)):
            seg = length + 1
            genseg = self.BASIC.threading.Thread(target=STREAMER.genSeg,
                                      args=("%s.ts" % seg, file_object.read(vod_length[length])))
            genseg.start()
        file_object.close()
        STREAMER.genFinish()
        print self.BASIC.time.ctime(self.BASIC.time.time())
    
    def openVOD(self, name):
        try:
            return open(name, "rb")
        except IOError, e:
            print e
            return None

    def start(self):

        self.BASIC.hls()
        for i in self.BASIC.os.listdir(self.BASIC.VODROOT):
            filepath = "%s/%s"% (self.BASIC.VODROOT, i)
            #print filepath
            vod2hls = self.BASIC.threading.Thread(target=self.vod2hls,
                             args=(filepath,))
            vod2hls.start()


if __name__ == "__main__":

    VODStreamer = VOD()
    VODStreamer.start()


