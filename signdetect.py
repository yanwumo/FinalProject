import time

import cv2


def detect_haar(classifier, gray, example=False):
    """
    Determines whether the input image contains a stop sign using the trained Haar classifier.
    If <example> is set, also draws a rectangle around the detected sign and displays the image.
    """

    # Detect any stop signs in the image using the classifier at various scales.
    stop_signs = classifier.detectMultiScale(gray, 1.02, 10)

    if example:
        # Draw a rectangle around each detected sign and display it. 
        for (x, y, w, h) in stop_signs:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("img", gray)
        cv2.waitKey(1)

    # True if any signs were detected.
    return stop_signs
