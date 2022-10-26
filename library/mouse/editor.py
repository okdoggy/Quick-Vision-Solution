import cv2
import numpy as np

class MouseEvent:
    def __init__(self, logging=True):
        self.logging = logging

        self.circles = []

    def draw_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.logging:
                print(f"event: EVENT_LBUTTONDBLCLK : {x}, {y}")
            self.circles.append([x, y])
        if event == cv2.EVENT_RBUTTONDBLCLK:
            # Delete all circles (clean the screen)
            if self.logging:
                print("event: EVENT_RBUTTONDBLCLK")
            self.circles[:] = []
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.logging:
                print("event: EVENT_RBUTTONDOWN")
            try:
                self.circles.pop()
            except (IndexError):
                print("no circles to delete")


def perspective_transform(frame, pts):
    if len(pts) == 4:
        sm = pts.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산
        diff = np.diff(pts, axis=1)  # 4쌍의 좌표 각각 x-y 계산

        topLeft = pts[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
        bottomRight = pts[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
        topRight = pts[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
        bottomLeft = pts[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

        pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

        w1 = abs(bottomRight[0] - bottomLeft[0])
        w2 = abs(topRight[0] - topLeft[0])
        h1 = abs(topRight[1] - bottomRight[1])
        h2 = abs(topLeft[1] - bottomLeft[1])
        width = max([w1, w2])
        height = max([h1, h2])

        pts2 = np.float32([[0, 0], [width - 1, 0],
                           [width - 1, height - 1], [0, height - 1]])

        mtrx = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(frame, mtrx, (width, height))

        return result


if __name__ == '__main__':
    editor = MouseEvent()

    cv2.namedWindow('Image mouse')
    cv2.setMouseCallback('Image mouse', editor.draw_circle)

    webcam = True
    if webcam:
        cap = cv2.VideoCapture(0)
    else:
        import os
        files = []
        imagefiles = os.listdir('images/')
        for name in imagefiles:
            if name.endswith('jpg') or name.endswith('jpeg'):
                files.append(name)

    count = 0

    while True:
        if webcam:
            ret, frame = cap.read()
            if not ret: break

        else:
            frame = cv2.imread(os.path.join('images/', files[count]))
            if min(frame.shape[0], frame.shape[1]) < 400:
                count += 1

        dst = frame.copy()

        for index, pos in enumerate(editor.circles):
            cv2.circle(dst, pos, 10, (255, 0, 255), -1)
            cv2.putText(dst, f'{index+1}', pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))

        cv2.imshow('Image mouse', dst)

        # Continue until 'q' is pressed:
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('w'):
            cut_image = perspective_transform(frame, np.array(editor.circles))
            fname = f'crop_{count}.png'
            cv2.imwrite(fname, cut_image)
            print(f'saved {fname}')
            count += 1

    # Destroy all generated windows:
    cv2.destroyAllWindows()
