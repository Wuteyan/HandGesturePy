import bluetooth

target_name = "My Phone"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    target_name = bluetooth.lookup_name( bdaddr )
    print (target_name)
    
#if target_address is not None:
#    print "found target bluetooth device with address ", target_address
#else:
#    print "could not find target bluetooth device nearby"

    
