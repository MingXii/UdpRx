package udp_master

import spinal.core._
import spinal.lib._
import spinal.lib.fsm.{EntryPoint, State, StateMachine}

case class IpRxGenerics(
    desIp: Int //目的IP地址 32bit
)

object IpRxConstant {
  val DATA_WIDTH = 8 //数据位宽
  val DES_IP_WIDTH = 32 //目的IP地址位宽
  val IP_HEAD_WIDTH = 6 //IP首部长度寄存器位宽
  val CNT_WIDTH = 5 //数据计数器位宽
}

case class IpRx(ipGenerics: IpRxGenerics) extends Component {
  val io = new Bundle {
    val dataIn = slave Stream (Fragment(Bits(IpRxConstant.DATA_WIDTH bits)))
    val dataOut = master Stream (Fragment(Bits(IpRxConstant.DATA_WIDTH bits)))
  }

  io.dataIn.ready := False
  io.dataOut.valid := False
  io.dataOut.fragment := 0
  io.dataOut.last := False

  val cnt = Reg(UInt(IpRxConstant.CNT_WIDTH bits)) init (0)
  val ipHeadByteNum = Reg(Bits(IpRxConstant.IP_HEAD_WIDTH bits))
  val desIp = Reg(Bits(IpRxConstant.DES_IP_WIDTH bits))

  val fsm = new StateMachine {
    val idle: State = new State with EntryPoint {
      onEntry {
        ipHeadByteNum := 0
        desIp := 0
      }
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataIn.ready := True
          cnt := cnt + 1
          when(cnt === 0) {
            ipHeadByteNum := (io.dataIn.fragment(3 downto 0) << 2)
          }.elsewhen(cnt >= 16 && cnt <= 18) {
            desIp := desIp(23 downto 0) ## io.dataIn.fragment
          } elsewhen (cnt === 19) {
            desIp := desIp(23 downto 0) ## io.dataIn.fragment
            when(
              (desIp(
                23 downto 0
              ) ## io.dataIn.fragment) === ipGenerics.desIp
            ) {
              when(cnt === (ipHeadByteNum.asUInt - 1)) {
                goto(stIp2udp)
                cnt := 0
              }
            }.otherwise {
              goto(stRxEnd)
              cnt := 0
            }
          }
        }
      }
    }

    val stIp2udp: State = new State {
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataOut << io.dataIn
        }.otherwise {
          goto(stRxEnd)
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
