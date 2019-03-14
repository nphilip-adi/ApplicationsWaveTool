# -*- coding: utf-8 -*-
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
import time
import datetime
import struct
import codecs
import socket

from ctypes import *

class awt_udp_transfer_class():
    
    def __init__(self):
        self.sock = ''
        self.samplecount = 0
        self.status = "Success"
        self.seqdatastr = ""
        self.num = 0
        self.dataX1arr = []
        self.dataX2arr = []
        self.dataX3arr = []
        self.dataX4arr = []
        self.dataY1arr = []
        self.dataY2arr = []
        self.dataY3arr = []
        self.dataY4arr = []
        self.samplecntarr = []
        self.DataArrayDict = {"DataX1arr": self.dataX1arr,
        "DataX2arr": self.dataX2arr,
        "DataX3arr": self.dataX3arr,
        "DataX4arr": self.dataX4arr,
        "DataY1arr": self.dataY1arr,
        "DataY2arr": self.dataY2arr,
        "DataY3arr": self.dataY3arr,
        "DataY4arr": self.dataY4arr,
        "SampleCntarr": self.samplecntarr}
        
    def opensock(self, sock, IP, Port=50007):
        status= awt_udp_response_ENUM_t.UDP_RESPONSE_SUCCESS
        try:
            sock.bind((IP, Port));
            self.sock = sock
        except:
            print("socket Bind Error "+str(sys.exc_info()))
            sock = ''
            status = awt_udp_response_ENUM_t.UDP_TRANSFER_SOCKBIND_FAILURE
        return status
        
    def closesock(self):
        self.sock.close()
        
    def _rx_pkts_udp(self, sock, Size = 200):
        recv_data = ""
        try:
            recv_data, recv_addr = sock.recvfrom(Size)
        except socket.timeout:
            logstr = "socket Receive time out  "+str(sys.exc_info()) 
            print (logstr)
            sock = ''
            return sock
        except :
            logstr = "Socket Receive Error "+str(sys.exc_info())
            print (logstr)
            return recv_data
        return recv_data

    def process(self):
        '''
        Function to convert the data from Wavetool to double values 
        to be stored in a log file or used for further processing
        '''
        Size = 200
        ReceivedPkts = self._rx_pkts_udp(self.sock, Size); 
        datasize = len(ReceivedPkts)
        if(datasize == 26):
            recvdata,data1 = ReceivedPkts[:26],ReceivedPkts[26:]
            ReceivedPkts = data1;
            sync, data1 = recvdata[:2],recvdata[2:]
            if (sync == b'F0'): # checking SYNC
                size, data2 = data1[:2],data1[2:]
                seqnum = ""
                seqnum, data1 = data2[:2],data2[2:]   
                self.num = int(seqnum,16)
                if(self.num == 0):
                    self.dataX1arr = []
                    self.samplecntarr = []
                self.samplecount = self.samplecount+1;
                self.samplecntarr.append(self.samplecount)
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    
                data1 = recvdata[10:] # skip prefix 10
                dataX1 = struct.unpack('d', codecs.decode(data1, 'hex'))[0]  ###Working
                self.dataX1arr.append(dataX1)
                self.seqdatastr = str(dataX1) + "\t" + str(timestamp) + "\t" + str(self.num) + "\n"
                self.status = "Success"                                     
            else:
                self.status = "Invalid Sync received"
    
        elif(datasize == 42):
                recvdata,data1 = ReceivedPkts[:42],ReceivedPkts[42:]
                ReceivedPkts = data1;
                sync, data1 = recvdata[:2],recvdata[2:]
                if (sync == b'F0'): # checking SYNC
                    size, data2 = data1[:2],data1[2:]
                    seqnum = ""
                    seqnum, data1 = data2[:2],data2[2:]   
                    self.num = int(seqnum,16)
                    if(self.num == 0):
                        self.dataX1arr = []
                        self.dataX2arr = []
                        self.samplecntarr = []
                    self.samplecount = self.samplecount+1;
                    self.samplecntarr.append(self.samplecount)
                    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    
                    data1 = recvdata[10:]  # skip prefix 10
                    dataX1, data2 = data1[:16], data1[16:]
                    dataX2, data1 = data2[:16], data2[16:]
                    dataX1 = struct.unpack('d', codecs.decode(dataX1, 'hex'))[0]
                    dataX2 = struct.unpack('d', codecs.decode(dataX2, 'hex'))[0]
                    
                    self.dataX1arr.append(dataX1)
                    self.dataX2arr.append(dataX2)
                    
                    self.seqdatastr = str(dataX1) + "\t" + str(dataX2) + "\t" + "\t" + str(
                            timestamp) + "\t" + str(self.num) + "\n"
                    self.status = "Success"                                      
                else:
                    self.status = "Invalid Sync received"
    
        elif(datasize == 74):
                recvdata,data1 = ReceivedPkts[:74],ReceivedPkts[74:]
                ReceivedPkts = data1;
                sync, data1 = recvdata[:2],recvdata[2:]
                if (sync == b'F0'): # checking SYNC
                    size, data2 = data1[:2],data1[2:]
                    seqnum = ""
                    seqnum, data1 = data2[:2],data2[2:]   
                    self.num = int(seqnum,16) 
                    if(self.num == 0):
                        self.dataX1arr = []
                        self.dataX2arr = []
                        self.dataY1arr = []
                        self.dataY2arr = []
                        self.samplecntarr = []
                    self.samplecount = self.samplecount+1;
                    self.samplecntarr.append(self.samplecount)
                    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    
                    data1 = recvdata[10:] # skip prefix 10
                    dataX1, data2 = data1[:16], data1[16:]
                    dataX2, data1 = data2[:16], data2[16:]
                    dataY1, data2 = data1[:16], data1[16:]
                    dataY2, data1 = data2[:16], data2[16:]
    
                    dataX1 = struct.unpack('d', codecs.decode(dataX1, 'hex'))[0]
                    dataX2 = struct.unpack('d', codecs.decode(dataX2, 'hex'))[0]
                    dataY1 = struct.unpack('d', codecs.decode(dataY1, 'hex'))[0]
                    dataY2 = struct.unpack('d', codecs.decode(dataY2, 'hex'))[0]
                    
                    self.dataX1arr.append(dataX1)
                    self.dataX2arr.append(dataX2)
                    self.dataY1arr.append(dataY1)
                    self.dataY2arr.append(dataY2)
                    
                    self.seqdatastr = str(dataX1) + "\t" + str(dataX2) + "\t" + str(
                            dataY1) + "\t" + str(dataY2) + "\t" + str(
                                    timestamp) + "\t" + str(self.num) + "\n"
                    self.status = "Success" 
                else:
                    self.status = "Invalid Sync received"
    
        elif(datasize == 90):
                recvdata,data1 = ReceivedPkts[:90],ReceivedPkts[90:]
                ReceivedPkts = data1;
                sync, data1 = recvdata[:2],recvdata[2:]
                if (sync == b'F0'): # checking SYNC
                    size, data2 = data1[:2],data1[2:]
                    seqnum = ""
                    seqnum, data1 = data2[:2],data2[2:]
                    self.num = int(seqnum,16)
                    if(self.num == 0):
                        self.dataX1arr = []
                        self.dataX2arr = []
                        self.dataX3arr = []
                        self.dataY1arr = []
                        self.dataY2arr = []
                        self.samplecntarr = []
                    self.samplecount = self.samplecount+1;
                    self.samplecntarr.append(self.samplecount)
                    
                    data1 = recvdata[10:] # skip prefix 10
                    dataX1,data2 = data1[:16],data1[16:]
                    dataX2,data1 = data2[:16],data2[16:]
                    dataY1,data2 = data1[:16],data1[16:]
                    dataY2,data1 = data2[:16],data2[16:]
                    dataX3,data2 = data1[:16],data1[16:]

                    dataX1 = struct.unpack('d', codecs.decode(dataX1, 'hex'))[0]
                    dataX2 = struct.unpack('d', codecs.decode(dataX2, 'hex'))[0]
                    dataY1 = struct.unpack('d', codecs.decode(dataY1, 'hex'))[0]
                    dataY2 = struct.unpack('d', codecs.decode(dataY2, 'hex'))[0]
                    dataX3 = struct.unpack('d', codecs.decode(dataX3, 'hex'))[0]
                    
                    self.dataX1arr.append(dataX1)
                    self.dataX2arr.append(dataX2)
                    self.dataX3arr.append(dataX3)
                    self.dataY1arr.append(dataY1)
                    self.dataY2arr.append(dataY2)
                
                    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
                    self.seqdatastr = str(dataX1)+"\t"+str(dataX2)+"\t"+str(
                            dataY1)+"\t"+str(dataY2)+"\t"+str(dataX3)+"\t"+str(
                                    timestamp)+"\t"+str(self.num)+"\n"
                    self.status = "Success"
                else:
                    self.status = "Invalid Sync received"
    
        elif (datasize == 138):
            recvdata, data1 = ReceivedPkts[:138], ReceivedPkts[138:]
            ReceivedPkts = data1;
            sync, data1 = recvdata[:2], recvdata[2:]
            if (sync == b'F0'):  # checking SYNC
                size, data2 = data1[:2], data1[2:]
                seqnum = ""
                seqnum, data1 = data2[:2], data2[2:]
                self.num = int(seqnum, 16)
                if(self.num == 0):
                    self.dataX1arr = []
                    self.dataX2arr = []
                    self.dataX3arr = []
                    self.dataX4arr = []
                    self.dataY1arr = []
                    self.dataY2arr = []
                    self.dataY3arr = []
                    self.dataY4arr = []
                    self.samplecntarr = []
                self.samplecount = self.samplecount+1;
                self.samplecntarr.append(self.samplecount)
                    
                data1 = recvdata[10:]  # skip prefix 10
                dataX1, data2 = data1[:16], data1[16:]
                dataX2, data1 = data2[:16], data2[16:]
                dataY1, data2 = data1[:16], data1[16:]
                dataY2, data1 = data2[:16], data2[16:]
    
                dataX3, data2 = data1[:16], data1[16:]
                dataX4, data1 = data2[:16], data2[16:]
                dataY3, data2 = data1[:16], data1[16:]
                dataY4, data1 = data2[:16], data2[16:]
    
                dataX1 = struct.unpack('d', codecs.decode(dataX1, 'hex'))[0]
                dataX2 = struct.unpack('d', codecs.decode(dataX2, 'hex'))[0]
                dataY1 = struct.unpack('d', codecs.decode(dataY1, 'hex'))[0]
                dataY2 = struct.unpack('d', codecs.decode(dataY2, 'hex'))[0]
                dataX3 = struct.unpack('d', codecs.decode(dataX3, 'hex'))[0]
                dataX4 = struct.unpack('d', codecs.decode(dataX4, 'hex'))[0]
                dataY3 = struct.unpack('d', codecs.decode(dataY3, 'hex'))[0]
                dataY4 = struct.unpack('d', codecs.decode(dataY4, 'hex'))[0]
                
                self.dataX1arr.append(dataX1)
                self.dataX2arr.append(dataX2)
                self.dataX3arr.append(dataX3)
                self.dataX4arr.append(dataX4)
                self.dataY1arr.append(dataY1)
                self.dataY2arr.append(dataY2)
                self.dataY3arr.append(dataY3)
                self.dataY4arr.append(dataY4)
                    
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
                self.seqdatastr = str(dataX1) + "\t" + str(dataX2) + "\t" + str(
                    dataY1) + "\t" + str(dataY2) + "\t" + str(
                    dataX3) + "\t" + str(dataX4) + "\t" + str(
                    dataY3) + "\t" + str(dataY4) + "\t" + str(
                    timestamp) + "\t" + str(self.num) + "\n"
                self.status = "Success"
            else:
                self.status = "Invalid Sync received"
                                                                
        else:
            if(ReceivedPkts != ""):                                                                           
                self.status = "Received pocket size less than 13bytes"
                
        return self.DataArrayDict
    
class awt_udp_controller_class():
    
    def __init__(self):

        self.response = ""
        self.responseStatus = awt_udp_response_ENUM_t.UDP_RESPONSE_SUCCESS
        self.responsedata = ""
        self.dcfgdict = {}
        self.command = ""
        self.requestopt = 0
        self.ipaddr = '0.0.0.0'
        self.txportnum = 50001
        self.rxportnum = 50002
        self.sock = ''
        
    def opensock(self, sock, IPaddr = 'localhost', TxPortNum = 50001, RxPortNum = 50002):
        try:
            self.txportnum = TxPortNum
            self.rxportnum = RxPortNum
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.ipaddr, self.rxportnum))
            self.sock.setblocking(0)
            self.sock.settimeout(60)
            self.ipaddr = IPaddr
        except:
            self.responseStatus = awt_udp_response_ENUM_t.UDP_CONTROLLER_SOCKBIND_FAILURE
            
    def closesock(self):
        self.sock.close()
        
    def _send_command_udp(self):
        size = self.sock.sendto(self.command, (self.ipaddr, self.txportnum));
        if size!= len(self.command) :
            self.responseStatus = awt_udp_response_ENUM_t.UDP_RESPONSE_SEND_FAILED
            
    def _rx_pkts_udp(self):
        recv_data = ""      # to return string object by default even if recvfrom is timedout and not returned any object/string for rec_data

        try:
            recv_data, recv_addr = self.sock.recvfrom(8192)    # size <- if size < UDP Packet size, only the partial data copied and rest of data in UDP packet will be ignored/lost

        except socket.timeout:
            self.responseStatus = awt_udp_response_ENUM_t.UDP_RESPONSE_FAILED

        return recv_data
        
    def regread(self, regaddr):
        '''
        The Controller Request API for Read register operation. 
        This function will:
            1. Create the message to READ register
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
            5. Register value is stored in self.responsedata
        '''
        str_array = bytearray(3)        
        str_array[0] = int("00", 16)
        str_array[1] = int("01", 16)
        str_array[2] = regaddr
        self.command = bytes(memoryview(str_array))
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
        
    def regwrite(self, regaddr, regval):
        '''
        The Controller Request Message Builder for Write register operation. 
        This function will:
            1. Create the message to WRITE register
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
            5. regaddr is one byte and regval is 2 bytes
        '''
        str_array = bytearray(5)
        str_array[0] = int("01", 16)
        str_array[1] = int("03", 16)
        str_array[2] = regaddr
        str_array[3] = regval.to_bytes(2, byteorder='big')[0]
        str_array[4] = regval.to_bytes(2, byteorder='big')[1]
        self.command = bytes(memoryview(str_array))
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
        
    def play(self):
        '''
        The Controller Request API for Play ADPD sensor operation. 
        This function will:
            1. Create the message to Play ADPD Sensor data
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
        '''
        str_array = bytearray(2)
        str_array[0] = int("02", 16)
        str_array[1] = int("00", 16)
        self.command = bytes(memoryview(str_array))
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)

    def stop(self):
        '''
        The Controller Request API for Stop ADPD sensor operation. 
        This function will:
            1. Create the message to Stop ADPD Sensor data
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
        '''
        str_array = bytearray(2)
        str_array[0] = int("03", 16)
        str_array[1] = int("00", 16)
        self.command = bytes(memoryview(str_array))     
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
        
    def start_udp_xfer(self, isEnable = 0):
        '''
        The Controller Request API for Stop ADPD sensor operation. 
        This function will:
            1. Create the message to start or stop data transfer
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
        '''
        str_array = bytearray(3)
        str_array[0] = int("06", 16)
        str_array[1] = int("01", 16)
        str_array[2] = isEnable
        self.command = bytes(memoryview(str_array))     
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)  
        
    def disconnect(self):
        '''
        The Controller Request API for disconnecting the sensor board. 
        This function will:
            1. Create the message to disconnect the ADPD sensor board
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
        '''
        str_array = bytearray(2)
        str_array[0] = int("0B", 16)
        str_array[1] = int("00", 16)
        self.command = bytes(memoryview(str_array))  
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
        
    def openview(self, view = 0):
        '''
        The Controller Request API for opening the ADPD View. 
        This function will:
            1. Create the message for opening the ADPD View
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
        '''
        str_array = bytearray(2)
        str_array[0] = int("0C", 16)
        str_array[1] = int("00", 16)
        self.command = bytes(memoryview(str_array))
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
            
    def listDCFGs(self):
        '''
        The Controller Request API for listing the available DCFG files. 
        This function will:
            1. Create the message for listing the available DCFG files
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
            5. The DCFG list is stored in a Dictionary and in 
               string format to be displayed to the user in console
        '''
        str_array = bytearray(2)
        str_array[0] = int("0D", 16)
        str_array[1] = int("00", 16)
        self.command = bytes(memoryview(str_array))
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)

    def loadDCFG(self, dcfgsel=0, dcfgfile=""):
        '''
        The Controller Request API for loading the selected DCFG file. 
        The selection can be either through the number corresponding to the file
        or by the dcfg filename itself.
        This function will:
            1. Create the message for opening the ADPD View
            2. Send the message to the Wavetool
            3. Get the response from the Wavetool
            4. Parse the response to match the request
            5. the DCFG list is stored in a Dictionary and in 
               string format to be displayed to the user in console
        '''
        str_array = bytearray(3)
        str_array[0] = int("0D", 16)
        str_array[1] = int("01", 16)
        if(dcfgfile==""):
            str_array[2] = dcfgsel
        else:
            try:
                dcfgsel = self.dcfgdict[dcfgfile]
                str_array[2] = dcfgsel
            except:
                self.responseStatus = awt_udp_response_ENUM_t.UDP_RESPONSE_CONFIGFILE_NOTFOUND_OR_INVALID
                return
        self.command = bytes(memoryview(str_array)) 
        self._send_command_udp();
        ReceivedPkts = self._rx_pkts_udp()
        self._udp_controller_response(ReceivedPkts)
            
    
    def _udp_controller_response(self, ReceivedPkts):
        '''
        The Controller Response Message Parser
        '''
        if len(ReceivedPkts)>0 :
           RegisterValue = [];
           Receiveddata = [];
           Receiveddata2 = [];
           Receiveddata,Receiveddata2=ReceivedPkts[:3],ReceivedPkts[3:]           

           arg1 = Receiveddata[0]
           arg2 = Receiveddata[1]
           self.requestopt = arg1
           self.response = Receiveddata
           self.responsedata = ""
           
           # If List config files
           if(arg1 == awt_udp_response_ENUM_t.UDP_LISTCONFIG_RESPONSE_ID):
               Receiveddata1 = Receiveddata2.decode('ascii')
               receivedfiles = Receiveddata1.split("\r\n")

               for i in range(len(receivedfiles)):
                   number = hex(i+1)
                   self.dcfgdict[str(receivedfiles[i])] = int(number, 16)
                   number = number.replace(number[:2],'')
                   if(len(number) == 1):
                       number = "0"+number                           
                   self.responsedata = self.responsedata + (""+number.upper()+" )"+receivedfiles[i] + "\n")
               
           # If Register Read operation    
           elif (len(Receiveddata2) == 2 and arg1 == awt_udp_response_ENUM_t.UDP_READREG_RESPONSE_ID):

               RegisterValue = int.from_bytes(Receiveddata2, byteorder='big')
               self.responsedata = RegisterValue
           else:
               if len(Receiveddata2) > 0:
                   self.responsedata = Receiveddata2.decode('ascii')

           self.responseStatus = arg2
           Receiveddata = ""
           Receiveddata2 = ""
        else :
            self.responseStatus = "Received message size is zero"
            
class awt_udp_response_ENUM_t(c_ushort):
    '''
    Class defining the Enumerations for the response status.
    '''
    UDP_RESPONSE_SUCCESS = 0x0
    UDP_RESPONSE_FAILED = 0x01
    UDP_RESPONSE_SEND_FAILED = 0x02
    UDP_RESPONSE_NOVIEW_AVAILABLE = 0x04
    UDP_RESPONSE_PLAY_FAILED = 0x05
    UDP_RESPONSE_STOP_FAILED = 0x06
    UDP_RESPONSE_CALIBRATE_FAILED = 0x07
    UDP_RESPONSE_RESET_REQUIRED_FOR_CALIB = 0x08
    UDP_RESPONSE_NOT_APPLICABLE = 0x09
    UDP_RESPONSE_ALREADY_CONNECTED = 0x0A
    UDP_RESPONSE_INVALID_COMMAND = 0x0B
    UDP_RESPONSE_OPENVIEW_FAILED = 0x0C
    UDP_RESPONSE_LOADCONFIG_FAILED = 0x0D
    UDP_RESPONSE_INVALID_PARAMETER = 0x0E
    UDP_RESPONSE_VIEWSPLUGIN_NOTFOUND_OR_INVALID = 0xA0
    UDP_RESPONSE_CONFIGFILE_NOTFOUND_OR_INVALID = 0xB0
    UDP_RESPONSE_DEVICE_NOTCONNECTED_FAILURE = 0xC0
    UDP_RESPONSE_NO_CONFIGFILES_AVAILABLE = 0xE0
    UDP_RESPONSE_REG_OPERATION_FAILED_NO_DEVICE_CONNECTED = 0xF0
    UDP_RESPONSE_DEVICE_ALREADY_DISCONNECTED = 0x1A
    UDP_RESPONSE_LOADCONFIG_FAILED_DATAPLAYBACK_ON = 0x1B
    UDP_RESPONSE_CONNECTION_FAILED_HARDWARE_NOT_FOUND = 0x1C
    UDP_RESPONSE_CANNOT_ON_RAWDATA = 0x1E
    UDP_RESPONSE_CANNOT_OFF_RAWDATA = 0x1F
    UDP_RESPONSE_LISTCONFIGFILES_USE_LOADCONFIG = 0x2A
    
    UDP_TRANSFER_SOCKOPEN_FAILURE = 0x30
    UDP_TRANSFER_SOCKBIND_FAILURE = 0x31
    UDP_CONTROLLER_SOCKBIND_FAILURE = 0x32
    
    UDP_LISTCONFIG_RESPONSE_ID = 0x95
    UDP_READREG_RESPONSE_ID = 0x80
    UDP_DATATRANSFER_RESPONSE_ID = 0x86
    
    UDP_ADPDVIEW_ID = 0x40
    UDP_SMOKEVIEW_IP = 0x41