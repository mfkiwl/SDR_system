import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math

# this part came from pulse shaping exercise
num_symbols = 100
sps = 8
fs = 1e6

bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0's
pulse_train = np.array([])
for bit in bits:
    pulse = np.zeros(sps)
    pulse[0] = bit*2-1 # set the first value to either a 1 or -1
    pulse_train = np.concatenate((pulse_train, pulse)) # add the 8 samples to the signal


# Create our raised-cosine filter
num_taps = 101
beta = 0.35
Ts = 8 # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
t = np.arange(-51, 52) # remember it's not inclusive of final number
h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)

# plot the frequency response
H = np.abs(np.fft.fft(h, 1024)) # take the 1024-point FFT and magnitude
H = np.fft.fftshift(H) # make 0 Hz in the center
f = np.linspace(-fs/2, fs/2, len(H))

# Filter our signal, in order to apply the pulse shaping
samples = np.convolve(pulse_train, h)

plt.figure(0)
# Plot the old vs new
plt.subplot(211)

plt.title("Символы")
plt.plot(np.real(pulse_train), '.-')
#plt.plot(np.imag(bits), '-')
#plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.subplot(212)

plt.title("Отфильтрованный сигнал")
plt.plot(np.real(samples), '.-')
#plt.plot(np.imag(bits), '-')
#plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.figure(1)
# Plot the old vs new
plt.subplot(211)

plt.title("Коэффициенты фильтра")
plt.plot(np.real(h), '.')
#plt.plot(np.imag(bits), '-')
#plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('h')

plt.subplot(212)

plt.title("Амплитудно-частотная характеристика")
plt.plot(f,np.real(H), '-')
#plt.plot(np.real(H), '-')
#plt.plot(np.imag(bits), '-')
#plt.legend(['real','imag'], loc=1)
plt.xlabel('f [Гц]')
plt.ylabel('H')

# Create and apply fractional delay filter
delay = 0.4 # fractional delay, in samples
N = 21 # number of taps
n = np.arange(-N//2, N//2) # ...-3,-2,-1,0,1,2,3...
h = np.sinc(n - delay) # calc filter taps
h *= np.hamming(N) # window the filter to make sure it decays to 0 on both sides
h /= np.sum(h) # normalize to get unity gain, we don't want to change the amplitude/power
samples_delay = np.convolve(samples, h) # apply filter

# apply a freq offset
fs = 1e6 # assume our sample rate is 1 MHz
fo = 1300 # simulate freq offset
Ts = 1/fs # calc sample period
t = np.arange(0, Ts*len(samples_delay), Ts) # create time vector
samples_df = samples_delay * np.exp(1j*2*np.pi*fo*t) # perform freq shift

plt.figure(2)
plt.title("Сдвиг по Частоте")
plt.plot(t, np.real(samples_df), '-')
plt.plot(t, np.imag(samples_df), '-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('t [c]')
plt.ylabel('S')

psd = np.fft.fftshift(np.abs(np.fft.fft(samples_df**2)))
f = np.linspace(-fs/2, fs/2, len(psd))

max_freq = f[np.argmax(psd)]

print(max_freq)

samples_interpolated = signal.resample_poly(samples_df, 16, 1)

plt.figure(3)
# Plot the old vs new
plt.subplot(211)

plt.title("Отсчёты")
plt.plot(np.real(samples_df), '.-')
plt.plot(np.imag(samples_df), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.subplot(212)

plt.title("После интерполяции")
plt.plot(np.real(samples_interpolated), '.-')
plt.plot(np.imag(samples_interpolated), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

mu = 0 # initial estimate of phase of sample
out = np.zeros(len(samples) + 10, dtype=np.complex)
out_rail = np.zeros(len(samples) + 10, dtype=np.complex) # stores values, each iteration we need the previous 2 values plus current value
i_in = 0 # input samples index
i_out = 2 # output index (let first two outputs be 0)
while i_out < len(samples) and i_in < len(samples):
    #out[i_out] = samples[i_in + int(mu)] # grab what we think is the "best" sample
    out[i_out] = samples_interpolated[i_in*16 + int(mu*16)]
    out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0)
    x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
    y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
    mm_val = np.real(y - x)
    mu += sps + 0.1*mm_val
    i_in += int(np.floor(mu)) # round down to nearest int since we are using it as an index
    mu = mu - np.floor(mu) # remove the integer part of mu
    i_out += 1 # increment output index
out = out[2:i_out] # remove the first two, and anything after i_out (that was never filled out)
samples_ts = out # only include this line if you want to connect this code snippet with the Costas Loop later on

plt.figure(4)

plt.subplot(211)

plt.title("Отсчёты")
plt.plot(np.real(samples_interpolated), '.-')
plt.plot(np.imag(samples_interpolated), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.subplot(212)

plt.title("Синхронизация по фазе + прореживание")
plt.plot(np.real(samples_ts), '.-')
plt.plot(np.imag(samples_ts), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')



N = len(samples_ts)
phase = 0
freq = 0
# These next two params is what to adjust, to make the feedback loop faster or slower (which impacts stability)
alpha = 0.132
beta = 0.00932
out = np.zeros(N, dtype=np.complex)
freq_log = []
for i in range(N):
    out[i] = samples_ts[i] * np.exp(-1j*phase) # adjust the input sample by the inverse of the estimated phase offset
    error = np.real(out[i]) * np.imag(out[i]) # This is the error formula for 2nd order Costas Loop (e.g. for BPSK)

    # Advance the loop (recalc phase and freq offset)
    freq += (beta * error)
    freq_log.append(freq * fs / (2*np.pi)) # convert from angular velocity to Hz for logging
    phase += freq + (alpha * error)

    # Optional: Adjust phase so its always between 0 and 2pi, recall that phase wraps around every 2pi
    while phase >= 2*np.pi:
        phase -= 2*np.pi
    while phase < 0:
        phase += 2*np.pi

samples_fs = out
# Plot freq over time to see how long it takes to hit the right offset
plt.figure(5)
plt.title("Синхронизация по частоте")
plt.plot(freq_log,'.-')
plt.xlabel('n')
plt.ylabel('f')

plt.figure(6)

plt.subplot(211)

plt.title("Символы")
plt.plot(np.real(pulse_train), '.-')
plt.plot(np.imag(pulse_train), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.subplot(212)

plt.title("Восстановленные символы")
plt.plot(np.real(samples_fs), '.-')
plt.plot(np.imag(samples_fs), '.-')
plt.legend(['real','imag'], loc=1)
plt.xlabel('n')
plt.ylabel('S')

plt.show()

k=int(num_symbols/2)

plt.figure(7)
plt.title("Созвездие")
plt.plot(np.real(samples_fs[k:num_symbols:1]), np.imag(samples_fs[k:num_symbols:1]), '.')
plt.axis([-1.3, 1.3, -1.3, 1.3])
plt.xlabel('I')
plt.ylabel('Q')

plt.figure(8)
plt.subplot(121)
plt.title("Созвездие без синхронизации")
plt.plot(np.real(samples_df[k:num_symbols:1]), np.imag(samples_df[k:num_symbols:1]), '.')
plt.axis([-1.3, 1.3, -1.3, 1.3])
plt.xlabel('I')
plt.ylabel('Q')

plt.subplot(122)
plt.title("Созвездие с синхронизацией")
plt.plot(np.real(samples_fs[k:num_symbols:1]), np.imag(samples_fs[k:num_symbols:1]), '.')
plt.axis([-1.3, 1.3, -1.3, 1.3])
plt.xlabel('I')
plt.ylabel('Q')

plt.show()
