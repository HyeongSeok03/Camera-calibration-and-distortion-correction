# Camera Calibration and Distortion Correction

This project perform **camera calibration** and then uses the calibration results to apply **lens distortion correction** on the video frames using OpenCV.

---

## Demonstration Video
[Youtube](https://youtu.be/gzxQPgYAVTI)

## Input Data
1. 'data/chessboard.MOV': Video taken with an iPhone. Less distortion. -> **Insignificant change.**
2. 'data/chessboard.avi': Sample video with high distortion. -> **Signigicant change.**

## How to Run
1. The chessboard video will start playing
2. Press **Spacebar** to pause and detect corners
3. Press **Enter** to select the current frame
4. After selecting enough frames, press **ESC** to begin calibration
5. The video will play agin with **lens distortion corrected**

## Key Functions

**select_img_from_video()**
- Displays video and allows you to manually select frames containing a visible chessboard
- Detects and visualizes chessboard corners before selection

**calib_camera_from_chessboard()**
- Extracts 2D corner points and associates them with 3D real-world coordinates
- Computes intrinsic matrix ( K ) and distortion coefficients ( \text{dist_coeff} )

**cv.initUndistortRectifyMap() + cv.remap()**
- Applies the distortion correction to video frames using the computed calibration results

## Output

### 1. chessboard.MOV (Iphone video)

Camera matrix (K) =

| fx        | fy         | cx        | cy         |
|-----------|------------|-----------|------------|
| 879.6767   | 888.7435   | 960.4426  | 517.8677   |

Distortion coefficient =

| k1        | k2         | p1        | p2         | k3        |
|-----------|------------|-----------|------------|-----------|
| 0.01952   | -0.05435   | -0.00476  | -0.00055   | 0.04780   |
  
### 2. chessboard.avi (Sample video)

Camera matrix (K) = 

| fx        | fy         | cx        | cy         |
|-----------|------------|-----------|------------|
| 433.89377641 | 432.32365694 | 476.0828139 | 289.27503804 |

Distortion coefficient = 

| k1        | k2         | p1        | p2         | k3        |
|-----------|------------|-----------|------------|-----------|
| -2.94933587e-01   | 1.16221151e-01   | -5.38614023e-04  | -1.90717162e-05   | -2.40132911e-02   |
