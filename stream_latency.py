import ffmpeg
import cv2
import numpy as np
import pytesseract
from datetime import datetime, timedelta


# Calculate latency in seconds
def get_latency(timestamp):
    #return
    if(timestamp == None):
        print('Timestamp read failed!')
        return None
    
    # Extract time from read string
    str_server_time = timestamp.split('| ')[1]

    # Convert to datetime.time (skipping this led to errors in reading date)
    t_server_time = datetime.strptime(str_server_time, '%H:%M:%S.%f').time()
    # Convert to datetime
    dt_server_time = datetime.combine(datetime.today(), t_server_time)

    latency = datetime.now() - dt_server_time
    latency_seconds = round(latency.total_seconds(), 2)

    return latency_seconds


# Date and time from video frame
def get_date_time_from_frame(frame):
    ocr_config='--psm 7'
    
    x, y, w, h = roi  # Define the top-left corner region
    # Crop the frame to the region of interest (ROI)
    date_time_region = frame[y:y+h, x:x+w]

    # Convert the cropped region to grayscale for OCR
    gray = cv2.cvtColor(date_time_region, cv2.COLOR_BGR2GRAY)

    # Apply OCR to extract the text
    dateTime = pytesseract.image_to_string(gray, config=ocr_config)
    dateTime = dateTime.strip()

    return dateTime

# Set up the FFmpeg SRT input stream
    # Replace the SRT URL with correct IP and PORT
process = (
    ffmpeg
    .input(r'srt://IP:PORT?mode=listener', protocol_whitelist='file,udp,rtp,srt')
    .output('pipe:', format='rawvideo', pix_fmt='bgr24', s='1280x720')
    .run_async(pipe_stdout=True)
)

print('Set up complete')

# Space out latency checks
check_frame = 0
check_frame_interval = 300

latency = 0

# Frame size for 1080p
width, height = 1280, 720

# Timestamp in frame - Region Of Interest
roi=(0, 0, round(width*0.46), round(height*0.1))

# Display using OpenCV
while True:
    in_bytes = process.stdout.read(width * height * 3)
    if not in_bytes:
        break

    # Display video
    frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])

    # Show reading frame
    x, y, w, h = roi
    frame_copy = frame.copy()
    frame_copy = cv2.rectangle(frame_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Show latency
        # Background box and text not scaled with window size
    displayed_latency = ('Latency: ' + str(latency))
    frame_copy = cv2.rectangle(frame_copy, (x, y+h), (x+250, y+2*h), (0, 0, 0), -1)
    frame_copy = cv2.putText(frame_copy, displayed_latency, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow('SRT Stream', frame_copy)
    
    # Space out latency checks
    if(check_frame == check_frame_interval):
        check_frame = 0
        # Extract date and time from the frame
        dateTime = get_date_time_from_frame(frame)
        
        latency = get_latency(dateTime)
        #print('Latency: ', latency, ' seconds')
    else:
        check_frame = check_frame + 1

    # Exit the display window when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

process.stdout.close()
cv2.destroyAllWindows()