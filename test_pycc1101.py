"""
run tests via pytest / pytest-3 command
"""

import pytest

from pycc1101.pycc1101 import TICC1101


@pytest.mark.parametrize(
    ("freq_mhz", "control_words"),
    [
        (433, (0x10, 0xA7, 0x62)),
        (433.42, (0x10, 0xAB, 0x85)),
        (434, (0x10, 0xB1, 0x3B)),
        (868, (0x21, 0x62, 0x76)),
    ],
)
def test_compute_frequency_control_words(freq_mhz, control_words):
    assert TICC1101._computeFrequencyControlWords(freq_mhz) == control_words
