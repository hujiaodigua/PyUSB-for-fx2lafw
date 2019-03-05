import usb.core
import usb.util
import time

# 先开pulseview保证fx2有固件

# find our device
dev = usb.core.find(idVendor=0x0925, idProduct=0x3881)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()
# print('===============================')
# print(dev)

# get an endpoint instance
cfg = dev.get_active_configuration()
# print('===============================')
print(cfg)

intf = cfg[(0,0)]
# print('===============================')
print(intf)

dev.ctrl_transfer(0xc0,0xb0,0,0,0x02,0x00)

time.sleep(1)
dev.ctrl_transfer(0xc0,0xb2,0,0,0x01,0x00)

time.sleep(1)
dev.ctrl_transfer(0x40,0xb1,0,0,0x03,0x00)

time.sleep(1)

dev.bulk_write(0x00,0x05,0xdb)

Set = [0x00,0x05,0xdb]

dev.write(0x82,Set)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None
print('===============================')
print(ep)

# write the data

print(intf[6])

ep.write('test')