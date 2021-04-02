import krpc
import time
import os

# Initialize
print("\033[0;32mINFO\t\033[0mConnecting to server...")
conn = krpc.connect()
print("\033[0;32mINFO\t\033[0mServer connected.")
print("\033[0;32mINFO\t\033[0mkRPC version:",conn.krpc.get_status().version)

vessel = conn.space_center.active_vessel
print("\033[0;32mINFO\t\033[0mVessel Name:",vessel.name)

ap = vessel.auto_pilot
parts = vessel.parts
ctrl = vessel.control
ap.reference_frame = vessel.orbit.body.reference_frame
ctrl.thrust_reference_frame = vessel.orbit.body.reference_frame

print("\033[0;32mINFO\t\033[0mInitialize Completed.")
time.sleep(1)
os.system("cls")

ctrl.rcs = True
ctrl.breaks = True
ap.sas = False
# ap.sas_mode = ap.sas_mode.retrograde

srf_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
ver_speed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'vertical_speed')
hor_speed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'horizontal_speed')
vel = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'velocity')

# while True:
# 	print(vel())

# PID Algorithm Configuration
tgt_altitude = 3
kp = 0.1
ki = 0
kd = 0.35
t = 0

while srf_altitude() != tgt_altitude:
	dh = tgt_altitude - srf_altitude()
	throttle = kp*dh - kd*ver_speed() # PID Core Algorithm
	velocity = vel()
	
	if throttle < 0:
		throttle = 0

	elif throttle > 1:
		throttle = 1
	ctrl.throttle = throttle

	print("\033[0;32mINFO\t\033[0;33mALT\033[0m", str(int(srf_altitude())), "\033[0;34mm\t\033[0;33mVS\033[0m", str(int(ver_speed())), "\033[0;34mm/s", "\t\033[0;33mHS\033[0m", str(int(hor_speed())), "\033[0;34mm/s\033[0m")

	if ver_speed() > 0:
		pass

	if ver_speed() <= -5 and srf_altitude() >=100:
		ap.target_direction = (-vel()[0], -vel()[1], -vel()[2])
		ap.engage()

#	if srf_altitude() <= 50 + tgt_altitude and hor_speed() < 2:
#		ap.target_pitch_and_heading(90,0)
#		ap.engage()

	
	# SpaceX-Styled landing gear release
	if srf_altitude() <= 50 + tgt_altitude or srf_altitude() <= 100:
		ctrl.gear = True
		ctrl.legs = True
		ap.target_pitch_and_heading(90,90)
		ap.engage()
	#	ctrl.rcs_direction = (-velocity[0], -velocity[1], -velocity[2])
		if t < 1000:
			print("\033[0;32mPROCESS\033[0m\tReleasing Landing Gear\n")
			t += 1
	
		if ver_speed() >= -0.1:
			ctrl.throttle = 0
			print("\033[0;31mLANDING PROCESS DONE.\033[0m\n")
			ctrl.rcs = False
			break
	time.sleep(0.001)