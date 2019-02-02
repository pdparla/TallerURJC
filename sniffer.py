#! /usr/bin/env python
# -*- coding: utf-8 -*-

#VERSION CON RAW SOCKETS
import socket, sys
from struct import *
from Clases import *

# CONSTANTES
# Recibir todas las capas del paquete
ETH_P_ALL = 3
# IPv4
IPv4 = 8
# tcp
TCP = 6
# udp
UDP = 17
# Sockets Conexion entrante
#s_tcp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#s_udp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

try:
    # Utilizado para recibir un paquete con todos los layer ya sea tcp o udp  http://man7.org/linux/man-pages/man7/packet.7.html
    s_raw = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
except(socket.error, error):
    print(f'Error: {str(error[0])}, Mensaje: {str(error[1])}')
    sys.exit()
# Recibir un paquete
while True:
    # Recibo los datos del socket como un string en bytes b''
    packet = s_raw.recv(65565)

    # Transformamos en el formato de ethernet
    eth = unpack('!6s6sH' , packet[:14])
    ethernet = EthPacket(eth[0],eth[1],eth[2])
    breakpoint()
    print ('############## MAC ##############')
    print (str(ethernet))
    # Si es IPv4
    if (ethernet.protocol == IPv4):
        # Para obtener la transformación entre tipos de C y Python
        # Obtenemos los caracteres en el formato indicado (ver !BBHHHBBH4s4s) ! indica red, B integer/unsigned char H integer/unsigned short , s String/char[]. los 4 indica tamaño del array/string
        iph = unpack('!BBHHHBBH4s4s' , packet[ethernet.length:ethernet.length+20])
        # Introducimos version De los 4 primeros bits del byte
        version = iph[0] >> 4
        # indica ip header length (ihl)
        ihl = iph[0] & 0xF * 4
        ipv4 = IPPacket(version,ihl,iph[2],iph[5],iph[6],iph[7],iph[8],iph[9])

        print ('############## IPv4 ##############')
        #Cambiar a esto
        print (str(ipv4))
        # TCP
        if (ipv4.protocol == TCP):
            # Formateamos el paquete
            tcph = unpack('!HHLLBBHHH' , packet[ipv4.ihl:ipv4.ihl + 20])
            Tcp = TCPPacket(tcph[0],tcph[1],tcph[2],tcph[3],tcph[4],tcph[6] )

            print ('############## TCP ##############')
            print (str(Tcp))
            h_size = ethernet.length + ipv4.ihl + Tcp.dataoffset * 4
            #Coger data del paquete
            Tcp.addData(packet[h_size:].decode('utf-8',errors='ignore'))
            print (f'\tData : {Tcp.data}\n')
            print
        # UDP
        elif (ipv4.protocol == UDP):
            u = ipv4.ihl + ethernet.length
            #Deshacemos binario
            udph = unpack('!HHHH' , packet[u:u+8])
            Udp = UDPPacket(udph[0],udph[1],udph[2],udph[3])

            print ('############## UDP ##############')
            print(str(Udp))
            # 8 es el numero de bytes de cabecera UDP
            h_size = ethernet.length + ipv4.ihl + 8
            #Coger data del paquete
            Udp.addData(packet[h_size:].decode('utf-8',errors='ignore'))
            print (f'\tData : {Udp.data}\n')
