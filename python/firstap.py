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

srf_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
ver_speed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'vertical_speed')
tgt_altitude = 3

while srf_altitude() != tgt_altitude:
	dh = tgt_altitude - srf_altitude()
	throttle = 0.1*dh - 0.4*ver_speed()
	if throttle < 0:
		throttle = 0
	elif throttle > 1:
		throttle = 1
	ctrl.throttle = throttle
	time.sleep(0.05)