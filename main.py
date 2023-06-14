import json
from pprint import pprint
from statistics import mean

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

plt.style.use("ggplot")


def load_json_data():
    filename = "test-2023-06-10_17-01-37.json"

    with open(filename, "r") as f:
        data = json.load(f)

    return data


def get_averages_from_test_data(test_data):
    delta_epochs = []
    inc_snrs = []
    inc_rssis = []
    for test_num in test_data:
        delta_epochs.append(test_data[test_num].get("delta_epoch"))
        inc_rssis.append(int(test_data[test_num].get("inc_rssi")))
        inc_snrs.append(int(test_data[test_num].get("inc_snr")))

    return mean(delta_epochs), mean(inc_rssis), mean(inc_snrs), len(delta_epochs)


def plot_test_data(test_data):
    packet_number = list(range(len(test_data)))
    delta_epochs = []
    bandwidth = ""
    spreading_factor = ""
    coding_rate = ""
    for test_num in test_data:
        delta_epochs.append(test_data[test_num].get("delta_epoch"))
        # time.append(test_data[test_num].get("inc_epoch"))

        if not bandwidth:
            bandwidth = test_data[test_num].get("bandwidth")
        if not spreading_factor:
            spreading_factor = test_data[test_num].get("spreading_factor")
        if not coding_rate:
            coding_rate = test_data[test_num].get("coding_rate")

    a, b = np.polyfit(packet_number, delta_epochs, 1)

    plt.plot(packet_number, delta_epochs)
    plt.plot(packet_number, a * np.asarray(packet_number) + b)
    plt.xlabel("Packets")
    plt.ylabel("Delta epoch")
    plt.title(
        f"Bandwidth: {bandwidth}, Spreading factor: {spreading_factor}, Coding rate: {coding_rate}"
    )
    plt.show()


def plot_multiple_test_data(full_test_data):
    for idx, test_data in enumerate(full_test_data):
        plt.subplot(4, 2, idx + 1)
        packet_number = list(range(len(test_data)))
        delta_epochs = []
        bandwidth = ""
        spreading_factor = ""
        coding_rate = ""
        for test_num in test_data:
            delta_epochs.append(test_data[test_num].get("delta_epoch"))
            # time.append(test_data[test_num].get("inc_epoch"))

            if not bandwidth:
                bandwidth = test_data[test_num].get("bandwidth")
            if not spreading_factor:
                spreading_factor = test_data[test_num].get("spreading_factor")
            if not coding_rate:
                coding_rate = test_data[test_num].get("coding_rate")

        a, b = np.polyfit(packet_number, delta_epochs, 1)

        plt.plot(packet_number, delta_epochs)
        plt.plot(packet_number, a * np.asarray(packet_number) + b)
        plt.xlabel("Packets")
        plt.ylabel("Time difference (s)")
        plt.title(
            f"BW: {bandwidth}, SF: {spreading_factor}, CR: {coding_rate}, Avg: {mean(delta_epochs):.3f}s, Packets: {packet_number[-1]}"
        )

    plt.subplots_adjust(
        top=0.972, bottom=0.043, left=0.029, right=0.994, hspace=0.318, wspace=0.063
    )

    plt.show()


if __name__ == "__main__":
    data = load_json_data()
    data_names = list(data.keys())

    bandwidth_4_tests = []
    for i in range(8):
        bandwidth_4_tests.append(data[data_names[i]])

    plot_multiple_test_data(bandwidth_4_tests)

    bandwidth_8_tests = []
    for i in range(8, 16):
        bandwidth_8_tests.append(data[data_names[i]])

    plot_multiple_test_data(bandwidth_8_tests)
