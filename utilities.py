"""
utilities.py

General-purpose utility functions for the SDR beamforming project.
"""

import time
import numpy as np


############################################################
# Time / Display Utilities
############################################################

def timestamp():
    """
    Return the current date and time as a formatted string.
    """

    return time.strftime("%Y-%m-%d %H:%M:%S")


def print_banner(title):
    """
    Print a formatted section banner.
    """

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


############################################################
# SDR Test Signal Generation
############################################################

def create_tone(
    sample_rate,
    frequency,
    num_points=2**16,
    amplitude=2**14
):
    """
    Generate a complex sinusoidal IQ signal
    for PlutoSDR transmission.
    """

    ts = 1 / sample_rate

    t = np.arange(
        0,
        num_points * ts,
        ts
    )

    i = (
        np.cos(2 * np.pi * frequency * t)
        * amplitude
    )

    q = (
        np.sin(2 * np.pi * frequency * t)
        * amplitude
    )

    return i + 1j * q


############################################################
# FFT Frequency Axis
############################################################

def create_frequency_axis(
    sample_rate,
    num_samples,
    center_freq=0):
    """
    Generate an FFT frequency axis in MHz.
    """

    ts = 1 / sample_rate

    xf = np.fft.fftfreq(
        num_samples,
        ts
    )

    return (np.fft.fftshift(xf) + center_freq) / 1e6 #Adding RF Center