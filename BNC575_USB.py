import pyvisa
import re
import time

def BNC575_Connect(DeviceComPort):
    Device='ASRL'+str(DeviceComPort)+'::INSTR'
    inst=pyvisa.ResourceManager().open_resource(Device)
    inst.timeout = 5000
    inst.read_termination = '\r\n'
    inst.write_termination = '\r\n'
    inst.baud_rate = 38400
    DeviceName=inst.query('*IDN?')
    time.sleep(.01)
    print("Connected to: "+ DeviceName[0:3]+ DeviceName[4:7] + ' on '+Device)
    return inst

def BNC575_Run(inst,Mode):
    wait=.001
    inst.write(':PULSE0:MODE ' + Mode) #NORM,SING,BURS,DCYC
    time.sleep(wait)
    inst.write(':PULSE0:STATE ' + 'ON')
    time.sleep(wait)

def BNC575_Stop(inst):
    wait=.01
    inst.write(':PULSE0:STATE ' + 'OFF')
    time.sleep(wait)

def BNC575_ChangeOne(inst,Chan,Param,Val,Period,Mode,Prnt):
    wait=.0001
    #inst.write(':PULSE0:MODE ' + Mode) #NORM,SING,BURS,DCYC
    #time.sleep(wait)
    if Chan=='A':
        let=1
    elif Chan=='B':
        let=2
    elif Chan=='C':
        let=3
    elif Chan=='D':
        let=4
    elif Chan=='E':
        let=5
    elif Chan=='F':
        let=6
    elif Chan=='G':
        let=7
    elif Chan=='H':
        let=8
        
    if Param == 'DELAY' or Param == 'WIDT':
        Val=round(Val,9)
        if Prnt == 'YES':
            print('Chan'+Chan+'_'+Param+'= '+f'{(1e6)*(round(Val,9)):.0f}'+' us')
        else:
            None
    elif Param == 'AMP':
        Val=round(Val,2)
        if Prnt == 'YES':
            print(round(Val,2))
            print('Chan'+Chan+'_'+Param+'= '+f'{abs(round(Val,2)):.2f}'+' V')
        else:
            None
    else:
        if Prnt == 'YES':
            print(round(Val,2))
            print('Chan'+Chan+'_'+Param+'= '+f'{abs(round(Val,2)):.2f}'+' V')
        else:
            None
        
    inst.write(':PULSE'+str(let)+':'+Param+' ' + str(Val))
    time.sleep(wait)
    if Mode == 'SING':
        inst.write(':PULSE0:STAT ' + 'ON') #start single shot on each function call
        time.sleep(wait)
    else:
        None




def BNC575_Settings(inst,ChA,A_width,A_delay,A_mode,A_amp,A_pol,ChB,B_width,B_delay,B_mode,B_amp,B_pol,ChC,C_width,C_delay,C_mode,C_amp,C_pol,
                    ChD,D_width,D_delay,D_mode,D_amp,D_pol,ChE,E_width,E_delay,E_mode,E_amp,E_pol,ChF,F_width,F_delay,F_mode,F_amp,F_pol,
                    ChG,G_width,G_delay,G_mode,G_amp,G_pol,ChH,H_width,H_delay,H_mode,H_amp,H_pol,Period,TrigMode):
    wait=.05

    inst.write(':PULSE0:PER ' + str(Period))
    time.sleep(wait)
    inst.write(':PULSE0:MODE ' + 'NORM') #NORM,SING,BURS,DCYC
    time.sleep(wait)
    inst.write(':PULSE0:TRIG:MOD ' + TrigMode)
    time.sleep(wait)

    for channel in range(1,8,1):
        if channel==1:
            Ch=ChA
            Ch_width=A_width
            Ch_delay=A_delay
            Ch_mode=A_mode
            Ch_amp=A_amp
            Ch_pol=A_pol
            Ch_sync='TO'
        elif channel==2:
            Ch=ChB
            Ch_width=B_width
            Ch_delay=B_delay
            Ch_mode=B_mode
            Ch_amp=B_amp
            Ch_pol=B_pol
            Ch_sync='CHA'
        elif channel==3:
            Ch=ChC
            Ch_width=C_width
            Ch_delay=C_delay
            Ch_mode=C_mode
            Ch_amp=C_amp
            Ch_pol=C_pol
            Ch_sync='CHA'
        elif channel==4:
            Ch=ChD
            Ch_width=D_width
            Ch_delay=D_delay
            Ch_mode=D_mode
            Ch_amp=D_amp
            Ch_pol=D_pol
            Ch_sync='CHA'
        elif channel==5:
            Ch=ChE
            Ch_width=E_width
            Ch_delay=E_delay
            Ch_mode=E_mode
            Ch_amp=E_amp
            Ch_pol=E_pol
            Ch_sync='CHA'
        elif channel==6:
            Ch=ChF
            Ch_width=F_width
            Ch_delay=F_delay
            Ch_mode=F_mode
            Ch_amp=F_amp
            Ch_pol=F_pol
            Ch_sync='CHA'
        elif channel==7:
            Ch=ChG
            Ch_width=G_width
            Ch_delay=G_delay
            Ch_mode=G_mode
            Ch_amp=G_amp
            Ch_pol=G_pol
            Ch_sync='CHA'
        elif channel==8:
            Ch=ChH
            Ch_width=H_width
            Ch_delay=H_delay
            Ch_mode=H_mode
            Ch_amp=H_amp
            Ch_pol=H_pol
            Ch_sync='CHA'
        else:
            None

        Ch_delay=round(Ch_delay,9)
        Ch_width=round(Ch_width,9)
        Ch_amp=round(Ch_width,2)

        inst.write(':PULSE'+str(channel)+':STATE ' + Ch)
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':WIDT ' + str(Ch_width))
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':DELAY ' + '{:.7f}'.format(Ch_delay))
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':MOD ' + Ch_mode)
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':AMP ' + str(Ch_amp))
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':POL ' + Ch_pol)
        time.sleep(wait)
        inst.write(':PULSE'+str(channel)+':SYNC ' + Ch_sync)
        time.sleep(wait)
