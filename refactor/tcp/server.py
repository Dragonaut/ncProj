import socket
import gobject
import pygst
pygst.require("0.10")
import gst

#necessary for calling back
def new_decode_pad(dbin, pad, islast):
	pad.link(conv.get_pad("sink"))

pipe = gst.Pipeline("server")
portNumber = "11337"

conn = gst.element_factory_make("tcpserversrc", "source")
pipe.add(conn)
conn.set_property("host", "localhost")
conn.set_property("port", int(portNumber))

decoder = gst.element_factory_make("decodebin", "decode")
decoder.connect("new-decoded-pad", new_decode_pad)
pipe.add(decoder)
conn.link(decoder)

conv = gst.element_factory_make("audioconvert", "conv")
pipe.add(conv)

localSink = gst.element_factory_make("alsasink", "localSink")
pipe.add(localSink)
conv.link(localSink)

pipe.set_state(gst.STATE_PLAYING)

print("Server 1 \n")
print("The fixed wav files are representative of PCM input \n")
print("The files used are metronome files used to test my full program's timeclock \n")
print("The wavs are meant to be evenly out-of-sync, creating pulse effect \n")
print("Operating on port " + portNumber)
loop = gobject.MainLoop()
loop.run()
