"""
signal_processing.py

Digital signal processing functions used throughout the
beamforming project.
"""

import numpy as np

############################################################
# FFT Processing
############################################################

def dbfs(raw_data):
    """
    Convert IQ samples into an FFT magnitude spectrum (dBFS).
    """

    num_samples = len(raw_data)

    window = np.hamming(num_samples)

    windowed = raw_data * window

    fft = np.fft.fft(windowed) / np.sum(window)

    fft_shifted = np.fft.fftshift(fft)

    fft_dbfs = 20 * np.log10(np.abs(fft_shifted) / (2**11))

    return fft_dbfs


############################################################
# Beamforming
############################################################

def apply_phase_delay(rx_channel, phase_deg):
    """
    Apply a phase delay to one receive channel.
    """

    return rx_channel * np.exp(1j * np.deg2rad(phase_deg))


def combine_channels(rx0, rx1):
    """
    Combine two receive channels.
    """

    return rx0 + rx1


############################################################
# FFT Metrics
############################################################

def compute_metrics(freq_axis, fft_data, noise_bins=100):
    """
    Compute useful FFT metrics for logging and analysis.
    """

    peak_index = np.argmax(fft_data)

    peak_value = fft_data[peak_index]

    peak_frequency = freq_axis[peak_index]

    noise_floor = np.mean(fft_data[:noise_bins])

    snr = peak_value - noise_floor

    return {

        "peak_dbfs": peak_value,

        "peak_index": peak_index,

        "peak_frequency_mhz": peak_frequency,

        "noise_floor_dbfs": noise_floor,

        "snr_db": snr

    }


############################################################
# Phase Sweep
############################################################

def best_phase(delay_phases, peak_values):
    """
    Determine the phase angle that produces
    the strongest received signal.
    """

    best_index = np.argmax(peak_values)

    return (

        delay_phases[best_index],

        peak_values[best_index]
    )

def peak_index(fft_data):
    """Return the index of the maximum FFT value."""
    return np.argmax(fft_data)