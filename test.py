import numpy as np
import cv2
import base64

with open("image1.jpg", 'rb') as f:
    binary_jpeg = f.read()

with open("image2.png", 'rb') as f:
    binary_png = f.read()

encoded = base64.b64encode(binary_jpeg)
print(encoded)
decoded = base64.decodebytes(encoded)
npimg = np.frombuffer(decoded, np.uint8)
cvimg = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

# cv2.imshow("image", cvimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()