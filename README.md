# ThesisCode-LiveStreamReceiver
Source codes for thesis work on video transmission over computer networks

There are two Python scripts included in this repository which are mean to be used in conjuncion with OBS on a local network.

## stream_latency.py
The file stream_latency.py uses Optical Character Recognition in order to extract a timestamp from a date and time overlay.
The overlay it was tested on can be found here: https://obsproject.com/forum/resources/time-and-date-overlay-updated.1461/
  Modification to the font and background opacity can be made for better legibility.

## timestamp_extract-py
The file timestamp_extract can extract the timestamp portion directly from the packet header.
  In order for it to work, the code assumes that the packets loop back. Byte counts may need to be corrected.
  The use of a packet analyzer (ex: Wireshark) is recommended to check the timestamp location.
  Latency tracking is not yet implemented in this script.

## OBS settings
OBS settings used in testing:
  Video: 1080x1920 60 fps
  Bitrate: 12000 Kbps
  Browser Hardware Acceleration: off (time overlay doesn't work otherwise)
  Stream: Set to custom - SRT URL in the form of: srt://IP:PORT?mode=caller
          Other options can be changed, but this proved to be the most reliable and has low latency.
