
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
        self.color_axis = self.request.get_param("ConfigColorAxis")
        self.load_parameters()
        self.load_colors()

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {"colors": [], "palette_name": [], "palette": [], "color_map": {}}

    def load_parameters(self) -> None:
        self.colors = self.bootstrap["colors"]
        self.palette_name = self.request.get_param("ConfigColorPalette")
        if self.palette_name == "custom":
            self.palette = self.request.get_param("configCustomColors")
        else:
            self.palette = self.request.get_param("ConfigPaletteSize")
        self.config_thickness = self.request.get_param("ConfigThickness")
        self.radius = self.request.get_param("ConfigRadius")

    def load_colors(self) -> None:
        if self.colors is None or self.palette_name != self.bootstrap["palette_name"] or self.palette != self.bootstrap["palette"]:
            self.colors = []
            self.bootstrap["color_map"] = {}
            if self.palette_name == "custom":
                for color_str in self.palette.split(','):
                    clean_hex = color_str.strip().lstrip('#')

                    if len(clean_hex) == 6:
                        bgr = (
                            int(clean_hex[4:6], 16),
                            int(clean_hex[2:4], 16),
                            int(clean_hex[0:2], 16)
                        )
                        self.colors.append(bgr)
            else:
                cmap = plt.get_cmap(self.palette_name).colors
                self.colors = [
                    tuple(int(255 * r) for r in cmap[i % len(cmap)])
                    for i in range(self.palette)
                ]
        self.bootstrap["colors"] = self.colors
        self.bootstrap["palette_name"] = self.palette_name
        self.bootstrap["palette"] = self.palette

    def select_color(self):
        num_items = len(self.detections)
        color_map = self.bootstrap["color_map"]
        if self.color_axis == "Class":
            class_ids = [det["classId"] for det in self.detections]
            color_dict = {}
            for class_id in class_ids:
                if class_id not in color_map:
                    next_index = len(color_map) % len(self.colors)
                    color_map[class_id] = self.colors[next_index]
                color_dict[class_id] = color_map[class_id]
            self.bootstrap["color_map"] = color_map

        elif self.color_axis == "Index":
            color_dict = {idx: self.colors[idx % len(self.colors)] for idx in range(num_items)}

        else:
            track_ids = [det["trackerID"] for det in self.detections]
            color_dict = {}
            for track_id in track_ids:
                if track_id not in color_map:
                    next_index = len(color_map) % len(self.colors)
                    color_map[track_id] = self.colors[next_index]
                color_dict[track_id] = color_map[track_id]

            self.bootstrap["color_map"] = color_map

        return color_dict

    def bounding_rectangle(self, image, color_dict):
        """
                Calculates and draws the Rotated Bounding Rectangle.
                Logic:
                1. Check for 'keyPoints' (from Segmentation).
                2. If found -> Calculate MinAreaRect -> Draw Rotated Rectangle.
                3. If not found -> Fallback to standard BoundingBox.
                """
        for idx, detection in enumerate(self.detections):

            # 1. SETUP DATA
            # Handle dictionary vs object access
            is_dict = isinstance(detection, dict)

            # Get KeyPoints (The Polygon Mask)
            key_points = detection.get("keyPoints") if is_dict else getattr(detection, "keyPoints", None)

            # Get Basic Box (Fallback)
            bbox = detection.get("boundingBox") if is_dict else getattr(detection, "boundingBox", None)

            if not bbox and not key_points:
                continue

            # Get Color
            class_id = detection.get("classId") if is_dict else getattr(detection, "classId", 0)
            tracker_id = detection.get("trackerID", 0) if is_dict else getattr(detection, "trackerID", 0)

            if self.color_axis == "Class":
                color = color_dict[class_id]
            elif self.color_axis == "Index":
                color = color_dict[idx]
            else:
                color = color_dict[tracker_id]

            # --- 2. LOGIC: ROTATED RECTANGLE (From Segmentation) ---
            if key_points and len(key_points) >= 3:
                # Convert KeyPoints to numpy array of points [[x,y], [x,y]...]
                # Note: Check if key_points is a list of dicts or list of objects
                pts = []
                for kp in key_points:
                    # Support both object access (kp.cx) and dict access (kp['cx'])
                    cx = kp.get('cx') if isinstance(kp, dict) else kp.cx
                    cy = kp.get('cy') if isinstance(kp, dict) else kp.cy
                    pts.append([int(cx), int(cy)])

                pts_np = np.array(pts, dtype=np.int32)

                # Calculate the Rotated Rectangle (The Physics!)
                # returns ((cx, cy), (w, h), angle)
                rect = cv2.minAreaRect(pts_np)

                # Convert to 4 corner points
                box_points = cv2.boxPoints(rect)
                box_points = np.int0(box_points)  # Convert to integer

                # Draw it!
                cv2.drawContours(image, [box_points], 0, color, self.config_thickness)

            # --- 3. LOGIC: STANDARD BOX (Fallback) ---
            elif bbox:
                # Fallback to standard upright box if no segmentation mask exists
                left = bbox.get("left") if isinstance(bbox, dict) else bbox.left
                top = bbox.get("top") if isinstance(bbox, dict) else bbox.top
                w = bbox.get("width") if isinstance(bbox, dict) else bbox.width
                h = bbox.get("height") if isinstance(bbox, dict) else bbox.height

                x1, y1 = int(left), int(top)
                x2, y2 = int(left + w), int(top + h)

                # Use your existing Radius logic for standard boxes
                if self.radius > 0:
                    # (Your existing radius drawing code...)
                    # Shortened for brevity, paste your specific radius code here if needed
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, self.config_thickness)
                else:
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, self.config_thickness)
        return image

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.bounding_rectangle(img.value, self.select_color())
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()