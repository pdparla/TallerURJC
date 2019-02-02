#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, traceback, paramiko, sys, stat
try:
    #Creamos una sesion ssh
    ssh = paramiko.SSHClient()
    # Si queremos cargar las Claves del sistema que se guardan en ~/.ssh/known_hosts (Para linux)
    # ssh.load_system_host_keys()
    # Para declarar una política (qué hacer) cuando te conectas a un servidor sin una clave conocida
    # se utiliza set_missing_host_key_policy( policy)
    # Utilizaremos la política de añadir automáticamente el host y su clave al objeto
    # HostKeys (AutoAddPolicy()) el cual usa SSHClient.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Una vez tengamos esto, podremos conectarnos al servidor con la opción connect()
    # Primero intentará conectar con las claves cargadas, y si no se encuentra el hostname
    # entre estas utilizará la política declarada anteriormente.
    # La autenticación la intentará realizar de 4 maneras DIFERENTES en orden de prioridad.
    # En caso de no obtener ningun fichero o clave como última opción intenta autenticarse con claves/usuario planas.
    ssh.connect('IP',port=1234,username='xxxx',password='xxxx')
    # Abrimos una sesion sftp para descargar ficheros.
    sftp = ssh.open_sftp()
    # Si el sistema operativo en el que estoy es windows descargo un modulo powershell a elección y lo ejecuto
    if (os.name == 'nt'):
        sftp.get('/asas/asas/prueba.ps1','.\\prueba.ps1')
        os.system('powershell.exe -noexit "& "".\\prueba.ps1"""')
    # Si el sistema operativo en el que estoy es linux descargo un script shell a elección y lo ejecuto
    else:
        sftp.get('./Clases.py','./Clases.py')
        #os.chmod('./Clases.py',0o555)
        #os.system('python3.7 Clases.py')
        sftp.get('./__init__.py','./__init__.py')
    # Si ahora queremos subir algo solo habría que hacer sftp.put(rutalocal,rutaremota)
    # Cerramos conexiones y finalizamos
    sftp.close()
    ssh.close()
    #os.remove('../prueba.sh')
    print(' Se ha ejecutado correctamente ')
except KeyboardInterrupt:
    #Si ocurre algún error damos la línea y limpiamos la información de esta
    print('Algo ha ocurrido, no he podido ejecutar correctamente la línea ' + str(sys.exc_info()[2].tb_lineno))
