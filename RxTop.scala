package udp_master

import spinal.core._
import spinal.lib._

case class RxTop(
    macGenerics: MacRxGenerics,
    ipGenerics: IpRxGenerics,
    udpGenerics: UdpRxGenerics
) extends Component {
  val io = new Bundle {
    val dataIn = slave Stream (Fragment(Bits(MacRxConstant.DATA_WIDTH bits)))
    val dataOut = master Stream (Fragment(Bits(udpGenerics.busWidth bits)))
    val rxDone = out Bool ()
    val byteNum = out UInt (UdpRxConstant.BYTE_NUM_WIDTH bits)
    val srcPort = out Bits (UdpRxConstant.PORT_WIDTH bits)
  }

  val macRx = new MacRx(macGenerics)
  val ipRx = new IpRx(ipGenerics)
  val udpRx = new UdpRx(udpGenerics)

  macRx.io.dataIn << io.dataIn
  ipRx.io.dataIn << macRx.io.dataOut
  udpRx.io.dataIn << ipRx.io.dataOut
  io.rxDone := udpRx.io.rxDone
  io.byteNum := udpRx.io.byteNum
  io.srcPort := udpRx.io.srcPort
  io.dataOut << udpRx.io.dataOut
}
