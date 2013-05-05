TCP implementation:

To mitigate severe issues with installing dependent libraries I implemented this reductive proof-of-concept for Ubuntu Linux since it comes with all necessary components pre-installed. The performance of this will be contrasted to the RTP implementation in my final report.

To run this program:
	1. Open a Terminal window in Linux
	2. Navigate to the tcp folder
	3. Execute the command "python main.py"

That command will spawn four terminal windows, two clients and two servers, and connect them. The clients will pass linear PCM WAV audio data from the wavSamples folder to each other and output the data as it is received. This is a drastically simplified version of the code described in the other documents.

RTP implementation:

This is the basis of my full program. This encompasses ONLY the core functionality of the program. The statistics and dynamic portions of the program are still being reimplemented. 

NOTE: Please turn down your system volume prior to running this. The ALSA audio test runs at different percentages of the local volume setting on different systems.

To run the test version:
	1. Open two terminal windows
	2. Navigate in both to the refactor/rtp folder
	3.1 In one terminal window execute: "python pcm-server.py"
	3.2 In one terminal window execute: "python pcm-client.py"

