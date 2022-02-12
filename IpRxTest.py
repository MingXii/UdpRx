from math import ceil
import os
os.environ['COCOTB_RESOLVE_X'] = 'ZEROS'
import cocotb
import random
from collections import deque
from cocotb.triggers import Timer
from cocotb.triggers import ClockCycles
from cocotb.clock import Clock
from cocotb.result import TestSuccess, TestFailure
from cocotb.triggers import RisingEdge
from queue import Queue
from cocotb.binary import *
#需要引入参考模型

CASES_NUM = 100  # the number of test cases
DES_IP = '17171717'

# class IpRxTester:
#     def __init__(self, target) -> None:  #-> None为没有返回值
#         self.dut = target
#         self.ref_outputs = deque()  # store reference results
#
#     async def reset_dut(self):
#         dut = self.dut
#         dut.reset.value = 0
#         await RisingEdge(dut.clk)
#         dut.reset.value = 1
#         for i in range(10):
#             await RisingEdge(dut.clk)
#
#         dut.reset.value = 0
#
#     async def generate_input(self):
#         cocotb.log.info("get a transaction in Input Driver")
#         dut = self.dut
#         edge = RisingEdge(dut.clk)
#         dut.io_dataIn_valid <= 1
#         dut.io_dataIn_payload_fragment <= 0x45
#         await edge
#         byte_cnt = 0
#         while byte_cnt < BYTE_NUM:
#             transaction = random.randint(0, 255)
#             self.outReady <= (random.random() > 0.3)
#             self.inValid <= 1
#             self.inFragment <= transaction
#             if(self.inValid.value & self.inReady.value):
#                 self.taskQ.append(transaction)
#             await edge
#         last = random.randint(0, 255)
#         self.inValid <= 1
#         self.outReady <= 1
#         self.inFragment <= last
#         self.inLast <=1
#         self.taskQ.append(last)
#         ipHead = self.taskQ.popleft(19)
#         desIp = list(ipHead.pop(4))
#         desIpStr = ''.join(desIp)
#         if(desIpStr == DES_IP):
#             self.aimResult = self.taskQ
#         else:
#             self.aimResult = deque()
#         await edge
#         self.inValid <= 0
#         self.inLast <= 0
#         await ClockCycles(self.clk,10,True)




# class clockDomain(object):
#     def __init__(self, clkSig,period,unit,resetSig=None,resetActiveHigh=True):
#         self.clk = clkSig
#         self.reset = resetSig
#         self.period = period
#         self.unit = unit
#         self.resetActiveHigh = resetActiveHigh
#     async def doReset(self):
#         clockCycle = ClockCycles(self.clk,10,True) #等待10个边沿
#         if(self.resetActiveHigh):
#             self.reset <= 1
#         else:
#             self.reset <= 0
#         await clockCycle
#         if(self.resetActiveHigh):
#             self.reset <= 0
#         else:
#             self.reset <= 1
#     async def genClk(self):
#         self.clk.setimmediatevalue(0) #阻塞赋值
#         while True:
#             await Timer(self.period/2,self.unit)
#             self.clk.setimmediatevalue(1) #阻塞赋值
#             await Timer(self.period/2,self.unit)
#             self.clk.setimmediatevalue(0) #阻塞赋值
#     async def start(self):
#         clockTh = cocotb.fork(self.genClk())
#         resetTh = cocotb.fork(self.doReset())
#         await resetTh.join()
#         return clockTh
#
# class inputDrv(object):
#     def __init__(self,inValidSig,inFragmentSig,inLastSig,inReadySig,outReadySig,clk):
#         self.inValid = inValidSig
#         self.inFragment = inFragmentSig
#         self.inLast = inLastSig
#         self.inReady = inReadySig
#         self.outReady = outReadySig
#         self.clk = clk
#         self.taskQ = deque()
#         #self.aimResult = deque()
#         self.inValid.setimmediatevalue(0)
#         self.inLast.setimmediatevalue(0)
#         self.outReady.setimmediatevalue(0)
#
#     async def timeGen(self):
#         cocotb.log.info("get a transaction in Input Driver")
#         edge = RisingEdge(self.clk)
#         self.inValid <= 1
#         self.inFragment <= 0x45
#         await edge
#         byte_cnt = 0
#         while byte_cnt < BYTE_NUM:
#             transaction = random.randint(0, 255)
#             self.outReady <= (random.random() > 0.3)
#             self.inValid <= 1
#             self.inFragment <= transaction
#             if(self.inValid.value & self.inReady.value):
#                 self.taskQ.append(transaction)
#             await edge
#         last = random.randint(0, 255)
#         self.inValid <= 1
#         self.outReady <= 1
#         self.inFragment <= last
#         self.inLast <=1
#         self.taskQ.append(last)
#         ipHead = self.taskQ.popleft(19)
#         desIp = list(ipHead.pop(4))
#         desIpStr = ''.join(desIp)
#         if(desIpStr == DES_IP):
#             self.aimResult = self.taskQ
#         else:
#             self.aimResult = deque()
#         await edge
#         self.inValid <= 0
#         self.inLast <= 0
#         await ClockCycles(self.clk,10,True)
#
# class outputMon(object):
#     def __init__(self,outValidSig,outFragmentSig,outReadySig,clk):
#         self.outValid = outValidSig
#         self.outFragment = outFragmentSig
#         self.outReady = outReadySig
#         self.clk = clk
#         self.recvQ = deque()
#         self.outReady.setimmediatevalue(0)
#     async def TaskMon(self):
#         edge = RisingEdge(self.clk)
#         while True:
#             if(self.outValid.value & self.outReady.value):
#                 cocotb.log.info("get a transaction in Output Monitor")
#                 self.recvQ.append(self.outFragment.value)
#             await edge
#
# class ipRxTb(object):
#     def __init__(self,dut):
#         self.dut = dut
#         self.inDrv = inputDrv(dut.io_dataIn_valid,dut.io_dataIn_payload_fragment,dut.io_dataIn_payload_last,dut.io_dataIn_ready,dut.io_dataOut_ready,dut.clk)
#         self.outMon = outputMon(dut.io_dataOut_valid,dut.io_dataOut_payload_fragment,dut.io_dataOut_ready,dut.clk)
#         self.clockCtrl = clockDomain(self.dut.clk,10,'ns',self.dut.reset,True)
#     async def start(self):
#         self.inDrvTh = cocotb.fork(self.inDrv.timeGen())
#         self.outMonTh = cocotb.fork(self.outMon.TaskMon())
#         self.clkckCtrlTh = await self.clockCtrl.start()
#     def stop(self):
#         self.inDrvTh.kill()
#         self.outMonTh.kill()
#         self.clkckCtrlTh.kill()
#     def resultCheck(self):
#         assert self.inDrv.aimResult == self.outMon.recvQ
#
# @cocotb.test()
# async def run_test(dut):
#     dut.io_dataOut_ready.value = False
#     tb = ipRxTb(dut)
#     await tb.start()
#     tb.stop()
#     tb.resultCheck()


# class clockDomain():
#     def __init__(self, clkSig,period,unit,resetSig=None,resetActiveHigh=True):
#         self.clk = clkSig
#         self.reset = resetSig
#         self.period = period
#         self.unit = unit
#         self.resetActiveHigh = resetActiveHigh
#     async def doReset(self):
#         clockCycle = ClockCycles(self.clk,5,True) #等待10个边沿
#         if(self.resetActiveHigh):
#             self.reset <= 1
#         else:
#             self.reset <= 0
#         await clockCycle
#         if(self.resetActiveHigh):
#             self.reset <= 0
#         else:
#             self.reset <= 1
#     async def genClk(self):
#         self.clk.setimmediatevalue(0) #阻塞赋值
#         while True:
#             await Timer(self.period/2,self.unit)
#             self.clk.setimmediatevalue(1) #阻塞赋值
#             await Timer(self.period/2,self.unit)
#             self.clk.setimmediatevalue(0) #阻塞赋值
#     async def start(self):
#         clockTh = cocotb.fork(self.genClk()) #一直运行
#         resetTh = cocotb.fork(self.doReset()) #clockTh和reseTh并行运行
#         await resetTh.join() #等resetTH运行结束
#         return clockTh #返回一个时钟clockTh
#
# class inputDrv():
#     def __init__(self,inValidSig,inFragmentSig,inLastSig,inReadySig,outReadySig,clk):
#         self.inValid = inValidSig
#         self.inFragment = inFragmentSig
#         self.inLast = inLastSig
#         self.inReady = inReadySig
#         self.outReady = outReadySig
#         self.clk = clk
#         self.taskQ = deque()
#         self.aimResult = deque()
#         self.inValid.setimmediatevalue(0)
#         self.inLast.setimmediatevalue(0)
#         self.outReady.setimmediatevalue(0)
#
#     async def timeGen(self):
#         cocotb.log.info("get a transaction in Input Driver")
#         edge = RisingEdge(self.clk)
#         self.inValid <= 1
#         self.inFragment <= 0x45
#         self.outReady <= (random.random() > 0.3)
#         await edge
#         byte_cnt = 0
#         while byte_cnt < BYTE_NUM:
#             transaction = random.randint(0, 255)
#             self.outReady <= (random.random() > 0.3)
#             self.inValid<= 1
#             self.inFragment <= transaction
#             if(self.inValid.value & self.inReady.value):
#                 self.taskQ.append(transaction)
#             await edge
#         last = random.randint(0, 255)
#         self.inValid <= 1
#         self.outReady <= 1
#         self.inFragment <= last
#         self.inLast <=1
#         self.taskQ.append(last)
#         ipHead = self.taskQ.popleft(19)
#         desIp = list(ipHead.pop(4))
#         desIpStr = ''.join(desIp)
#         if(desIpStr == DES_IP):
#             self.aimResult = self.taskQ
#         await edge
#         self.inValid <= 0
#         self.inLast <= 0
#         await ClockCycles(self.clk,10,True)
#
# class outputMon():
#     def __init__(self,outValidSig,outFragmentSig,outReadySig,clk):
#         self.outValid = outValidSig
#         self.outFragment = outFragmentSig
#         self.outReady = outReadySig
#         self.clk = clk
#         self.recvQ = deque()
#     async def TaskMon(self):
#         edge = RisingEdge(self.clk)
#         while True:
#             if(self.outValid.value & self.outReady.value) == True:
#                 cocotb.log.info("get a transaction in Output Monitor")
#                 self.recvQ.append(self.outFragment.value)
#             await edge
#
# class ipRxTb():
#     def __init__(self,dut):
#         self.dut = dut
#         self.inDrv = inputDrv(dut.io_dataIn_valid,dut.io_dataIn_payload_fragment,dut.io_dataIn_payload_last,dut.io_dataIn_ready,dut.io_dataOut_ready,dut.clk)
#         self.outMon = outputMon(dut.io_dataOut_valid,dut.io_dataOut_payload_fragment,dut.io_dataOut_ready,dut.clk)
#         self.clockCtrl = clockDomain(self.dut.clk,10,'ns',self.dut.reset,True)
#     async def start(self):
#         self.clk =
#         self.clkckCtrlTh = await self.clockCtrl.start()
#         self.inDrvTh = cocotb.fork(self.inDrv.timeGen())
#         self.outMonTh = cocotb.fork(self.outMon.TaskMon())
#     def stop(self):
#         self.inDrvTh.kill()
#         self.outMonTh.kill()
#         self.clkckCtrlTh.kill()
#     def resultCheck(self):
#         assert self.inDrv.aimResult == self.outMon.recvQ
#
# @cocotb.test()
# async def run_test(dut):
#     tb = ipRxTb(dut)
#     await tb.start()
#     tb.stop()
#     tb.resultCheck()


# class IpRxTester:
#     def __init__(self, target) -> None:  #-> None为没有返回值
#         self.dut = target
#         self.taskQ = []  # store reference results
#         self.aimResult = []
#         self.recvQ = []
#
#     async def reset_dut(self):
#         dut = self.dut
#         dut.reset.value = 0
#         await RisingEdge(dut.clk)
#         dut.reset.value = 1
#         for i in range(10):
#             await RisingEdge(dut.clk)
#         dut.reset.value = 0
#
#     async def generate_input(self):
#         dut = self.dut
#         cocotb.log.info("get a transaction in Input Driver")
#         edge = RisingEdge(dut.clk)
#         case_cnt = 0
#         while case_cnt < CASES_NUM:
#             BYTE_NUM = random.randint(50, 200)
#             dut.io_dataIn_valid <= 1
#             dut.io_dataIn_payload_fragment <= 0x45
#             self.taskQ.append(0x45)
#             dut.io_dataOut_ready <= (random.random() > 0.3)
#             await edge
#             byte_cnt = 0
#             while byte_cnt < BYTE_NUM:
#                 # transaction = random.randint(16, 18)
#                 transaction = 17
#                 dut.io_dataOut_ready <= (random.random() > 0.3)
#                 dut.io_dataIn_valid <= 1
#                 dut.io_dataIn_payload_fragment <= transaction
#                 if(dut.io_dataIn_valid.value & dut.io_dataIn_ready.value) == True:
#                     self.taskQ.append(transaction)
#                     # print(self.taskQ)
#                 await edge
#                 byte_cnt = byte_cnt + 1
#             last = random.randint(0, 255)
#             dut.io_dataIn_valid <= 1
#             dut.io_dataOut_ready <= 1
#             dut.io_dataIn_payload_fragment <= last
#             dut.io_dataIn_payload_last <= 1
#             self.taskQ.append(last)
#             ipHead = self.taskQ[0:20]
#             # print(ipHead)
#             desIp = ipHead[16:20]
#             # print(desIp)
#             strIP = [str(i) for i in desIp]
#             desIpStr = ''.join(strIP)
#             # print(desIpStr)
#             if(desIpStr == DES_IP):
#                 self.aimResult.append(self.taskQ[20:])
#             self.taskQ.clear()
#             print(self.aimResult)
#             await edge
#             dut.io_dataIn_valid <= 0
#             dut.io_dataIn_payload_last <= 0
#             await ClockCycles(dut.clk,10,True)
#             case_cnt = case_cnt + 1
#
#         if case_cnt == CASES_NUM - 1 :
#             raise TestSuccess(" pass {} test cases".format(CASES_NUM))
#
#     async def TaskMon(self):
#         dut = self.dut
#         edge = RisingEdge(dut.clk)
#         while True:
#             if(dut.io_dataOut_valid.value & dut.io_dataOut_ready.value) == True:
#                 cocotb.log.info("get a transaction in Output Monitor")
#                 self.recvQ.append(dut.io_dataOut_payload_fragment.value)
#                 # print(self.recvQ)
#             await edge
#
#     # async def Start(self):
#     #     cocotb.fork(self.generate_input)
#     #     cocotb.fork(self.TaskMon())
#
#
#     # async def waitAllDone(self):
#     #     dut = self.dut
#     #     edge = RisingEdge(dut.clk)
#     #     last_cnt = 0
#     #     while True:
#     #         if(dut.io_dataIn_payload_last.value == True):
#     #             last_cnt = last_cnt + 1
#     #             print(last_cnt)
#     #         if(last_cnt == CASES_NUM ):
#     #             break
#     #         await edge
#     #     cocotb.fork(self.generate_input()).kill()
#     #     cocotb.fork(self.TaskMon()).kill()
#
#     # async def TaskMon(self):
#     #     dut = self.dut
#     #     edge = RisingEdge(dut.clk)
#     #     last_cnt = 0
#     #     if(last_cnt < CASES_NUM):
#     #         print(last_cnt)
#     #         if(dut.io_dataOut_valid.value & dut.io_dataOut_ready.value) == True:
#     #             cocotb.log.info("get a transaction in Output Monitor")
#     #             self.recvQ.append(dut.io_dataOut_payload_fragment)
#     #         if dut.io_dataIn_payload_last.value == True:
#     #             last_cnt = last_cnt + 1
#     #         await edge
#
# @cocotb.test(timeout_time=200000, timeout_unit="ns")
# async def IpRxTest(dut):
#     await cocotb.start(Clock(dut.clk, 10, "ns").start())
#     # set default values to all dut input ports
#     dut.io_dataIn_valid.value = False
#     dut.io_dataIn_payload_fragment.value = 0
#     dut.io_dataIn_payload_last.value = 0
#
#     dut.io_dataOut_ready = False
#
#     # start testing
#     tester = IpRxTester(dut)
#     await tester.reset_dut()
#     await Timer(100,'ns')
#     # await tester.Start()
#     await cocotb.start(tester.generate_input())
#     await cocotb.start(tester.TaskMon())
#     # await tester.generate_input()
#     # await tester.TaskMon()
#     # await cocotb.start(tester.generate_input())
#     # await cocotb.strat(tester.TaskMon())
#     # await tester.waitAllDone()
#     # assert tester.aimResult == tester.recvQ
#     while True:
#         await RisingEdge(dut.clk)

class IpRxTester:
    def __init__(self, target) -> None:  #-> None为没有返回值
        self.dut = target
        self.taskQ = []  # store reference results
        self.aimResult = []
        self.recvQ = []

    async def reset_dut(self):
        dut = self.dut
        dut.reset.value = 0
        await RisingEdge(dut.clk)
        dut.reset.value = 1
        for i in range(10):
            await RisingEdge(dut.clk)
        dut.reset.value = 0

    async def InputDrv(self):
        dut = self.dut
        cocotb.log.info("get a transaction in Input Driver")
        edge = RisingEdge(dut.clk)
        case_cnt = 0
        while case_cnt < CASES_NUM:
            BYTE_NUM = random.randint(50, 200)
            dut.io_dataIn_valid <= 1
            dut.io_dataIn_payload_fragment <= 0x45
            # self.taskQ.append(0x45)
            dut.io_dataOut_ready <= (random.random() > 0.3)
            await edge
            byte_cnt = 0
            while byte_cnt < BYTE_NUM:
                transaction = random.randint(16, 18)
                # transaction = 17
                dut.io_dataOut_ready <= (random.random() > 0.3)
                dut.io_dataIn_valid <= 1
                dut.io_dataIn_payload_fragment <= transaction
                if(dut.io_dataIn_valid.value & dut.io_dataIn_ready.value) == True:
                    self.taskQ.append(dut.io_dataIn_payload_fragment.value.integer)
                    # print("dut.io_dataIn_payload_fragment.value.integer" + str(dut.io_dataIn_payload_fragment.value.integer) )
                    # print("transaction" + str(transaction))
                    # print(self.taskQ)
                byte_cnt = byte_cnt + 1
                await edge
            last = random.randint(0, 255)
            dut.io_dataIn_valid <= 1
            dut.io_dataOut_ready <= 1
            dut.io_dataIn_payload_fragment <= last
            dut.io_dataIn_payload_last <= 1
            self.taskQ.append(dut.io_dataIn_payload_fragment.value.integer)
            await edge
            dut.io_dataIn_valid <= 0
            dut.io_dataIn_payload_last <= 0
            self.taskQ.append(dut.io_dataIn_payload_fragment.value.integer)
            ipHead = self.taskQ[0:20]
            # print(ipHead)
            desIp = ipHead[16:20]
            # print(desIp)
            strIP = [str(i) for i in desIp]
            desIpStr = ''.join(strIP)
            # print(desIpStr)
            if(desIpStr == DES_IP):
                self.aimResult.append(self.taskQ[20:])
                # print(self.aimResult)
                # print(self.taskQ)
            self.taskQ.clear()
            # print(self.aimResult)
            await ClockCycles(dut.clk,10,True)
            case_cnt = case_cnt + 1


    async def TaskMon(self):
        dut = self.dut
        edge = RisingEdge(dut.clk)
        case_cnt = 0
        while True:
            if(dut.io_dataOut_valid.value & dut.io_dataOut_ready.value) == True:
                cocotb.log.info("get a transaction in Output Monitor")
                self.recvQ.append(dut.io_dataOut_payload_fragment.value.integer)
                # print(self.aimResult)
                # print(self.recvQ)
            if(dut.io_dataOut_payload_last.value == True):
                print(self.aimResult)
                print(self.recvQ)
                assert self.aimResult[0] == self.recvQ
                case_cnt = case_cnt + 1
            await edge

            if case_cnt == 1:
                raise TestSuccess(" pass {} test cases".format(CASES_NUM))


@cocotb.test(timeout_time=200000, timeout_unit="ns")
async def IpRxTest(dut):
    await cocotb.start(Clock(dut.clk, 10, "ns").start())
    # set default values to all dut input ports
    dut.io_dataIn_valid.value = False
    dut.io_dataIn_payload_fragment.value = 0
    dut.io_dataIn_payload_last.value = 0

    dut.io_dataOut_ready = False

    # start testing
    tester = IpRxTester(dut)
    await tester.reset_dut()
    await Timer(100,'ns')
    await cocotb.start(tester.InputDrv())
    await cocotb.start(tester.TaskMon())

    while True:
        await RisingEdge(dut.clk)

