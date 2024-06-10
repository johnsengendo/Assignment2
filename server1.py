import signal
import socket
import time
import cv2

INTERNAL_IP_H2 = "192.168.0.12"
INTERNAL_PORT = 9999
SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

def term_signal_handler(signum, frame):
    print("Received signal to terminate. Exiting...")
    exit(0)

signal.signal(signal.SIGTERM, term_signal_handler)

# Open the video file for reading and extract its metadata
cap = cv2.VideoCapture("python /home/big_buck_bunny_720p_5mb.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create a UDP socket and bind it to the specified IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVICE_IP, SERVICE_PORT))

# Read and send frames from the video file until it's exhausted
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Compress the frame using H.264 and send it over the network
    _, buf = cv2.imencode(".h264", frame, [
        cv2.IMWRITE_H264_PARAMS_KEY,
        dict(
            profile=cv2.VIDEO_WRITER_H264_PROFILE_BASELINE,
            level=cv2.VIDEO_WRITER_H264_LEVEL_3_0,
            keyint=30
        )
    ])
    sock.sendto(buf, (INTERNAL_IP_H2, INTERNAL_PORT))

    # Sleep for a short time to prevent the server from using too much CPU time
    time.sleep(1 / fps)

# Release the video file and close the socket
cap.release()
sock.close()
