
import os
import sys
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BoundingRectangle.src.utils.response import build_response
from components.BoundingRectangle.src.models.PackageModel import PackageModel
from sdks.novavision.src.base.model import ROI

class BoundingRectangle(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.detections = self.request.get_param("inputDetections")


    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_detections(self):
        """
        Iterates through detections. If a segmentation mask (keyPoints) exists,
        it calculates the upright bounding box for that mask and updates
        the detection's 'boundingBox' field.
        """
        if not self.detections:
            return []

        for detection in self.detections:
            # Check if we are dealing with a Dictionary or an Object
            is_dict = isinstance(detection, dict)

            # Get KeyPoints safely
            key_points = detection.get("keyPoints") if is_dict else getattr(detection, "keyPoints", None)

            if key_points and len(key_points) >= 3:
                # 1. Convert KeyPoints to numpy array
                pts = []
                for kp in key_points:
                    cx = kp.get('cx') if isinstance(kp, dict) else kp.cx
                    cy = kp.get('cy') if isinstance(kp, dict) else kp.cy
                    pts.append([int(cx), int(cy)])

                pts_np = np.array(pts, dtype=np.int32)

                # 2. Calculate the Standard Upright Bounding Box
                x, y, w, h = cv2.boundingRect(pts_np)

                # 3. CRITICAL FIX: Convert Numpy Ints to Standard Python Ints
                # JSON cannot serialize numpy types, causing "No Output" errors.
                x, y, w, h = int(x), int(y), int(w), int(h)

                # 4. Update the Detection Object
                if is_dict:
                    # If input is a Dict, we assign a Dict
                    detection["boundingBox"] = {
                        "left": x, "top": y, "width": w, "height": h
                    }
                else:
                    # If input is an Object, we MUST assign an ROI Object.
                    # Assigning a dict to an object field causes validation crashes.
                    if 'ROI' in globals():
                        detection.boundingBox = ROI(left=x, top=y, width=w, height=h)
                    else:
                        # Fallback if ROI isn't imported (but please import it!)
                        # We try to construct a simple object structure if needed
                        class TempROI:
                            pass
                        temp = TempROI()
                        temp.left, temp.top, temp.width, temp.height = x, y, w, h
                        detection.boundingBox = temp

        return self.detections

    def run(self):
        # We process the data (Detections)
        self.detections = self.process_detections()

        # We pass the image through (unmodified) and the updated detections
        # Note: We usually don't need to 'set_frame' if we didn't draw on it,
        # but we keep the flow consistent.

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()