"""
experiment_config.py

Senior Design
Software Controlled Beamforming
RF Energy Harvesting
The Setup derived from line 38
"""

"""
experiment_config.py

Experiment configuration parameters.
Contains only user-editable constants.
"""
USE_MOCK_DATA = True  # Set to True to use mock data instead of real SDR

##############################
# SDR Connection
##############################

# SDR_IP = "ip:192.168.2.1" remove for sdr

##############################
# Sampling
##############################

SAMPLE_RATE = int(2e6)
NUM_SAMPLES = 2**12

##############################
# RF Bandwidth
##############################

RX_RF_BANDWIDTH = int(600e3)
TX_RF_BANDWIDTH = int(600e3)

##############################
# RF Frequencies
##############################

RX_LO = int(2.30e9)
TX_LO = RX_LO

BASEBAND_TONE = int(200e3)

##############################
# Receiver Gain
##############################

RX_GAIN_MODE = "manual"

RX_GAIN_CH0 = 40
RX_GAIN_CH1 = 40

##############################
# Transmitter Gain
##############################

TX_GAIN_CH0 = -3
TX_GAIN_CH1 = -8

##############################
# Beamforming
##############################

PHASE_CAL = -52

PHASE_START = -180
PHASE_STOP = 180
PHASE_STEP = 2

##############################
# Antenna
##############################

ANTENNA_TYPE = "12 dBi Directional Yagi"

ANTENNA_GAIN = 12

POLARIZATION = "Vertical"

FREQUENCY_BAND = "2.4 GHz ISM"

##############################
# Experiment
##############################

EXPERIMENT_NAME = "Phase Sweep"

ENVIRONMENT = "Laboratory"

DISTANCE_M = 1.0

ENVIRONMENT_LOSS_DB = 0.0

TEST_NUMBER = 1

##############################
# Data Logging
##############################

SAVE_PHASE_SWEEP = True

SAVE_SUMMARY = True

PHASE_SWEEP_FILE = "PhaseSweep.csv" # data during sweep

SUMMARY_FILE = "ExperimentSummary.csv" # main results of experiment

##############################
# Plotting
##############################

PLOT_YMIN = -100
PLOT_YMAX = 0

PLOT_PAUSE = 0.05