import numpy as np
import cv2 as cv

def select_img_from_video(video_file, board_pattern, wait_msec=10, wnd_name='Camera Calibration'):
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    img_select = []
    while True:
        valid, img = video.read()
        if not valid:
            break

        display = img.copy()
        cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        cv.imshow(wnd_name, display)

        key = cv.waitKey(wait_msec)
        if key == ord(' '):
            complete, pts = cv.findChessboardCorners(img, board_pattern)
            if complete:
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)
        if key == 27:
            break

    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)

    rms, K, dist_coeff, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    return rms, K, dist_coeff

if __name__ == '__main__':
    video_file = 'data/chessboard.avi'
    board_pattern = (10, 7)
    board_cellsize = 0.025

    print("1. 이미지 선택.")
    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'There is no selected images!'

    print("2. 카메라 캘리브레이션 수행.")
    rms, K, dist_coeff = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    print('\n## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient = {dist_coeff.flatten()}')

    print("\n3. 왜곡이 보정된 영상 출력.")
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    map1, map2 = None, None
    while True:
        valid, img = video.read()
        if not valid:
            break

        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1)
        rectified = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)

        cv.putText(rectified, 'Rectified', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        cv.imshow("Rectified Video", rectified)

        key = cv.waitKey(10)
        if key == 27:
            break

    video.release()
    cv.destroyAllWindows()