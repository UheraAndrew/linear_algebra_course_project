import cv2
import numpy as np

from config import dnn_classes, dnn_config, dnn_weights


class Detect:
    def __init__(self, weights, config, classes):
        self.classes = classes
        with open(self.classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.image = None
        self.Width = None
        self.Height = None
        self.scale = 0.00392
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4
        self.net = cv2.dnn.readNet(weights, config)

    def take_image(self, img):
        self.image = img
        self.Width = self.image.shape[1]
        self.Height = self.image.shape[0]

    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    def detect(self):
        blob = cv2.dnn.blobFromImage(self.image, self.scale, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())
        confidences = []
        boxes = []
        class_ids = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.conf_threshold:
                    center_x = int(detection[0] * self.Width)
                    center_y = int(detection[1] * self.Height)
                    w = int(detection[2] * self.Width)
                    h = int(detection[3] * self.Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)
        user_frames = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            if self.classes[class_ids[i]] == "person":
                user_frames.append([round(x), round(y), round(w), round(h)])
        return user_frames


__detect_obj = Detect(dnn_weights, dnn_config, dnn_classes)


def detect(img):
    __detect_obj.take_image(img)
    return __detect_obj.detect()
