from gpio.gpio_handler import RelayHandler
from ui.gui import RodentRefreshmentGUI
from notifications.notifications import NotificationHandler
from settings.config import load_settings
from PyQt5.QtWidgets import QApplication
import threading
import time

def main():
    settings = load_settings()
    relay_handler = RelayHandler(settings['relay_pairs'], settings['num_hats'])
    notification_handler = NotificationHandler(settings['slack_token'], settings['channel_id'])

    def run_program():
        nonlocal settings
        new_settings = gui.get_settings()
        settings.update(new_settings)
        print("Settings updated:", settings)
        if not settings['selected_relays']:
            settings['selected_relays'] = settings['relay_pairs']
        if not settings['num_triggers']:
            settings['num_triggers'] = {tuple(pair): 1 for pair in settings['relay_pairs']}
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
            window_start, window_end = settings['window_start'], settings['window_end']
            if (window_start <= current_hour < 24) or (0 <= current_hour < window_end) if window_start > window_end else (window_start <= current_hour < window_end):
                current_time = time.time()
                if current_time % settings['interval'] < 1:
                    print(f"Triggering relays at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
                    relay_info = relay_handler.trigger_relays(settings['selected_relays'], settings['num_triggers'], settings['stagger'])
                    print(f"Relay info: {relay_info}")
                    message = (
                        f"The pumps have been successfully triggered as follows:\n"
                        f"{'; '.join(relay_info)}\n"
                        f"** Next trigger due in {settings['interval']} seconds.\n\n"
                        f"Current settings:\n"
                        f"- Interval: {settings['interval']} seconds\n"
                        f"- Stagger: {settings['stagger']} seconds\n"
                        f"- Water window: {window_start:02d}:00 - {window_end:02d}:00\n"
                        f"- Relays enabled: {', '.join(f'({rp[0]} & {rp[1]})' for rp in settings['selected_relays']) if settings['selected_relays'] else 'None'}"
                    )
                    if notification_handler.is_internet_available():
                        notification_handler.send_slack_notification(message)
                    else:
                        notification_handler.log_pump_trigger(message)
                    time.sleep(settings['interval'] - 1)

    app = QApplication([])
    gui = RodentRefreshmentGUI(run_program, stop_program, lambda: None)
    gui.show()
    app.exec_()

if __name__ == "__main__":
    main()
