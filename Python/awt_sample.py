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
import socket
import time
import AWTModule.awt_module as awtmod
import datetime

COM_PORT = 39
DCFG_FILE = 'ADPD188GGZ_EVAL_PPG_Normal_01.dcfg'
CONTROL_UDP_RX_PORT = 50002
CONTROL_UDP_TX_PORT = 50001
DATA_UDP_TX_PORT = 50007
UDP_TRANSFER_IP_ADDRESS = "localhost"

AppVersion = 1.0
TIME_RUN_SECONDS = 20
TEST_SAMPLE_APPLN = True
DATAFILENAME = "udpdatafile"
UDP_ENABLE = 1
UDP_DISABLE = 0
LOG_ENABLE = 1
LOG_DISABLE = 0
ADPD188_REG_OPMODECFG_ADDR = 0x11
ADPD188_REG_CHIPID_ADDR = 0x08
ADPD188_REG_OPMODECFG_VAL = 0x0

def awt_module_control_init():
    awtmodulecontrInst = awtmod.awt_module_controller_class()    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    awtmodulecontrInst.opensock(sock, UDP_TRANSFER_IP_ADDRESS, CONTROL_UDP_TX_PORT, CONTROL_UDP_RX_PORT)
    return awtmodulecontrInst

def run_sample_controller_appln(awtmodulecontrInst):
    awtmodulecontrInst.connect(COM_PORT)
    parse_response(awtmodulecontrInst)
    if awtmodulecontrInst.responseStatus == awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_SUCCESS:
        print ("Device Connected successfully")
    time.sleep(5)
    print ("Opening ADPD View")
    awtmodulecontrInst.openview()
    parse_response(awtmodulecontrInst)
    if awtmodulecontrInst.responseStatus == awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_SUCCESS:
        print ("Modifying OPMODE Register")
        awtmodulecontrInst.regwrite(ADPD188_REG_OPMODECFG_ADDR, ADPD188_REG_OPMODECFG_VAL)    
        parse_response(awtmodulecontrInst)
        print ("Reading OPMODE Register")
        awtmodulecontrInst.regread(ADPD188_REG_OPMODECFG_ADDR)  
        parse_response(awtmodulecontrInst)
        print ("Reading Chip Register")
        awtmodulecontrInst.regread(ADPD188_REG_CHIPID_ADDR)  
        parse_response(awtmodulecontrInst)
        time.sleep(3)
        print ("\nAvailable DCFG File\n")
        awtmodulecontrInst.listDCFGs()
        parse_response(awtmodulecontrInst)
        time.sleep(2)
        print ("\nLoading the DCFG File " + DCFG_FILE + " \n")
        awtmodulecontrInst.loadDCFG(0, DCFG_FILE)
        parse_response(awtmodulecontrInst)
        print ("Selecting Plot 1 with Slot A")
        awtmodulecontrInst.slot_plot_select(1, 1)
        parse_response(awtmodulecontrInst)
        print ("Selecting Plot 2 with Slot B")
        awtmodulecontrInst.slot_plot_select(2, 2)
        parse_response(awtmodulecontrInst)
        print ("\nPlaying the data from the sensor for " + str(TIME_RUN_SECONDS) + " seconds \n")
        awtmodulecontrInst.play()
        parse_response(awtmodulecontrInst)
        if awtmodulecontrInst.responseStatus == awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_SUCCESS:
            print ("\nEnabling the Log and UDP Data transfer for " + str(TIME_RUN_SECONDS) + " seconds \n")
            awtmodulecontrInst.start_log_xfer(LOG_ENABLE)
            parse_response(awtmodulecontrInst)
            awtmodulecontrInst.start_udp_xfer(UDP_ENABLE)
            parse_response(awtmodulecontrInst)
            if awtmodulecontrInst.responseStatus == awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_SUCCESS:
                run_awtmoduletransfer_data()
            print("\nDisabling the Log \n")
            awtmodulecontrInst.start_log_xfer(LOG_DISABLE)
            parse_response(awtmodulecontrInst)
            print ("\nDisabling the UDP Data transfer\n")
            awtmodulecontrInst.start_udp_xfer(UDP_DISABLE)
            parse_response(awtmodulecontrInst)    
            print ("\nStopping the Playback of the ADPD sensor data \n")
            awtmodulecontrInst.stop()
            parse_response(awtmodulecontrInst)
            print ("\nDisconnecting the device \n")
        awtmodulecontrInst.disconnect()
        parse_response(awtmodulecontrInst)
        awtmodulecontrInst.closesock()
        
def run_awtmoduletransfer_data():
    '''
    Initiate the UDP Transfer class and start data transfer
    '''
    udpTransferInst = awtmod.awt_module_transfer_class()
    filemode = "w"; # default mode as 'write'
    
    # Open socket 
    try:            
        
        status = udpTransferInst.opensock(DATA_UDP_TX_PORT)

        print ("UDP connection status :" + str(status))
    except:
        udpTransferInst.sock = ""

    if(udpTransferInst.sock == ""):
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
         # Open files to store data and error
        try:
            currentDT = datetime.datetime.now()

            filename = DATAFILENAME + "_" + (currentDT.strftime("%Y_%m_%d_%H_%M_%S")) + ".txt"
            file = open(filename,filemode);
        except:
            file = ""
            logstr = "Data File open Error : "+str(sys.exc_info())
            print(logstr)
            
        t_end = time.time() + TIME_RUN_SECONDS
        while time.time() < t_end:    
            udpTransferInst.process()                        
            #sys.stdout.write(udpTransferInst.seqdatastr)
            if udpTransferInst.seqdatastr != "":
                file.write(udpTransferInst.seqdatastr);
            
        udpTransferInst.closesock();
        file.close()
        
def parse_response(awtmodulecontrInst):        
        if( awtmodulecontrInst.requestopt == awtmod.awt_module_response_ENUM_t.AWT_LISTCONFIG_RESPONSE_ID):
            print (awtmodulecontrInst.responsedata)
            print ("Enter load config command with any of above choice as shown below..\n")
            print ("\tEg.,0D 01 <01/02/03...>choice\n")
            print ("Response Data: ",awtmodulecontrInst.response)
        elif awtmodulecontrInst.requestopt == awtmod.awt_module_response_ENUM_t.AWT_READREG_RESPONSE_ID:
            print ("Response Data: ",awtmodulecontrInst.response,awtmodulecontrInst.responsedata)
            print ("Register Value is ", awtmodulecontrInst.responsedata)
        else:
            print ("Response Data: ",awtmodulecontrInst.response)
                      
        if(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_SUCCESS):
           print ("Response Status: Success")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_FAILED): 
          print ("Response Status: Failure")           
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_NOVIEW_AVAILABLE): 
          print ("Response Status: No View is available")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_PLAY_FAILED): 
          print ("Response Status: Cannot Play, Already in Play state")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_STOP_FAILED):                   
          print ("Response Status: Cannot Stop, Already in Stop state ")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_CALIBRATE_FAILED):
          print ("Response Status: Cannot Calibrate, Not in Stop state") 
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_RESET_REQUIRED_FOR_CALIB): 
          print ("Response Status: Reset is must for clock calibration")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_NOT_APPLICABLE): 
          print ("Response Status: Not Applicable")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_ALREADY_CONNECTED): 
          print ("Response Status: Invalid Command")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_INVALID_COMMAND): 
          print ("Response Status: Already Connected")           
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_OPENVIEW_FAILED): 
          print ("Response Status: Open Failed or View Already Opened")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_LOADCONFIG_FAILED): 
          print ("Response Status: Load Configuration Failed")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_INVALID_PARAMETER): 
          print ("Response Status: Invalid Parameter")           
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_VIEWSPLUGIN_NOTFOUND_OR_INVALID):
          print ("Response Status: Views Plugin removed or not found")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_CONFIGFILE_NOTFOUND_OR_INVALID):
          print ("Response Status: Load Configuration file not found or Invalid")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_DEVICE_NOTCONNECTED_FAILURE):
          print ("Response Status: Failed..Please Connect the device.")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_NO_CONFIGFILES_AVAILABLE):
          print ("Response Status: Failed..No Config files available")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_REG_OPERATION_FAILED_NO_DEVICE_CONNECTED):
          print ("Response Status: Failed..Connect device to Write/Read Register")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_DEVICE_ALREADY_DISCONNECTED): 
          print ("Response Status: Already Disconnected")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_LOADCONFIG_FAILED_DATAPLAYBACK_ON):
          print ("Response Status: Load Configuration Failed, Not in Stop State")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_CONNECTION_FAILED_HARDWARE_NOT_FOUND):
          print ("Response Status: Connection Failed, Target Hardware Not Found")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_CANNOT_ON_RAWDATA):
          print ("Response Status: Cannot ON the Raw data, Already in ON state")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_CANNOT_OFF_RAWDATA):
          print ("Response Status: Cannot OFF the Raw data, Already in OFF state")
        elif(awtmodulecontrInst.responseStatus==awtmod.awt_module_response_ENUM_t.AWT_RESPONSE_LISTCONFIGFILES_USE_LOADCONFIG):
          print ("Response Status: List the Configurations and use Load Config")


if __name__ == "__main__":
    awtcontrInst = awt_module_control_init()
    run_sample_controller_appln(awtcontrInst)

  

