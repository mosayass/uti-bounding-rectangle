
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
            # Handle dictionary vs object access
            is_dict = isinstance(detection, dict)

            # Get KeyPoints (The Polygon Mask)
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

                # 3. Create the new Bounding Box Object
                # CRITICAL FIX: Cast numpy ints to standard python ints using int()
                # Otherwise, JSON serialization will fail silently.
                new_bbox = {
                    "left": int(x),
                    "top": int(y),
                    "width": int(w),
                    "height": int(h)
                }

                # 4. Update the Detection Object
                if is_dict:
                    detection["boundingBox"] = new_bbox
                else:
                    # Depending on your object structure, you might need to instantiate a class
                    # or just assign values if the attribute already exists.
                    if hasattr(detection, 'boundingBox') and detection.boundingBox is not None:
                        detection.boundingBox.left = int(x)
                        detection.boundingBox.top = int(y)
                        detection.boundingBox.width = int(w)
                        detection.boundingBox.height = int(h)
                    else:
                        # If it's None, you might need to assign a dict or object based on your framework
                        # Assuming simple assignment works for now:
                        detection.boundingBox = new_bbox

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