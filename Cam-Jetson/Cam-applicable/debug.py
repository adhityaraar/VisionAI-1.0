import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Create a pipeline
pipeline = Gst.parse_launch("videotestsrc ! autovideosink")

# Set the pipeline state to "playing" to start it
pipeline.set_state(Gst.State.PLAYING)

# At this point, a video window should appear with a test pattern

# After a delay, set the pipeline state to "NULL" to stop it
import time
time.sleep(2)

pipeline.set_state(Gst.State.NULL)

