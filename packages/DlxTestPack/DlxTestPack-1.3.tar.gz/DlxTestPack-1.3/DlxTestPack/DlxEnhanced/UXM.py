from ..DlxTestClassV5 import scpi_communication_pack
class scpi_UXM_test_cmd(scpi_communication_pack):
    def __init__(self):
        super().__init__()
    def COM_CellApply(self,cell):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:LTE:CELL{}:APPLY".format(cell))
    def LTE_DuplexSet(self,cell,duplex):
        self._send("BSE:CONFig:LTE:CELL{}:DUPLex:MODE {}".format(cell,duplex))
    def LTE_BandSet(self,cell,bandnum):
        '''int|str cell 1,2,3,4'''
        self._send("BSE:CONFig:LTE:CELL{}:BAND {}".format(cell,bandnum))
    def LTE_BandWidthSet(self,cell,bandwidth):
        '''int|str cell 1,2,3,4'''
        self._send("BSE:CONFig:LTE:CELL{}:BW {}".format(cell,bandwidth))
    def LTE_ChannelSet(self,cell,channel):
        '''int|str cell 1,2,3,4'''
        self._send("BSE:CONFig:LTE:CELL{}:DL:CHANnel {}".format(cell,channel))
    def LTE_MimoSet(self,cell,mimo):
        '''int|str cell 1,2,3,4'''
        self._send("BSE:CONFig:LTE:CELL{}:PHY:DL:ANTenna:CONFig {}".format(cell,mimo))
    def LTE_UdcSet(self,cell,udc):
        self._send("BSE:CONFig:LTE:CELL{}:PHY:TDD:ULDL:CONFig {}".format(cell,udc))
    #NR--------
    def NR_CellApply(self,cell):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:APPLY".format(cell))
    def NR_RtxSet(self,cell,rtx):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:RTX {}".format(cell,rtx))
    def NR_DuplexSet(self,cell,duplex):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:DUPLEX:MODe {}".format(cell,duplex))
    def NR_BandSet(self,cell,bandnum):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:BAND N{}".format(cell,bandnum))
    def NR_BandWidthSet(self,cell,bandwidth):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:DL:BW {}".format(cell,bandwidth))
    def NR_ScsSet(self,cell,scs):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:SUBCarrier:SPACing:COMMon MU{}".format(cell,["15kHz","30kHz"].index(scs)))
    def NR_ChannelSet(self,cell,channel:str):
        '''cell 1,2,3,4'''
        if channel.isdigit():
            self._send("BSE:CONFig:NR5G:CELL{}:DL:CHANnel {}".format(cell,channel))
            return
        self._send("BSE:CONFig:NR5G:CELL{}:TESTChanLoc {}".format(cell,channel))
    def NR_DlMimoSet(self,cell,dlmimo):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:DL:MIMO:CONFig {}".format(cell,dlmimo))
    def NR_UlMimoSet(self,cell,ulmimo):
        '''cell 1,2,3,4'''
        self._send("BSE:CONFig:NR5G:CELL{}:UL:MIMO:CONFig {}".format(cell,ulmimo))
    def NR_UdcSet(self,cell,defult:str="8D1U"):
        '''cell 1,2,3,4'''
        def Part_8D1U_1(p_in):
            will_send =["BSE:CONFig:NR5G:CELL1:DL:PHASe:COMPensation:STATe DLCF",
                        "BSE:CONFig:NR5G:CELL1:UL:PHASe:COMPensation:STATe ULCF",
                        "BSE:CONFIG:NR5G:CELL1:DL:POWer:DBMbw -30",
                        "BSE:MEASure:NR5G:ULPWr:EIP:AUPDate:CONTinuous:STATe ON",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:SIRNti:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:SIRNti:DL:IMCS 2",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TCRNti:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TCRNti:DL:IMCS 16",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:K0 0",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:SSTart 2",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:SLENgth 12",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:MTYPe TYPE_A",
                        "BSE:CONFig:NR5G:CELL1:PHY:DL:HARQ:PROCesses N16",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PDSCh:MCS:TABle Q256",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:MCS:TABle Q256",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:TPRecoding:MCS:TABle Q256",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:TPENabled 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:DL:DMRS:ADDPosition APOS1",
                        "BSE:CONFig:NR5G:CELL1:PHY:UL:DMRS:ADDPosition APOS1",
                        "BSE:CONFig:NR5G:CELL1:PHY:DL:BWP0:CRB:STARt 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:DL:BWP0:NUM:PRBS 24",
                        "BSE:CONFig:NR5G:CELL1:PHY:UL:BWP0:CRB:STARt 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:UL:BWP0:NUM:PRBS 24",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:PRB:STARting 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:SYMBols:STARt 13",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:SYMBols:NUM 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:ICYC:SHIFt 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:PRB:STARting 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:SYMBols:STARt 13",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:SYMBols:NUM 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:ICYC:SHIFt 0",
                        "BSE:CONFig:NR5G:CELL1:PAGing:DCYCle RF32",
                        "BSE:CONFig:NR5G:CELL1:PAGing:TFRAmes HALFT",
                        "BSE:CONFig:NR5G:CELL1:PAGing:FRAME:OFFS 0",
                        "BSE:CONFig:NR5G:CELL1:APPLY"]
            if p_in=="1":
                for idx in will_send:
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)
        def Part_8D1U_2(p_in):
            will_send =["BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:STATe 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:FDOMain \'1E0000000000\'",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET:ID 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:CDURation 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:STATe 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:FDOMain \'1E0000000000\'",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:ID 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:CDURation 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:CSS:SSID1:STATe 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:COReset 0",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:IDENtity 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:FOUR 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:TWO 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:ONE 4",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:STATe 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:COReset 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:IDENtity 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:FOUR 1",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:TWO 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:ONE 4",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA1:VALue 10",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA2:VALue 2",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA3:VALue 3",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA4:VALue 4",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA5:VALue 5",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA6:VALue 6",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA7:VALue 7",
                        "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA8:VALue 8",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:PERiod MS5",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:DLSLots 8",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:ULSLots 1", 
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:DLSYmbols 10",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:ULSYmbols 2",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:STATE 1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC:COUNT 1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SCCount 9",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:SMAP \'00000000000000000003\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:SMAP \'00000000000000001004\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:SMAP \'00000000000000002008\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:SMAP \'00000000000000004010\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:SMAP \'00000000000000008020\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:SMAP \'00000000000000010040\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:SMAP \'00000000000000020080\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:SMAP \'00000000000000040100\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:SMAP \'00000000000000000C00\'",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:SMAP \'00000000000000080200\'",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:K0 0",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SSTart 1",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SLENgth 13",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:MTYPe TYPE_A",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:K0 0",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SSTart 1",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SLENgth 9",
                        "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:MTYPe TYPE_A"]
            if p_in=="1":
                for idx in will_send:
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)
        def Part_8D1U_3(p_in):
            will_send =["BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 8",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 7",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 6",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 5",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 4",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC4:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 3",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC5:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 2",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC6:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:TDOMain:RASSignment 1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 10",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC7:DL:DCI:PCANdidate 0",
                        # "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBSTart 24",
                        # "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBNumber 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 8",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:PUCCh:RINDex 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:DCI:PCANdidate 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:RBALlocation:FIXed:RBSTart 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC8:DL:RBALlocation:FIXed:RBNumber 24",
                        "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:K2 1",
                        "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SSTart 0",
                        "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SLENgth 14",
                        "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:MTYPe TYPE_A",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:TDOMain:RASSignment 0",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:IMCS 27",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:DCI:AUTO:AGGRegation:LEVel N1",
                        "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:DCI:PCANdidate 1"]
            if p_in=="1":
                for idx in will_send:
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)
        def Part_3D6U_1(p_in):
            will_send=[
                "BSE:CONFig:NR5G:CELL1:APPLY",
                "BSE:CONFig:NR5G:CELL1:DL:PHASe:COMPensation:STATe DLCF",
                "BSE:CONFig:NR5G:CELL1:UL:PHASe:COMPensation:STATe ULCF",
                "BSE:CONFIG:NR5G:CELL1:DL:POWer:DBMbw -30",
                "BSE:MEASure:NR5G:ULPWr:EIP:AUPDate:CONTinuous:STATe ON",
                "BSE:CONFig:NR5G:CELL1:SCHeduling:SIRNti:DL:TDOMain:RASSignment 0",
                "BSE:CONFig:NR5G:CELL1:SCHeduling:SIRNti:DL:IMCS 2",
                "BSE:CONFig:NR5G:CELL1:SCHeduling:TCRNti:DL:TDOMain:RASSignment 0",
                "BSE:CONFig:NR5G:CELL1:SCHeduling:TCRNti:DL:IMCS 16",
                "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:K0 0",
                "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:SSTart 2",
                "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:SLENgth 12",
                "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:COMMON:TABLe:IND0:MTYPe TYPE_A",
                "BSE:CONFig:NR5G:CELL1:PHY:DL:HARQ:PROCesses N16",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PDSCh:MCS:TABle  Q256",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:MCS:TABle Q256",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:TPRecoding:MCS:TABle Q256",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUSCh:TPENabled 0",
                "BSE:CONFig:NR5G:CELL1:PHY:DL:DMRS:ADDPosition APOS1",
                "BSE:CONFig:NR5G:CELL1:PHY:UL:DMRS:ADDPosition APOS1",
                "BSE:CONFig:NR5G:CELL1:PHY:DL:BWP0:CRB:STARt 0",
                "BSE:CONFig:NR5G:CELL1:PHY:DL:BWP0:NUM:PRBS 273",
                "BSE:CONFig:NR5G:CELL1:PHY:UL:BWP0:CRB:STARt 0",
                "BSE:CONFig:NR5G:CELL1:PHY:UL:BWP0:NUM:PRBS 273",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:PRB:STARting 0",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:SYMBols:STARt 13",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:SYMBols:NUM 1",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID0:ICYC:SHIFt 0",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:PRB:STARting 0",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:SYMBols:STARt 13",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:SYMBols:NUM 1",
                "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:RESID8:ICYC:SHIFt 0",
                "BSE:CONFig:NR5G:CELL1:PAGing:DCYCle RF32",
                "BSE:CONFig:NR5G:CELL1:PAGing:TFRAmes HALFT",
                "BSE:CONFig:NR5G:CELL1:PAGing:FRAME:OFFS 0",
                "BSE:CONFig:NR5G:CELL1:APPLY",
                "BSE:CONFig:NR5G:SECurity:AUTHenticate:KEY:TYPE TEST3GPP",
                "BSE:CONFig:NR5G:CELL1:APPLY",
            ]
            if p_in=="1":
                for idx in will_send:
                    # input(idx+"][")
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)
        def Part_3D6U_2(p_in):
            will_send=[
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:STATe 0",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:FDOMain '1E0000000000'",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET:ID 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET1:CDURation 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:STATe 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:FDOMain '1FFFE0000000'",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:ID 2",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CORESET2:CDURation 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:CSS:SSID1:STATe 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:COReset 0",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:IDENtity 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:FOUR 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:TWO 2",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:CSS:SSID1:AGGRlevel:ONE 4",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:STATe 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:COReset 2",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:IDENtity 2",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:FOUR 4",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:TWO 4",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:UESS:SSID1:AGGRlevel:ONE 4",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA1:VALue 1",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA2:VALue 2",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA3:VALue 3",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA4:VALue 4",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA5:VALue 5",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA6:VALue 6",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA7:VALue 7",
                    "BSE:CONFig:NR5G:CELL1:PHY:BWP0:PUCCh:COMMon:DTUA8:VALue 10",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:PERiod MS5",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:DLSLots 3",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:ULSLots 6",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:DLSYmbols 10",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:ULSYmbols 2",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:TDDPATtern:STATE 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC:COUNT 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SCCount 4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:SMAP \'00000000000000000401\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:SMAP \'00000000000000000802\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:SMAP \'00000000000000001004\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:SMAP \'00000000000000002008\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:SMAP \'00000000000000004210\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:UL:SMAP \'00000000000000018060\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:UL:SMAP \'00000000000000060180\'",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:UL:SMAP \'00000000000000080200\'",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:K0 0",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SSTart 1",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SLENgth 13",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND0:MTYPe TYPE_A",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:K0 0",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SSTart 1",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SLENgth 9",
                    "BSE:CONFig:NR5G:CELL1:PDSCH:TDRA:DEDicated:IBWP:TABLe:IND1:MTYPe TYPE_A"
            ]
            if p_in=="1":
                for idx in will_send:
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)
        def Part_3D6U_3(p_in):
            will_send=[
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:TDOMain:RASSignment 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 3",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:PUCCh:RINDex 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:DCI:PCANdidate 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBSTart 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:DL:RBALlocation:FIXed:RBNumber 273",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:TDOMain:RASSignment 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 2",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:PUCCh:RINDex 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:DCI:PCANdidate 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBSTart 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBNumber 273",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:TDOMain:RASSignment 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:PUCCh:RINDex 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:DCI:PCANdidate 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:RBALlocation:FIXed:RBSTart 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:DL:RBALlocation:FIXed:RBNumber 273",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:TDOMain:RASSignment 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:PDSCh:HARQ:FEEDback:TIMing:KONE 10",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:PUCCh:RINDex 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:DL:DCI:PCANdidate 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBSTart 24",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:DL:RBALlocation:FIXed:RBNumber 249",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:SIZE 4",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:K2 3",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SSTart 0",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:SLENgth 14",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND0:MTYPe TYPE_A",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND1:K2 4",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SSTart 0",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND1:SLENgth 14",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND1:MTYPe TYPE_A",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND2:K2 5",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND2:SSTart 0",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND2:SLENgth 14",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND2:MTYPe TYPE_A",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND3:K2 6",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND3:SSTart 0",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND3:SLENgth 14",
                    "BSE:CONFig:NR5G:CELL1:PUSCH:TDRA:DEDicated:IBWP:TABLe:IND3:MTYPe TYPE_A",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:TDOMain:RASSignment 0",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC0:UL:DCI:PCANdidate 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:UL:TDOMain:RASSignment 1",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:UL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:UL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC1:UL:DCI:PCANdidate 2",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:UL:TDOMain:RASSignment 2",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:UL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:UL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC2:UL:DCI:PCANdidate 3",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:UL:TDOMain:RASSignment 3",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:UL:IMCS 27",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:UL:DCI:AUTO:AGGRegation:LEVel N4",
                    "BSE:CONFig:NR5G:CELL1:SCHeduling:FC0:SC3:UL:DCI:PCANdidate 1",
                    "BSE:CONFig:NR5G:CELL1:APPLY"
            ]
            if p_in=="1":
                for idx in will_send:
                    self._send(idx)
            else:
                for idx in will_send:
                    idx = idx.replace("CELL1","CELL2")
                    self._send(idx)

        if defult=="8D1U":
            Part_8D1U_1(cell)
            Part_8D1U_2(cell)
            Part_8D1U_3(cell)
        elif defult=="3D6U":
            Part_3D6U_1(cell)
            Part_3D6U_2(cell)
            Part_3D6U_3(cell)
