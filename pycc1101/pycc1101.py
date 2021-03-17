import spidev
import time

class TICC1101(object):
    WRITE_SINGLE_BYTE = 0x00
    WRITE_BURST = 0x40
    READ_SINGLE_BYTE = 0x80
    READ_BURST = 0xC0

    # Configuration Register Details - Registers with preserved values in SLEEP state
    # TI-CC1101 Datasheet

    IOCFG2 = 0x00  # GDO2 Output Pin Configuration
    IOCFG1 = 0x01  # GDO1 Output Pin Configuration
    IOCFG0 = 0x02  # GDO0 Output Pin Configuration
    FIFOTHR = 0x03  # RX FIFO and TX FIFO Thresholds
    SYNC1 = 0x04  # Sync Word, High Byte
    SYNC0 = 0x05  # Sync Word, Low Byte
    PKTLEN = 0x06  # Packet Length
    PKTCTRL1 = 0x07  # Packet Automation Control
    PKTCTRL0 = 0x08  # Packet Automation Control
    ADDR = 0x09  # Device Address
    CHANNR = 0x0A  # Channel Number
    FSCTRL1 = 0x0B  # Frequency Synthesizer Control
    FSCTRL0 = 0x0C  # Frequency Synthesizer Control
    FREQ2 = 0x0D  # Frequency Control Word, High Byte
    FREQ1 = 0x0E  # Frequency Control Word, Middle Byte
    FREQ0 = 0x0F  # Frequency Control Word, Low Byte
    MDMCFG4 = 0x10  # Modem Configuration
    MDMCFG3 = 0x11  # Modem Configuration
    MDMCFG2 = 0x12  # Modem Configuration
    MDMCFG1 = 0x13  # Modem Configuration
    MDMCFG0 = 0x14  # Modem Configuration
    DEVIATN = 0x15  # Modem Deviation Setting
    MCSM2 = 0x16  # Main Radio Control State Machine Configuration
    MCSM1 = 0x17  # Main Radio Control State Machine Configuration
    MCSM0 = 0x18  # Main Radio Control State Machine Configuration
    FOCCFG = 0x19  # Frequency Offset Compensation Configuration
    BSCFG = 0x1A  # Bit Synchronization Configuration
    AGCCTRL2 = 0x1B  # AGC Control
    AGCCTRL1 = 0x1C  # AGC Control
    AGCCTRL0 = 0x1D  # AGC Control
    WOREVT1 = 0x1E  # High Byte Event0 Timeout
    WOREVT0 = 0x1F  # Low Byte Event0 Timeout
    WORCTRL = 0x20  # Wake On Radio Control
    FREND1 = 0x21  # Front End RX Configuration
    FREND0 = 0x22  # Front End TX Configuration
    FSCAL3 = 0x23  # Frequency Synthesizer Calibration
    FSCAL2 = 0x24  # Frequency Synthesizer Calibration
    FSCAL1 = 0x25  # Frequency Synthesizer Calibration
    FSCAL0 = 0x26  # Frequency Synthesizer Calibration
    RCCTRL1 = 0x27  # RC Oscillator Configuration
    RCCTRL0 = 0x28  # RC Oscillator Configuration

    # Configuration Register Details - Registers that Loose Programming in SLEEP State

    FSTEST = 0x29  # Frequency Synthesizer Calibration Control
    PTEST = 0x2A  # Production Test
    AGCTEST = 0x2B  # AGC Test
    TEST2 = 0x2C  # Various Test Settings
    TEST1 = 0x2D  # Various Test Settings
    TEST0 = 0x2E  # Various Test Settings

    # Command Strobe Registers

    SRES = 0x30  # Reset chip
    SFSTXON = 0x31  # Enable and calibrate frequency synthesizer (if MCSM0.FS_AUTOCAL=1).
    # If in RX (with CCA): Go to a wait state where only the synthesizer
    # is running (for quick RX / TX turnaround).

    SXOFF = 0x32  # Turn off crystal oscillator.
    SCAL = 0x33  # Calibrate frequency synthesizer and turn it off.
    # SCAL can be strobed from IDLE mode without setting manual calibration mode.

    SRX = 0x34  # Enable RX. Perform calibration first if coming from IDLE and MCSM0.FS_AUTOCAL=1.
    STX = 0x35  # In IDLE state: Enable TX. Perform calibration first
    # if MCSM0.FS_AUTOCAL=1.
    # If in RX state and CCA is enabled: Only go to TX if channel is clear.

    SIDLE = 0x36  # Exit RX / TX, turn off frequency synthesizer and exit Wake-On-Radio mode if applicable.
    SWOR = 0x38  # Start automatic RX polling sequence (Wake-on-Radio)
    # as described in Section 19.5 if WORCTRL.RC_PD=0.

    SPWD = 0x39  # Enter power down mode when CSn goes high.
    SFRX = 0x3A  # Flush the RX FIFO buffer. Only issue SFRX in IDLE or RXFIFO_OVERFLOW states.
    SFTX = 0x3B  # Flush the TX FIFO buffer. Only issue SFTX in IDLE or TXFIFO_UNDERFLOW states.
    SWORRST = 0x3C  # Reset real time clock to Event1 value.
    SNOP = 0x3D  # No operation. May be used to get access to the chip status byte.

    PATABLE = 0x3E  # PATABLE
    TXFIFO = 0x3F  # TXFIFO
    RXFIFO = 0x3F  # RXFIFO

    # Status Register Details

    PARTNUM = 0xF0  # Chip ID
    VERSION = 0xF1  # Chip ID
    FREQEST = 0xF2  # Frequency Offset Estimate from Demodulator
    LQI = 0xF3  # Demodulator Estimate for Link Quality
    RSSI = 0xF4  # Received Signal Strength Indication
    MARCSTATE = 0xF5  # Main Radio Control State Machine State
    WORTIME1 = 0xF6  # High Byte of WOR Time
    WORTIME0 = 0xF7  # Low Byte of WOR Time
    PKTSTATUS = 0xF8  # Current GDOx Status and Packet Status
    VCO_VC_DAC = 0xF9  # Current Setting from PLL Calibration Module
    TXBYTES = 0xFA  # Underflow and Number of Bytes
    RXBYTES = 0xFB  # Overflow and Number of Bytes
    RCCTRL1_STATUS = 0xFC  # Last RC Oscillator Calibration Result
    RCCTRL0_STATUS = 0xFD  # Last RC Oscillator Calibration Result

    def __init__(self, bus=0, device=0, speed=50000, debug=True):
        try:
            self.debug = debug
            self._spi = spidev.SpiDev()
            self._spi.open(bus, device)
            self._spi.max_speed_hz = speed

        except Exception as e:
            print(e)

    def _usDelay(self, useconds):
        time.sleep(useconds / 1000000.0)

    def _writeSingleByte(self, address, byte_data):
        return self._spi.xfer([self.WRITE_SINGLE_BYTE | address, byte_data])

    def _readSingleByte(self, address):
        return self._spi.xfer([self.READ_SINGLE_BYTE | address, 0x00])[1]

    def _readBurst(self, start_address, length):
        buff = []
        ret = []

        for x in range(length + 1):
            addr = (start_address + (x * 8)) | self.READ_BURST
            buff.append(addr)

        ret = self._spi.xfer(buff)[1:]

        if self.debug:
            print("_readBurst | start_address = {:x}, length = {:x}".format(start_address, length))

        return ret

    def _writeBurst(self, address, data):
        data.insert(0, (self.WRITE_BURST | address))

        return self._spi.xfer(data)

    def reset(self):
        return self._strobe(self.SRES)

    def _strobe(self, address):
        return self._spi.xfer([address, 0x00])

    def selfTest(self):
        part_number = self._readSingleByte(self.PARTNUM)
        component_version = self._readSingleByte(self.VERSION)

        # These asserts are based on the documentation
        # Section 29.3 "Status Register Details"
        # On reset PARTNUM == 0x00
        # On reset VERSION == 0x14

        assert part_number == 0x00
        assert component_version == 0x14

        if self.debug:
            print("Part Number: {:x}".format(part_number))
            print("Component Version: {:x}".format(component_version))
            print("Self test OK")

    def sidle(self):
        self._strobe(self.SIDLE)

        while (self._readSingleByte(self.MARCSTATE) != 0x01):
            self._usDelay(100)

        self._strobe(self.SFTX)
        self._usDelay(100)

    def powerDown(self):
        self.sidle()
        self._strobe(self.SPWD)

    @staticmethod
    def _computeFrequencyControlWords(freq_mhz: float) -> tuple:
        return tuple(int(freq_mhz * 2520.6155).to_bytes(length=3, byteorder="big"))

    def setCarrierFrequency(self, freq=433):
        freq2, freq1, freq0 = self._computeFrequencyControlWords(freq)
        self._writeSingleByte(self.FREQ2, freq2)
        self._writeSingleByte(self.FREQ1, freq1)
        self._writeSingleByte(self.FREQ0, freq0)

    def setChannel(self, channel=0x00):
        self._writeSingleByte(self.CHANNR, channel)

    def setSyncWord(self, sync_word="FAFA"):
        assert len(sync_word) == 4

        self._writeSingleByte(self.SYNC1, int(sync_word[:2], 16))
        self._writeSingleByte(self.SYNC0, int(sync_word[2:], 16))

    def getRegisterConfiguration(self, register, showConfig=True):
        def toBits(byte):
            return bin(byte)[2:].zfill(8)

        if register == "PKTCTRL1":
            bits = toBits(self._readSingleByte(self.PKTCTRL1))

            if showConfig:
                print("PKTCTRL1")
                print("PQT[7:5] = {}".format(bits[:3]))
                print("CRC_AUTOFLUSH = {}".format(bits[4]))
                print("APPEND_STATUS = {}".format(bits[5]))
                print("ADR_CHK[1:0] = {}".format(bits[6:]))

        elif register == "PKTCTRL0":
            bits = toBits(self._readSingleByte(self.PKTCTRL0))

            if showConfig:
                print("PKTCTRL0")
                print("WHITE_DATA = {}".format(bits[1]))
                print("PKT_FORMAT[1:0] = {}".format(bits[2:4]))
                print("CRC_EN = {}".format(bits[5]))
                print("LENGTH_CONFIG[1:0] = {}".format(bits[6:]))

        elif register == "ADDR":
            bits = toBits(self._readSingleByte(self.ADDR))

            if showConfig:
                print("ADDR")
                print("DEVICE_ADDR = {}".format(bits))

        elif register == "CHANNR":
            bits = toBits(self._readSingleByte(self.CHANNR))

            if showConfig:
                print("CAHNNR")
                print("CHAN = {}".format(bits))

        elif register == "PKTSTATUS":
            bits = toBits(self._readSingleByte(self.CHANNR))

            if showConfig:
                print("PKTSTATUS")
                print("CRC_OK = {}".format(bits[0]))
                print("CS = {}".format(bits[1]))
                print("PQT_REACHED = {}".format(bits[2]))
                print("CCA = {}".format(bits[3]))
                print("SFD = {}".format(bits[4]))
                print("GDO2 = {}".format(bits[5]))
                print("GDO0 = {}".format(bits[7]))

        elif register == "MDMCFG2":
            bits = toBits(self._readSingleByte(self.MDMCFG2))

            if showConfig:
                print("MDMCFG2")
                print("DEM_DCFILT_OFF = {}".format(bits[0]))
                print("MOD_FORMAT = {}".format(bits[1:4]))
                print("MANCHESTER_EN = {}".format(bits[4]))
                print("SYNC_MODE = {}".format(bits[5:]))

        elif register == "MDMCFG1":
            bits = toBits(self._readSingleByte(self.MDMCFG1))

            if showConfig:
                print("MDMCFG1")
                print("FEC_EN = {}".format(bits[0]))
                print("NUM_PREAMBLE = {}".format(bits[1:4]))
                print("CHANSPC_E = {}".format(bits[6:]))

        return bits

    def setDefaultValues(self, version=1):

        # Default values extracted from Smart RF Studio 7

        self._writeSingleByte(self.IOCFG2, 0x2E)    # Panstamp
        self._writeSingleByte(self.IOCFG1, 0x2E)    # Panstamp
        self._writeSingleByte(self.IOCFG0, 0x06)    # Panstamp
        self._writeSingleByte(self.FIFOTHR, 0x07)   # Panstamp
        self._writeSingleByte(self.PKTLEN, 20)
        self._writeSingleByte(self.PKTCTRL1, 0x06)  # Panstamp
        self._writeSingleByte(self.PKTCTRL0, 0x04)  # Panstamp

        self.setSyncWord()
        self.setChannel()
        self.configureAddressFiltering()

        self._writeSingleByte(self.FSCTRL1, 0x08)   # Panstamp
        self._writeSingleByte(self.FSCTRL0, 0x00)   # Panstamp

        self.setCarrierFrequency()

        self._writeSingleByte(self.MDMCFG4, 0xCA)   # Panstamp
        self._writeSingleByte(self.MDMCFG3, 0x83)   # Panstamp
        self._writeSingleByte(self.MDMCFG2, 0x93)   # Panstamp
        self._writeSingleByte(self.MDMCFG1, 0x22)
        self._writeSingleByte(self.MDMCFG0, 0xF8)

        self._writeSingleByte(self.DEVIATN, 0x35)   # Panstamp
        self._writeSingleByte(self.MCSM2, 0x07)
        self._writeSingleByte(self.MCSM1, 0x20)     # Panstamp
        self._writeSingleByte(self.MCSM0, 0x18)
        self._writeSingleByte(self.FOCCFG, 0x16)
        self._writeSingleByte(self.BSCFG, 0x6C)
        self._writeSingleByte(self.AGCCTRL2, 0x43)  # Panstamp
        self._writeSingleByte(self.AGCCTRL1, 0x40)
        self._writeSingleByte(self.AGCCTRL0, 0x91)
        self._writeSingleByte(self.WOREVT1, 0x87)
        self._writeSingleByte(self.WOREVT0, 0x6B)
        self._writeSingleByte(self.WORCTRL, 0xFB)
        self._writeSingleByte(self.FREND1, 0x56)
        self._writeSingleByte(self.FREND0, 0x10)
        self._writeSingleByte(self.FSCAL3, 0xE9)
        self._writeSingleByte(self.FSCAL2, 0x2A)
        self._writeSingleByte(self.FSCAL1, 0x00)
        self._writeSingleByte(self.FSCAL0, 0x1F)
        self._writeSingleByte(self.RCCTRL1, 0x41)
        self._writeSingleByte(self.RCCTRL0, 0x00)
        self._writeSingleByte(self.FSTEST, 0x59)
        self._writeSingleByte(self.PTEST, 0x7F)
        self._writeSingleByte(self.AGCTEST, 0x3F)
        self._writeSingleByte(self.TEST2, 0x81)
        self._writeSingleByte(self.TEST1, 0x35)
        self._writeSingleByte(self.TEST0, 0x09)
        self._writeSingleByte(0x3E, 0xC0)           # Power 10dBm

    def setSyncMode(self, syncmode):
        regVal = list(self.getRegisterConfiguration("MDMCFG2"))

        if syncmode > 7:
            raise Exception("Invalid SYNC mode")

        regVal[5:] = bin(syncmode)[2:].zfill(3)

        regVal = int("".join(regVal), 2)
        self._writeSingleByte(self.MDMCFG2, regVal)

    def setModulation(self, modulation):
        regVal = list(self.getRegisterConfiguration("MDMCFG2"))

        if modulation == "2-FSK":
            modVal = "000"

        elif modulation == "GFSK":
            modVal = "001"

        elif modulation == "ASK" or modulation == "OOK":
            modVal = "011"

        elif modulation == "4-FSK":
            modVal = "100"

        elif modulation == "MSK":
            modVal = "111"

        else:
            raise Exception("Modulation type NOT SUPPORTED!")

        regVal[1:4] = modVal

        regVal = int("".join(regVal), 2)
        self._writeSingleByte(self.MDMCFG2, regVal)

    def _flushRXFifo(self):
        self._strobe(self.SFRX)
        self._usDelay(2)

    def _flushTXFifo(self):
        self._strobe(self.SFTX)
        self._usDelay(2)

    def _setTXState(self):
        self._strobe(self.STX)
        self._usDelay(2)

    def _setRXState(self):
        self._strobe(self.SRX)
        self._usDelay(2)

    def getRSSI(self):
        return self._readSingleByte(self.RSSI)

    def _getMRStateMachineState(self):
        # The &0x1F works as a mask due to the fact
        # that the MARCSTATE register only uses the
        # first 5 bits
        return (self._readSingleByte(self.MARCSTATE) & 0x1F)

    def getPacketConfigurationMode(self):
        pktCtrlVal = self.getRegisterConfiguration("PKTCTRL0", False)

        if pktCtrlVal[6:] == "00": # Packet len is fixed
            return "PKT_LEN_FIXED"

        elif pktCtrlVal[6:] == "01": # Packet len is variable
            return "PKT_LEN_VARIABLE"

        elif pktCtrlVal[6:] == "10":  # Infinite packet len mode
            return "PKT_LEN_INFINITE"

    def setPacketMode(self, mode="PKT_LEN_VARIABLE"):
        regVal = list(self.getRegisterConfiguration("PKTCTRL0", False))

        if mode == "PKT_LEN_FIXED":
            val = "00"

        elif mode == "PKT_LEN_VARIABLE":
            val = "01"

        elif mode == "PKT_LEN_INFINITE":
            val = "10"

        else:
            raise Exception("Packet mode NOT SUPPORTED!")

        regVal[6:] = val
        regVal = int("".join(regVal), 2)
        self._writeSingleByte(self.PKTCTRL0, regVal)

    def setFilteringAddress(self, address=0x0E):
        self._writeSingleByte(self.ADDR, address)

    def configureAddressFiltering(self, value="DISABLED"):
        regVal = list(self.getRegisterConfiguration("PKTCTRL1", False))

        if value == "DISABLED":
            val = "00"

        elif value == "ENABLED_NO_BROADCAST":
            val = "01"

        elif value == "ENABLED_00_BROADCAST":
            val = "10"

        elif value == "ENABLED_00_255_BROADCAST":
            val = "11"

        else:
            raise Exception("Address filtering configuration NOT SUPPORTED!")

        regVal[6:] = val

        regVal = int("".join(regVal), 2)
        self._writeSingleByte(self.PKTCTRL1, regVal)

    def sendData(self, dataBytes):
        self._setRXState()
        marcstate = self._getMRStateMachineState()
        dataToSend = []

        while ((marcstate & 0x1F) != 0x0D):
            if self.debug:
                print("marcstate = %x".format(marcstate))
                print("waiting for marcstate == 0x0D")

            if marcstate == 0x11:
                self._flushRXFifo()

            marcstate = self._getMRStateMachineState()

        if len(dataBytes) == 0:
            if self.debug:
                print("sendData | No data to send")
            return False

        sending_mode = self.getPacketConfigurationMode()
        data_len = len(dataBytes)

        if sending_mode == "PKT_LEN_FIXED":
            if data_len > self._readSingleByte(self.PKTLEN):
                if self.debug:
                    print("Len of data exceeds the configured packet len")
                return False

            if self.getRegisterConfiguration("PKTCTRL1", False)[6:] != "00":
                dataToSend.append(self._readSingleByte(self.ADDR))

            dataToSend.extend(dataBytes)
            dataToSend.extend([0] * (self._readSingleByte(self.PKTLEN) - len(dataToSend)))

            if self.debug:
                print("Sending a fixed len packet")
                print("data len = %d".format((data_len)))

        elif sending_mode == "PKT_LEN_VARIABLE":
            dataToSend.append(data_len)

            if self.getRegisterConfiguration("PKTCTRL1", False)[6:] != "00":
                dataToSend.append(self._readSingleByte(self.ADDR))
                dataToSend[0] += 1

            dataToSend.extend(dataBytes)

            if self.debug:
                print("Sending a variable len packet")
                print("Length of the packet is: %d".format(data_len))

        elif sending_mode == "PKT_LEN_INFINITE":
            # ToDo
            raise Exception("MODE NOT IMPLEMENTED")

        print("{}".format(dataToSend))
        self._writeBurst(self.TXFIFO, dataToSend)
        self._usDelay(2000)
        self._setTXState()
        marcstate = self._getMRStateMachineState()

        if marcstate not in [0x13, 0x14, 0x15]:  # RX, RX_END, RX_RST
            self.sidle()
            self._flushTXFifo()
            self._setRXState()

            if self.debug:
                print("senData | FAIL")
                print("sendData | MARCSTATE: %x".format(self._readSingleByte(self.MARCSTATE)))

            return False

        remaining_bytes = self._readSingleByte(self.TXBYTES) & 0x7F
        while remaining_bytes != 0:
            self._usDelay(1000)
            remaining_bytes = self._readSingleByte(self.TXBYTES) & 0x7F
            if self.debug:
                print("Waiting until all bytes are transmited, remaining bytes: %d".format(remaining_bytes))


        if (self._readSingleByte(self.TXBYTES) & 0x7F) == 0:
            if self.debug:
                print("Packet sent!")

            return True

        else:
            if self.debug:
                print("{}".format(self._readSingleByte(self.TXBYTES) & 0x7F))
                print("sendData | MARCSTATE: %x".format(self._getMRStateMachineState()))
                self.sidle()
                self._flushTXFifo()
                time.sleep(5)
                self._setRXState()

            return False

    def recvData(self):
        rx_bytes_val = self._readSingleByte(self.RXBYTES)

        #if rx_bytes_val has something and Underflow bit is not 1
        if (rx_bytes_val & 0x7F and not (rx_bytes_val & 0x80)):
            sending_mode = self.getPacketConfigurationMode()

            if sending_mode == "PKT_LEN_FIXED":
                data_len = self._readSingleByte(self.PKTLEN)

            elif sending_mode == "PKT_LEN_VARIABLE":
                max_len = self._readSingleByte(self.PKTLEN)
                data_len = self._readSingleByte(self.RXFIFO)

                if data_len > max_len:
                    if self.debug:
                        print("Len of data exceeds the configured maximum packet len")
                    return False

                if self.debug:
                    print("Receiving a variable len packet")
                    print("max len: %d".format(max_len))
                    print("Packet length: %d".format(data_len))

            elif sending_mode == "PKT_LEN_INFINITE":
                # ToDo
                raise Exception("MODE NOT IMPLEMENTED")

            data = self._readBurst(self.RXFIFO, data_len)
            valPktCtrl1 = self.getRegisterConfiguration("PKTCTRL1", False)

            if valPktCtrl1[5] == "1":  # PKTCTRL1[5] == APPEND_STATUS
            # When enabled, two status bytes will be appended to the payload of the
            # packet. The status bytes contain RSSI and LQI values, as well as CRC OK.

                rssi = self._readSingleByte(self.RXFIFO)
                val = self._readSingleByte(self.RXFIFO)
                lqi = val & 0x7f

            if self.debug and valPktCtrl1[5] == "1":
                print("Packet information is enabled")
                print("RSSI: %d".format((rssi)))
                print("VAL: %d".format((val)))
                print("LQI: %d".format((lqi)))

            print("Data: ") + str(data)

            self._flushRXFifo()
            return data
