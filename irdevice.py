 #!/usr/bin/python3

def get_device():
	try:
		import irdevice_adrsir
		return irdevice_adrsir.IrDeviceAdrsir()
	except Exception:
		return None

class IrDevice:
	def send(self, usecs):
		raise NotImplementedError
