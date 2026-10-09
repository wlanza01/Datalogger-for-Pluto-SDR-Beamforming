"""
Jon Kraft, Oct 30 2022
https://github.com/jonkraft/Pluto_Beamformer
video walkthrough of this at:  https://www.youtube.com/@jonkraft

"""
# Copyright (C) 2020 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.

import sys
print(f"sys.path = {sys.path}")

# import adi uncomment this to test PlutoSDR 
import numpy as np
import time

# ----------------------------
# Project Modules
# ----------------------------

import experiment_config as cfg

from signal_processing import (
    compute_metrics,
    combine_channels,
    apply_phase_delay,
    dbfs,
    peak_index,
)

from plotting import plot_fft

from utilities import (
    create_tone,
    create_frequency_axis
)

from data_logger import DataLogger

from mock_data import generate_mock_iq
use_mock_data = True  # Set to True to use mock data instead of real SDR

# ----------------------------
# Configure Pluto
# ----------------------------

if not cfg.USE_MOCK_DATA:
    from pluto_config import configure_pluto
    sdr = configure_pluto()
else:
    sdr = None

# ----------------------------
# Initialize Loggers
# ----------------------------

logger = DataLogger(cfg.PHASE_SWEEP_FILE) #both loggers are initialized to write to the files specified in experiment_config.py

summary_logger = DataLogger(cfg.SUMMARY_FILE)
# ----------------------------
# Generate Test Signal
# ----------------------------

if cfg.USE_MOCK_DATA:

    Rx_0, Rx_1 = generate_mock_iq(
        cfg.SAMPLE_RATE,
        cfg.NUM_SAMPLES,
        cfg.BASEBAND_TONE
    )

else:

    iq = create_tone(
        cfg.SAMPLE_RATE,
        cfg.BASEBAND_TONE
    )

    sdr.tx([iq, iq])

# ----------------------------
# Frequency Axis
# ----------------------------

xf = create_frequency_axis(
    sample_rate=cfg.SAMPLE_RATE,
    num_samples=cfg.NUM_SAMPLES,
    center_freq=cfg.RX_LO
)

# ----------------------------
# Allow SDR Calibration / Acquire IQ Data
# ----------------------------

if cfg.USE_MOCK_DATA:

    # Use simulated IQ data
    data = generate_mock_iq(
        sample_rate=cfg.SAMPLE_RATE,
        num_samples=cfg.NUM_SAMPLES,
        tone_frequency=cfg.BASEBAND_TONE,
        phase_difference=0,
        distance_m=cfg.DISTANCE_M,
        environment_loss_db=cfg.ENVIRONMENT_LOSS_DB
    )

else:

    # Allow PlutoSDR to calibrate
    for i in range(20):
        sdr.rx()

    # Acquire real IQ data
    data = sdr.rx()


Rx_0 = data[0]
Rx_1 = data[1]


# ----------------------------
# Phase Sweep
# ----------------------------

peak_sum = []

delay_phases = np.arange(
    cfg.PHASE_START,
    cfg.PHASE_STOP,
    cfg.PHASE_STEP
)

for phase_delay in delay_phases:

    delayed_rx1 = apply_phase_delay(
        Rx_1,
        phase_delay + cfg.PHASE_CAL
    )

    combined = combine_channels(
        Rx_0,
        delayed_rx1
    )

    fft_data = dbfs(combined)

    metrics = compute_metrics(
        xf,
        fft_data
    )   


    peak_sum.append(metrics["peak_dbfs"])

    logger.log(

        phase_delay=phase_delay,

        distance_m=cfg.DISTANCE_M,

        environment_loss_db=cfg.ENVIRONMENT_LOSS_DB,

        frequency_hz=cfg.RX_LO,

        fft_peak_dbfs=metrics["peak_dbfs"],

        peak_frequency_mhz=metrics["peak_frequency_mhz"],

        noise_floor_dbfs=metrics["noise_floor_dbfs"],

        snr_db=metrics["snr_db"],

    rx_gain0=cfg.RX_GAIN_CH0,

    rx_gain1=cfg.RX_GAIN_CH1,

    tx_gain=cfg.TX_GAIN_CH0,

    sample_rate=cfg.SAMPLE_RATE,

    num_samples=cfg.NUM_SAMPLES
)

    plot_fft(

        xf,

        fft_data,

        phase_delay

    )

    time.sleep(cfg.PLOT_PAUSE)

# ----------------------------
# Determine Best Phase
# ----------------------------

best_index = peak_index(peak_sum)

best_phase_deg = delay_phases[best_index]

best_peak = peak_sum[best_index]

# ----------------------------
# Calculate Metrics for Best Phase
# ----------------------------

best_delayed_rx1 = apply_phase_delay(
    Rx_1,
    best_phase_deg + cfg.PHASE_CAL
)

best_delayed_sum = combine_channels(
    Rx_0,
    best_delayed_rx1
)

best_fft = dbfs(best_delayed_sum)

best_metrics = compute_metrics(
    best_fft,
    xf
)

best_peak_frequency = best_metrics["peak_frequency_mhz"]
best_noise_floor = best_metrics["noise_floor_dbfs"]
best_snr = best_metrics["snr_db"]

summary_logger.log(
    test_number=cfg.TEST_NUMBER,

    experiment_name=cfg.EXPERIMENT_NAME,

    distance_m=cfg.DISTANCE_M,

    environment=cfg.ENVIRONMENT,

    environment_loss_db=cfg.ENVIRONMENT_LOSS_DB,

    rx_frequency_hz=cfg.RX_LO,

    tx_frequency_hz=cfg.TX_LO,

    best_phase_deg=best_phase_deg,

    best_fft_peak_dbfs=best_peak,

    best_peak_frequency_mhz=best_peak_frequency,

    best_noise_floor_dbfs=best_noise_floor,

    best_snr_db=best_snr,

    rx_gain0_db=cfg.RX_GAIN_CH0,

    rx_gain1_db=cfg.RX_GAIN_CH1,

    tx_gain_db=cfg.TX_GAIN_CH0,

    sample_rate=cfg.SAMPLE_RATE,

    num_samples=cfg.NUM_SAMPLES
)
# ----------------------------
# Print Summary of Metrics, along with experiment name and test no. 
# ----------------------------
print("\n========== Experiment Summary ==========")

print(f"Experiment        : {cfg.EXPERIMENT_NAME}")
print(f"Test Number       : {cfg.TEST_NUMBER}")

print(f"Distance           : {cfg.DISTANCE_M:.2f} m")
print(f"Environment Loss   : {cfg.ENVIRONMENT_LOSS_DB:.1f} dB")

print(f"RX Frequency       : {cfg.RX_LO / 1e9:.3f} GHz")
print(f"TX Frequency       : {cfg.TX_LO / 1e9:.3f} GHz")

print(f"TX Gain            : {cfg.TX_GAIN_CH0} dB")
print(f"RX Gain CH0        : {cfg.RX_GAIN_CH0} dB")
print(f"RX Gain CH1        : {cfg.RX_GAIN_CH1} dB")

print(f"Best Phase         : {best_phase_deg}°")
print(f"Peak FFT           : {best_peak:.2f} dBFS")

print(f"Peak Frequency     : {best_peak_frequency:.3f} MHz")
print(f"Noise Floor        : {best_noise_floor:.2f} dBFS")
print(f"SNR                : {best_snr:.2f} dB")

print("========================================")

if not cfg.USE_MOCK_DATA:
    sdr.tx_destroy_buffer()