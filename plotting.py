import matplotlib.pyplot as plt

def plot_fft(xf, fft_data, phase_delay):

    plt.clf()

    plt.plot(xf, fft_data)

    plt.xlabel("Frequency (MHz)")

    plt.ylabel("Amplitude (dBFS)")

    plt.title("Beamforming FFT")

    plt.text(-1,-10,f"Phase = {phase_delay}°")

    plt.ylim(-100,0)

    plt.draw()

    plt.pause(0.05)