#coding=utf-8 
'''
Created on 02/06/2014

@author: fengjian
'''


class TSParser(object):

	'''
	This class parse MPEG-TS packages
	'''
	TS_SYNC_BYTE = 0x47
	TS_PACKET_SIZE = 188
	
	def __init__(self):

		self.pid_dict = dict()
		self.clock_begin = 0
		self.clock_end = 0
		self.__clock = 0

        def isTsPackage(self, pac):

                if len(pac) != self.TS_PACKET_SIZE:
			return 0
                if ord(pac[0]) != self.TS_SYNC_BYTE:
                        return 0
		return 1
		
	def get_length(self, package):

		'''
		get the time stamp of MPEG-TS stream or VOD 
		'''
		try:	
			#If this packet doesn't contain a PCR, then we're not interested in it:
			adaptation_field_control = (ord(package[3]) & 0x30) >> 4
			#print adaptation_field_control
			if (adaptation_field_control != 2 and adaptation_field_control != 3):
				return 
			# // there's no adaptation_field  
			adaptation_field_length = package[4]
			if (adaptation_field_length == 0):
				return
			
			#no PCR
			pcr_flag = ord(package[5]) & 0x10
			if (pcr_flag == 0):
				return
			
			#yes, we get a pcr 
			pcr_base_high = (ord(package[6]) << 24) | (ord(package[7]) << 16) | (ord(package[8]) << 8)  | ord(package[9])
			
			#caculate the clock
			self.__clock = pcr_base_high / 45000.0
			if ((ord(package[10]) & 0x80)):
				self.__clock += 1 / 90000.0 # add in low-bit (if set)
			pcr_extra = ((ord(package[10]) & 0x01) << 8) | ord(package[11])
			self.__clock += pcr_extra / 27000000.0
			pid = ((ord(package[1]) & 0x1F) << 8) | ord(package[2])
			self.pid_dict[pid] = self.__clock
			#print "PID: %s , %s" % (pid, self.__clock)
		except Exception, e:
			print e
			return
			
	def get_clock(self, pid=0):
			
		'''
		return the time stamp of MPEG-TS
		'''
		if pid:
			return self.pid_dict[pid]
		return self.__clock

if __name__ == "__main__":
	VOD = "../vod/Jeopardy.ts"
	TS = TSParser()
	file_reader = open(VOD, "rb")
	timer = 0
	seg_number = 0
	count = 0
	sec = file_reader.read(188)
	while len(sec) == 188:
		count += 1
		TS.get_length(sec)
		sec = file_reader.read(188)
		timer = TS.get_clock()
		#print timer
		count = int(timer)/10
		#print count, seg_number
		if count > seg_number:
			seg_number = count
			print "Gen %s.ts" % seg_number
		#break
	print TS.pid_dict
