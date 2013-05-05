#Ray Alfano
#Core server class
#5/2/13

import pygst
pygst.require("0.10")
import gst
import gobject

#define the source of audio
src = 'audiotestsrc'
#src = "autoaudiosrc"
#define the encoder mechanism
enc = 'alawenc'
#enc = 'wavparse'
#define the payload type
payload = 'rtppcmapay'
#payload = 'rtpL16pay'

#define the IP address to use
outbound = "localhost"
#RTP port
rtpSender = 17404
#RTCP outbound port
#Conventionally should be RTPSEND+1
rtcpSender = 17405
#RTCP receive port
rtcpReceiver = 17409

#initialize pipeline
pipe = gst.Pipeline('rtp_server')

#set gstreamer audio parameters
#source
audiosrc = gst.element_factory_make(src, 'audiosrc')
#audiosrc = gst.element_factory_make("filesrc", '../../wavSamples/timecodeAlignTest2.wav')
#conversion
audioconv = gst.element_factory_make('audioconvert', 'audioconv')
#resample rate
audiores = gst.element_factory_make('audioresample', 'audiores')
#encoding type
audioenc = gst.element_factory_make(enc, 'audioenc')
#payload element
audiopay = gst.element_factory_make(payload, 'audiopay')

#line up the pipeline elements instantiated so far
pipe.add(audiosrc, audioconv, audiores, audioenc, audiopay)

#fit together the pipeline elements 
res = gst.element_link_many(audiosrc, audioconv, audiores, audioenc, audiopay)

#create an rtpbin element
rtpbin = gst.element_factory_make('gstrtpbin', 'rtpbin')

#line up the pipeline element
pipe.add(rtpbin)

# Instantiate UDP sink utilizing RTP
rtpsink = gst.element_factory_make('udpsink', 'rtpsink')
#set up port for RTP to send
rtpsink.set_property('port', rtpSender)
#set up host
rtpsink.set_property('host', outbound)

#instantiate UDP sink utilizing RTCP
#RTCP provides control packets
rtcpsink = gst.element_factory_make('udpsink', 'rtcpsink')
#set up port for RTCP to send
rtcpsink.set_property('port', rtcpSender)
#set up host for RTCP
rtcpsink.set_property('host', outbound)
#Explicitly disallow synchronization... no need in my application
rtcpsink.set_property('async', False)
rtcpsink.set_property('sync', False)

#receiver for rtcp packets
rtcpsrc = gst.element_factory_make('udpsrc', 'rtcpsrc')
rtcpsrc.set_property('port', rtcpReceiver)

#line up the pipeline elements just instantiated
pipe.add(rtpsink, rtcpsink, rtcpsrc)

# fit together pipes for rtpbin
#gettan RTP sinkpad for session 0
sinkpad = gst.Element.get_request_pad(rtpbin, 'send_rtp_sink_0')
srcpad = gst.Element.get_static_pad(audiopay, 'src')
lres = gst.Pad.link(srcpad, sinkpad)

# Get RTP syncpad from above
# fit together pipes to rtpsink sinkpad
srcpad = gst.Element.get_static_pad(rtpbin, 'send_rtp_src_0')
sinkpad = gst.Element.get_static_pad(rtpsink, 'sink')
lres = gst.Pad.link(srcpad, sinkpad)

# get an RTCP srcpad for sending RTCP to the receiver
srcpad = gst.Element.get_request_pad(rtpbin, 'send_rtcp_src_0')
sinkpad = gst.Element.get_static_pad(rtcpsink, 'sink')
lres = gst.Pad.link(srcpad, sinkpad)

# This will receive RTCP packets
# So, request an RTCP sinkpad for session 0 and
# fit it to the srcpad of the udpsrc for RTCP
srcpad = gst.Element.get_static_pad(rtcpsrc, 'src')
sinkpad = gst.Element.get_request_pad(rtpbin, 'recv_rtcp_sink_0')
lres = gst.Pad.link(srcpad, sinkpad)

# set the pipeline to playing
gst.Element.set_state(pipe, gst.STATE_PLAYING)

# Then we receive messages iteratively using GObject loop
# NOTE: Change this to GTK+ loop if changing to GUI-based system
mainloop = gobject.MainLoop()
gobject.threads_init()
context = mainloop.get_context()
#mainloop.run()

while 1: 
	print("Beginning audio transmission")
	n = raw_input("Type a whitespace character (" ") and <ENTER> or ctrl+c to exit")
	if n == " ":
		break
	context.iteration(True)

gst.Element.set_state(pipe, gst.STATE_NULL)
