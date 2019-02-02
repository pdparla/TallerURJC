import socket 
'''
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Ethernet destination address (first 32 bits)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ethernet d addr (last 16 bits) |Ethernet s addr (first 16 bits)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Ethernet source address (last 32 bits)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        Type code              |                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

class EthPacket:
    length = 14

    def __init__(self,dst_addr,src_addr,type_code):
        self.src_addr = self.strip_addr(src_addr)
        self.dst_addr = self.strip_addr(dst_addr)
        self.protocol = socket.ntohs(type_code)

    def __str__(self):
        return f'Src address: {str(self.src_addr)}\tDst address: {str(self.dst_addr)}\tType: {str(self.protocol)}\n'
    def strip_addr(self,addr):                                                                    
        return ':'.join('%02x' % ord(chr(b)) for b in addr)
'''
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
class IPPacket:
    def __init__(self,version,ihl,tot_length,ttl,protocol,checksum,s_addr,d_addr):
      self.version = version
      self.ihl = ihl
      self.tot_length = socket.ntohs(tot_length)
      self.ttl = ttl
      self.protocol = protocol
      self.checksum = checksum
      self.s_addr = socket.inet_ntop(socket.AF_INET, s_addr)
      self.d_addr = socket.inet_ntop(socket.AF_INET, d_addr) 
    
    def __str__(self):
        return f'\tVersion: {str(self.version)}\n\tIHL: {str(self.ihl)}\n\tTotal length of packet: {str(self.tot_length)}\n\tTTL: {str(self.ttl)}\n\tProtocol: {str(self.protocol)}\n\tChecksum: {str(self.protocol)}\n\tSrc address: {str(self.s_addr)}\n\tDst address: {str(self.d_addr)}\n'

'''
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
class TCPPacket:
    def __init__(self,s_port,d_port,seq_number,ack_number,dataoffset,window):
        self.s_port = s_port
        self.d_port = d_port
        self.seq_number = seq_number
        self.ack_number = ack_number
        self.dataoffset = dataoffset >> 4
        self.window = window

    def addData(self,data):
        self.data = data

    def __str__(self):
        return f'\tSrc port: {str(self.s_port)}\n\tDst port: {str(self.d_port)}\n\tSequence number: {str(self.seq_number)}\n\tAck: {str(self.ack_number)}\n\tOffset: {str(self.dataoffset)}\n\tWindow: {str(self.window)}\n'
'''
0      7 8     15 16    23 24      31  
 +--------+--------+--------+--------+ 
 |     Source      |   Destination   | 
 |      Port       |      Port       | 
 +--------+--------+--------+--------+ 
 |                 |                 | 
 |     Length      |    Checksum     | 
 +--------+--------+--------+--------+ 
 |                                     
 |          data octets ...            
 +---------------- ...
'''
class UDPPacket:
    def __init__(self, s_port,d_port,length,checksum):
        self.s_port = s_port
        self.d_port = d_port
        self.length = length
        self.checksum = checksum

    def __str__(self):
        return f'\tSrc port: {str(self.s_port)}\n\tDst port: {str(self.d_port)}\n\tLength: {str(self.length)}\n\tChecksum: {str(self.checksum)}'

    def addData(self, data):
        self.data = data 

'''
0                       1                       2                   
0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                       |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ 
|                    QDCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|           DATA  (QUERY OR RESPONSE)           |
+--+--+--+--+--+.................................
'''
class DNS:
    def __init__(id,qr,opcode,flags,rcode,qdcount,ancount,nscount,arcount):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.flags = flags
        self.rcode = rcode
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

    def addQuestion(self,question):
        self.question = question
    
    def addAnswer(self,answer):
        self.answer = answer

    def __str__(self):
        a = f'\tID: {str(self.id)}\n\tQR: {str(self.qr)}\n\OPCode: {str(self.opcode)}\n\tFlags: {str(self.flags)}\n\tRCode: {str(self.rcode)}\n\QDCount: {str(self.qdcount)}\n\tANCount: {str(self.ancount)}\n\tNSCount: {str(self.nscount)}\n\tARCount: {str(self.arcount)}'
        if hasattr(self,'answer'):
            a = a + str(self.answer)
        if hasattr(self,'question'):
            a = a + str(self.question)
        return a

class Question():
    def __init__(self,qname,qtype,qclass):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass
        return self
    
    def __str__(self):
        return f'\tQName: {str(self.qname)}\n\tQType: {str(self.qtype)}\n\tQClass: {str(self.qclass)}'

class Answer():
    def __init__(self,aquery,aname,atype,aclass,attl,ardlength,ardata):
        self.aname = aname
        self.atype = atype
        self.aclass = aclass
        self.attl = attl
        self.ardlength = ardlength
        self.ardata = ardata
        return self

    def isQuery(self):
        return self.qr == 0

    def __str__(self):
        return f'\tAName: {str(self.aname)}\n\tAType: {str(self.atype)}\n\tAClass: {str(self.aclass)}\n\TTL: {str(self.attl)}\n\tRDLength: {str(self.ardlength)}\n\tRData: {str(self.ardata)}'

