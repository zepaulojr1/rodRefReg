import time

class MockRelayHandler:
    def __init__(self, relay_pairs):
        self.relay_pairs = relay_pairs
        print("Mock GPIO setup complete")

    def set_all_relays(self, state):
        print(f"Set all relays to {state}")

    def trigger_relays(self, selected_relays, num_triggers, stagger):
        relay_info = []
        for relay_pair in self.relay_pairs:
            if relay_pair in selected_relays:
                triggers = num_triggers.get(relay_pair, 1)
                for _ in range(triggers):
                    relay1, relay2 = relay_pair
                    print(f"Pumps connected to {relay_pair} triggered")
                    time.sleep(stagger)
                    print(f"Pumps connected to {relay_pair} stopped")
                    time.sleep(stagger)
                relay_info.append(f"{relay_pair} triggered {triggers} times")
        return relay_info
