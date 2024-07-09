import RPi.GPIO as GPIO
import sm_16relind
import time

def test_relays():
    num_hats = 1  # Adjust based on your setup
    relay_hats = [sm_16relind.SM16relind(i) for i in range(num_hats)]
    GPIO.setmode(GPIO.BOARD)

    for hat in relay_hats:
        print(f"Initialized relay hat {hat}")
        hat.set_all(0)

    relay_pairs = [(1, 2), (3, 4), (5, 6)]  # Adjust based on your setup
    stagger = 1

    for relay_pair in relay_pairs:
        relay1, relay2 = relay_pair
        hat_index1, relay_index1 = divmod(relay1 - 1, 16)
        hat_index2, relay_index2 = divmod(relay2 - 1, 16)
        print(f"Triggering relay pair {relay_pair}: hat {hat_index1 + 1}, relays {relay_index1 + 1} & {relay_index2 + 1}")
        relay_hats[hat_index1].set(relay_index1 + 1, 1)
        relay_hats[hat_index2].set(relay_index2 + 1, 1)
        time.sleep(stagger)
        relay_hats[hat_index1].set(relay_index1 + 1, 0)
        relay_hats[hat_index2].set(relay_index2 + 1, 0)
        time.sleep(stagger)
        print(f"Relay pair {relay_pair} triggered successfully")

if __name__ == "__main__":
    test_relays()
