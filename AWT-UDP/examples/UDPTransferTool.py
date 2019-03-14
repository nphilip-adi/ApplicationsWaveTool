"""
/******************************************************************************
* Copyright (c) 2019 Analog Devices, Inc.  All rights reserved. 
*  
* Redistribution and use in source and binary forms, with or without 
* modification, are permitted provided that the following conditions are met:   
* - Redistributions of source code must retain the above copyright notice, this 
*   list of conditions and the following disclaimer.   
* - Redistributions in binary form must reproduce the above copyright notice, 
*   this list of conditions and the following disclaimer in the documentation 
*   and/or other materials provided with the distribution.     
* - Modified versions of the software must be conspicuously marked as such.   
* - This software is licensed solely and exclusively for use with 
*   processors/products manufactured by or for Analog Devices, Inc.   
* - This software may not be combined or merged with other code in any manner 
*   that would cause the software to become subject to terms and conditions 
*   which differ from those listed here.   
* - Neither the name of Analog Devices, Inc. nor the names of its contributors 
*   may be used to endorse or promote products derived from this software 
*   without specific prior written permission.   
* - The use of this software may or may not infringe the patent rights of one 
*   or more patent holders.  This license does not release you from the 
*   requirement that you obtain separate licenses from these patent holders to 
*   use this software. 
* 
* THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS" 
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
* NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
* ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE 
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR 
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF 
* CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF 
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
* POSSIBILITY OF SUCH DAMAGE. 
******************************************************************************/

"""

import sys
import os
import time
import socket
import msvcrt

from ctypes import *
import awt_udp_module as udpmod

AppVersion = 0.4

def FileOpen(name = "test.txt", mode = "w"):
    try:
            ipfile = open(name, mode)
    except :
            ipfile = ""
            return ipfile
    else:
            return ipfile

def FileClose(file ):
    file.close()

def FileWrite(ipfile, data):
    ipfile.write(data);

def OpenSocket():
    sock = ''
    try:
        print ("opensocket",IP)
        sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    except:
        print("Socket Open Error "+str(sys.exc_info()))
        return sock
    
    sock.settimeout(5); #1sec

    return sock

if __name__ == '__main__':        
        Size = 200;
        Port = 50007;
        IP = '0.0.0.0';
        filename = "test.txt";
        filemode = "w"; # default mode as 'write'
        SequenceNumber = 0;
        num = 0;
        flag = True;
        packetsize = 26; # 13bytes -> sync(F0) 1byte + size 2 byte + sequence number 2 byte + time stamp 2 bytes + x1 2bytes + x2 2bytes + y1 2bytes + y2 2bytes
        recvcount = 0;
        samplecount = 0;
        Initial = True
        Escape = False

        udpTransferInst = udpmod.awt_udp_transfer_class()
        
        # Open socket 
        try:            
            sock = OpenSocket()
            status = udpTransferInst.opensock(sock, IP, Port)

            print ("UDP connection status :" + str(status))
        except Exception as ex:
            sock = ""

        if(sock == ""):
            print ("Exiting the application socket block")
            time.sleep(1);
            sys.stdin.close();
            sys.exit(0);
        else:
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print ("\t\t\tUDP TRANSFER TOOL\n")
            print ("UDP Port Number: 50007")
            print ("Version        : " + str(AppVersion))
            print ("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")           
            
            
            print ("Press ESC to Stop Receiving Data")
            try:                        
                while True:
                        
                    if(Initial == True):                                                                                                
                        # Get file name
                        try:                                                        
                            while True:
                                UserFile = input('Enter the File name : ');
                                if(UserFile != ""):
                                    break
                                else:
                                    continue                                                                                                        
                        except:
                            print ("\nQuitting ...")
                            udpTransferInst.closesock();
                            FileClose(file);
                            time.sleep(2);
                            sys.stdin.close();
                            sys.exit(0);

                        filename = UserFile;

                        # Open files to store data and error
                        try:
                            file = FileOpen(filename,filemode);
                        except:
                            file = ""
                            logstr = "Data File open Error : "+str(sys.exc_info())
                            print(logstr)
                                        
                        if(file == ""):
                            print ("Couldn't Open File. Exiting the application")
                            time.sleep(1);
                            sys.stdin.close();
                            sys.exit(0);
                        Initial = False
                    
                    if msvcrt.kbhit():
                        if ord(msvcrt.getch()) == 27:
                                Escape = True                                                        
                    sys.stdout.write("\rReceived Packet Count: " +str(udpTransferInst.samplecount))
                    #sys.stdout.write("\rSequence Number: "+str(num))
                    
                    if(Escape == False):

                        udpTransferInst.process()
                        
                        sys.stdout.write("\rSequence Number: "+str(udpTransferInst.num))
                        FileWrite(file,udpTransferInst.seqdatastr);
                        sys.stdout.write("\rReceived Packet Count: "+str(udpTransferInst.samplecount))   
                                                
                    if(Escape == True):
                            print ("\nUDP files saved at :")
                            print ("\nRaw data      :",os.path.abspath(file.name))
                            print ("\nPress Ctrl+C to Quit\n")
                            FileClose(file);
                            #FileClose(logfile);                                       
                            Initial = True
                            Escape = False
                            samplecount = 0
                            ReceivedPkts = ""
                                                                    
            except KeyboardInterrupt:
                print ("\nKeyboard Interrupt")
                udpTransferInst.closesock();
                FileClose(file);

                time.sleep(2)
                sys.stdin.close();
                sys.exit(0);

