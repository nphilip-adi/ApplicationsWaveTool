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


import time
import datetime
import struct
import codecs
from enum import Enum


class CoolidgeDataBuffers:
    def __init__(self):
        self.SLOTA_DataArr = [[],[]]
        self.SLOTB_DataArr = [[],[]]
        self.SLOTC_DataArr = [[],[]]
        self.SLOTD_DataArr = [[],[]]
        self.SLOTE_DataArr = [[],[]]
        self.SLOTF_DataArr = [[],[]]
        self.SLOTG_DataArr = [[],[]]
        self.SLOTH_DataArr = [[],[]]
        self.SLOTI_DataArr = [[],[]]
        self.SLOTJ_DataArr = [[],[]]
        self.SLOTK_DataArr = [[],[]]
        self.SLOTL_DataArr = [[],[]]
        self.SLOTA_CntArr = []
        self.SLOTB_CntArr = []
        self.SLOTC_CntArr = []
        self.SLOTD_CntArr = []
        self.SLOTE_CntArr = []
        self.SLOTF_CntArr = []
        self.SLOTG_CntArr = []
        self.SLOTH_CntArr = []
        self.SLOTI_CntArr = []
        self.SLOTJ_CntArr = []
        self.SLOTK_CntArr = []
        self.SLOTL_CntArr = []
        self.slotA_samplecount = 0
        self.slotB_samplecount = 0
        self.slotC_samplecount = 0
        self.slotD_samplecount = 0
        self.slotE_samplecount = 0
        self.slotF_samplecount = 0
        self.slotG_samplecount = 0
        self.slotH_samplecount = 0
        self.slotI_samplecount = 0
        self.slotJ_samplecount = 0
        self.slotK_samplecount = 0
        self.slotL_samplecount = 0

class GraphDataParser():

    def __init__(self):
        self.datazize = 0
        self.samplecount = 0
        self.status = "Success"
        self.seqdatastr = ""
        self.m2m2datastr = ""
        self.frameSz = 34

        self.num = 0
        self.dataarr = []
        self.slotarr = []
        self.unitarr = []
        self.offsetarr = []
        self.slotinfoarr = []
        self.channel_infoarr = []
        self.DSLinfoarr = []

        # ADPD/SMOKE
        self.slot_a = ""
        self.slot_b = ""
        self.SlotA_DataArr = [[], [], [], []]
        self.SlotB_DataArr = [[], [], [], []]
        self.SlotA_CntArr = []  # no need of cnt array
        self.SlotB_CntArr = []
        self.samplecntarr = []

        #Sync PPG and PPG
        self.HR_DataArr = []
        self.X_DataArr = []
        self.Y_DataArr = []
        self.Z_DataArr = []
        self.PPG_DataArr = []
        self.SyncPPG_CntArr = []

        self.samplecntarr = []
        self.adpd4000CH1_inst = CoolidgeDataBuffers()
        self.adpd4000CH2_inst = CoolidgeDataBuffers()

        self.header_write = False

    def parse_GraphData(self, ReceivedPkts):
        self.dataarr.clear()
        self.slotarr.clear()
        self.unitarr.clear()
        self.offsetarr.clear()
        self.slotinfoarr.clear()
        self.channel_infoarr.clear()
        self.DSLinfoarr.clear()
        self.seqdatastr = ""

        sync = ReceivedPkts[0]

        if sync == 0xA0: #ADPD,SMOKE
            size_data = ReceivedPkts[1:3]
            seq_num = ReceivedPkts[3:5]
            ts = ReceivedPkts[5:9]
            slot_info = ReceivedPkts[9]
            plot1_info = ReceivedPkts[10]
            plot2_info = ReceivedPkts[11]

            self.num = struct.unpack('H', seq_num)[0]

            if ((self.samplecount % self.frameSz) == 0):
                self.clear_data_buffers()

            self.samplecount = self.samplecount + 1;
            self.samplecntarr.append(self.samplecount)

            timestamp = struct.unpack('I', ts)[0]
            timestamp = self.get_time(timestamp)

            slot1 = self.getBitValues(slot_info, 0, 3)
            slot2 = self.getBitValues(slot_info, 4, 7)
            unit1 = self.getBitValues(plot1_info, 0, 1)
            offset1 = self.getBitValues(plot1_info, 4, 5)
            unit2 = self.getBitValues(plot2_info, 0, 1)
            offset2 = self.getBitValues(plot2_info, 4, 5)

            self.slot_a = self.get_slotname(slot1)
            self.slot_b = self.get_slotname(slot2)
            self.slotarr.append(self.slot_a)
            self.slotarr.append(self.slot_b)

            unit_a = self.get_unitname(unit1)
            unit_b = self.get_unitname(unit2)
            self.unitarr.append(str(unit_a))
            self.unitarr.append(str(unit_b))

            offset_a = self.get_offsetname(offset1)
            offset_b = self.get_offsetname(offset2)
            self.offsetarr.append(str(offset_a))
            self.offsetarr.append(str(offset_b))

            data1 = ReceivedPkts[12:]  # skip prefix 12
            length = int(len(data1) / 8)
            increment = 8
            startbit = 12

            if len(data1) % 8 != 0:
                print("Not in a correct length")

            for x in range(length):
                data = ReceivedPkts[startbit:(startbit + increment)]
                data = struct.unpack('d', data)[0]
                self.dataarr.append(data)
                startbit += increment

            if not self.header_write:
                self.write_header(self.slotarr,self.unitarr,self.offsetarr)

            data_index = 0
            if(self.slot_a is not Slotsize.SLOT_OFF):
                if self.slot_a == Slot.SLOT_SUM:
                    self.SlotA_DataArr[0].append(self.dataarr[data_index])
                    self.seqdatastr += str(self.dataarr[data_index]) + "\t"
                    data_index += 1
                elif self.slot_a == Slot.SLOT_4CH:
                    for i in range(4):
                        self.SlotA_DataArr[i].append(self.dataarr[i])
                    self.seqdatastr += str(self.dataarr[0]) + "\t" + str(self.dataarr[1]) + "\t" + str(self.dataarr[2]) + "\t" + str(self.dataarr[3]) + "\t"
                    data_index += 4

            if (self.slot_b is not Slotsize.SLOT_OFF):
                if self.slot_b == Slot.SLOT_SUM:
                    self.SlotB_DataArr[0].append(self.dataarr[data_index])
                    self.seqdatastr += str(self.dataarr[data_index]) + "\t"
                elif self.slot_b == Slot.SLOT_4CH:
                    for i in range(4):
                        self.SlotB_DataArr[i].append(self.dataarr[data_index])
                        data_index += 1
                    self.seqdatastr += str(self.dataarr[data_index - 4]) + "\t" + str(self.dataarr[data_index - 3]) + "\t" + str(self.dataarr[data_index - 2]) + "\t" + str(self.dataarr[data_index - 1]) + "\t"


            self.status = "Success"
            self.seqdatastr += str(timestamp) + "\t" + str(self.num) + "\n"
            self.m2m2datastr = ""

        elif sync == 0xB0: #ADPDCL,ECG
            size_data = ReceivedPkts[1:3]
            seq_num = ReceivedPkts[3:5]
            ts = ReceivedPkts[5:9]
            slot_info = ReceivedPkts[9:21]

            length = int(len(slot_info))
            for x in range(length):
                info = slot_info[x]
                DSL_info = self.getBitValues(info, 0, 5)
                channel_info = self.getBitValues(info, 6, 7)
                self.slotinfoarr.append(info)
                self.channel_infoarr.append(channel_info)
                self.DSLinfoarr.append(DSL_info)

            view_info = ReceivedPkts[21]
            plot1_info = ReceivedPkts[22]
            plot2_info = ReceivedPkts[23]

            self.num = struct.unpack('H', seq_num)[0]

            self.samplecount = self.samplecount + 1
            self.samplecntarr.append(self.samplecount)

            timestamp = struct.unpack('I', ts)[0]
            timestamp = self.get_time(timestamp)

            #timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

            unit1 = self.getBitValues(plot1_info, 0, 1)
            offset1 = self.getBitValues(plot1_info, 4, 5)
            unit2 = self.getBitValues(plot2_info, 0, 1)
            offset2 = self.getBitValues(plot2_info, 4, 5)

            unit_a = self.get_unitname(unit1)
            unit_b = self.get_unitname(unit2)
            self.unitarr.append(str(unit_a))
            self.unitarr.append(str(unit_b))

            offset_a = self.get_offsetname(offset1)
            offset_b = self.get_offsetname(offset2)
            self.offsetarr.append(str(offset_a))
            self.offsetarr.append(str(offset_b))

            data1 = ReceivedPkts[24:]  # skip prefix 24
            length = int(len(data1) / 8)
            increment = 8
            startbit = 24

            if len(data1) % 8 != 0:
                print("Not in a correct length")

            for x in range(length):
                data = ReceivedPkts[startbit:(startbit + increment)]
                data = struct.unpack('d',data)[0]
                self.dataarr.append(data)
                startbit += increment


            length = int(len(slot_info))
            idx = 0
            ndatabuffindex = 0
            for x in range(length):
                d1_data = 0
                d2_data = 0
                s1_data = 0
                s2_data = 0
                ch1_bit = self.channel_infoarr[idx] >> 0 & 1
                ch2_bit = self.channel_infoarr[idx] >> 1 & 1
                d1_bit = self.DSLinfoarr[idx] >> 0 & 1
                d2_bit = self.DSLinfoarr[idx] >> 1 & 1
                s1_bit = self.DSLinfoarr[idx] >> 2 & 1
                s2_bit = self.DSLinfoarr[idx] >> 3 & 1
                if d1_bit is 1:
                    d1_data = self.dataarr[ndatabuffindex]
                    ndatabuffindex += 1
                if s1_bit is 1:
                    s1_data = self.dataarr[ndatabuffindex]
                    ndatabuffindex += 1
                if d2_bit is 1:
                    d2_data = self.dataarr[ndatabuffindex]
                    ndatabuffindex += 1
                if s2_bit is 1:
                    s2_data = self.dataarr[ndatabuffindex]
                    ndatabuffindex += 1

                if idx is 0 and self.channel_infoarr[idx] != 0: #SLOTA
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotA_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTA_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTA_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTA_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotA_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotA_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTA_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTA_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTA_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotA_samplecount += 1
                elif idx is 1 and self.channel_infoarr[idx] != 0:  #SLOTB
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotB_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTB_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTB_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTB_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotB_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotB_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTB_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTB_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTB_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotB_samplecount += 1
                elif idx is 2 and self.channel_infoarr[idx] != 0:  #SLOTC
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotC_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTC_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTC_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTC_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotC_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotC_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTC_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTC_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTC_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotC_samplecount += 1
                elif idx is 3 and self.channel_infoarr[idx] != 0:  #SLOTD
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotD_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTD_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTD_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTD_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotD_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotD_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTD_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTD_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTD_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotD_samplecount += 1
                elif idx is 4 and self.channel_infoarr[idx] != 0:  #SLOTE
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotE_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTE_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTE_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTE_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotE_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotE_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTE_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTE_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTE_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotE_samplecount += 1
                elif idx is 5 and self.channel_infoarr[idx] != 0:  #SLOTF
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotF_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTF_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTF_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTF_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotF_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotF_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTF_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTF_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTF_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotF_samplecount += 1
                elif idx is 6 and self.channel_infoarr[idx] != 0:  #SLOTG
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotG_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTG_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTG_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTG_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotG_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotG_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTG_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTG_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTG_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotG_samplecount += 1
                elif idx is 7 and self.channel_infoarr[idx] != 0:  #SLOTH
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotH_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTH_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTH_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTH_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotH_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotH_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTH_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTH_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTH_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotH_samplecount += 1
                elif idx is 8 and self.channel_infoarr[idx] != 0:  #SLOTI
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotI_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTI_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTI_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTI_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotI_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotI_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTI_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTI_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTI_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotI_samplecount += 1
                elif idx is 9 and self.channel_infoarr[idx] != 0:  #SLOTJ
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotJ_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTJ_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTJ_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTJ_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotJ_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotJ_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTJ_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTJ_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTJ_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotJ_samplecount += 1
                elif idx is 10 and self.channel_infoarr[idx] != 0:  #SLOTK
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotK_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTK_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTK_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTK_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotK_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotK_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTK_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTK_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTK_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotK_samplecount += 1
                elif idx is 11 and self.channel_infoarr[idx] != 0:  #SLOTL
                    if ch1_bit is 1:
                        if (self.adpd4000CH1_inst.slotL_samplecount % self.frameSz) == 0:
                            self.adpd4000CH1_inst.SLOTL_DataArr = [[],[]]
                        self.adpd4000CH1_inst.SLOTL_DataArr[0].append(d1_data)
                        self.adpd4000CH1_inst.SLOTL_DataArr[1].append(s1_data)
                        self.adpd4000CH1_inst.slotL_samplecount += 1
                    if ch2_bit is 1:
                        if (self.adpd4000CH2_inst.slotL_samplecount % self.frameSz) == 0:
                            self.adpd4000CH2_inst.SLOTL_DataArr = [[],[]]
                        self.adpd4000CH2_inst.SLOTL_DataArr[0].append(d2_data)
                        self.adpd4000CH2_inst.SLOTL_DataArr[1].append(s2_data)
                        self.adpd4000CH2_inst.slotL_samplecount += 1
                idx += 1

            if not self.header_write:
                self.write_ADPDCL_header(view_info)

            length = len(self.dataarr)
            str_data = ""
            for x in range(length):
                str_data += str(self.dataarr[x]) + "\t"

            self.seqdatastr += str_data + str(timestamp) + "\t" + str(self.num) + "\n"

        elif sync == 0xD0:  #PPG
            size_data = ReceivedPkts[1:3]
            seq_num = ReceivedPkts[3:5]
            ts = ReceivedPkts[5:9]

            self.num = struct.unpack('H', seq_num)[0]

            timestamp = struct.unpack('I', ts)[0]
            timestamp = self.get_time(timestamp)

            data1 = ReceivedPkts[9:]  # skip prefix 9
            length = int(len(data1) / 8)
            increment = 8
            startbit = 9

            if len(data1) % 8!= 0:
                print("Not in a correct length")

            for x in range(length):
                data = ReceivedPkts[startbit:(startbit + increment)]
                data = struct.unpack('d', data)[0]
                self.dataarr.append(data)
                startbit += increment

            if not self.header_write:
                self.seqdatastr = "ADPD_Data" + "\t" + "Data_X" + "\t" + "Data_Y" + "\t" + "Data_Z" + "\t" + "HR" + "\t" + "Time Stamp" + "\t" + "Sequence Number\n"
                self.header_write = True

            if ((self.samplecount % self.frameSz) == 0):
                self.clear_ppg_data_buffers()

            self.samplecount = self.samplecount + 1
            self.SyncPPG_CntArr.append(self.samplecount)

            self.PPG_DataArr.append(self.dataarr[0])
            self.X_DataArr.append(self.dataarr[1])
            self.Y_DataArr.append(self.dataarr[2])
            self.Z_DataArr.append(self.dataarr[3])
            self.HR_DataArr.append(self.dataarr[4])

            self.seqdatastr += str(self.dataarr[0]) + "\t" + str(self.dataarr[1]) + "\t" + str(
                self.dataarr[2]) + "\t" + str(self.dataarr[3]) + "\t" + str(self.dataarr[4]) + "\t" + str(
               timestamp) + "\t" + str(self.num) + "\n"
          

        return self.seqdatastr

    def getBitValues(self,value, startBit, endBit):
        '''
        To get the value of the bits specified
        '''
        Temp = value
        Temp <<= 15 - endBit
        Temp = Temp & 0xffff
        Temp >>= 15 - endBit + startBit
        Temp = Temp & 0xffff
        return Temp

    def clear_data_buffers(self):
        self.SlotA_DataArr = [[], [], [], []]
        self.SlotB_DataArr = [[], [], [], []]
        self.samplecntarr = []

    def clear_ppg_data_buffers(self):
        self.PPG_DataArr.clear()
        self.X_DataArr.clear()
        self.Y_DataArr.clear()
        self.Z_DataArr.clear()
        self.HR_DataArr.clear()
        self.SyncPPG_CntArr.clear()


    def get_slotname(self, slot):
        if slot == 1:
            active_slot = Slot.SLOT_SUM
        elif slot == 2:
            active_slot = Slot.SLOT_4CH
        elif slot == 3:
            active_slot = Slot.SLOT_DIM
        else:
            active_slot = Slot.SLOT_OFF
        return active_slot

    def get_unitname(self, unit):
        if unit == 0:
            unit_name = Unit.COUNT.name
        elif unit == 1:
            unit_name = Unit.CTR.name
        elif unit == 2:
            unit_name = Unit.PTR.name
        elif unit == 3:
            unit_name = Unit.UV.name

        return unit_name

    def get_offsetname(self, offset):
        if offset == 0:
            offset_name = Offset.NO_OFFSET.name
        elif offset == 1:
            offset_name = Offset.NULL_OFFSET.name
        elif offset == 2:
            offset_name = Offset.STATS_OFFSET.name
        elif offset == 3:
            offset_name = Offset.NULL_STATS_OFFSET.name

        return offset_name

    def get_slotsize(self,slot):
        if slot == Slot.SLOT_OFF.value:
            size = 0
        elif slot == Slot.SLOT_SUM.value:
            size = 1
        elif slot == Slot.SLOT_4CH.value:
            size = 4
        elif slot == Slot.SLOT_DIM.value:
            size = 1

        return size

    def write_header(self,slot,unit,offset):
        str_header = ""
        if slot[0] != Slot.SLOT_OFF.name:
            if slot[0] == Slot.SLOT_SUM.name:
                str_header = "Slot A : SUM " + "\t"
            elif slot[0] == Slot.SLOT_4CH.name:
                str_header = "Slot A : 4CH " + "\t"

            str_header += "Plot 1 Unit : " + str(unit[0]) + "\t"
            str_header += "Plot 1 Offset : " + str(offset[0]) + "\t"

        if slot[1] != Slot.SLOT_OFF.name:
            if slot[1] == Slot.SLOT_SUM.name:
                str_header += "Slot B : SUM " + "\t"
            elif slot[1] == Slot.SLOT_4CH.name:
                str_header += "Slot B : 4CH " + "\t"

            str_header += "Plot 2 Unit : " + str(unit[1]) + "\t"
            str_header += "Plot 2 Offset : " + str(offset[1]) + "\t"

        str_header += "\n"

        if slot[0] != Slot.SLOT_OFF:
            if slot[0] == Slot.SLOT_SUM:
                str_header += "SUM" + "\t"
            elif slot[0] == Slot.SLOT_4CH:
                str_header += "CH1" + "\t" + "CH2" + "\t" + "CH3" + "\t" + "CH4" + "\t"

        if slot[1] != Slot.SLOT_OFF:
            if slot[1] == Slot.SLOT_SUM:
                str_header += "SUM" + "\t"
            elif slot[1] == Slot.SLOT_4CH:
                str_header += "CH1" + "\t" + "CH2" + "\t" + "CH3" + "\t" + "CH4" + "\t"

        self.seqdatastr += str_header + "Time Stamp" + "\t" + "Sequence Number\n"
        self.header_write = True

    def write_ADPDCL_header(self,view_info):
        str_header = ""

        if view_info == 1:
            str_header += "View : MultiSlot View" + "\t"
            str_header += "Plot Unit : " + str(self.unitarr[0]) + "\t"
            str_header += "Plot Offset : " + str(self.offsetarr[0]) + "\n"
        elif view_info == 0:
            str_header += "View : Time View" + "\t"
            str_header += "Plot 1 Unit : " + str(self.unitarr[0]) + "\t"
            str_header += "Plot 1 Offset : " + str(self.offsetarr[0]) + "\t"

            str_header += "Plot 2 Unit : " + str(self.unitarr[1]) + "\t"
            str_header += "Plot 2 Offset : " + str(self.offsetarr[1]) + "\n"

        length = len(self.slotinfoarr)
        for x in range(length):
            if self.slotinfoarr[x] != 0:
                if self.channel_infoarr[x] == 1:
                    str_header += ADPDCL_Slot(x).name + " CH1 " + "\t"
                elif self.channel_infoarr[x] == 2:
                    str_header += ADPDCL_Slot(x).name + " CH1 " + "\t" +  ADPDCL_Slot(x).name + " CH2 " + "\t"

        self.seqdatastr = str_header + "Time Stamp" + "\t" + "Sequence Number\n"
        self.header_write = True

    def get_time(self, timestamp):
        str_time = ""

        seconds = (timestamp / 1000) % 60
        seconds = int(seconds)
        minutes = (timestamp / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (timestamp / (1000 * 60 * 60)) % 24
        hours = int(hours)

        str_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        return str_time

class Slot(Enum):
    SLOT_OFF = 0
    SLOT_SUM = 1
    SLOT_4CH = 2
    SLOT_DIM = 3

class Slotsize(Enum):
    SLOT_OFF = 0
    SLOT_SUM = 1
    SLOT_SUM_SUM = 2
    SLOT_4CH = 4
    SLOT_SUM_4CH = 5
    SLOT_4CH_4CH = 8

class Unit(Enum):
    COUNT = 0
    CTR = 1
    PTR = 2
    UV = 3

class Offset(Enum):
    NO_OFFSET = 0
    NULL_OFFSET = 1
    STATS_OFFSET = 2
    NULL_STATS_OFFSET = 3

class ADPDCL_Slot(Enum):
    SLOT_A = 0
    SLOT_B = 1
    SLOT_C = 2
    SLOT_D = 3
    SLOT_E = 4
    SLOT_F = 5
    SLOT_G = 6
    SLOT_H = 7
    SLOT_I = 8
    SLOT_J = 9
    SLOT_K = 10
    SLOT_L = 11


