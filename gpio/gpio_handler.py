import RPi.GPIO as GPIO
import sm_16relind
import time

class RelayHandler:
    def __init__(self, relay_pairs):
        self.relay_pairs = relay_pairs
        GPIO.setmode(GPIO.BOARD)
        self.rel = sm_16relind.SM16relind(0)
        self.rel.set_all(0)

    def set_all_relays(self, state):
        self.rel.set_all(state)

    def trigger_relays(self, selected_relays, num_triggers, stagger):
        relay_info = []
        for relay_pair in self.relay_pairs:
            if relay_pair in selected_relays:
                triggers = num_triggers.get(relay_pair, 1)
                for _ in range(triggers):
                    relay1, relay2 = relay_pair
                    self.rel.set(relay1, 1)
                    self.rel.set(relay2, 1)
                    print(f"Pumps connected to {relay_pair} triggered")
                    time.sleep(stagger)
                    self.rel.set(relay1, 0)
                    self.rel.set(relay2, 0)
                    time.sleep(stagger)
                relay_info.append(f"{relay_pair} triggered {triggers} times")
        return relay_info
