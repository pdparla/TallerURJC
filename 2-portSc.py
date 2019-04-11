#! /usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import sys
from datetime import datetime

cerrado = 0
#Para hacer ping
def ping(d_addr):
    try:
        ping = sr1(IP(dst=d_addr)/ICMP())
        print(f'+ Host {d_addr} activo')
        return True
    except Exception:
        print (f'+ Host {d_addr} no activo')
        return False

#Scanner SYN
def scanSYN(d_addr, port):
    try:
        s_port = random.randint(0,1000)
        SYNACK = None
        breakpoint();
        SYNACK = sr1(IP(dst=d_addr)/TCP(sport=s_port, dport=port,flags='S'), verbose=0, timeout=1)
        # Salta timeout
        if SYNACK is None:
            print(f'+\tPuerto {str(port)} filtrado')
        # SYNACK
        elif str(SYNACK[TCP].flags) == 'SA':
            print(f'+\tPuerto {str(port)} activo')
            RST = IP(dst=d_addr)/TCP(sport=s_port, dport=port,flags = 'R')
            send(RST, verbose = 0)
        # RSTACK
        elif str(SYNACK[TCP].flags) == 'RA':
            global cerrado
            cerrado = cerrado + 1
    except Exception:
        # Si salta cualquier fallo: cerramos conexion 
        RST = IP(dst=d_addr)/TCP(sport=s_port, dport=port,flags = 'R')
        send(RST)
        print(f'No he podido escanear {d_addr} en el puerto {str(port)}')
try:
    d_addr = sys.argv[1]
    min_port = int(sys.argv[2])
    max_port = int(sys.argv[3])
    # ping(d_addr): por si quieres comprobar si esta activo
    tiempo_ini = datetime.now()
    for port in range (min_port,max_port,1):
        scanSYN(d_addr,port)
    tiempo_fin = datetime.now()
    print(f'Puertos cerrados: {str(cerrado)}')
    print(f'Duracion total: {str(tiempo_fin - tiempo_ini)}')
except KeyboardInterrupt:
    print('[*] Adios!')
