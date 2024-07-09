import sys

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from tests.mock_gpio import MockGPIO as GPIO

try:
    import sm_16relind
except (ImportError, RuntimeError):
    from tests.mock_sm_16relind import MockSM16relind as sm_16relind

import time

class RelayHandler:
    def __init__(self, relay_pairs, num_hats=1):
        self.relay_pairs = relay_pairs
        self.num_hats = num_hats
        GPIO.setmode(GPIO.BOARD)
        self.relay_hats = [sm_16relind(i) for i in range(num_hats)]
        for hat in self.relay_hats:
            hat.set_all(0)

    def set_all_relays(self, state):
        for hat in self.relay_hats:
            hat.set_all(state)

    def trigger_relays(self, selected_relays, num_triggers, stagger):
        relay_info = []
        for relay_pair in self.relay_pairs:
            if relay_pair in selected_relays:
                triggers = num_triggers.get(relay_pair, 1)
                for _ in range(triggers):
                    relay1, relay2 = relay_pair
                    hat_index1, relay_index1 = divmod(relay1 - 1, 16)
                    hat_index2, relay_index2 = divmod(relay2 - 1, 16)
                    self.relay_hats[hat_index1].set(relay_index1 + 1, 1)
                    self.relay_hats[hat_index2].set(relay_index2 + 1, 1)
                    print(f"Pumps connected to {relay_pair} triggered")
                    time.sleep(stagger)
                    self.relay_hats[hat_index1].set(relay_index1 + 1, 0)
                    self.relay_hats[hat_index2].set(relay_index2 + 1, 0)
                    time.sleep(stagger)
                relay_info.append(f"{relay_pair} triggered {triggers} times")
        return relay_info
