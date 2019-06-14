# Application WaveTool Data Analysis Path

## Python Modules

Requirement: Applications WaveTool 3.2.0.
Python: 3.7.1+

*ex:* python3 awt_sample.py

### Using the example

#### Configure the example

Open *awt_sample.py*

```
COM_PORT = 39
DCFG_FILE = 'ADPD188GGZ_EVAL_PPG_Normal_01.dcfg'
CONTROL_UDP_RX_PORT = 50002
CONTROL_UDP_TX_PORT = 50001
DATA_UDP_TX_PORT = 50007
Host_IP = "localhost"
```
**COM_PORT**: *COM Port* the evaluation board is connected. This allows the python script to connect to device, as would using the *Applications WaveTool **Connect*** button.

**DCFG_FILE**: The DCFG file to load from the local folder. See you WaveTool installation *cfg* folder.

**CONTROL_UDP_RX_PORT**, **CONTROL_UDP_TX_PORT**, **DATA_UDP_TX_PORT**: See *Applications WaveTool Settings->UDP* for the ports being used. The selection above is the default selection.

#### Sample output

---
\
**(base) > python awt_sample.py**\
\
Response Data:  b'\x99\x00\x00'\
Response Status: Success\
Device Connected successfully\
Opening ADPD View\
Response Data:  b'\x98\x00\x00'\
Response Status: Success\
Modifying OPMODE Register\
Response Data:  b'\x81\x00\x00'\
Response Status: Success\
Reading OPMODE Register\
Response Data:  b'\x80\x00\x02' 0\
Register Value is  0\
Response Status: Success\
Reading Chip Register\
Response Data:  b'\x80\x00\x02' 2582\
Register Value is  2582\
Response Status: Success\
\
Available DCFG File\
\
01 )ADPD1080Z-GST_EVAL_ANGLE_Nominal_01.dcfg\
02 )ADPD1080Z-GST_EVAL_GEST_Nominal_01.dcfg\
03 )ADPD1080Z-PRX_EVAL_PROX_LEDwaNominal_01.dcfg\
04 )ADPD1081Z-PPG_EVAL_Float_01.dcfg\
05 )ADPD1081Z-PPG_EVAL_Normal_01.dcfg\
06 )ADPD144RIZ-SF_EVAL_PPG_EarOrig_01.dcfg\
07 )ADPD188BIZ-SK_EVAL_SMOKE_chop_01.dcfg\
08 )ADPD188BIZ-SK_TEST_SMOKE_OpenAir_01.dcfg\
09 )ADPD188GGZ_EVAL_PPG_Float_01.dcfg\
0A )ADPD188GGZ_EVAL_PPG_Normal_01.dcfg\
0B )ADPD188GGZ_TEST_PPGECG_AD8233_01.dcfg\
0C )ADPD188GGZ_TEST_PPGECG_NoBuffer_01.dcfg\
0D )ADPD188GGZ_TEST_StartingPoint_01.dcfg\
0E )ADPD2140Z_EVAL_ANGLE_Nominal_01.dcfg\
0F )ADPD2140Z_EVAL_GEST_Nominal_01.dcfg\
10 )ADPD2140Z_TEST_GEST_LED1_slotB.dcfg\
11 )ADPD2140Z_TEST_GEST_LED2_HParray_slotA.dcfg\
12 )ADPD2140Z_TEST_GEST_LED3_slotA.dcfg\
13 )ADPD4000Z_EVAL_ECG_sAIN34_01.dcfg\
14 )ADXL.dcfg\
\
Enter load config command with any of above choice as shown below..\
\
        Eg.,0D 01 <01/02/03...>choice\
\
Response Data:  b'\x95\xd0\xeb'\
\
Loading the DCFG File ADPD188GGZ_EVAL_PPG_Normal_01.dcfg\
\
Response Data:  b'\x97\x00\x00'\
Response Status: Success\
Selecting Plot 1 with Slot A\
Response Data:  b'\x88\t\x00'\
Response Status: Not Applicable\
Selecting Plot 2 with Slot B\
Response Data:  b'\x88\t\x00'\
Response Status: Not Applicable\
\
Playing the data from the sensor for 20 seconds\
\
Response Data:  b'\x82\x00\x00'\
Response Status: Success\
\
Enabling the Log and UDP Data transfer for 20 seconds\
\
Response Data:  b'\x85\x00\x00'\
Response Status: Success\
Response Data:  b'\x86\x00\x00'\
Response Status: Success\
UDP connection status :0\
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\
                        UDP TRANSFER TOOL\
\
UDP Port Number: 50007\
Version        : 1.0\
\
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\
Received Packet Count: 991\
Disabling the Log\
\
Response Data:  b'\x85\x00\x00'\
Response Status: Success\
\
Disabling the UDP Data transfer\
\
Response Data:  b'\x86\x00\x00'\
Response Status: Success\
\
Stopping the Playback of the ADPD sensor data\
\
Response Data:  b'\x83\x00\x00'\
Response Status: Success\
\
Disconnecting the device\
\
Response Data:  b'\x91\x00\x00'\
Response Status: Success

---

