import cv2
import time

# Load the pre-trained eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Start video capture from the webcam (change the argument to 1 for external cameras)
cap = cv2.VideoCapture(0)

# Parameters for determining focus
not_focused_threshold = 12  # Number of consecutive frames without eyes to consider as not focused
not_focused_counter = 0  # Counter to track consecutive frames without eyes
not_focused_duration_threshold = 3  # Duration (in seconds) to consider as "not focused"

# Initialize time variables
start_time = time.time()
focus_durations = []
focus_loss_timestamps = []

is_focused = True  # Track the focus state

while True:
    # Read the video frame
    ret, frame = cap.read()

    # Convert the frame to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the grayscale frame
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(eyes) == 0:
        # No eyes detected
        not_focused_counter += 1
        if not_focused_counter >= not_focused_threshold and is_focused:
            # If consecutive frames without eyes exceed the threshold and currently in focused state
            elapsed_time = time.time() - start_time
            if elapsed_time >= not_focused_duration_threshold:
                is_focused = False
                print("Not focused")

                # Calculate focus duration
                focus_duration = elapsed_time
                focus_durations.append(focus_duration)
                focus_loss_timestamps.append(elapsed_time)

    else:
        # Eyes detected
        not_focused_counter = 0  # Reset the counter

        if not is_focused:
            is_focused = True
            print("Focused")

            # Reset start time for the next focus session
            start_time = time.time()

        # Iterate over the detected eyes
        for (x, y, w, h) in eyes:
            # Draw rectangles around the eyes
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Eye Tracking', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Print and store the focus durations
print("Focus durations:", focus_durations)
print("Time stamps:", focus_loss_timestamps)

# Store the focus durations in a file or database for further analysis
# ... (code for storing the data)
