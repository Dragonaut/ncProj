import socket
import gobject
import pygst
pygst.require("0.10")
import gst

pipe = gst.Pipeline("client")

src = gst.element_factory_make("filesrc", "src")
src.set_property("location", "../wavSamples/timecodeAlignTest2.wav")
pipe.add(src)

client = gst.element_factory_make("tcpclientsink", "client")
pipe.add(client)
client.set_property("host", "localhost")
client.set_property("port", 21337)
src.link(client)

pipe.set_state(gst.STATE_PLAYING)

print("Client 2 \n")
loop = gobject.MainLoop()
loop.run()
