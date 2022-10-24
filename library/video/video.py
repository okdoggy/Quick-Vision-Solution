import cv2
from threading import Thread


class WriteVideo:
    def __init__(self, path='record.mp4', fps=30, fourcc='MP4V', logging=True):
        self.video = None
        self.count = 0
        self.fname = path
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.logging = logging

        if self.logging:
            print(f'{__class__.__name__} : file name={self.fname}, fps={self.fps}')

    def write(self, frame):
        if frame is None:
            return

        if self.count == 0 and self.video is None:
            height, width, _ = frame.shape
            self.video = cv2.VideoWriter(self.fname, self.fourcc, self.fps, (width, height))

        self.video.write(frame)

        self.count += 1

    def stop(self):
        self.video.release()
        self.video = None

        if self.logging:
            print(f'{__class__.__name__} : stop {__class__.__name__}')


class ReadVideo:
    def __init__(self, path=0, logging=True):
        self.capture = cv2.VideoCapture(path)
        self.stopped = False
        self.logging = logging

        (self.status, self.frame) = self.capture.read()

        if self.logging:
            print(f'{__class__.__name__} : init {__class__.__name__} {path}')

    def start(self):
        if self.logging:
            print(f'{__class__.__name__} : start {__class__.__name__}')

        Thread(target=self.update, args=()).start()
        #   self.thread.daemon = True
        return self

    def stop(self):
        self.stopped = True
        self.capture.release()

        if self.logging:
            print(f'{__class__.__name__} : stop {__class__.__name__}')


    def update(self):
        while not self.stopped:
            if not self.status:
                self.stop()
            else:
                (self.status, self.frame) = self.capture.read()


class DebugVideo:
    def __init__(self, path=0, logging=True):
        self.capture = cv2.VideoCapture(path)
        self.stopped = False
        self.logging = logging

        (self.status, self.frame) = self.capture.read()
        self.index = self.capture.get(cv2.CAP_PROP_POS_FRAMES)

        if self.logging:
            print(f'{__class__.__name__} : init {__class__.__name__} {path}')

    def start(self):
        if self.logging:
            print(f'{__class__.__name__} : start {__class__.__name__}')

        while not self.stopped:
            if not self.status:
                self.stop()
            else:
                (self.status, self.frame) = self.capture.read()
                self.index += 1

            cv2.imshow(f'{__class__.__name__}', self.frame)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                self.stop()
            elif key == ord('a'):
                self.index -= 2
                if self.index < 0:
                    self.index = 0
                    if self.logging:
                        print(f"{__class__.__name__} : index < 0, don't move index.")
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.index)
            elif key == ord('A'):
                if self.index > 10:
                    self.index -= 10
                else:
                    self.index -= 1
                    if self.logging:
                        print(f"{__class__.__name__} : index < 0, don't move index.")
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.index)

            if self.logging:
                print(f'{__class__.__name__} : index = {self.index}')

    def stop(self):
        self.stopped = True
        self.capture.release()

        if self.logging:
            print(f'{__class__.__name__} : stop {__class__.__name__}')




def example():
    logging = True
    show = True
    video = WriteVideo()
    reading = ReadVideo().start()

    while True:
        try:
            if reading.stopped:
                reading.stop()
                video.stop()
                break

            frame = reading.frame
            video.write(frame)

            if show:
                cv2.imshow('test', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    reading.stopped = True

        except AttributeError:
            print("AttributeError")
            pass

    reading.capture.release()
    cv2.destroyAllWindows()


def example2():
    debug = DebugVideo('record.mp4')
    debug.start()
    debug.stop()


if __name__ == '__main__':
    example()
    # example2()
