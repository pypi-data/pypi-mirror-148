import math

import cv2

try:
  from PyQt6.QtCore import pyqtSignal, Qt, QAbstractAnimation, QEventLoop, QLine, QParallelAnimationGroup, QPoint, QPointF, QPropertyAnimation, QRectF, QSize, QSizeF, QTimer
  from PyQt6.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QPixmap, QPolygonF, QTransform
  from PyQt6.QtWidgets import QApplication, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGridLayout, QLabel, QLayout, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, QSlider, QSpinBox, QToolButton, QToolTip, QVBoxLayout, QWidget
  PYQT6 = True
except ImportError:
  from PyQt5.QtCore import pyqtSignal, Qt, QAbstractAnimation, QEventLoop, QLine, QParallelAnimationGroup, QPoint, QPointF, QPropertyAnimation, QRectF, QSize, QSizeF, QTimer
  from PyQt5.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QPixmap, QPolygonF, QTransform
  from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGridLayout, QLabel, QLayout, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, QSlider, QSpinBox, QToolButton, QToolTip, QVBoxLayout, QWidget
  PYQT6 = False

import zebrazoom.videoFormatConversion.zzVideoReading as zzVideoReading


PRETTY_PARAMETER_NAMES = {
  'frameGapComparision': 'Compare frame n with frame n+?',
  'thresForDetectMovementWithRawVideo': 'Threshold applied on frame n+? minus frame n',
  'halfDiameterRoiBoutDetect': 'Size of sub-frame used for the comparison',
  'minNbPixelForDetectMovementWithRawVideo': 'Minimum number of white pixels in frame n+? minus frame n for bout detection',
  'headEmbededAutoSet_BackgroundExtractionOption': 'Background Extraction',
  'overwriteFirstStepValue': 'Minimum number of pixels between subsequent points',
  'overwriteLastStepValue': 'Maximum number of pixels between subsequent points',
  'overwriteHeadEmbededParamGaussianBlur': 'Gaussian blur applied on the image',
}

TITLE_FONT = QFont('Helvetica', 18, QFont.Weight.Bold, True)
LIGHT_YELLOW = '#FFFFE0'
LIGHT_CYAN = '#E0FFFF'
LIGHT_GREEN = '#90ee90'
GOLD = '#FFD700'
SPINBOX_STYLESHEET = '''
QSpinBox::down-button  {
  subcontrol-origin: border;
  subcontrol-position: center left;
  height: 20;
  width: 20;
}

QSpinBox::up-button  {
  subcontrol-origin: border;
  subcontrol-position: center right;
  height: 20;
  width: 20;
}'''


def apply_style(widget, **kwargs):
    font = kwargs.pop('font', None)
    if font is not None:
        widget.setFont(font)
    widget.setStyleSheet(';'.join('%s: %s' % (prop.replace('_', '-'), val)  for prop, val in kwargs.items()))
    return widget


def transformCoordinates(fromRect, toRect, point):
  transform = QTransform()
  QTransform.quadToQuad(QPolygonF((fromRect.topLeft(), fromRect.topRight(), fromRect.bottomLeft(), fromRect.bottomRight())),
                        QPolygonF((toRect.topLeft(), toRect.topRight(), toRect.bottomLeft(), toRect.bottomRight())), transform)
  return transform.map(point)


def _dialogClosed(loop, fn):
  def inner(*args, **kwargs):
    loop.exit()
    return fn(*args, **kwargs)
  return inner


def _getButtonsLayout(buttons, loop, dialog=None):
  buttonsLayout = QHBoxLayout()
  buttonsLayout.addStretch()

  def callback(cb):
    if cb is not None:
      cb()
    if dialog is not None:
      dialog.close()
    else:
      loop.exit()

  for text, *args in buttons:
    if len(args) == 1:
      cb, = args
      exitLoop = True
      enabledSignal = None
    elif len(args) == 2:
      cb, exitLoop = args
      enabledSignal = None
    else:
      assert len(args) == 3
      cb, exitLoop, enabledSignal = args
    button = QPushButton(text)
    if enabledSignal is not None:
      button.setEnabled(False)
      enabledSignal.connect(lambda enabled, btn=button: btn.setEnabled(bool(enabled)))
    if exitLoop:
      button.clicked.connect(lambda *args, cb=cb: callback(cb))
    else:
      button.clicked.connect(cb)
    buttonsLayout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
  buttonsLayout.addStretch()
  return buttonsLayout


def showBlockingPage(layout, title=None, buttons=(), dialog=False, labelInfo=None, exitSignals=()):
  loop = QEventLoop()
  for signal in exitSignals:
    signal.connect(lambda *args: loop.exit())
  mainLayout = QVBoxLayout()
  if title is not None:
    mainLayout.addWidget(apply_style(QLabel(title), font=TITLE_FONT), alignment=Qt.AlignmentFlag.AlignCenter)
  mainLayout.addLayout(layout)
  mainLayout.addLayout(_getButtonsLayout(buttons, loop))
  app = QApplication.instance()
  assert app is not None
  temporaryPage = QWidget()
  temporaryPage.setLayout(mainLayout)
  stackedLayout = app.window.centralWidget().layout()
  stackedLayout.addWidget(temporaryPage)
  oldWidget = stackedLayout.currentWidget()
  with app.suppressBusyCursor():
    stackedLayout.setCurrentWidget(temporaryPage)
    if labelInfo is not None:
      if len(labelInfo) == 2:
        img, label = labelInfo
        zoomable = False
      else:
        assert len(labelInfo) == 3
        img, label, zoomable = labelInfo
      label.setMinimumSize(1, 1)
      label.show()
      setPixmapFromCv(img, label, zoomable=zoomable)
    loop.exec()
    stackedLayout.setCurrentWidget(oldWidget)
  stackedLayout.removeWidget(temporaryPage)


def showDialog(layout, title=None, buttons=(), dialog=False, labelInfo=None, timeout=None):
  dialog = QWidget()
  loop = QEventLoop()
  mainLayout = QVBoxLayout()
  mainLayout.addLayout(layout)
  mainLayout.addLayout(_getButtonsLayout(buttons, loop, dialog=dialog))
  app = QApplication.instance()
  if app is not None:
    app.registerWindow(dialog)
  dialog.setWindowTitle(title)
  dialog.move(0, 0)
  dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
  dialog.setLayout(mainLayout)
  if labelInfo is not None:
    img, label = labelInfo
    height, width = img.shape[:2]
    label.setMinimumSize(width, height)
    layoutSize = mainLayout.totalSizeHint()
    label.setMinimumSize(1, 1)
  else:
    layoutSize = mainLayout.totalSizeHint()
  screenSize = QApplication.primaryScreen().availableSize()
  if app is not None:
    screenSize -= app.window.frameSize() - app.window.size()
  if layoutSize.width() > screenSize.width() or layoutSize.height() > screenSize.height():
    layoutSize.scale(screenSize, Qt.AspectRatioMode.KeepAspectRatio)
  dialog.setFixedSize(layoutSize)
  dialog.show()
  if labelInfo is not None:
    setPixmapFromCv(*labelInfo, preferredSize=QSize(width, height).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))
  dialog.closeEvent = _dialogClosed(loop, dialog.closeEvent)
  if timeout is not None:
    QTimer.singleShot(timeout, lambda: dialog.close())
  loop.exec()

def _cvToPixmap(img):
  if len(img.shape) == 2:
    height, width = img.shape
    fmt = QImage.Format.Format_Grayscale8
    bytesPerLine = width
  else:
    assert len(img.shape) == 3
    height, width, channels = img.shape
    fmt = QImage.Format.Format_BGR888
    bytesPerLine = width * channels
  return QPixmap.fromImage(QImage(img.data.tobytes(), width, height, bytesPerLine, fmt))


class ZoomableImage(QGraphicsView):
  pointSelected = pyqtSignal(QPoint)
  proceed = pyqtSignal()

  def __init__(self, parent=None):
    super(ZoomableImage, self).__init__(parent)
    self._zoom = 0
    self._scene = QGraphicsScene(self)
    self._pixmap = QGraphicsPixmapItem()
    self._scene.addItem(self._pixmap)
    self.setScene(self._scene)
    self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setFrameShape(QFrame.Shape.NoFrame)
    self._point = None
    self._dragging = False
    self._tooltipShown = False

  def fitInView(self):
    rect = QRectF(self._pixmap.pixmap().rect())
    self.setSceneRect(rect)
    unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
    self.scale(1 / unity.width(), 1 / unity.height())
    viewrect = self.viewport().rect()
    scenerect = self.transform().mapRect(rect)
    factor = min(viewrect.width() / scenerect.width(),
                 viewrect.height() / scenerect.height())
    self.scale(factor, factor)
    self._zoom = 0

  def setPixmap(self, pixmap):
    self._zoom = 0
    self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
    self._pixmap.setPixmap(pixmap)
    self.fitInView()

  def _update(self, scaleFactor):
    if self._zoom > 0:
      self.scale(scaleFactor, scaleFactor)
    elif self._zoom == 0:
      self.fitInView()
    else:
      self._zoom = 0

  def wheelEvent(self, evt):
    if evt.angleDelta().y() > 0:
      self._zoom += 1
      self._update(1.25)
    else:
      self._zoom -= 1
      self._update(0.8)

  def keyPressEvent(self, evt):
    if self._point is not None and (evt.key() == Qt.Key.Key_Enter or evt.key() == Qt.Key.Key_Return):
      self.proceed.emit()
      return
    elif evt.modifiers() & Qt.KeyboardModifier.ControlModifier:
      if evt.key() == Qt.Key.Key_Plus:
        self._zoom += 1
        self._update(1.25)
        return
      if evt.key() == Qt.Key.Key_Minus:
        self._zoom -= 1
        self._update(0.8)
        return
    super().keyPressEvent(evt)

  def mouseMoveEvent(self, evt):
    if evt.buttons() == Qt.MouseButton.LeftButton and not self._dragging:
      self._dragging = True
      QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
    super().mouseMoveEvent(evt)

  def mouseReleaseEvent(self, evt):
    if not self._dragging:
      if self._pixmap.isUnderMouse():
        self._point = self.mapToScene(evt.pos()).toPoint()
        self.viewport().update()
        self.pointSelected.emit(self._point)
        if not self._tooltipShown:
          QToolTip.showText(self.mapToGlobal(self._point), "If you aren't satisfied with the selection, click again.", self, self.rect(), 5000)
          self._tooltipShown = True
    else:
      self._dragging = False
      QApplication.restoreOverrideCursor()
    super(ZoomableImage, self).mouseReleaseEvent(evt)

  def paintEvent(self, evt):
    super().paintEvent(evt)
    if self._point is None:
      return
    qp = QPainter(self.viewport())
    if self._point is not None:
      qp.setBrush(QColor(255, 0, 0))
      qp.setPen(Qt.PenStyle.NoPen)
      qp.drawEllipse(self.mapFromScene(QPointF(self._point)), 2, 2)
    qp.end()

  def enterEvent(self, evt):
    QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
    super().enterEvent(evt)

  def leaveEvent(self, evt):
    QApplication.restoreOverrideCursor()
    super().leaveEvent(evt)


def setPixmapFromCv(img, label, preferredSize=None, zoomable=False):
  originalPixmap = _cvToPixmap(img)
  if not label.isVisible():
    label.setPixmap(originalPixmap)
    return
  scaling = label.devicePixelRatio() if PYQT6 else label.devicePixelRatioF()
  if label.pixmap() is None or label.pixmap().isNull():
    label.hide()
    label.setPixmap(originalPixmap)
    label.show()
  if preferredSize is None:
    preferredSize = label.pixmap().size()
  size = preferredSize.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
  if not zoomable:
    img = cv2.resize(img, (int(size.width() * scaling), int(size.height() * scaling)))
    pixmap = _cvToPixmap(img)
    pixmap.setDevicePixelRatio(scaling)
    label.setPixmap(pixmap)
  else:
    label.hide()
    image = ZoomableImage()
    image.sizeHint = lambda: size
    image.viewport().setFixedSize(size)
    image.setPixmap(originalPixmap)
    label.parentWidget().layout().replaceWidget(label, image)
    image.setFocus()
    if hasattr(image, "pointSelected"):
      def pointSelected(point):
        label.pointSelected.emit(point)
        label.getCoordinates = lambda: (point.x(), point.y())
      image.pointSelected.connect(pointSelected)
      image.proceed.connect(label.proceed.emit)


class SliderWithSpinbox(QWidget):
  valueChanged = pyqtSignal(int)

  def __init__(self, value, minimum, maximum, name=None):
    super().__init__()
    minimum = int(minimum)
    maximum = int(maximum)

    layout = QGridLayout()
    layout.setRowStretch(0, 1)
    layout.setColumnStretch(0, 1)
    layout.setRowStretch(3, 1)
    layout.setColumnStretch(5, 1)
    layout.setVerticalSpacing(0)

    minLabel = QLabel(str(minimum))
    layout.addWidget(minLabel, 1, 1, Qt.AlignmentFlag.AlignLeft)
    maxLabel = QLabel(str(maximum))
    layout.addWidget(maxLabel, 1, 3, Qt.AlignmentFlag.AlignRight)
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setMinimumWidth(350)
    slider.setRange(minimum, maximum)
    slider.setValue(value)
    layout.addWidget(slider, 2, 1, 1, 3)

    spinbox = QSpinBox()
    spinbox.setStyleSheet(SPINBOX_STYLESHEET)
    spinbox.setMinimumWidth(90)
    spinbox.setRange(minimum, maximum)
    spinbox.setValue(value)
    layout.addWidget(spinbox, 2, 4)

    def spinboxValueChanged():
      value = spinbox.value()
      slider.setValue(value)
      self.valueChanged.emit(value)
    spinbox.valueChanged.connect(spinboxValueChanged)
    slider.valueChanged.connect(lambda: spinbox.setValue(slider.value()))

    layout.setContentsMargins(20, 5, 20, 5)
    self.setLayout(layout)

    if name is not None:
      self.setFixedWidth(layout.totalSizeHint().width())
      titleLabel = QLabel(PRETTY_PARAMETER_NAMES.get(name, name))
      titleLabel.setMinimumSize(1, 1)
      titleLabel.resizeEvent = lambda evt: titleLabel.setMinimumWidth(evt.size().width()) or titleLabel.setWordWrap(evt.size().width() <= titleLabel.sizeHint().width())
      slider.rangeChanged.connect(lambda: titleLabel.setMinimumWidth(1) or titleLabel.setWordWrap(False))
      layout.addWidget(titleLabel, 1, 2, Qt.AlignmentFlag.AlignCenter)

    self.value = spinbox.value
    self.minimum = spinbox.minimum
    self.maximum = spinbox.maximum
    self.setValue = lambda value: spinbox.setValue(value) or slider.setValue(value)
    self.setMinimum = lambda min_: spinbox.setMinimum(min_) or slider.setMinimum(min_) or minLabel.setText(str(int(min_)))
    self.setMaximum = lambda max_: spinbox.setMaximum(max_) or slider.setMaximum(max_) or maxLabel.setText(str(int(max_)))
    self.setRange = lambda min_, max_: spinbox.setRange(min_, max_) or slider.setRange(min_, max_)
    self.isSliderDown = slider.isSliderDown
    self.sliderWidth = slider.width
    self.setPosition = slider.setSliderPosition


def _chooseFrameLayout(cap, spinboxValues, title, titleStyle=None):
  if titleStyle is None:
    titleStyle = {'font': TITLE_FONT}
  layout = QVBoxLayout()
  titleLabel = apply_style(QLabel(title), **titleStyle)
  titleLabel.setMinimumSize(1, 1)
  titleLabel.resizeEvent = lambda evt: titleLabel.setMinimumWidth(evt.size().width()) or titleLabel.setWordWrap(evt.size().width() <= titleLabel.sizeHint().width())
  layout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
  video = QLabel()
  layout.addWidget(video, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

  firstFrame, minFrame, maxFrame = spinboxValues
  frameSlider = SliderWithSpinbox(firstFrame, minFrame, maxFrame, name="Frame")

  def getFrame():
    cap.set(1, frameSlider.value())
    ret, img = cap.read()
    return img
  frameSlider.valueChanged.connect(lambda: setPixmapFromCv(getFrame(), video))

  sublayout = QHBoxLayout()
  sublayout.addStretch(1)
  sublayout.addWidget(frameSlider, alignment=Qt.AlignmentFlag.AlignCenter)
  if maxFrame > 1000:
    adjustLayout = QVBoxLayout()
    adjustLayout.setSpacing(0)
    adjustLayout.addStretch()
    zoomInSliderBtn = QPushButton("Zoom in slider")

    def updatePreciseFrameSlider(value):
      if frameSlider.minimum() == value and frameSlider.minimum():
        frameSlider.setMinimum(frameSlider.minimum() - 1)
        frameSlider.setMaximum(frameSlider.maximum() - 1)
      elif value == frameSlider.maximum() and frameSlider.maximum() != maxFrame:
        frameSlider.setMinimum(frameSlider.minimum() + 1)
        frameSlider.setMaximum(frameSlider.maximum() + 1)

    def zoomInButtonClicked():
      if "in" in zoomInSliderBtn.text():
        zoomInSliderBtn.setText("Zoom out slider")
        value = frameSlider.value()
        minimum = value - 250
        maximum = value + 250
        if minimum < 0:
          maximum = 500
          minimum = 0
        if maximum > frameSlider.maximum():
          maximum = frameSlider.maximum()
          minimum = maximum - 500
        frameSlider.setMinimum(max(0, minimum))
        frameSlider.setMaximum(min(frameSlider.maximum(), maximum))
        frameSlider.setValue(value)
        frameSlider.valueChanged.connect(updatePreciseFrameSlider)
      else:
        zoomInSliderBtn.setText("Zoom in slider")
        frameSlider.setMinimum(0)
        frameSlider.setMaximum(maxFrame)
        frameSlider.valueChanged.disconnect(updatePreciseFrameSlider)
    zoomInSliderBtn.clicked.connect(zoomInButtonClicked)
    adjustLayout.addWidget(QLabel())
    adjustLayout.addWidget(zoomInSliderBtn, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1)
    adjustLayout.addStretch()
    sublayout.addLayout(adjustLayout, stretch=1)
  else:
    sublayout.addStretch(1)
  layout.addLayout(sublayout)

  return layout, video, frameSlider

def chooseBeginningPage(app, videoPath, title, chooseFrameBtnText, chooseFrameBtnCb, extraButtonInfo=None, titleStyle=None, additionalLayout=None):
  cap = zzVideoReading.VideoCapture(videoPath)
  cap.set(1, 1)
  ret, frame = cap.read()
  layout, label, valueWidget = _chooseFrameLayout(cap, (1, 0, cap.get(7) - 2), title, titleStyle=titleStyle)
  if additionalLayout is not None:
    layout.addLayout(additionalLayout)

  buttonsLayout = QHBoxLayout()
  buttonsLayout.addStretch()
  if app.configFileHistory:
    backBtn = QPushButton("Back")
    backBtn.setObjectName("back")
    buttonsLayout.addWidget(backBtn)
  chooseFrameBtn = QPushButton(chooseFrameBtnText)
  def chooseFrameBtnClicked():
    app.configFile["firstFrame"] = valueWidget.value()
    chooseFrameBtnCb()
  chooseFrameBtn.clicked.connect(chooseFrameBtnClicked)
  buttonsLayout.addWidget(chooseFrameBtn)
  extraBtn = None
  if extraButtonInfo is not None:
    if len(extraButtonInfo) == 2:
      text, cb = extraButtonInfo
      styleKwargs = {}
    else:
      assert len(extraButtonInfo) == 3
      text, cb, styleKwargs = extraButtonInfo
    extraBtn = apply_style(QPushButton(text), **styleKwargs)
    extraBtn.clicked.connect(cb)
    buttonsLayout.addWidget(extraBtn)
  buttonsLayout.addStretch()
  layout.addLayout(buttonsLayout)
  page = QWidget()
  page.setLayout(layout)
  stackedLayout = app.window.centralWidget().layout()
  stackedLayout.addWidget(page)
  oldWidget = stackedLayout.currentWidget()
  with app.suppressBusyCursor():
    stackedLayout.setCurrentWidget(page)
    label.setMinimumSize(1, 1)
    label.show()
    setPixmapFromCv(frame, label)
  buttons = []
  if app.configFileHistory:
    buttons.append(backBtn)
  buttons.append(chooseFrameBtn)
  if extraBtn is not None:
    buttons.append(extraBtn)
  for btn in buttons:
    btn.clicked.connect(lambda: stackedLayout.removeWidget(page))


def chooseEndPage(app, videoPath, title, chooseFrameBtnText, chooseFrameBtnCb):
  cap = zzVideoReading.VideoCapture(videoPath)
  maximum = cap.get(7) - 2
  cap.set(1, maximum)
  ret, frame = cap.read()
  layout, label, valueWidget = _chooseFrameLayout(cap, (maximum, app.configFile["firstFrame"] + 1, maximum), title)

  buttonsLayout = QHBoxLayout()
  buttonsLayout.addStretch()
  if app.configFileHistory:
    backBtn = QPushButton("Back")
    backBtn.setObjectName("back")
    buttonsLayout.addWidget(backBtn)
  chooseFrameBtn = QPushButton(chooseFrameBtnText)
  def chooseFrameBtnClicked():
    app.configFile["lastFrame"] = valueWidget.value()
    chooseFrameBtnCb()
  chooseFrameBtn.clicked.connect(chooseFrameBtnClicked)
  buttonsLayout.addWidget(chooseFrameBtn)
  buttonsLayout.addStretch()
  layout.addLayout(buttonsLayout)
  page = QWidget()
  page.setLayout(layout)
  stackedLayout = app.window.centralWidget().layout()
  stackedLayout.addWidget(page)
  oldWidget = stackedLayout.currentWidget()
  with app.suppressBusyCursor():
    stackedLayout.setCurrentWidget(page)
    label.setMinimumSize(1, 1)
    label.show()
    setPixmapFromCv(frame, label)
  for btn in (backBtn, chooseFrameBtn) if app.configFileHistory else (chooseFrameBtn,):
    btn.clicked.connect(lambda: stackedLayout.removeWidget(page))


class _InteractiveLabelPoint(QLabel):
  pointSelected = pyqtSignal(QPoint)
  proceed = pyqtSignal()

  def __init__(self, width, height, selectingRegion):
    super().__init__()
    self._width = width
    self._height = height
    self._point = None
    self._selectingRegion = selectingRegion
    self._currentPosition = None
    self._tooltipShown = False
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    if self._selectingRegion:
      self.setMouseTracking(True)

  def keyPressEvent(self, evt):
    if self._point is not None and (evt.key() == Qt.Key.Key_Enter or evt.key() == Qt.Key.Key_Return):
      self.proceed.emit()
      return
    super().keyPressEvent(evt)

  def mouseMoveEvent(self, evt):
    if self._selectingRegion:
      self._currentPosition = evt.pos()
      self.update()

  def mousePressEvent(self, evt):
    self._point = evt.pos()
    self.update()
    self.pointSelected.emit(self._point)

  def mouseReleaseEvent(self, evt):
    if self._point is not None and not self._tooltipShown:
      QToolTip.showText(self.mapToGlobal(self._point), "If you aren't satisfied with the selection, click again.", self, self.rect(), 5000)
      self._tooltipShown = True

  def enterEvent(self, evt):
    QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)

  def leaveEvent(self, evt):
    QApplication.restoreOverrideCursor()
    self._currentPosition = None
    self.update()

  def paintEvent(self, evt):
    super().paintEvent(evt)
    if self._currentPosition is None and self._point is None:
      return
    qp = QPainter()
    qp.begin(self)
    if self._currentPosition is not None:
      qp.setPen(QColor(255, 0, 0))
      qp.drawLine(0, self._currentPosition.y(), self.width(), self._currentPosition.y())
      qp.drawLine(self._currentPosition.x(), 0, self._currentPosition.x(), self.height())
    if self._point is not None:
      qp.setBrush(QColor(255, 0, 0))
      qp.setPen(Qt.PenStyle.NoPen)
      qp.drawEllipse(self._point, 2, 2)
    qp.end()

  def resizeEvent(self, evt):
    super().resizeEvent(evt)
    self._size = self.size()

  def getCoordinates(self):
    if self._point is None:
      return 0, 0
    point = self._point
    if self._size.height() != self._height or self._size.width() != self._width:
      point = transformCoordinates(QRectF(QPointF(0, 0), QSizeF(self._size)), QRectF(QPointF(0, 0), QSizeF(self._width, self._height)), self._point)
    return point.x(), point.y()


def getPoint(frame, title, extraButtons=(), selectingRegion=False, backBtnCb=None, zoomable=False, useNext=True):
  height, width = frame.shape[:2]

  layout = QVBoxLayout()
  additionalText = "Enter/Return keys can be used instead of clicking Next."
  if zoomable:
    additionalText += "\nYou can zoom in/out using the mouse wheel or Ctrl and +/- and drag the image."
  layout.addWidget(QLabel(additionalText), alignment=Qt.AlignmentFlag.AlignCenter)

  video = _InteractiveLabelPoint(width, height, selectingRegion)
  extraButtons = tuple((text, lambda: cb(video), exitLoop) for text, cb, exitLoop in extraButtons)
  buttons = (("Back", backBtnCb, True),) if backBtnCb is not None else ()
  buttons += (("Next", None, True, video.pointSelected),) if useNext else ()
  layout.addWidget(video, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
  if not useNext:
    video.pointSelected.connect(lambda: QApplication.restoreOverrideCursor())
  showBlockingPage(layout, title=title, buttons=buttons + extraButtons, labelInfo=(frame, video, zoomable), exitSignals=(video.proceed,) if useNext else (video.pointSelected,))
  return video.getCoordinates()


class _InteractiveLabelRect(QLabel):
  regionSelected = pyqtSignal(bool)

  def __init__(self, width, height):
    super().__init__()
    self._width = width
    self._height = height
    self._topLeft = None
    self._currentPosition = None
    self._bottomRight = None
    self._size = None
    self._tooltipShown = False
    self.setMouseTracking(True)

  def mousePressEvent(self, evt):
    if self._topLeft is None or self._bottomRight is not None:
      self._topLeft = evt.pos()
      self._bottomRight = None
      self._currentPosition = None
      self.regionSelected.emit(False)
    else:
      self._bottomRight = evt.pos()
      self.regionSelected.emit(True)
    self.update()

  def mouseReleaseEvent(self, evt):
    if self._bottomRight is not None and not self._tooltipShown:
      QToolTip.showText(self.mapToGlobal(self._bottomRight), "If you aren't satisfied with the selection, click again.", self, self.rect(), 5000)
      self._tooltipShown = True

  def mouseMoveEvent(self, evt):
    self._currentPosition = evt.pos()
    self.update()

  def enterEvent(self, evt):
    QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)

  def leaveEvent(self, evt):
    QApplication.restoreOverrideCursor()
    self._currentPosition = None
    self.update()

  def paintEvent(self, evt):
    super().paintEvent(evt)
    if self._currentPosition is None and self._topLeft is None:
      return
    qp = QPainter()
    qp.begin(self)
    if self._currentPosition is not None and \
        (self._topLeft is None and self._bottomRight is None or self._bottomRight is not None):
      qp.setPen(QColor(255, 0, 0))
      qp.drawLine(0, self._currentPosition.y(), self.width(), self._currentPosition.y())
      qp.drawLine(self._currentPosition.x(), 0, self._currentPosition.x(), self.height())
    if self._topLeft is not None:
      qp.setPen(QColor(0, 0, 255))
      x = self._topLeft.x()
      y = self._topLeft.y()
      bottomRight = self._bottomRight or self._currentPosition
      if bottomRight is None:
        qp.drawPoint(x, y)
      else:
        width = bottomRight.x() - x
        height = bottomRight.y() - y
        qp.drawRect(x, y, width, height)
    qp.end()

  def resizeEvent(self, evt):
    super().resizeEvent(evt)
    self._size = self.size()

  def getCoordinates(self):
    if self._topLeft is None or self._bottomRight is None:
      return [0, 0], [0, 0]
    points = (self._topLeft, self._bottomRight)
    if self._size.height() != self._height or self._size.width() != self._width:
      points = (transformCoordinates(QRectF(QPointF(0, 0), QSizeF(self._size)), QRectF(QPointF(0, 0), QSizeF(self._width, self._height)), point) for point in points)
    return ([point.x(), point.y()] for point in points)


def getRectangle(frame, title, backBtnCb=None):
  height, width, _ = frame.shape

  layout = QVBoxLayout()

  video = _InteractiveLabelRect(width, height)
  layout.addWidget(video, alignment=Qt.AlignmentFlag.AlignCenter)
  if backBtnCb is not None:
    buttons = (("Back", backBtnCb, True), ("Next", None, True, video.regionSelected))
  else:
    buttons = (("Next", None, True, video.regionSelected),)
  showBlockingPage(layout, title=title, buttons=buttons, labelInfo=(frame, video))

  return video.getCoordinates()


def addToHistory(fn):
  def inner(*args, **kwargs):
    app = QApplication.instance()
    configFileState = app.configFile.copy()
    def restoreState(restoreConfig=True):
      if restoreConfig:
        app.configFile.clear()
        app.configFile.update(configFileState)
      del app.configFileHistory[-1:]
      fn(*args, **kwargs)
    app.configFileHistory.append(restoreState)
    return fn(*args, **kwargs)
  return inner


class Expander(QWidget):
  def __init__(self, parent, title, layout, animationDuration=200, showFrame=False, addScrollbars=False):
    super(Expander, self).__init__(parent)

    toggleButton = QToolButton()
    toggleButton.setStyleSheet("QToolButton { border: none; }")
    toggleButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
    toggleButton.setArrowType(Qt.ArrowType.RightArrow)
    toggleButton.setText(str(title))
    toggleButton.setCheckable(True)
    toggleButton.setChecked(False)

    self._contentArea = contentArea = QScrollArea()
    if not showFrame:
      contentArea.setFrameShape(QFrame.Shape.NoFrame)
    contentArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    contentArea.setMaximumHeight(0)
    contentArea.setMinimumHeight(0)

    mainLayout = QGridLayout()
    mainLayout.setVerticalSpacing(0)
    mainLayout.setContentsMargins(0, 0, 0, 0)
    mainLayout.addWidget(toggleButton, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
    mainLayout.addWidget(contentArea, 1, 0, 1, 3)
    self.setLayout(mainLayout)

    if not addScrollbars:
      contentArea.setLayout(layout)
    else:
      widget = QWidget(self)
      widget.setLayout(layout)
      contentArea.setWidgetResizable(True)
      contentArea.setWidget(widget)
    self._collapseHeight = self.sizeHint().height() - contentArea.maximumHeight()
    contentHeight = layout.sizeHint().height()
    self._toggleAnimation = toggleAnimation = QParallelAnimationGroup()
    toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
    toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
    toggleAnimation.addAnimation(QPropertyAnimation(contentArea, b"maximumHeight"))
    for i in range(toggleAnimation.animationCount() - 1):
      spoilerAnimation = toggleAnimation.animationAt(i)
      spoilerAnimation.setDuration(animationDuration)
      spoilerAnimation.setStartValue(self._collapseHeight)
      spoilerAnimation.setEndValue(self._collapseHeight + contentHeight)
    contentAnimation = toggleAnimation.animationAt(toggleAnimation.animationCount() - 1)
    contentAnimation.setDuration(animationDuration)
    contentAnimation.setStartValue(0)
    contentAnimation.setEndValue(contentHeight)

    def startAnimation(checked):
      arrowType = Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow
      direction = QAbstractAnimation.Direction.Forward if checked else QAbstractAnimation.Direction.Backward
      toggleButton.setArrowType(arrowType)
      toggleAnimation.setDirection(direction)
      toggleAnimation.start()
    toggleButton.clicked.connect(startAnimation)

  def refresh(self, availableHeight):
    layout = self._contentArea.layout()
    height = layout.sizeHint().height() if layout is not None else self._contentArea.widget().sizeHint().height() + 5
    contentHeight = min(height, availableHeight - self._collapseHeight - 10)
    if self._contentArea.maximumHeight():
      self._contentArea.setMaximumHeight(contentHeight)
      self.setMinimumHeight(self._collapseHeight + contentHeight)
      self.setMaximumHeight(self._collapseHeight + contentHeight)
    for i in range(self._toggleAnimation.animationCount() - 1):
      self._toggleAnimation.animationAt(i).setEndValue(self._collapseHeight + contentHeight)
    self._toggleAnimation.animationAt(self._toggleAnimation.animationCount() - 1).setEndValue(contentHeight)


class _InteractiveLabelCircle(QLabel):
  circleSelected = pyqtSignal(bool)

  def __init__(self, width, height):
    super().__init__()
    self._width = width
    self._height = height
    self._center = None
    self._currentPosition = None
    self._radius = None
    self._size = None
    self._tooltipShown = False
    self.setMouseTracking(True)

  def mousePressEvent(self, evt):
    if self._center is None or self._radius is not None:
      self._center = evt.pos()
      self._radius = None
      self._currentPosition = None
      self.circleSelected.emit(False)
    else:
      self._radius = QLine(self._center, evt.pos())
      self.circleSelected.emit(True)
    self.update()

  def mouseReleaseEvent(self, evt):
    if self._radius is not None and not self._tooltipShown:
      QToolTip.showText(evt.globalPos(), "If you aren't satisfied with the selection, click again.", self, self.rect(), 5000)
      self._tooltipShown = True

  def mouseMoveEvent(self, evt):
    self._currentPosition = evt.pos()
    self.update()

  def enterEvent(self, evt):
    QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)

  def leaveEvent(self, evt):
    QApplication.restoreOverrideCursor()
    self._currentPosition = None
    self.update()

  def paintEvent(self, evt):
    super().paintEvent(evt)
    if self._currentPosition is None and self._center is None:
      return
    qp = QPainter()
    qp.begin(self)
    if self._center is not None:
      qp.setBrush(QColor(255, 0, 0))
      qp.setPen(Qt.PenStyle.NoPen)
      radius = self._radius if self._radius is not None else QLine(self._center, self._currentPosition) if self._currentPosition is not None else None
      qp.drawEllipse(self._center, 2, 2)
      if radius is not None:
        radius = math.sqrt(radius.dx() * radius.dx() + radius.dy() * radius.dy())
        qp.setBrush(Qt.BrushStyle.NoBrush)
        qp.setPen(QColor(0, 0, 255))
        qp.drawEllipse(self._center, radius, radius)
    qp.end()

  def resizeEvent(self, evt):
    super().resizeEvent(evt)
    self._size = self.size()

  def getInfo(self):
    if self._center is None or self._radius is None:
      return None, None
    if self._size.height() != self._height or self._size.width() != self._width:
      center = transformCoordinates(QRectF(QPointF(0, 0), QSizeF(self._size)), QRectF(QPointF(0, 0), QSizeF(self._width, self._height)), self._center)
      radius = transformCoordinates(QRectF(QPointF(0, 0), QSizeF(self._size)), QRectF(QPointF(0, 0), QSizeF(self._width, self._height)), self._radius)
    else:
      center = self._center
      radius = self._radius
    return center, int(math.sqrt(radius.dx() * radius.dx() + radius.dy() * radius.dy()))


def getCircle(frame, title, backBtnCb=None):
  height, width, _ = frame.shape

  layout = QVBoxLayout()

  video = _InteractiveLabelCircle(width, height)
  layout.addWidget(video, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
  if backBtnCb is not None:
    buttons = (("Cancel", backBtnCb, True), ("Ok", None, True, video.circleSelected))
  else:
    buttons = (("Ok", None, True, video.circleSelected),)
  showBlockingPage(layout, title=title, buttons=buttons, labelInfo=(frame, video))
  return video.getInfo()
