import os
import cv2
from tqdm import tqdm
from copy import deepcopy, copy
import matplotlib.pyplot as plt
import numpy as np


def find_charuco_corners(framesync, imgs_src, fes, board, aruco_dict, min_corners=20,
                         start_frame=0, max_frame_cutoff=None,
                         display_detections=False):
    cams = list(fes)
    allCorners = {cam: [] for cam in cams}
    allIds = {cam: [] for cam in cams}
    res2 = {cam: [] for cam in cams}
    timegaps, gyros = [], []

    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
    df = framesync.iloc[start_frame:max_frame_cutoff]

    for n, dfrow in tqdm(df.iterrows(), total=len(df)):
        fn_pair = {cam: dfrow[cam] for cam in cams}
        if max_frame_cutoff and n > max_frame_cutoff:
            break
        # if 'out559.png' not in paths['gopro']:
        #     continue
        try:
            if not all([os.path.isfile(imgs_src[cam].input_path + '/' + os.path.basename(fn_pair[cam])) for cam in cams
                        if isinstance(fn_pair[cam], str)]):
                continue
        except:
            1==1

        # get images
        imgs_dist = {cam: imgs_src[cam].get_image(fn_pair[cam]) for cam in cams}
        imgs = deepcopy(imgs_dist)
        imgs.update({cam: 255 * imgs[cam] for cam in cams if imgs[cam].max() < 1})
        imgs.update({cam: fes[cam].transform(imgs_dist[cam], fes[cam].undist_maps).astype(np.float32) for cam in cams
                     if fes[cam].w > 0})
        imgs.update({cam: cv2.cvtColor(imgs[cam], cv2.COLOR_RGB2GRAY).astype(np.uint8) for cam in cams
                     if len(imgs[cam].shape) == 3})
        imgs = {cam: imgs[cam].astype(np.uint8) for cam in cams}
        corners_ids_rej = {cam: cv2.aruco.detectMarkers(imgs[cam], aruco_dict) for cam in cams}

        # SUB PIXEL DETECTION
        if all([corners_ids_rej[cam][0] for cam in cams]):
            for cam in cams:
                for corner in corners_ids_rej[cam][0]:
                    cv2.cornerSubPix(imgs[cam], corner,
                                     winSize=(3, 3),
                                     zeroZone=(-1, -1),
                                     criteria=criteria)
                res2[cam] = cv2.aruco.interpolateCornersCharuco(corners_ids_rej[cam][0], corners_ids_rej[cam][1], imgs[cam], board)

            if all([res2[cam][1] is not None for cam in cams]) and all([res2[cam][2] is not None for cam in cams]):
                if all([len(res2[cam][1]) >= min_corners for cam in cams]):
                    # find common corners of both cameras
                    ids_common = set([t[0] for t in res2[list(res2)[0]][2]]).intersection(
                        set([t[0] for t in res2[list(res2)[1]][2]]))

                    d = {id_: 1 for id_ in ids_common}
                    for cam in cams:
                        res2_tmp = np.stack([r2 for r2 in np.dstack(res2[cam][1:]).squeeze() if d.get(int(r2[2]))])
                        res2_tmp = res2_tmp.astype(np.float32)
                        res2[cam] = [len(res2_tmp),
                                     res2_tmp[:, :2][:, None, :],
                                     res2_tmp[:, 2].astype(int)[:, None]]
                    if display_detections:
                        for cam in cams:
                            plt.imshow(imgs[cam])
                            plt.scatter(x=res2[cam][1][:, 0, 0], y=res2[cam][1][:, 0, 1], s=4, c='k', marker='o')
                            plt.scatter(x=res2[cam][1][:, 0, 0], y=res2[cam][1][:, 0, 1], s=2, c='r', marker='o')
                            plt.scatter(x=res2[cam][1][0, 0, 0], y=res2[cam][1][0, 0, 1], marker='x', c='r')
                            plt.scatter(x=res2[cam][1][-1, 0, 0], y=res2[cam][1][-1, 0, 1], marker='x', c='k')
                            plt.show()

                    # store corners
                    example_img = copy(imgs)
                    example_ids = copy(res2[cam][2])[:, 0]
                    for cam in cams:
                        allCorners[cam].append(res2[cam][1])
                        allIds[cam].append(res2[cam][2])
                        print('found {} corners in {}: {}!'.format(res2[cam][0], n, imgs_src[cam].list_imgs()[n]))
                    if 'timegap' in dfrow.index:
                        timegaps.append(dfrow['timegap'])
                    if 'timegap' in dfrow.index:
                        gyros.append(dfrow['gopro_gyro_smooth'])

    return allCorners, allIds, timegaps, gyros, example_img, example_ids


def validate_calibration(board, M, allCorners, fes, img_example, example_ids):
    cams = list(fes.keys())
    ret, rvec, tvec = cv2.solvePnP(objectPoints=board.chessboardCorners[example_ids],
                                   imagePoints=np.array([allCorners[cams[0]][-1]])[0, :, 0, :],
                                   cameraMatrix=fes[cams[0]]._camMat[:, :3],
                                   distCoeffs=np.array([0, 0, 0, 0])
                                   )
    fig, ax = plt.subplots(1, 2)
    plt.suptitle('validating relative exrinsics')
    makehomo = lambda pts_: np.pad(pts_, ((0, 1), (0, 0)), mode='constant', constant_values=1)
    pts = makehomo(board.chessboardCorners.T)
    K_tst = np.eye(4)
    K_tst[:3, :3] = cv2.Rodrigues(rvec)[0]
    K_tst[:3, 3] = tvec.squeeze()
    pts_new_h = fes[cams[0]]._camMat @ K_tst @ pts
    pts_new = (pts_new_h / pts_new_h[2, :])[:2, :]
    ax[0].imshow(img_example[cams[0]], cmap='gray')
    ax[0].scatter(pts_new[0, :], pts_new[1, :], c='r', s=1)

    pts_new_cam2_h = fes[cams[1]]._camMat @ M @ K_tst @ pts
    pts_new_cam2 = (pts_new_cam2_h / pts_new_cam2_h[2, :])[:2, ]
    ax[1].imshow(img_example[cams[1]], cmap='gray')
    ax[1].scatter(pts_new_cam2[0, :], pts_new_cam2[1, :], c='r', s=1)
    plt.show()