# mock_data.py

import numpy as np


def generate_mock_iq(
    sample_rate,
    num_samples,
    tone_frequency,
    phase_difference=0,
    signal_amplitude=500,
    noise_amplitude=20,
    distance_m=1.0,
    environment_loss_db=0
):
    t = np.arange(num_samples) / sample_rate

    # Distance-dependent attenuation
    distance_factor = 1 / distance_m

    # Environmental attenuation
    environment_factor = 10 ** (-environment_loss_db / 20)

    amplitude = (
        signal_amplitude
        * distance_factor
        * environment_factor
    )

    rx0 = amplitude * np.exp(
        1j * 2 * np.pi * tone_frequency * t
    )

    rx1 = amplitude * np.exp(
        1j * (
            2 * np.pi * tone_frequency * t
            + np.deg2rad(phase_difference)
        )
    )

    noise0 = noise_amplitude * (
        np.random.randn(num_samples)
        + 1j * np.random.randn(num_samples)
    )

    noise1 = noise_amplitude * (
        np.random.randn(num_samples)
        + 1j * np.random.randn(num_samples)
    )

    rx0 += noise0
    rx1 += noise1

    return [rx0, rx1]