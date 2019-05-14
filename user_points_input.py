import cv2


class Mouse:
    x = 0
    y = 0
    rightClicked = False
    leftClicked = False

    def leftClick(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
            self.leftClicked = True


def get_field_main_points(image, windowName):
    mouse = Mouse()
    cv2.imshow(windowName, image)
    cv2.setMouseCallback(windowName, mouse.leftClick)
    i = 0
    coords = []
    while i < 4:
        i += 1
        mouse.x = 0
        mouse.y = 0
        mouse.leftClicked = False
        while mouse.leftClicked == False:
            key = cv2.waitKey(1) & 0xFF
        coords.append((mouse.x, mouse.y))
    cv2.destroyAllWindows()
    return coords
