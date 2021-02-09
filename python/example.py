import krpc
import time

def init():
	print("Connecting to server...")
	global conn
	conn = krpc.connect()
	print("Server connected.")
	print("kRPC version:",conn.krpc.get_status().version)
	global vessel
	vessel = conn.space_center.active_vessel
	print("Vessel Name:",vessel.name)
	global ap
	ap = vessel.auto_pilot
	ap.target_pitch_and_heading(90, 90)
	ap.engage()
	print("Initialize Complete.")

def countdown(n):
	n = int(n)
	print("Counting Down in:")
	for i in range(0,n):
		time.sleep(1)
		print(n-i)