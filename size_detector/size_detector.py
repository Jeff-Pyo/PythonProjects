import cv2
# Import the OpenCV library for image processing
# from object_detector import *
# If you have a custom object detector, you can import it here

class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert the input image to grayscale, as it is easier to work with

        # Create a Mask with adaptive threshold
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
        # Apply an adaptive threshold to the grayscale image, to create a binary mask
        # This mask will help us to segment the foreground objects from the background

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Find the contours of the objects in the binary mask
        # RETR_EXTERNAL retrieves only the extreme outer contours, while CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments and leaves only their end points

        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Calculate the area of the contour
            if area > 2000:
                objects_contours.append(cnt)
                # If the area of the contour is larger than a certain threshold, add it to the list of objects

        return objects_contours

# Load Image
img = cv2.imread('abc.jpg')
# Load the input image

# Create HomogeneousBgDetector object
detector = HomogeneousBgDetector()
# Create an instance of the object detector

# Detect Objects and Contours
contours = detector.detect_objects(img)
# Detect the objects in the input image, and get their contours

# Calculate Sizes and Sort in descending order
sizes = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    # Get the bounding rectangle of the contour
    sizes.append(w * h)
    # Calculate the size of the contour by multiplying its width and height
sizes.sort(reverse=True)
# Sort the sizes of the objects in descending order, so that the largest objects come first

# Draw Labels
font = cv2.FONT_HERSHEY_SIMPLEX
# Choose a font for the labels
font_scale = 1.5
# Set the font scale
font_thickness = 3
# Set the font thickness
color = (0, 0, 255)
# Set the color of the labels
label_id = 1

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    # Get the bounding rectangle of the contour
    size = w * h
    # Calculate the size of the contour by multiplying its width and height
    size_rank = sizes.index(size) + 1
    # Get the rank of the object based on its size
    label_text = str(size_rank)
    # Convert the rank to a string
    label_size, _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
    # Get the size of the label text
    cv2.putText(img, label_text, (int(x+w/2-label_size[0]/2), int(y+h/2+label_size[1]/2)), font, font_scale, color, font_thickness, cv2.LINE_AA)
    # Draw the label text on the input image, centered on

    if label_id > 5:
        break

centers = []
for cnt in contours:
    # Calculate the moments of the contour
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        # Calculate the center of the contour
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        centers.append((cx, cy))
centers.sort(key=lambda c: c[1], reverse=True)

# Print Sorted Centers
print("Object Centers (sorted by size):")
for i, center in enumerate(centers):
    print(f"{i+1}: ({center[0]}, {center[1]})")

# Display Image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()