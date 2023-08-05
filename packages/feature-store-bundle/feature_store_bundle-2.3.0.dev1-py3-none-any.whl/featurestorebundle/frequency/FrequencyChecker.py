import re
from featurestorebundle.frequency.FriendlyFrequencies import FriendlyFrequencies


class FrequencyChecker:
    def check_frequency_valid(self, frequency: str):
        if frequency in FriendlyFrequencies.friendly_frequencies:
            return

        matches = re.match(r"([1-9][0-9]*)(d)", frequency)

        if not matches:
            raise Exception(f"Invalid frequency format, allowed values are {FriendlyFrequencies.friendly_frequencies} or e.g. '5d'")
