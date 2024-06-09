import socket
import time
import cv2

SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set up a video capture object to receive and decode the H.264 video stream
    cap = cv2.VideoCapture()
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"H264"))

    # Print a message to indicate that the video is streaming
    print("Video is streaming...")

    while True:
        # Receive the next video frame from the server
        data, _ = sock.recvfrom(1024 * 1024)

        # Decode the H.264 video frame and display it
        ret, frame = cap.decode(data)
        if ret:
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Sleep for a short time to prevent the client from using too much CPU time
        time.sleep(1 / 30)

    # Release the video capture object and close the socket
    cap.release()
    sock.close()

    # Print a message to indicate that the video has stopped
    print("Video has stopped.")