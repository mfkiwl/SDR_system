#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import numpy
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

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sps_TX = sps_TX = 40*2
        self.sps_RX = sps_RX = 4
        self.nfilts = nfilts = 32
        self.EBW = EBW = 350e-3
        self.time_offset_0 = time_offset_0 = 1.00
        self.taps = taps = [1.0 + 0.0j, ]
        self.samp_rate = samp_rate = 76.8e3*20
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps_RX), 0.35, 45*nfilts)
        self.noise_volt_0 = noise_volt_0 = 0.0001
        self.len_vect = len_vect = 1024
        self.freq_offset_value = freq_offset_value = 30e3
        self.freq_offset_0 = freq_offset_0 = 0
        self.freq_dev = freq_dev = 0
        self.delay = delay = 147
        self.center_freq = center_freq = 433e6
        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts,1, EBW, 5*sps_TX*nfilts)
        self.BPSK = BPSK = digital.constellation_calcdist([-1, 1], [0, 1],
        4, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self._time_offset_0_range = Range(0.999, 1.001, 0.0001, 1.00, 200)
        self._time_offset_0_win = RangeWidget(self._time_offset_0_range, self.set_time_offset_0, 'Timing Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._time_offset_0_win, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_volt_0_range = Range(0, 1, 0.01, 0.0001, 200)
        self._noise_volt_0_win = RangeWidget(self._noise_volt_0_range, self.set_noise_volt_0, 'Noise Voltage', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_volt_0_win, 14, 0, 1, 1)
        for r in range(14, 15):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_0_range = Range(-0.1, 0.1, 0.001, 0, 200)
        self._freq_offset_0_win = RangeWidget(self._freq_offset_0_range, self.set_freq_offset_0, 'Frequency Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_0_win, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._delay_range = Range(0, 400, 1, 147, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, 'Delay', "counter_slider", float)
        self.top_grid_layout.addWidget(self._delay_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(sps_TX/sps_RX),
                taps=None,
                fractional_bw=None)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            512, #size
            samp_rate/80, #samp_rate
            '', #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Rx Bits', 'Diff', 'Tx Bits', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_1_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_1_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/20, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_win, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Error")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -10)
            self.qtgui_number_sink_0.set_max(i, 0)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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

        for i in range(1):
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
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_win, 16, 0, 1, 1)
        for r in range(16, 17):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_dev_range = Range(-20e3, 20e3, 1, 0, 200)
        self._freq_dev_win = RangeWidget(self._freq_dev_range, self.set_freq_dev, 'freq_dev', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_dev_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_pfb_clock_sync_xxx_1 = digital.pfb_clock_sync_ccf(sps_RX, 6.28/400*2, rrc_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_fll_band_edge_cc_1 = digital.fll_band_edge_cc(sps_RX, EBW, 45, 0.02)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_1 = digital.costas_loop_cc(10e-3, 2, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=BPSK,
            differential=True,
            samples_per_symbol=sps_TX,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_binary_slicer_fb_0_0_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt_0,
            frequency_offset=freq_offset_0,
            epsilon=time_offset_0,
            taps=taps,
            noise_seed=0,
            block_tags=False)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_udp_sink_1_0_0 = blocks.udp_sink(gr.sizeof_char*len_vect, '127.0.0.1', 40871, 1472, False)
        self.blocks_udp_sink_1_0 = blocks.udp_sink(gr.sizeof_char*len_vect, '127.0.0.1', 40870, 1472, False)
        self.blocks_udp_sink_1 = blocks.udp_sink(gr.sizeof_char*len_vect*2, '127.0.0.1', 40869, 1472*2, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate/sps_TX,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_streams_to_vector_1 = blocks.streams_to_vector(gr.sizeof_char*len_vect, 2)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_char*1, len_vect)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_char*1, len_vect)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_char*1, len_vect)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, len_vect)
        self.blocks_pack_k_bits_bb_0_1 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1.3)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/artiom/shared/konf/SDR_analis/data.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_char*1, int(delay))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, int(delay))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0_0_0 = blocks.add_const_ff(-1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(-1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.analog_pwr_squelch_xx_1 = analog.pwr_squelch_cc(-20, 0.01, 0, True)
        self.analog_feedforward_agc_cc_1 = analog.feedforward_agc_cc(512, 1.0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_1, 0), (self.digital_pfb_clock_sync_xxx_1, 0))
        self.connect((self.analog_pwr_squelch_xx_1, 0), (self.digital_fll_band_edge_cc_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_binary_slicer_fb_0_0_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0_0, 0), (self.digital_binary_slicer_fb_0_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_const_vxx_0_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0_0, 2))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_pack_k_bits_bb_0_1, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_streams_to_vector_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_streams_to_vector_1, 1))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_udp_sink_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_udp_sink_1_0_0, 0))
        self.connect((self.blocks_streams_to_vector_1, 0), (self.blocks_udp_sink_1, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_sink_x_1_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_pack_k_bits_bb_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.digital_fll_band_edge_cc_1, 0), (self.analog_feedforward_agc_cc_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_1, 0), (self.digital_costas_loop_cc_1, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_pwr_squelch_xx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_sink_x_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps_TX(self):
        return self.sps_TX

    def set_sps_TX(self, sps_TX):
        self.sps_TX = sps_TX
        self.blocks_throttle_0.set_sample_rate(self.samp_rate/self.sps_TX)

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

    def get_time_offset_0(self):
        return self.time_offset_0

    def set_time_offset_0(self, time_offset_0):
        self.time_offset_0 = time_offset_0
        self.channels_channel_model_0.set_timing_offset(self.time_offset_0)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.channels_channel_model_0.set_taps(self.taps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate/self.sps_TX)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate/20)
        self.qtgui_sink_x_1_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate/80)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_1.update_taps(self.rrc_taps)

    def get_noise_volt_0(self):
        return self.noise_volt_0

    def set_noise_volt_0(self, noise_volt_0):
        self.noise_volt_0 = noise_volt_0
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt_0)

    def get_len_vect(self):
        return self.len_vect

    def set_len_vect(self, len_vect):
        self.len_vect = len_vect

    def get_freq_offset_value(self):
        return self.freq_offset_value

    def set_freq_offset_value(self, freq_offset_value):
        self.freq_offset_value = freq_offset_value

    def get_freq_offset_0(self):
        return self.freq_offset_0

    def set_freq_offset_0(self, freq_offset_0):
        self.freq_offset_0 = freq_offset_0
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset_0)

    def get_freq_dev(self):
        return self.freq_dev

    def set_freq_dev(self, freq_dev):
        self.freq_dev = freq_dev

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(int(self.delay))
        self.blocks_delay_0_0.set_dly(int(self.delay))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

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

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
