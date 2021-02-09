from sys import version
import krpc
import time

print("Connecting to kRPC Server...")
conn = krpc.connect()
krpcversion = conn.krpc.get_status().version
print("Connected.\nkRPC Version:",krpcversion+"\n")

vessel = conn.space_center.active_vessel
vessel.name = "Falcon 9 Test Unmanned Ship"
flight_info = vessel.flight()
refframe = vessel.orbit.body.reference_frame

while True:
	print("Altitude",flight_info.mean_altitude)
	print("Position",vessel.position(refframe))
	print()
	time.sleep(1)