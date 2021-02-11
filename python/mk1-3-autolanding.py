import krpc
import time
import os

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
time.sleep(1)

ctrl.rcs = True
ap.sas_mode = ap.sas_mode.retrograde
srf_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
ver_speed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'vertical_speed')
hor_speed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'horizontal_speed')

# PID Algorithm Configuration
tgt_altitude = 0
kp = 0.1
ki = 0
kd = 0.3

while srf_altitude() != tgt_altitude:
	dh = tgt_altitude - srf_altitude()
	throttle = kp*dh - kd*ver_speed()
	
	if throttle < 0:
		throttle = 0
	elif throttle > 1:
		throttle = 1
	ctrl.throttle = throttle
	print("\033[0;32mINFO\t\033[0;33mALT\033[0m",str(int(srf_altitude()))," m\t\033[0;33mVS\033[0m",str(int(ver_speed()))," m/s")

	if srf_altitude() <= 50 + tgt_altitude and hor_speed() < 2:
		ap.sas_mode = ap.sas_mode.stability_assist
		ap.target_pitch_and_heading(90,0)
		ap.engage()
	
	# SpaceX-Styled landing gear release
	if srf_altitude() <= 20 + tgt_altitude and srf_altitude() <= 30:
	#	ctrl.gear = True
	#	print("\033[0;32mPROCESS\033[0m\tReleasing Landing Gear\n")
	
	#	because there are no landing gears on the vessel
		if ver_speed() >= -0.1:
			ctrl.throttle = 0
			print("\033[0;31mLANDING PROCESS DONE.\033[0m")
			ctrl.rcs = False
			break
	time.sleep(0.001)