import krpc
import time
from example import *

# Initialize
print("Connecting to server...")
conn = krpc.connect()
print("Server connected.")
print("kRPC version:",conn.krpc.get_status().version)

vessel = conn.space_center.active_vessel
print("Vessel Name:",vessel.name)
ap = vessel.auto_pilot
ctrl = vessel.control
print("Initialize Completed.")
print()

# Start Mission
ctrl.throttle = 1
# countdown(10)
vessel.control.activate_next_stage()
print("Ignition.")
vessel.control.activate_next_stage()
print("Liftoff.")

ap.target_pitch_and_heading(90, 90)
ap.engage()