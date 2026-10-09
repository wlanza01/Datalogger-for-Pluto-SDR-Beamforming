import adi
import experiment_config as cfg


def configure_pluto():

    sdr = adi.ad9361(uri=cfg.SDR_IP)

    sdr.rx_enabled_channels = [0, 1]

    sdr.sample_rate = cfg.SAMPLE_RATE

    sdr.rx_rf_bandwidth = cfg.RX_RF_BANDWIDTH

    sdr.rx_lo = cfg.RX_LO

    sdr.gain_control_mode = cfg.RX_GAIN_MODE

    sdr.rx_hardwaregain_chan0 = cfg.RX_GAIN_CH0

    sdr.rx_hardwaregain_chan1 = cfg.RX_GAIN_CH1

    sdr.rx_buffer_size = cfg.NUM_SAMPLES

    sdr._rxadc.set_kernel_buffers_count(1)

    sdr.tx_rf_bandwidth = cfg.TX_RF_BANDWIDTH

    sdr.tx_lo = cfg.TX_LO

    sdr.tx_cyclic_buffer = True

    sdr.tx_hardwaregain_chan0 = cfg.TX_GAIN_CH0

    sdr.tx_hardwaregain_chan1 = cfg.TX_GAIN_CH1

    sdr.tx_buffer_size = 2**18

    return sdr