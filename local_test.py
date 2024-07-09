import sys
import os
import threading
import time
import math
from PyQt5.QtWidgets import QApplication, QWidget
from gpio.gpio_handler import RelayHandler
from notifications.notifications import NotificationHandler
from ui.gui import RodentRefreshmentGUI
from settings.config import load_settings

class MockSM16relind:
    def __init__(self, stack):
        self.stack = stack
        self.relay_states = [0] * 16

    def set_all(self, state):
        print(f"MockSM16relind set all relays to state {state}")
        self.relay_states = [state] * 16

    def set(self, relay, state):
        print(f"MockSM16relind relay {relay} set to state {state}")
        self.relay_states[relay - 1] = state

# Ensure the mock module is properly available as sm_16relind
sys.modules['sm_16relind'] = MockSM16relind

def main():
    settings = load_settings()
    relay_handler = RelayHandler(settings['relay_pairs'], settings['num_hats'])
    notification_handler = NotificationHandler(settings['slack_token'], settings['channel_id'])

    def run_program():
        global running
        running = True
        threading.Thread(target=program_loop).start()
        print("Program Started")

    def stop_program():
        global running
        running = False
        relay_handler.set_all_relays(0)
        print("Program Stopped")
        app.quit()

    def program_loop():
        global running
        while running:
            current_hour = time.localtime().tm_hour
            if (settings['window_start'] <= current_hour < 24) or (0 <= current_hour < settings['window_end']) if settings['window_start'] > settings['window_end'] else (settings['window_start'] <= current_hour < settings['window_end']):
                current_time = time.time()
                if current_time % settings['interval'] < 1:
                    relay_info = relay_handler.trigger_relays(settings['selected_relays'], settings['num_triggers'], settings['stagger'])
                    message = (
                        f"The pumps have been successfully triggered as follows:\n"
                        f"{'; '.join(relay_info)}\n"
                        f"** Next trigger due in {settings['interval']} seconds.\n\n"
                        f"Current settings:\n"
                        f"- Interval: {settings['interval']} seconds\n"
                        f"- Stagger: {settings['stagger']} seconds\n"
                        f"- Water window: {settings['window_start']:02d}:00 - {settings['window_end']:02d}:00\n"
                        f"- Relays enabled: {', '.join(f'({rp[0]} & {rp[1]})' for rp in settings['selected_relays']) if settings['selected_relays'] else 'None'}"
                    )
                    if notification_handler.is_internet_available():
                        notification_handler.send_slack_notification(message)
                    else:
                        notification_handler.log_pump_trigger(message)
                    time.sleep(settings['interval'] - 1)

    def update_all_settings():
        new_settings = gui.get_settings()
        settings.update(new_settings)
        print("Settings updated")

    app = QApplication([])
    gui = RodentRefreshmentGUI(run_program, stop_program, update_all_settings, style='idea3')
    gui.show()
    app.exec_()

if __name__ == "__main__":
    main()
