import time

print("Starting ESP32...")
time.sleep(5)   # <-- startup delay (5 seconds)

print("Launching Marino API app...")

import marino_api

marino_api.run()
