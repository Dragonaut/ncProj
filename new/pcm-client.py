import pygst
pygst.require("0.10")
import gst
import gobject    

#Define the audio capture source
AUDIO_CAPS = 'application/x-rtp,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA'
#AUDIO_CAPS = 'application/x-rtp,media=(string)audio,clock-rate=(int)44100,encoding-name=(string)WAV'
#Define audio depayload property
AUDIO_DEPAY = 'rtppcmadepay'
#Define audio decoder
AUDIO_DEC = 'alawdec'
#AUDIO_DEC = 'wavparse'
#Define audio sink for playback
AUDIO_SINK = 'autoaudiosink'

#set destination IP address
DEST = '127.0.0.1'

#set RTP receiver port
RTP_RECV_PORT = 5002
#set RTCP receiver port
#conventially is RTP+1
RTCP_RECV_PORT = 5003
#Set RTCP sender port
RTCP_SEND_PORT = 5007 

#define function for adding sinkpad according to example conventions
def pad_added_cb(rtpbin, new_pad, depay):
    sinkpad = gst.Element.get_static_pad(depay, 'sink')
    lres = gst.Pad.link(new_pad, sinkpad)

# Instantiate a pipeline
pipe = gst.Pipeline('rtp_client')

# UDP source element
rtpsrc = gst.element_factory_make('udpsrc', 'rtpsrc')
# Prepare for RTP receive
rtpsrc.set_property('port', RTP_RECV_PORT)

# Explicitly set CAPS for UDP source
caps = gst.caps_from_string(AUDIO_CAPS)
rtpsrc.set_property('caps', caps)

#instantiate the RTCP source
rtcpsrc = gst.element_factory_make('udpsrc', 'rtcpsrc')
rtcpsrc.set_property('port', RTCP_RECV_PORT)

#Instantiate RTCP sink for UDP
rtcpsink = gst.element_factory_make('udpsink', 'rtcpsink')
rtcpsink.set_property('port', RTCP_SEND_PORT)
rtcpsink.set_property('host', DEST)
#Explicitly disallow the synchronization properties
rtcpsink.set_property('async', False)
rtcpsink.set_property('sync', False) 

#fit together the pipeline elements
pipe.add(rtpsrc, rtcpsrc, rtcpsink)

# define depayloading
audiodepay = gst.element_factory_make(AUDIO_DEPAY, 'audiodepay')
# define decoding of audio
audiodec = gst.element_factory_make(AUDIO_DEC, 'audiodec')
#audio conversion
audioconv = gst.element_factory_make('audioconvert', 'audioconv')
#audio sample rate resolution
audiores = gst.element_factory_make('audioresample', 'audiores')
#audio sink definition
audiosink = gst.element_factory_make(AUDIO_SINK, 'audiosink')

# fit the above together to pipeline
pipe.add(audiodepay, audiodec, audioconv, audiores, audiosink)

res = gst.element_link_many(audiodepay, audiodec, audioconv, audiores, audiosink)

# the rtpbin element
rtpbin = gst.element_factory_make('gstrtpbin', 'rtpbin') 

#fit together pipeline with rtpbin
pipe.add(rtpbin)

# fit everything to the RTPbin
# start by getting an RTP sinkpad for session 0
srcpad = gst.Element.get_static_pad(rtpsrc, 'src')
sinkpad = gst.Element.get_request_pad(rtpbin, 'recv_rtp_sink_0')
lres = gst.Pad.link(srcpad, sinkpad)

# define an RTCP sinkpad in session 0
srcpad = gst.Element.get_static_pad(rtcpsrc, 'src')
sinkpad = gst.Element.get_request_pad(rtpbin, 'recv_rtcp_sink_0')
lres = gst.Pad.link(srcpad, sinkpad)

# define an RTCP srcpad for sending RTCP back to the sender
srcpad = gst.Element.get_request_pad(rtpbin, 'send_rtcp_src_0')
sinkpad = gst.Element.get_static_pad(rtcpsink, 'sink')
lres = gst.Pad.link(srcpad, sinkpad)

#explicit connection to RTPbin
rtpbin.connect('pad-added', pad_added_cb, audiodepay) 

#play!
gst.Element.set_state(pipe, gst.STATE_PLAYING)

#NOTE this must be changed to GTK+ type
mainloop = gobject.MainLoop()
gobject.threads_init()
context = mainloop.get_context()
#mainloop.run() 

while 1:
	context.iteration(True)

gst.Element.set_state(pipe, gst.STATE_NULL) 
