import time
from ..DlxTestClassV5 import scpi_communication_pack

class scpi_CMW500(scpi_communication_pack):
    def __init__(self):
        super().__init__()
        self.TDD_BAND=[33,34,35,36,37,38,39,40,41,42,43,44,45,48,250]

    def Init_Instr(self):
        print("初始化仪器,5s ....")
        key = self._send("*RST; *OPC?")
        time.sleep(5)
        return key
  
    def Pic_Save(self,message:str=""):
        self._send("HCOPy:INTerior:FILE '@PRINT\\{}_Pic'".format(str))
    
    
class LTE(scpi_CMW500):
    def __init__(self):
        super().__init__()
    def HandOver_get_BandWidth(self):
        bandwidthdict={"B014":1.4,"B030":3,"B050":5,"B100":10,"B150":15,"B200":20}
        data=self._query("CONFigure:LTE:SIGN:CELL:BANDwidth:PCC:UL?")
        data:str=data.replace('\n','')
        return bandwidthdict[data]
    def HandOver_get_Channel(self):
        return self._query("CONFigure:LTE:SIGN:RFSettings:PCC:CHANnel:UL?")
    def HandOver_QueryTxPowerAVERage(self):
        self.Instr_MEAS_ON()
        for idx in range(5):
            try:
                data:str = self._query("FETCh:LTE:MEAS:MEValuation:MODulation:AVERage?")
                TxPowerAVERage=data.split(",")[17]
                return float(TxPowerAVERage)
            except:
                pass
            time.sleep(1)
        raise Exception("Tx Power获取失败")
    def SetLoss(self,value:float):
        self._send("CONFigure:LTE:SIGN:RFSettings:EATTenuation:INPut {:.2f}".format(value))
    def HandOver_to_other_Band(self,band_num:str,BW_active:bool=False,BW:str="10"):
        InToBw = {"1.4":"B014","3":"B030","5":"B050","10":"B100","15":"B150","20":"B200"}
        TDDorFDD = "TDD"
        if int(band_num) in self.TDD_BAND:
            TDDorFDD = "TDD"
        else:
            TDDorFDD = "FDD"
        if BW_active:
            self._send("PREPare:LTE:SIGN:HANDover:ENHanced {},OB{},KEEP,{},KEEP".format(TDDorFDD,band_num,InToBw[BW]))
        else:
            self._send("PREPare:LTE:SIGN:HANDover:ENHanced {},OB{},KEEP,KEEP,KEEP".format(TDDorFDD,band_num))
        self._send("CALL:LTE:SIGN:PSWitched:ACTion HANDover")#CONNect
        # time.sleep(10)
    def HandOver_Init_Lte(self):
        self._send("CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXPower")
        self._send("CONFigure:LTE:MEAS:MEValuation:REPetition CONTinuous")
        self._send("CONFigure:LTE:MEAS:MEValuation:MSUBframes 2,1,0")
        time.sleep(2)
        
        # self._send("CONFigure:LTE:SIGN:UL:PUSCh:TPC:PEXecute")
    def Instr_MEAS_ON(self):
        # self._send("ABORt:LTE:MEAS:MEValuation")
        # time.sleep(1)
        self._send("ROUTe:LTE:MEAS:SCENario:CSPath \'LTE Sig1\'")
        self._send("INITiate:LTE:MEAS:MEValuation")
        print("等待5s MEAS ON")
        time.sleep(5)
    def SIGN_ON(self):
        self._send("SOURce:LTE:SIGN:CELL:STATe ON")
        print("等待5s SIGN ON")
        time.sleep(10)
    def SetBand(self,bandnum="1"):
        dmode = "FDD"
        if int(bandnum) in self.TDD_BAND:
            dmode = "TDD"
        self._send("CONFigure:LTE:SIGN:DMODe {}".format(dmode))
        self._send("CONFigure:LTE:SIGN:BAND OB{}".format(bandnum))
class GSM(scpi_CMW500):
    def __init__(self):
        super().__init__()
    def GSM_LossSet(self,value:float=0.5):
        self._send("CONFigure:GSM:SIGN:RFSettings:EATTenuation:INPut {:.2f}".format(value))
    def Mes2GInit(self):
        self._send("ROUTe:GSM:MEAS:SCENario:CSPath \"GSM Sig2\"")
        self._send("CONFigure:GSM:MEAS:MEValuation:REPetition CONTinuous")#SINGleshot | CONTinuous
    def Mes2GOn(self):
        self._send("INITiate:GSM:MEAS:MEValuation")
    def TxPower2GGet(self):
        return self._query("FETCh:GSM:MEAS:MEValuation:MODulation:AVERage?")
    def HandOver2G_to_Band(self,band:str="G09"):
        '''
        "G085","G09","G18","G19"
        '''
        # self._send("CONFigure:GSM:SIGN:DUALband:BAND:TCH {}".format(band))
        self._send("PREPare:GSM:SIGN:HANDover:TARGet {}".format(band))

        if band=="G09" or band == "G085":
            self._send("PREPare:GSM:SIGN:HANDover:PCL 5")
        else:
            self._send("PREPare:GSM:SIGN:HANDover:PCL 0")
        # self._send("CALL:GSM:SIGN:PSWitched:ACTion HANDover")
        self._send("CALL:GSM:SIGN:HANDover:STARt")
        time.sleep(1)
    def query2GChannel(self):
        return self._query("CONFigure:GSM:SIGN:RFSettings:CHANnel:BCCH?")
    def query2GPcl(self):
        return self._query("CONFigure:GSM:SIGN:RFSettings:PCL:TCH:CSWitched?")
    def Sign2GSwitch(self,OnOff:str="ON"):
        '''
        ON | OFF
        '''
        self._send("SOURce:GSM:SIGN:CELL:STATe {}".format(OnOff))
        time.sleep(8)
    def setPcl2G(self,pcl:str="5"):
        '''
        850\900 5
        1800\1900 0
        '''
        self._send("CONFigure:GSM:SIGN:RFSettings:PCL:TCH:CSWitched {}".format(pcl))
    def set2GBand(self,band:str="G09"):
        '''
        "850":"G085","900":"G09","1800":"G18","1900":"G19"
        '''
        if band=="G09" or band=="G085":
            self.setPcl2G("5")
        else:
            self.setPcl2G("0")
        self._send("CONFigure:GSM:SIGN:BAND:BCCH {}".format(band))
    def ConnectPDP(self):
        self._send("CALL:GSM:SIGN:PSWitched:ACTion CONNect")

class CATM(scpi_CMW500):
    def __init__(self):
        super().__init__()
    def Init_Regist_Pra(self):
        '''
        初始化注网信令参数
        '''
        self._send("CONFigure:LTE:SIGN:EMTC:ENABle ON")
        self._send("CONFigure:LTE:SIGN:CONNection:STYPe RMC")
    def SetBand(self,bandnum="1"):
        dmode = "FDD"
        if int(bandnum) in self.TDD_BAND:
            dmode = "TDD"
        self._send("CONFigure:LTE:SIGN:DMODe {}".format(dmode))
        self._send("CONFigure:LTE:SIGN:BAND OB{}".format(bandnum))
    def HandOver_to_other_Band(self,band_num:str):
        TDDorFDD = "FDD"
        BandWidth ="KEEP"
        if int(band_num) in self.TDD_BAND:
            TDDorFDD = "TDD"
        if band_num in ["31","72","87","88"]:
            BandWidth= "B050"
        self._send("PREPare:LTE:SIGN:HANDover:ENHanced {},OB{},KEEP,{},KEEP".format(TDDorFDD,band_num,BandWidth))
        self._send("CALL:LTE:SIGN:PSWitched:ACTion HANDover")#CONNect
    def MeasInit(self):
        self._send("CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXPower")
        self._send("CONFigure:LTE:MEAS:MEValuation:REPetition CONTinuous")
        self._send("CONFigure:LTE:MEAS:MEValuation:MSUBframes 5,4,0")
        time.sleep(2)
    def MEAS_ON(self):
        # self._send("ABORt:LTE:MEAS:MEValuation")
        # time.sleep(1)
        self._send("ROUTe:LTE:MEAS:SCENario:CSPath \'LTE Sig1\'")
        self._send("INITiate:LTE:MEAS:MEValuation")
        print("等待5s MEAS ON")
        time.sleep(5)
    def SetLoss(self,value:float):
        self._send("CONFigure:LTE:SIGN:RFSettings:EATTenuation:INPut {:.2f}".format(value))
    def SIGN_ON(self):
        '''
        打开信令
        '''
        self._send("SOURce:LTE:SIGN:CELL:STATe ON")
        print("等待5s SIGN ON")
        time.sleep(10)
    def HandOver_QueryTxPowerAVERage(self):
        self.MEAS_ON()
        for idx in range(5):
            try:
                data:str = self._query("FETCh:LTE:MEAS:MEValuation:MODulation:AVERage?")
                TxPowerAVERage=data.split(",")[17]
                return float(TxPowerAVERage)
            except:
                pass
            time.sleep(1)
        raise Exception("Tx Power获取失败")
    def GetBandWidth(self):
        bandwidthdict={"B014":1.4,"B030":3,"B050":5,"B100":10,"B150":15,"B200":20}
        data=self._query("CONFigure:LTE:SIGN:CELL:BANDwidth:PCC:UL?")
        data:str=data.replace('\n','')
        return bandwidthdict[data]
    def GetChannel(self):
        return self._query("CONFigure:LTE:SIGN:RFSettings:PCC:CHANnel:UL?")
class NB(scpi_CMW500):
    def __init__(self):
        super().__init__()
    def NB_COMMON_parameters(self):
        '''
        BLER:REPetition CONTinuous
        BLER:SAMPles 1000
        CONNection:STYPe UDEF
        '''
        print("配置公共参数")
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:BLER:REPetition CONTinuous") #SINGleshot|CONTinuous
        count+=self._send("CONFigure:NIOT:SIGN:BLER:SAMPles 1000")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:STYPe UDEF")
        if count==3:
            return True
        else:
            return False
    def NB_BandSet(self,bandnum):
        self._send("CONFigure:NIOT:SIGN:BAND OB{}".format(bandnum))
    def NB_UplinkNominalPower(self,power=33.8):
        self._send("CONFigure:NIOT:SIGN:UL:NPUSch:ULNPower {}".format(power))
    def NB_UlSubcarrierSpacing(self,SK:str="S15K"):
        '''
        S3K75 | S15K 
        '''
        self._send("CONFigure:NIOT:SIGN:CELL:SCSPacing {}".format(SK))
    def NB_LossSet(self,loss=1):
        self._send("CONFigure:NIOT:SIGN:RFSettings:EATTenuation:INPut {}".format(loss))
    def NB_GetChannel(self):
        return self._query("CONFigure:NIOT:SIGN:RFSettings:CHANnel:UL?")
    def SIGN_ON(self,OnOff=True):
        SwitchKey="OFF"
        if OnOff:
            SwitchKey="ON"
        self._send("SOURce:NIOT:SIGN:CELL:STATe {}".format(SwitchKey))
    def Instr_MEAS_ON(self):
        # self._send("ABORt:LTE:MEAS:MEValuation")
        # time.sleep(1)
        self._send("ROUTe:NIOT:MEAS:SCENario:CSPath \'NB-IoT Sig1\'")
        self._send("INITiate:NIOT:MEAS:MEValuation")
        print("等待5s MEAS ON")
        time.sleep(5)
    def MeasInit(self):
        self._send("CONFigure:NIOT:MEAS:PRACh:REPetition CONTinuous")
        time.sleep(2)
    def GetTxPower(self):
        for idx in range(5):
            try:
                data:str = self._query("FETCh:NIOT:MEAS:MEValuation:MODulation:AVERage?")
                TxPowerAVERage=data.split(",")[11]
                return float(TxPowerAVERage)
            except:
                pass
            time.sleep(1)
        raise Exception("Tx Power获取失败")
class WCDMA(scpi_CMW500):
    def __init__(self):
        super().__init__()
    def SetBand(self,band_num):
        self._send("CONFigure:WCDMa:SIGN:CARRier:BAND OB{}".format(band_num))
    def SIGN_ON(self):
        self._send("SOURce:WCDMa:SIGN:CELL:STATe ON")
        time.sleep(10)
    def MeasInit(self):
        self._send("ROUTe:WCDMa:MEAS:SCENario:CSPath \'WCDMA Sig1\'")
    def Instr_MEAS_ON(self):
        self._send("INITiate:WCDMa:MEAS:MEValuation")
    def CSWitch(self):
        self._send("CALL:WCDMa:SIGN:CSWitched:ACTion CONNect")
        for idx in range(5):
            if self._query("FETCh:WCDMa:SIGN:CSWitched:STATe?","CEST")[0]:
                return True
        return False
    def QCWitch(self):
        print(self._query("FETCh:WCDMa:SIGN:CSWitched:STATe?"))#REG 注册上 CEST 连接上CS

        #CONFigure:WCDMa:SIGN:UL:TPC:SET ALL1
        #
    def SetLoss(self,loss):
        self._send("CONFigure:WCDMa:SIGN:RFSettings:CARRier:EATTenuation:INPut {}".format(loss))
    def GetTxPower(self):
        for idx in range(5):
            try:
                data:str = self._query("FETCh:WCDMa:MEAS:MEValuation:LIST:MODulation:AVERage?")
                TxPowerAVERage=data.split(",")[-1]
                return float(TxPowerAVERage)
            except:
                pass
            time.sleep(1)
        raise Exception("Tx Power获取失败")
    def GetChannel(self):
        return self._query("CONFigure:WCDMa:SIGN:RFSettings:CARRier:CHANnel:DL?")
    def HandOverToOtherBand(self,band_num):
        self._send("PREPare:WCDMa:SIGN:HANDover:EXTernal:WCDMa OB{},KEEP".format(band_num))
        self._send("CALL:WCDMa:SIGN:CSWitched:ACTion HANDover")#CONNect