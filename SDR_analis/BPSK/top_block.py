#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Dec 27 18:57:08 2021
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import numpy
import osmosdr
import sip
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.sps_TX = sps_TX = 40*2
        self.sps_RX = sps_RX = 4
        self.nfilts = nfilts = 32
        self.EBW = EBW = 350e-3
        self.samp_rate = samp_rate = 76.8e3*20
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps_RX), 0.35, 45*nfilts)
        self.freq_offset_value = freq_offset_value = 30e3
        self.freq_dev = freq_dev = 0
        self.center_freq = center_freq = 433e6

        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts, 1, EBW, 5*sps_TX*nfilts)


        self.BPSK = BPSK = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()


        ##################################################
        # Blocks
        ##################################################
        self._freq_dev_range = Range(-20e3, 20e3, 1, 0, 200)
        self._freq_dev_win = RangeWidget(self._freq_dev_range, self.set_freq_dev, "freq_dev", "counter_slider", float)
        self.top_layout.addWidget(self._freq_dev_win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_time_source('gpsdo', 0)
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_freq+freq_dev-9007, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(40, 0)
        self.rtlsdr_source_0.set_if_gain(0, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(sps_TX/sps_RX)/20,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/10, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_1_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_1_0_win)

        self.qtgui_sink_x_1_0.enable_rf_freq(False)



        self.qtgui_sink_x_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/10, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_1_win)

        self.qtgui_sink_x_1.enable_rf_freq(False)



        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_1_win)
        self.digital_pfb_clock_sync_xxx_1 = digital.pfb_clock_sync_ccf(sps_RX, 6.28/400*2, (rrc_taps), nfilts, nfilts/2, 1.5, 1)
        self.digital_fll_band_edge_cc_1 = digital.fll_band_edge_cc(sps_RX, EBW, 45, 0.02)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_1 = digital.costas_loop_cc(10e-3, 2, False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 40868, 126, True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.3, ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -freq_offset_value, 1, 0)
        self.analog_pwr_squelch_xx_1 = analog.pwr_squelch_cc(-20, 0.01, 0, True)
        self.analog_feedforward_agc_cc_1 = analog.feedforward_agc_cc(512, 1.0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_1, 0), (self.digital_pfb_clock_sync_xxx_1, 0))
        self.connect((self.analog_pwr_squelch_xx_1, 0), (self.digital_fll_band_edge_cc_1, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_sink_x_1_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_fll_band_edge_cc_1, 0), (self.analog_feedforward_agc_cc_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_1, 0), (self.digital_costas_loop_cc_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_pwr_squelch_xx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_multiply_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps_TX(self):
        return self.sps_TX

    def set_sps_TX(self, sps_TX):
        self.sps_TX = sps_TX

    def get_sps_RX(self):
        return self.sps_RX

    def set_sps_RX(self, sps_RX):
        self.sps_RX = sps_RX
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps_RX), 0.35, 45*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps_RX), 0.35, 45*self.nfilts))

    def get_EBW(self):
        return self.EBW

    def set_EBW(self, EBW):
        self.EBW = EBW

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_1_0.set_frequency_range(0, self.samp_rate/10)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate/10)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_1.update_taps((self.rrc_taps))

    def get_freq_offset_value(self):
        return self.freq_offset_value

    def set_freq_offset_value(self, freq_offset_value):
        self.freq_offset_value = freq_offset_value
        self.analog_sig_source_x_0_0.set_frequency(-self.freq_offset_value)

    def get_freq_dev(self):
        return self.freq_dev

    def set_freq_dev(self, freq_dev):
        self.freq_dev = freq_dev
        self.rtlsdr_source_0.set_center_freq(self.center_freq+self.freq_dev-9007, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.rtlsdr_source_0.set_center_freq(self.center_freq+self.freq_dev-9007, 0)

    def get_RRC_filter_taps(self):
        return self.RRC_filter_taps

    def set_RRC_filter_taps(self, RRC_filter_taps):
        self.RRC_filter_taps = RRC_filter_taps

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
