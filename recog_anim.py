import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer


class YamunaAnimation(QMainWindow):
    def __init__(self, video_path):
        super().__init__()

        # 🔹 Transparent Frameless Window
        self.setWindowTitle("Voice Animation")
        self.setGeometry(1250, 550, 640, 480)  # Position and size
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 🔹 Video Label
        self.label = QLabel(self)
        self.label.setGeometry(190, 0, 465, 535)
        self.label.setAlignment(Qt.AlignCenter)

        # 🎥 Load Video File Using OpenCV
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        # ✅ Reduce CPU Usage: Lower Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # 🕒 Optimized Timer for Smooth Playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS (Smooth Playback)

        # Hide the animation initially
        self.is_active = False
        self.hide()

    def update_frame(self):
        """ Optimized frame update for smooth, translucent animation """
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            return

        # Convert BGR to RGBA (adding alpha channel)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        # Apply transparency (adjust alpha values)
        alpha = 150  # Adjust between 0 (fully transparent) to 255 (fully visible)
        frame[:, :, 3] = alpha

        height, width, channel = frame.shape
        bytes_per_line = 4 * width  # 4 channels (RGBA)

        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        self.label.setPixmap(QPixmap.fromImage(q_image))


    def show_overlay(self):
        """ Display animation when Yamuna starts listening """
        if not self.is_active:
            self.show()
            self.is_active = True
            self.timer.start(33)  # Start video loop (~30 FPS)
            # Hide animation automatically after 2 seconds

    '''def hide_overlay(self):
        """ Hide animation when Yamuna stops listening """
        self.timer.stop()
        self.hide()
        self.is_active = False'''


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 🔹 Set Video Path (Ensure It's a Transparent MP4)
    video_path = "animation.mp4"
    animation_overlay = YamunaAnimation(video_path)
    
    animation_overlay.show_overlay()  # Show animation while listening

    # Wait for animation to finish, then quit app
    QTimer.singleShot(5000, QApplication.quit)  # ✅ Exit app after 5 seconds

    sys.exit(app.exec_())  # Start the app loop
