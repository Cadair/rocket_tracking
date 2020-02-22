import cv2


def setup_camera(id=0, width=1280, height=720):
    """
    Open camera and setup capture resolution.
    """
    cam = cv2.VideoCapture(id)
    cam.open(id)
    cam.set(3, width)
    cam.set(4, height)
    return cam


def get_gs_image(cam):
    """
    Capture an image and convert to greyscale.
    """
    ret, frame = cam.read()
    if not ret:
        raise ValueError("No image can be read.")
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def find_bright_spot(im, radius=31):
    """
    Find the brightest spot in the image.

    Gaussian blur with a given radius (in pixels), then find the location of
    the maxima.
    """
    blur = cv2.GaussianBlur(im, (radius, radius), 0)
    vmin, vmax, minloc, maxloc = cv2.minMaxLoc(blur)
    return maxloc


def get_offset(im, point, x_fov=1, y_fov=1):
    """
    Calculate the angular offset from centre of the point, based on given
    angular field of view for camera.
    """
    height, width = im.shape
    xpos, ypos = point

    offset_x = xpos - width/2
    offset_y = ypos - height/2

    xscale = x_fov / width
    yscale = y_fov / height

    return xscale * offset_x, yscale * offset_y


cam = setup_camera()

while True:
    pixel_radius = 31
    im = get_gs_image(cam)
    point = find_bright_spot(im, pixel_radius)
    angular_offset = get_offset(im, point, x_fov=70.42, y_fov=43.3)

    print(angular_offset)

    cv2.circle(im, point, pixel_radius, (255, 0, 0), 5)
    cv2.imshow("athing", im)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break