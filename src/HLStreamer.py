#coding=utf-8 
'''
Created on 2014年2月7日

@author: fengjian
'''
import Basic

BASIC = Basic.Basic()

class HLStreamer():
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__buffer = ""
        self.ENDSEGMENTFILE = ".old"
        BASIC = Basic.Basic()
        BASIC.hls()
        self.HLSROOTPATH = BASIC.HTTPROOT

    def getVODRoot(self):
        
        return self.HTTPROOT

    def isNewStream(self, name, stream_type="vod"):

        self.HLSROOTPATH = "%s/%s" % (BASIC.HTTPROOT, name)
        if not BASIC.os.path.exists(self.HLSROOTPATH):
            BASIC.os.makedirs(self.HLSROOTPATH)
        if stream_type == "live":
            return 1
        else:
            if BASIC.os.path.exists("%s/%s" % (self.HLSROOTPATH, self.ENDSEGMENTFILE)):
                return 0
            else:
                return 1

    def genSeg(self, name, content):

        try:
            segment_file = None
            if BASIC.os.path.isfile("%s/%s" %(self.HLSROOTPATH, name)):
                return 1
            segment_file = open("%s/%s" %(self.HLSROOTPATH, name), "w")
            segment_file.write(content)
            return 1
        except IOError, e:
            print "Open segment %s Error: %s" % (name, e)
            return 0
        finally:
            if segment_file:
                segment_file.close()

    def openSeg(self, name):

        segment_file = open("%s/%s" %(self.HLSROOTPATH, name), "w")
        return segment_file

    def getVERSION(self):
        
        self.__buffer += "#EXT-X-VERSION:%d\n" % BASIC.EXT_X_VERSION
       
    def getPLAYLISTTYPE(self, playlist_type):

        self.__buffer += "#EXT-X-PLAYLIST-TYPE:%s\n" % playlist_type.upper()
 
    def getTARGETDURATION(self):
        
        self.__buffer += "#EXT-X-TARGETDURATION:%d\n" % BASIC.EXT_X_TARGETDURATION
   
    def getMEDIASEQUENCE(self, number):

        self.__buffer += "#EXT-X-MEDIA-SEQUENCE:%s\n" % number

    def getKEY(self, key_type="", method="NONE"):

        self.__buffer += "#EXT-X-KEY%s:METHOD=%s\n" % (key_type, method)
 
    def getM3U(self):

        self.__buffer += "#EXTM3U\n"
    
    def getINF(self, dur, segurl):
        
        self.__buffer += "#EXTINF:%.1f,\n%s\n" % (dur, segurl)
    
    def getENDLIST(self):
        
        self.__buffer += "#EXT-X-ENDLIST\n"
    
    def genM3U8(self, name):
        
        try:
            m3u8_file = None
            m3u8_file = open("%s/%s" % (self.HLSROOTPATH, name), "w")
            m3u8_file.write(self.__buffer)
            return 1
        except IOError, e:
            print "Open %s m3u8 Error: %s" % (name, e)
            return 0
        finally:
            self.__buffer = ""
            if m3u8_file:
                m3u8_file.close()

    def genFinish(self):

        try:
            seged = None
            seged = open("%s/%s" % (self.HLSROOTPATH, self.ENDSEGMENTFILE), "w")
            seged.write("")
            seged.close()
        except IOError, e:
            print "Open old Error: %s" % (e)
        finally:
            if seged:
                seged.close()

class VOD():
    
    def __init__(self):

        BASIC = Basic.Basic()
        self.tsParser_object = BASIC.tsparser

    def vod2hls(self, filename):
        #print BASIC.time.ctime(BASIC.time.time())
        start_time = 0
        end_time = 0
        timer = 0
        duration = 0
        segpackage = 0
        seg_number = 1
        vod_length = list()
        STREAMER = HLStreamer()
        STREAMER.getM3U()
        STREAMER.getVERSION()
        STREAMER.getTARGETDURATION()
        STREAMER.getPLAYLISTTYPE("vod")
        STREAMER.getMEDIASEQUENCE("1")
        STREAMER.getKEY()
        file_object = self.openVOD("%s" % (filename))
        sec = file_object.read(188)
        if not self.tsParser_object.isTsPackage(sec):
            return
        if not STREAMER.isNewStream(BASIC.os.path.split(filename)[-1].split(".")[0]):
            return
        while len(sec) == 188:
            segpackage += 1
            #print 1111
            self.tsParser_object.get_length(sec)
            timer = self.tsParser_object.get_clock()
            if timer and not start_time:
                start_time = timer
            #print timer
            if timer - start_time > 10:
                duration = timer - start_time
                start_time = timer
                vod_length.append(segpackage * 188)
                segpackage = 0
                STREAMER.getINF(float(duration), "%s.ts" % seg_number)
                seg_number += 1
            sec = file_object.read(188)
        vod_length.append(segpackage * 188)
        STREAMER.getINF(float(timer - start_time), "%s.ts" % (seg_number))
        STREAMER.getENDLIST()
        if not STREAMER.genM3U8("%s.m3u8" % "playlist"):
            return
        file_object.seek(0)
        #print vod_length
        for length in range(len(vod_length)):
            seg = length + 1
            STREAMER.genSeg("%s.ts" % seg, file_object.read(vod_length[length]))
##            genseg = BASIC.threading.Thread(target=STREAMER.genSeg,
##                                      args=("%s.ts" % seg, file_object.read(vod_length[length])))
##            genseg.start()
        file_object.close()
        STREAMER.genFinish()
        #print BASIC.time.ctime(BASIC.time.time())
    
    def openVOD(self, name):
        try:
            return open(name, "rb")
        except IOError, e:
            print "Open VOD %s Error: %s" % (name, e)
            return None

    def start(self):

        BASIC.hls()
        for i in BASIC.os.listdir(BASIC.VODROOT):
            filepath = "%s/%s"% (BASIC.VODROOT, i)
            #print filepath
            self.vod2hls(filepath)
##            vod2hls = BASIC.threading.Thread(target=self.vod2hls,
##                             args=(filepath,))
##            vod2hls.start()

class LIVE():

    def __init__(self):

        self.STREAMER = HLStreamer()

    def reciveUnicastUDP(self, url):

        BASIC.live()
        BASIC.hls()
        parsed_url = BASIC.urlparse.urlsplit(url)
        if parsed_url.scheme.lower() != "udp":
            return
        udp_unicast_server = BASIC.socketserver.UDPUnicastServer()
        udp_unicast_server.bind(("", parsed_url.port))
        udp_unicast_server.settimeout(60)

        seg_info_list = list()
        start_time = 0
        last_time = 0
        end_time = 0
        timer = 0
        duration = 0
        seg_number = 1
        save_segment = True
        segment_file = None
        streamname = parsed_url.path.split("/")[-1].split(".")[0]
        
        self.STREAMER.isNewStream(streamname, "live")
        try: 
            message, address = udp_unicast_server.recvfrom(188)
            if address[0] != parsed_url.hostname:
                return
            if not BASIC.tsparser.isTsPackage(message):
                return
            while len(message) == 188:
                if save_segment:
                    #print "creating %s.ts" % seg_number
                    segment_file = self.STREAMER.openSeg("%s.ts" % seg_number)
                    save_segment = False
                segment_file.write(message)
                BASIC.tsparser.get_length(message)
                timer = BASIC.tsparser.get_clock()
                if timer and not last_time and not start_time:
                    last_time = timer
                    start_time = timer
                if abs(timer - last_time) > 10:
                    timer = last_time
                else:
                    last_time = timer
                if timer - start_time > 10:
                    segment_file.close()
                    save_segment = True
                    if len(seg_info_list) == BASIC.SEGMENT_NUMBER:
                        del seg_info_list[0]
                    duration = timer - start_time
                    start_time = timer
                    seg_info_list.append((duration, "%s.ts" % seg_number))
                    if len(seg_info_list) == BASIC.SEGMENT_NUMBER:
                        self._genM3U8(streamname, seg_info_list)
                    seg_number += 1
                message, address = udp_unicast_server.recvfrom(188)
        except BASIC.socket.timeout, e:
            print "Connecting %s session timeout" % url
        except Exception, e:
            print "%s" % e
        finally:
            if save_segment and segment_file:
                segment_file.close()
            self._genM3U8(streamname, seg_info_list, end_list=1)
                
    def _genM3U8(self, streamname, seg_info_list, end_list=0):

        if not seg_info_list:
            return
        self.STREAMER.getM3U()
        self.STREAMER.getVERSION()
        self.STREAMER.getTARGETDURATION()
        self.STREAMER.getPLAYLISTTYPE("live")
        self.STREAMER.getMEDIASEQUENCE(seg_info_list[0][-1].split(".")[0])
        self.STREAMER.getKEY()
        for i in seg_info_list:
            self.STREAMER.getINF(float(i[0]), i[1])
        if end_list:
            self.STREAMER.getENDLIST()
        if not self.STREAMER.genM3U8("%s.m3u8" % "playlist"):
            return
   
    
 
if __name__ == "__main__":

    #VODStreamer = VOD()
    #VODStreamer.start()
    LIVEStreamer = LIVE()
    LIVEStreamer.reciveUnicastUDP("udp://192.168.36.231:12345/fe.ts")


