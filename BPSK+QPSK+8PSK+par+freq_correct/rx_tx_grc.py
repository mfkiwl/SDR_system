#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rx Tx Grc
# Generated: Wed Jan 19 21:19:32 2022
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import numpy
import osmosdr
import sip
import sys
import threading
import time
from gnuradio import qtgui


class rx_tx_grc(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Rx Tx Grc")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Rx Tx Grc")
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

        self.settings = Qt.QSettings("GNU Radio", "rx_tx_grc")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.sps_TX = sps_TX = 40*2
        self.sps_RX = sps_RX = 4
        self.samp_rate = samp_rate = 76.8e3*20
        self.nfilts = nfilts = 32
        self.EBW = EBW = 350e-3
        self.sweep_time = sweep_time = 10
        self.steps = steps = 20
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps_RX), 0.35, 45*nfilts)
        self.psk_tx_sel = psk_tx_sel = 2
        self.nyquist_rate = nyquist_rate = samp_rate/2
        self.func_center_freq = func_center_freq = -30e3
        self.freqency_offset_tx = freqency_offset_tx = 0
        self.freqency_offset_rx = freqency_offset_rx = 0
        self.freq_offset_value = freq_offset_value = 60e3
        self.freq_dev_rx = freq_dev_rx = 0
        self.center_freq_min = center_freq_min = 10e3
        self.center_freq_max = center_freq_max = samp_rate/2
        self.center_freq = center_freq = 433e6
        self.bin_size = bin_size = 1024*4

        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts, 1, EBW, 5*sps_TX*nfilts)

        self.QPSK = QPSK = digital.constellation_rect(([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()

        self.PSK8 = PSK8 = digital.constellation_calcdist(([0.383+0.924j, 0.924+0.383j, 0.924-0.383j, 0.383-0.924j, -0.383-0.924j, -0.924-0.383j, -0.924+0.383j, -0.383+0.924j]), ([1, 0, 7, 6, 5, 4, 3, 2]), 8, 1).base()


        self.BPSK = BPSK = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()


        ##################################################
        # Blocks
        ##################################################
        self._psk_tx_sel_options = (2, 3, 5, )
        self._psk_tx_sel_labels = ('BPSK', 'QPSK', '8-PSK', )
        self._psk_tx_sel_group_box = Qt.QGroupBox('BPSK/QPSK/8-PSK')
        self._psk_tx_sel_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._psk_tx_sel_button_group = variable_chooser_button_group()
        self._psk_tx_sel_group_box.setLayout(self._psk_tx_sel_box)
        for i, label in enumerate(self._psk_tx_sel_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._psk_tx_sel_box.addWidget(radio_button)
        	self._psk_tx_sel_button_group.addButton(radio_button, i)
        self._psk_tx_sel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._psk_tx_sel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._psk_tx_sel_options.index(i)))
        self._psk_tx_sel_callback(self.psk_tx_sel)
        self._psk_tx_sel_button_group.buttonClicked[int].connect(
        	lambda i: self.set_psk_tx_sel(self._psk_tx_sel_options[i]))
        self.top_grid_layout.addWidget(self._psk_tx_sel_group_box, 10, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(10,11)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.probe_center_freq = blocks.probe_signal_vi(1)
        self._freqency_offset_tx_range = Range(-1.5e6/2, 1.5e6/2, 1, 0, 200)
        self._freqency_offset_tx_win = RangeWidget(self._freqency_offset_tx_range, self.set_freqency_offset_tx, "freqency_offset_tx", "counter_slider", float)
        self.top_grid_layout.addWidget(self._freqency_offset_tx_win, 0, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self._freqency_offset_rx_range = Range(-1.5e6/2, 1.5e6/2, 1, 0, 200)
        self._freqency_offset_rx_win = RangeWidget(self._freqency_offset_rx_range, self.set_freqency_offset_rx, "freqency_offset_rx", "counter_slider", float)
        self.top_grid_layout.addWidget(self._freqency_offset_rx_win, 1, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self._freq_dev_rx_range = Range(-20e3, 20e3, 1, 0, 200)
        self._freq_dev_rx_win = RangeWidget(self._freq_dev_rx_range, self.set_freq_dev_rx, "freq_dev_rx", "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_dev_rx_win, 7, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(7,8)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_time_source('gpsdo', 0)
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_freq-freq_offset_value-freqency_offset_rx, 0)
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
                decimation=int(sps_TX/sps_RX),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	False, #plotwaterfall
        	True, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_1_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_1_win = sip.wrapinstance(self.qtgui_sink_x_1_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_1_win, 4, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(4,5)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]

        self.qtgui_sink_x_1_1.enable_rf_freq(True)



        self.qtgui_sink_x_1_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_1_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_0_win, 2, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(2,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]

        self.qtgui_sink_x_1_0.enable_rf_freq(True)



        self.qtgui_sink_x_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/20, #bw
        	"", #name
        	True, #plotfreq
        	False, #plotwaterfall
        	True, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_win, 8, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(8,9)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]

        self.qtgui_sink_x_1.enable_rf_freq(True)



        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 3, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(3,4)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_1.set_update_time(0.05)
        self.qtgui_number_sink_1.set_title("Peak Rx Power")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_1.set_min(i, -70)
            self.qtgui_number_sink_1.set_max(i, 1)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(False)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_1_win, 6, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(6,7)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.05)
        self.qtgui_number_sink_0.set_title("Peak Rx Frequency")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -nyquist_rate)
            self.qtgui_number_sink_0.set_max(i, nyquist_rate)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 5, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(5,6)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
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
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_win, 9, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(9,10)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.osmosdr_sink_0_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '000000000000000017c467dc214531c3' )
        self.osmosdr_sink_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_0.set_center_freq(center_freq+freqency_offset_tx, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(10, 0)
        self.osmosdr_sink_0_0.set_if_gain(20, 0)
        self.osmosdr_sink_0_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(0, 0)


        def _func_center_freq_probe():
            while True:
                val = self.analog_sig_source_x_1.set_frequency(self.probe_center_freq.level()[0])
                try:
                    self.set_func_center_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (2))
        _func_center_freq_thread = threading.Thread(target=_func_center_freq_probe)
        _func_center_freq_thread.daemon = True
        _func_center_freq_thread.start()

        self.fft_vxx_0 = fft.fft_vcc(bin_size, True, (window.blackmanharris(4096)), True, 1)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
          constellation_points=4,
          mod_code="gray",
          differential=True,
          samples_per_symbol=20,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.digital_pfb_clock_sync_xxx_1 = digital.pfb_clock_sync_ccf(sps_RX, 6.28/400*2, (rrc_taps), nfilts, nfilts/2, 1.5, 1)
        self.digital_map_bb_0_0 = digital.map_bb((1, 0, 7, 6, 5, 4, 3, 2))
        self.digital_map_bb_0 = digital.map_bb((0,1,3,2))
        self.digital_fll_band_edge_cc_1 = digital.fll_band_edge_cc(sps_RX, EBW, 45, 0.02)
        self.digital_diff_decoder_bb_0_1 = digital.diff_decoder_bb(2)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(4)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(8)
        self.digital_costas_loop_cc_1_1 = digital.costas_loop_cc(10e-3, 8, False)
        self.digital_costas_loop_cc_1_0 = digital.costas_loop_cc(10e-3, 2, False)
        self.digital_costas_loop_cc_1 = digital.costas_loop_cc(10e-3, 4, False)
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
          constellation=BPSK,
          differential=True,
          samples_per_symbol=20,
          pre_diff_code=True,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=PSK8,
          differential=True,
          samples_per_symbol=20,
          pre_diff_code=True,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(QPSK)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(PSK8)
        self.digital_cma_equalizer_cc_0_0 = digital.cma_equalizer_cc(11, 1, 10e-3, 1)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(11, 1, 10e-3, 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(3)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_udp_sink_0_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 40868, 126, True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 40868, 126, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 40868, 126, True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, bin_size)
        self.blocks_short_to_float_1 = blocks.short_to_float(1, 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_short*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, 1, 0)
        self.blocks_multiply_xx_0_2_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_2_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_2_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_1 = blocks.multiply_const_ff(10)
        self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_ff(935.674e-9/4)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(samp_rate/bin_size)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vii((-5000, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.001/5, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((1.3, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.3, ))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, 0.001, 10000)
        self.blocks_max_xx_0 = blocks.max_ff(bin_size,1)
        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/ar/shared/konf/SDR_spi/tx_data', True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(bin_size)
        self.blocks_argmax_xx_0 = blocks.argmax_fs(bin_size)
        self.blocks_add_xx_1_0 = blocks.add_vcc(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-nyquist_rate, ))
        self.blks2_packet_encoder_0_1 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=1,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='',
        		pad_for_usrp=False,
        	),
        	payload_length=16,
        )
        self.blks2_packet_encoder_0_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=4,
        		bits_per_symbol=3,
        		preamble='',
        		access_code='',
        		pad_for_usrp=False,
        	),
        	payload_length=16,
        )
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=1,
        		bits_per_symbol=2,
        		preamble='',
        		access_code='',
        		pad_for_usrp=False,
        	),
        	payload_length=16,
        )
        self.blks2_packet_decoder_0_1 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0_1.recv_pkt(ok, payload),
        	),
        )
        self.blks2_packet_decoder_0_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0_0.recv_pkt(ok, payload),
        	),
        )
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -freq_offset_value+freq_dev_rx, 1, 0)
        self.analog_pwr_squelch_xx_1 = analog.pwr_squelch_cc(-20, 0.01, 0, True)
        self.analog_feedforward_agc_cc_1 = analog.feedforward_agc_cc(512, 1.0)
        self.analog_const_source_x_0_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 15%psk_tx_sel)
        self.analog_const_source_x_0_0_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, (20%psk_tx_sel)/2)
        self.analog_const_source_x_0_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 6%psk_tx_sel)
        self.analog_const_source_x_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 6%psk_tx_sel)
        self.analog_const_source_x_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, (20%psk_tx_sel)/2)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 15%psk_tx_sel)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_multiply_xx_0_2, 1))
        self.connect((self.analog_const_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_2_0, 1))
        self.connect((self.analog_const_source_x_0_0_0_0, 0), (self.blocks_multiply_xx_0_2_0_0, 1))
        self.connect((self.analog_const_source_x_0_0_1, 0), (self.blocks_multiply_xx_0_2_1, 1))
        self.connect((self.analog_const_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.analog_feedforward_agc_cc_1, 0), (self.digital_pfb_clock_sync_xxx_1, 0))
        self.connect((self.analog_pwr_squelch_xx_1, 0), (self.digital_fll_band_edge_cc_1, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.qtgui_sink_x_1_1, 0))
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_udp_sink_0_0_0, 0))
        self.connect((self.blks2_packet_decoder_0_0, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.blks2_packet_decoder_0_1, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blks2_packet_encoder_0_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blks2_packet_encoder_0_1, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_add_xx_1_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_argmax_xx_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_argmax_xx_0, 0), (self.blocks_short_to_float_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_argmax_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0_1, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_int_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.probe_center_freq, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.qtgui_sink_x_1_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_add_xx_1_0, 0))
        self.connect((self.blocks_multiply_xx_0_2, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_multiply_xx_0_2_0, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_multiply_xx_0_2_0_0, 0), (self.blocks_add_xx_1_0, 2))
        self.connect((self.blocks_multiply_xx_0_2_1, 0), (self.blocks_add_xx_1_0, 1))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_multiply_const_xx_1, 0))
        self.connect((self.blocks_short_to_float_1, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blks2_packet_decoder_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0_1, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_xx_0_2_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.blocks_multiply_xx_0_2_1, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_costas_loop_cc_1_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_costas_loop_cc_1_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.digital_costas_loop_cc_1_1, 0), (self.blocks_multiply_xx_0_2_0_0, 0))
        self.connect((self.digital_costas_loop_cc_1_1, 0), (self.digital_cma_equalizer_cc_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_1, 0), (self.blks2_packet_decoder_0_1, 0))
        self.connect((self.digital_fll_band_edge_cc_1, 0), (self.analog_feedforward_agc_cc_1, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_map_bb_0_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_1, 0), (self.digital_costas_loop_cc_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_1, 0), (self.digital_costas_loop_cc_1_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_1, 0), (self.digital_costas_loop_cc_1_1, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_xx_0_2, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_pwr_squelch_xx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_multiply_xx_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rx_tx_grc")
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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_nyquist_rate(self.samp_rate/2)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_1_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate/20)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.osmosdr_sink_0_0.set_sample_rate(self.samp_rate)
        self.set_center_freq_max(self.samp_rate/2)
        self.blocks_multiply_const_xx_0.set_k(self.samp_rate/self.bin_size)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps_RX), 0.35, 45*self.nfilts))

    def get_EBW(self):
        return self.EBW

    def set_EBW(self, EBW):
        self.EBW = EBW

    def get_sweep_time(self):
        return self.sweep_time

    def set_sweep_time(self, sweep_time):
        self.sweep_time = sweep_time

    def get_steps(self):
        return self.steps

    def set_steps(self, steps):
        self.steps = steps

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_1.update_taps((self.rrc_taps))

    def get_psk_tx_sel(self):
        return self.psk_tx_sel

    def set_psk_tx_sel(self, psk_tx_sel):
        self.psk_tx_sel = psk_tx_sel
        self._psk_tx_sel_callback(self.psk_tx_sel)
        self.analog_const_source_x_0_1.set_offset(15%self.psk_tx_sel)
        self.analog_const_source_x_0_0_1.set_offset((20%self.psk_tx_sel)/2)
        self.analog_const_source_x_0_0_0_0.set_offset(6%self.psk_tx_sel)
        self.analog_const_source_x_0_0_0.set_offset(6%self.psk_tx_sel)
        self.analog_const_source_x_0_0.set_offset((20%self.psk_tx_sel)/2)
        self.analog_const_source_x_0.set_offset(15%self.psk_tx_sel)

    def get_nyquist_rate(self):
        return self.nyquist_rate

    def set_nyquist_rate(self, nyquist_rate):
        self.nyquist_rate = nyquist_rate
        self.blocks_add_const_vxx_0.set_k((-self.nyquist_rate, ))

    def get_func_center_freq(self):
        return self.func_center_freq

    def set_func_center_freq(self, func_center_freq):
        self.func_center_freq = func_center_freq

    def get_freqency_offset_tx(self):
        return self.freqency_offset_tx

    def set_freqency_offset_tx(self, freqency_offset_tx):
        self.freqency_offset_tx = freqency_offset_tx
        self.osmosdr_sink_0_0.set_center_freq(self.center_freq+self.freqency_offset_tx, 0)

    def get_freqency_offset_rx(self):
        return self.freqency_offset_rx

    def set_freqency_offset_rx(self, freqency_offset_rx):
        self.freqency_offset_rx = freqency_offset_rx
        self.rtlsdr_source_0.set_center_freq(self.center_freq-self.freq_offset_value-self.freqency_offset_rx, 0)

    def get_freq_offset_value(self):
        return self.freq_offset_value

    def set_freq_offset_value(self, freq_offset_value):
        self.freq_offset_value = freq_offset_value
        self.rtlsdr_source_0.set_center_freq(self.center_freq-self.freq_offset_value-self.freqency_offset_rx, 0)
        self.analog_sig_source_x_0_0_0.set_frequency(-self.freq_offset_value+self.freq_dev_rx)

    def get_freq_dev_rx(self):
        return self.freq_dev_rx

    def set_freq_dev_rx(self, freq_dev_rx):
        self.freq_dev_rx = freq_dev_rx
        self.analog_sig_source_x_0_0_0.set_frequency(-self.freq_offset_value+self.freq_dev_rx)

    def get_center_freq_min(self):
        return self.center_freq_min

    def set_center_freq_min(self, center_freq_min):
        self.center_freq_min = center_freq_min

    def get_center_freq_max(self):
        return self.center_freq_max

    def set_center_freq_max(self, center_freq_max):
        self.center_freq_max = center_freq_max

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.rtlsdr_source_0.set_center_freq(self.center_freq-self.freq_offset_value-self.freqency_offset_rx, 0)
        self.osmosdr_sink_0_0.set_center_freq(self.center_freq+self.freqency_offset_tx, 0)

    def get_bin_size(self):
        return self.bin_size

    def set_bin_size(self, bin_size):
        self.bin_size = bin_size
        self.blocks_multiply_const_xx_0.set_k(self.samp_rate/self.bin_size)

    def get_RRC_filter_taps(self):
        return self.RRC_filter_taps

    def set_RRC_filter_taps(self, RRC_filter_taps):
        self.RRC_filter_taps = RRC_filter_taps

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK

    def get_PSK8(self):
        return self.PSK8

    def set_PSK8(self, PSK8):
        self.PSK8 = PSK8

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK


def main(top_block_cls=rx_tx_grc, options=None):

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
