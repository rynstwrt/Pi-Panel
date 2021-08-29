import cv2


def camera(frame):
    return frame


def edge_detection(frame):
    return cv2.Canny(frame, 100, 300)


def cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)

    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon