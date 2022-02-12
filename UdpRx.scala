/*
package workshop.udp_master
import spinal.core._
import spinal.lib._
import spinal.lib.fsm.{EntryPoint, State, StateMachine}

case class UdpRxGenerics(udpWidth: Int,//UDP数据位宽
                       cntWidth: Int,
                       des_port : Int,
                       byteNum: Int)

case class UdpRxData(g : UdpRxGenerics) extends Bundle{
  val byteNum  = UInt(g.byteNum bits)
  val data      = Bits(g.udpWidth bits)
  val srcPort   = Bits(16 bits)
}

case class UdpRx(udpGenerics:UdpRxGenerics) extends Component {
  val io = new Bundle {
    val mac_rxdata = slave Stream (Fragment(Bits(8 bits)))
    val rx = master Stream (Fragment(UdpRxData(udpGenerics)))
    val rx_done = out Bool()
/*    val byteNum = out UInt(udpGenerics.byteNum bits)
    val srcPort = out Bits(16 bits)*/
  }

  val rec_valid = Reg(Bool()) init(False)
  io.mac_rxdata.ready := False
  io.rx.valid := rec_valid
  io.rx_done := False
  io.rx.byteNum := 0
  io.rx.payload.last := False


  val cnt = Reg(UInt(udpGenerics.cntWidth bits)) init(0)
  val udp_byteNum = Reg(UInt(udpGenerics.byteNum bits)) init (0)
  val data_byteNum = Reg(UInt(udpGenerics.byteNum bits)) init (0)
  val des_port = Reg(Bits(udpGenerics.byteNum bits)) init (0)
  val src_port = Reg(Bits(16 bits)) init (0)

  io.rx.srcPort := src_port

  val dataCnt = Reg(UInt(udpGenerics.byteNum bits)) init (0)
/*  val rec_en_cnt = Reg(UInt(log2Up(udpGenerics.udpWidth/8) bits)) init (0)
 // val rec_en_cnt_next = RegNext(rec_en_cnt) init(0)
  val rec_data = Reg(Bits(udpGenerics.udpWidth bits)) init(0)

  io.rx.data := rec_data*/

  val fsm = new StateMachine {
    val idle: State = new State with EntryPoint {
      onEntry {
        udp_byteNum := 0
        data_byteNum := 0
        des_port := 0
        src_port := 0
      }
      whenIsActive {
        when(io.mac_rxdata.valid) {
          io.mac_rxdata.ready := True
          cnt := cnt + 1
          when(cnt === 0) {
            src_port(15 downto 8) := io.mac_rxdata.fragment
          }.elsewhen(cnt === 1) {
            src_port(7 downto 0) := io.mac_rxdata.fragment
          }.elsewhen(cnt === 2) {
            des_port(15 downto 8) := io.mac_rxdata.fragment
          }.elsewhen(cnt === 3) {
            des_port(7 downto 0) := io.mac_rxdata.fragment
          }.elsewhen(cnt === 4) {
            udp_byteNum(15 downto 8) := io.mac_rxdata.fragment.asUInt
          }.elsewhen(cnt === 5) {
            udp_byteNum(7 downto 0) := io.mac_rxdata.fragment.asUInt
          }.elsewhen(cnt === 7 ){
            when(des_port === udpGenerics.des_port){
              data_byteNum := udp_byteNum - 8
              cnt := 0
              goto(rx_data)
            }.otherwise{
              goto(rx_end)
            }
          }
        }
      }
    }

    val rx_data: State = new State {
      onEntry {
        dataCnt := 0
/*        rec_en_cnt := 0
        rec_data := 0*/
      }
      whenIsActive {
        when(io.mac_rxdata.valid) {
          /*when(rec_en_cnt === rec_en_cnt.maxValue && !io.rx.ready) {
            rec_valid := True
            rec_en_cnt := rec_en_cnt
            io.mac_rxdata.ready := False
          }.elsewhen(rec_en_cnt === rec_en_cnt.maxValue && io.rx.ready) {
            rec_valid := True
            rec_en_cnt := 0
            io.mac_rxdata.ready := True
          }.otherwise {
            rec_valid := False
            rec_en_cnt := rec_en_cnt + 1
            io.mac_rxdata.ready := True
          }

          //io.rx.data(8 * (rec_en_cnt + 1) - 1 downto 8 * rec_en_cnt) := io.mac_rxdata.fragment
          when(rec_en_cnt === 0) {
            rec_data(31 downto 24) := io.mac_rxdata.fragment
          }.elsewhen(rec_en_cnt === 1) {
            rec_data(23 downto 16) := io.mac_rxdata.fragment
          }.elsewhen(rec_en_cnt === 2) {
            rec_data(15 downto 8) := io.mac_rxdata.fragment
          }.elsewhen(rec_en_cnt === 3) {
            rec_data(7 downto 0) := io.mac_rxdata.fragment
          }*/

          StreamFragmentWidthAdapter(input = io.mac_rxdata,output = io.rx)

          when(io.mac_rxdata.fire) {
            dataCnt := dataCnt +1
          }
        }
        when(dataCnt === data_byteNum ) {
//          rec_data := 0
          dataCnt := 0
//          rec_en_cnt := 0
          io.rx_done := True
          io.rx.payload.last := True
          io.rx.byteNum := data_byteNum
          goto(rx_end)
        }
      }
    }


    val rx_end: State = new State {
      whenIsActive {
        when(io.mac_rxdata.valid) {
          io.mac_rxdata.ready := True
        }.otherwise {
          io.mac_rxdata.ready := False
          goto(idle)
        }
      }
    }
  }
}
 */
package udp_master

import spinal.core._
import spinal.lib._
import spinal.lib.fsm.{EntryPoint, State, StateMachine}

case class UdpRxGenerics(
    busWidth: Int, //UDP数据位宽
    desPort: Int //目标端口号 16bit
)

object UdpRxConstant {
  val UDP_DATA_WIDTH = 8
  val BYTE_NUM_WIDTH = 16
  val CNT_WIDTH = 6
  val PORT_WIDTH = 16
}

case class UdpRx(udpGenerics: UdpRxGenerics) extends Component {
  val io = new Bundle {
    val dataIn =
      slave Stream (Fragment(Bits(UdpRxConstant.UDP_DATA_WIDTH bits)))
    val dataOut = master Stream (Fragment(Bits(udpGenerics.busWidth bits)))
    val rxDone = out Bool ()
    val byteNum = out UInt (UdpRxConstant.BYTE_NUM_WIDTH bits)
    val srcPort = out Bits (UdpRxConstant.PORT_WIDTH bits)
  }

  val cnt = Reg(UInt(UdpRxConstant.CNT_WIDTH bits)) init (0)
  val udpByteNum = Reg(UInt(UdpRxConstant.BYTE_NUM_WIDTH bits))
  val dataByteNum = Reg(UInt(UdpRxConstant.BYTE_NUM_WIDTH bits))
  val desPort = Reg(Bits(UdpRxConstant.PORT_WIDTH bits))
  val srcPort = Reg(Bits(UdpRxConstant.PORT_WIDTH bits))

  io.dataIn.ready := False
  io.rxDone := False
  io.dataOut.fragment := 0
  io.dataOut.valid := False
  io.dataOut.last := False

  io.srcPort := srcPort
  io.byteNum := dataByteNum

  val dataCnt = Reg(UInt(UdpRxConstant.BYTE_NUM_WIDTH bits)) init (0)

  val fsm = new StateMachine {
    val idle: State = new State with EntryPoint {
      onEntry {
        udpByteNum := 0
        dataByteNum := 0
        desPort := 0
        srcPort := 0
      }
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataIn.ready := True
          cnt := cnt + 1
          when(cnt === 0) {
            srcPort(15 downto 8) := io.dataIn.fragment
          }.elsewhen(cnt === 1) {
            srcPort(7 downto 0) := io.dataIn.fragment
          }.elsewhen(cnt === 2) {
            desPort(15 downto 8) := io.dataIn.fragment
          }.elsewhen(cnt === 3) {
            desPort(7 downto 0) := io.dataIn.fragment
          }.elsewhen(cnt === 4) {
            udpByteNum(15 downto 8) := io.dataIn.fragment.asUInt
          }.elsewhen(cnt === 5) {
            udpByteNum(7 downto 0) := io.dataIn.fragment.asUInt
          }.elsewhen(cnt === 7) {
            when(desPort === udpGenerics.desPort) {
              dataByteNum := udpByteNum - 8
              cnt := 0
              goto(stRxData)
            }.otherwise {
              goto(stRxEnd)
            }
          }
        }
      }
    }

    val stRxData: State = new State {
      onEntry {
        dataCnt := 0
      }
      whenIsActive {
        when(io.dataIn.valid) {
          StreamFragmentWidthAdapter(input = io.dataIn, output = io.dataOut)
          when(io.dataIn.fire) {
            dataCnt := dataCnt + 1
          }
          when(dataCnt === dataByteNum - 1) {
            dataCnt := 0
            io.rxDone := True
            goto(stRxEnd)
          }
        }
      }
    }

    val stRxEnd: State = new State {
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataIn.ready := True
        }.otherwise {
          io.dataIn.ready := False
          goto(idle)
        }
      }
    }
  }
}
