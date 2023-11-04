import cv2
import cv2.aruco as aruco
import numpy as np

# Load your image
image_path = 'test_images/test_img2.jpeg'  # Replace with your image file path
frame = cv2.imread(image_path)

# Initialize ArUco dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)
aruco_square_length = 200

# Set camera parameters (you need to calibrate your camera for accurate results)
camera_matrix = np.load('camera_matrix.npy')
dist_coeffs = np.load('dist_coeffs.npy')

# Detect ArUco tags
corners, ids, rejected = detector.detectMarkers(frame)
img = aruco.drawDetectedMarkers(frame, corners, ids)

if ids is not None:
  # Calculate camera pose for each detected tag
  rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, aruco_square_length, camera_matrix, dist_coeffs)

  # Visualize the pose (e.g., draw axis on the tag)
  for i in range(len(ids)):
    frame = cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec[i], tvec[i], 100)
    t = tvec[0]
    print(t)
    print(rvec)
    position = f"Position: X={t[0][0]:.2f}, Y={t[0][1]:.2f}, Z={t[0][2]:.2f}"
    cv2.putText(img, position, (10, (30 + i * 20) * 3), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

# Display the image with pose estimation
cv2.imshow("ArUco Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
