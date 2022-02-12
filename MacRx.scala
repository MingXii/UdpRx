package udp_master

import spinal.core._
import spinal.lib._
import spinal.lib.fsm.{EntryPoint, State, StateMachine}

case class MacRxGenerics(
    desMac: Long //目的MAC地址 48bit
)

object MacRxConstant {
  val DATA_WIDTH = 8
  val CNT_WIDTH = 6
  val PREAMBLE = 0x55 //8bit
  val SFD = 0xd5
  val ETH_TYPE = 0x0800
  val ETH_TYPE_WIDTH = 16
  val DES_MAC_WIDTH = 48
}

case class MacRx(macGenerics: MacRxGenerics) extends Component {
  val io = new Bundle {
    val dataIn = slave Stream (Fragment(Bits(MacRxConstant.DATA_WIDTH bits)))
    val dataOut = master Stream (Fragment(Bits(MacRxConstant.DATA_WIDTH bits)))
  }

  io.dataIn.ready := False
  io.dataOut.valid := False
  io.dataOut.fragment := 0
  io.dataOut.last := False

  val cnt = Reg(UInt(MacRxConstant.CNT_WIDTH bits)) init (0)
  val desMacReg = Reg(Bits(MacRxConstant.DES_MAC_WIDTH bits))
  val ethTypeReg = Reg(Bits(MacRxConstant.ETH_TYPE_WIDTH bits))

  val fsm = new StateMachine {
    val idle: State = new State with EntryPoint {
      whenIsActive {
        when(
          io.dataIn.valid
        ) {
          io.dataIn.ready := True
          when(io.dataIn.fragment === MacRxConstant.PREAMBLE) {
            goto(stPreamble)
          }
        }
      }
    }

    val stPreamble: State = new State {
      onEntry {
        cnt := 0
      }
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataIn.ready := True
          cnt := cnt + 1
          when(cnt < 6 && io.dataIn.fragment =/= MacRxConstant.PREAMBLE) {
            goto(stRxEnd)
          }.elsewhen(cnt === 6) {
            cnt := 0
            when(io.dataIn.fragment === MacRxConstant.SFD) {
              goto(stEthHead)
            }.otherwise {
              goto(stRxEnd)
            }
          }
        }
      }
    }

    val stEthHead: State = new State {
      onEntry {
        desMacReg := 0
        ethTypeReg := 0
      }
      whenIsActive {
        when(io.dataIn.valid) {
          io.dataIn.ready := True
          cnt := cnt + 1
          when(cnt < 6) {
            desMacReg := desMacReg(39 downto 0) ## io.dataIn.fragment
          }.elsewhen(cnt === 12) {
            ethTypeReg(15 downto 8) := io.dataIn.fragment
          }.elsewhen(cnt === 13) {
            ethTypeReg(7 downto 0) := io.dataIn.fragment
            cnt := 0
            when(
              (desMacReg === macGenerics.desMac || desMacReg === 0xffffffffffffL) && ((ethTypeReg(
                15 downto 8
              ) ## io.dataIn.fragment) === MacRxConstant.ETH_TYPE)
            ) {
              goto(stMac2ip)
            }.otherwise {
              goto(stRxEnd)
            }
          }
        }
      }
    }

    val stMac2ip: State = new State {
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
