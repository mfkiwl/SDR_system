import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math

SNR_bpsk = [3, 2, 1, 0]
err_bpsk =  [10**(-5.5), 10**(-5.5), 10**(-5.5), 10**(-5.5)]

SNR_qpsk = [3, 2, 1, 0]
err_qpsk = [10**(-5.5), 10**(-4.5), 10**(-3.8), 10**(-3.2)]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')

ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='y', colors='white')

fig.patch.set_facecolor('black')
fig.patch.set_alpha(1.0)

ax = fig.add_subplot(111)
ax.patch.set_facecolor('black')
ax.patch.set_alpha(1.0)

plt.plot(SNR_bpsk, err_bpsk, '.-')

plt.plot(SNR_qpsk, err_qpsk, '.-')

plt.legend(['BPSK','QPSK'], loc=1)

plt.yscale('log')
plt.xlabel('SNR[dB]')
plt.ylabel('Bit_err')

plt.show()
