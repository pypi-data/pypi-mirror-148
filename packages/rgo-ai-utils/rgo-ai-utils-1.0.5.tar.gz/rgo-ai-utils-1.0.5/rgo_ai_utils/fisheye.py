import matplotlib.pyplot as plt
import numpy as np
import time
import cv2
from lxml import etree
import exiftool
import os
import subprocess as sp
import shutil
from inspect import signature

Rx = lambda t: np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
Ry = lambda t: np.array([[np.cos(t), 0, np.sin(t)], [0, 1, 0], [-np.sin(t), 0, np.cos(t)]])
Rz = lambda t: np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
Rxyz = lambda x, y, z: np.matmul(np.matmul(Rx(x), Ry(y)), Rz(z))


class timer(object):
    def __enter__(self):
        self.t = time.clock()
        return self

    def __exit__(self, type, value, traceback):
        self.t = time.clock() - self.t


def find_file_with_camera_otp(path_for_otp, calib_database_path):
    if path_for_otp and os.path.isfile(os.path.abspath(path_for_otp)):
        if path_for_otp.lower()[-3:] in ['jpg', 'mp4']:
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(path_for_otp)
                # et.execute(b"-SerialNumber=11.12", path_for_otp.encode())
                sn = [metadata[sn_key] for sn_key
                      in ['EXIF:SerialNumber', 'QuickTime:CameraSerialNumber']
                      if sn_key in metadata.keys()][0]
                otp = sn + '_' + metadata['Composite:ImageSize']
        elif path_for_otp.endswith('gopro_metadata.txt'):
            with open(path_for_otp, 'r') as f:
                # otp = [l.split(',')[-1] for l in f.readlines() if 'CameraSerialNumber' in l]
                metadata = {l.split(',')[0].replace('\n', '').strip(): l.split(',')[1].replace('\n', '').strip()
                            for l in f.readlines()}
                sn = [metadata[k] for k in metadata.keys() if 'cameraserialnumber' in k.lower()][0]
                imsize = [metadata[k] for k in metadata.keys() if 'imagesize' in k.lower()][0]
                assert len(sn) & len(imsize), "couldnt find CameraSerialNumber in " + path_for_otp
                otp = sn + '_' + imsize
        elif path_for_otp.split('/')[-1] == 'cam_otp.txt':
            with open(path_for_otp, 'r') as f_otp:
                otp = f_otp.readlines()[0].replace(' \n', '')

        calib_file_local = [os.path.dirname(path_for_otp) + '/' + calib_f for calib_f in
                            os.listdir(os.path.dirname(path_for_otp)) if 'calibration.xml' in calib_f]
        if calib_file_local:
            found_calibs = [flocal.split('/')[-1] in
                            sp.getoutput("grep -nw {}/* -e {}".format(os.path.dirname(calib_file_local[0]), otp))
                            for flocal in calib_file_local]
            calib_file = calib_file_local[found_calibs.index(True)]
            print('using local calibration file', calib_file)
            assert os.path.isfile(calib_file), 'couldnt find calibration file {}'.format(calib_file)
        else:
            calib_file = sp.getoutput("grep -rnw {} -e {}".format(calib_database_path, otp)).split(':')[0]
            print('using database calibration file', calib_file)
            assert os.path.isfile(calib_file), 'couldnt find calibration file {}'.format(calib_file)
            shutil.copy(calib_file, os.path.dirname(path_for_otp))
        return calib_file


def extract_cam_params_from_calib_file(calib_file, crop_info_file=None):
    et = etree.parse(calib_file)
    root = et.getroot()
    hw = [int([e.text for e in root[0].findall('Base/Size/Height')][0]),
          int([e.text for e in root[0].findall('Base/Size/Width')][0])]
    w = float([e.text for e in root.findall('Global/w')][0])
    f = [float([e.text for e in root[0][0].findall('Fy')][0]),
         float([e.text for e in root[0][0].findall('Fx')][0])]
    c = [float([e.text for e in root[0][0].findall('Py')][0]),
         float([e.text for e in root[0][0].findall('Px')][0])]

    if crop_info_file is not None:
        with open(crop_info_file, 'r') as cropfile:
            crop_data = cropfile.readlines()
        hw_crp = np.stack([line.replace('\n', '').split(',') for line in crop_data]).astype(
            int) - 1  # "-1" due to matlab indexing
        hw = [hw_crp[0, 1] - hw_crp[0, 0] + 1, hw_crp[1, 1] - hw_crp[1, 0] + 1]
        c = [c[0] - hw_crp[0, 0], c[1] - hw_crp[1, 0]]
    print('\nExtracted intrinsics from file {}:\nhw={},{}\nw={}\nf={},{}\nc={},{}\n'.format(calib_file, *hw, w, *f, *c))
    return hw, w, f, c


class Fisheye:
    def __init__(self, hw=None, w=0, f=0, c=None, padval=200, path_for_otp=None, crop_info_file=None,
                 calib_database_path='/media/noam/Datasets_old/cameraCalibration/Results'):
        '''

        @param hw:
        @param w:
        @param f: assuming the components order (fy, fx)
        @param c: assuming the components order (cy, cx)
        @param padval:
        @param path_for_otp: camera intrinsics can be extracted by extracting the otp(rgo), or
        serial (gopro) from a cam_otp.txt (rgo), or media (gopro) file
        @param calib_database_path: path where the intrinsics are obtained, given an otp
        '''

        self.padval = padval

        if hw is None:
            calib_file = find_file_with_camera_otp(path_for_otp, calib_database_path)
            hw, w, f, c = extract_cam_params_from_calib_file(calib_file, crop_info_file=crop_info_file)

        self.hw = hw
        self.w = w
        self.w_sphere = 2 * np.arctan(0.5)
        if (not hasattr(f, "__len__")) or (len(f) == 1):
            self.f = np.array([f, f])
        else:
            self.f = np.array(f)
        self.hw_padded = [hw[0] + 2*self.padval, hw[1] + 2*self.padval]
        if c is not None:
            self._c = self.padval + np.array(c)
        else:
            self._c = np.array([self.hw_padded[0] / 2, self.hw_padded[1] / 2])

        self.rot_bag = []
        self.build_camera_matrix()
        self.undist_maps = [None, None]
        self.dist_maps = [None, None]
        self.fe2usphere_maps = [None, None]
        self.usphere2fe_maps = [None, None]
        self.fe2usphere_maps = [None, None]
        self.shell2fe_maps = [None, None]

        self.undist_f = lambda w_, rd_: np.tan(w_ * rd_) / (2 * np.tan(w_ / 2))
        self.dist_f = lambda w_, ru_: np.arctan(2 * ru_ * np.tan(w_ / 2)) / w_
        # the 2nd term below relates to a branch choice of arctan
        self.sphere_f = lambda w_ud, w_d, rd_: \
            self.dist_f(w_d, self.undist_f(w_ud, rd_)) + (np.pi / w_d) * (w_ud * rd_ / (np.pi / 2)).astype(int)
        # self.fe2usphere_f = lambda w_ud, rd_: self.sphere_f(w_ud, self.w_sphere, rd_)
        # self.usphere2fe_f = lambda w_d, rd_: self.sphere_f(self.w_sphere, w_d, rd_)
        self.usphere2fe_f = lambda w_, rd_: self.dist_f(w_, np.tan(rd_))
        self.fe2usphere_f = lambda w_, rd_: np.arctan(self.undist_f(w_, rd_))

        self.make_maps()

        # self.make_rot_collection()
        # exps = lambda y: (np.exp(-1j * y) - np.exp(1j * y)) / (np.exp(-1j * y) + np.exp(1j * y))
        # self.fe2usphere_f = lambda w_, rd_: np.arctan(2 * (np.tan(w_ * rd_) / (2 * np.tan(w_ / 2))) * np.tan(w0 / 2)) / w0
        # self.atanXtanY = lambda x, y: 0.5 * 1j * (np.log(1 + x * exps(y)) - np.log(1 - x * exps(y)))
        # self.usphere_f = lambda w1, w2, rd_: self.atanXtanY(2 / (2 * np.tan(w1 / 2)) * np.tan(w2 / 2), w1 * rd_) / w2

    def build_camera_matrix(self):
        self._camMat = np.array(
            [[self.f[1], 0,         self._c[1], 0],
             [0,         self.f[0], self._c[0], 0],
             [0,         0,         1,          0]])
        self._camMatI = np.array(
            [[1 / self.f[1], 0,             -self._c[1] / self.f[1]],
             [0,             1 / self.f[0], -self._c[0] / self.f[0]],
             [0,             0,             1],
             [0,             0,             0]])
        
    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = np.array(value)
        self.build_camera_matrix()

    def fe2fe_maps(self, f1, c1, w1, f2, c2, w2):
        x, y = np.meshgrid(range(self.hw_padded[1]), range(self.hw_padded[0]))
        x_h, y_h = (x - c1[1]) / f1[1], (y - c1[0]) / f1[0]
        r_h = (x_h**2 + y_h**2)**0.5
        r_h_post = self.usphere2fe_f(w2, self.fe2usphere_f(w1, r_h))
        r_fact = r_h_post / r_h
        x_post = x_h * r_fact * f2[1] + c2[1]
        y_post = y_h * r_fact * f2[0] + c2[0]
        x_post = x_post.astype(np.float32)[..., None]
        y_post = y_post.astype(np.float32)[..., None]
        self.fe2f2_maps = x_post, y_post

    def make_maps(self):
        # remap() uses maps the DESTINATION to SOURCE, so self.a2b_f <--> self.b2a_maps
        # Also, I enlarged the img & meshgrid & self._c by padding, so that remap will capture the wide field of view
        xy = np.stack(np.meshgrid(range(self.hw_padded[1]), range(self.hw_padded[0])))
        xy_h = (xy - self._c[::-1, None, None]) / self.f[::-1, None, None]
        r_h = np.linalg.norm(xy_h, axis=0)

        dist_funcs_names = [func for func in self.__dict__.keys()
                            if func.endswith('_f') and len(signature(getattr(self, func)).parameters) == 2]
        dist_funcs = [getattr(self, func) for func in dist_funcs_names]
        dist_maps = [getattr(self, func.replace('_f', '_maps')) for func in dist_funcs_names]
        dist_maps_swapped = [val for pair in zip(dist_maps[1::2], dist_maps[::2]) for val in pair]

        for f, maps in zip(dist_funcs, dist_maps_swapped):
            r_fact = f(self.w, r_h) / r_h
            xy_new = xy_h * r_fact * self.f[::-1, None, None] + self._c[::-1, None, None]
            maps[0], maps[1] = xy_new.astype(np.float32)[..., None]

    def transform(self, img, maps, border_value=0):
        # self.undist_maps = cv2.convertMaps(*self.undist_maps, dstmap1type=cv2.CV_16SC2)
        img_padded = np.pad(img, ((self.padval, self.padval), (self.padval, self.padval)) +
                            ((0, 0),) * (len(img.shape) == 3), constant_values=border_value, mode='constant')
                            # mode='symmetric')  #
        remapped = cv2.remap(img_padded.astype(float), *maps, cv2.INTER_LINEAR, borderValue=border_value)
        if (len(img.shape) == 3) & (len(remapped.shape) == 2):
            remapped = remapped[..., None]
        return remapped  #[self.padval:self.hw[0] - self.padval, self.padval:self.hw[1] - self.padval]

    def fe2plane(self, img, border_value=0):
        return self.transform(img, self.undist_maps, border_value)

    def plane2fe(self, img, border_value=0):
        return self.transform(img, self.dist_maps, border_value)

    def prepRot_planeBased(self, rot=None):
        # definitions
        if rot is None:
            rot = [np.random.uniform(low=0, high=0.2) - 0.1,
                   np.random.uniform(low=0.1, high=0.2) * [-1, 1][np.random.randint(2)],
                   np.random.uniform(low=0, high=0.2) - 0.1]

        assert (abs((np.matmul(self._camMatI, self._camMat)[:-1, :-1] - np.eye(3))) < 1e-8).all(), "Error: camMat * camMatI != I"
        extM = np.concatenate([Rxyz(*rot)] + [np.array([[0, 0, 0]])], axis=0)
        extM = np.concatenate([extM] + [np.array([[0, 0, 0, 1]]).T], axis=1)
        T = np.matmul(extM, self._camMatI)
        T = np.matmul(self._camMat, T)
        return T

    def rot_w_plane_proj(self, rot, img, msk=None, aux_label=2, p=1):
        if np.random.uniform() > p:
            return img, msk
        rot_trans = self.prepRot_planeBased(rot)
        # processing: undist -> transform -> dist
        img_u = self.fe2plane(img)
        img_t = cv2.warpPerspective(img_u, rot_trans, dsize=img_u.shape[:-1])
        # img_t = cv2.warpPerspective(img_u, T, dsize=tuple([s + 400 for s in img_u.shape[:-1]]), borderMode=cv2.BORDER_REFLECT)
        # ctr_wrpd = np.matmul(T, [*self._c, 1])
        # c_ctrd = [int(c / ctr_wrpd[-1]) for c in ctr_wrpd][:-1][::-1]
        # img_t = self.plane2fe(np.roll(img_t, int(self._c[1]) - c_ctrd[1], axis=1))
        img_t = self.plane2fe(img_t)
        # img_t = self.plane2fe(np.hstack([img_t[:, self.padval:-self.padval, :]] * 3))[self.padval:self.hw_padded[0] - self.padval, self.padval:self.hw_padded[1] - self.padval]
        img_t = img_t[self.padval:self.hw_padded[0] - self.padval, self.padval:self.hw_padded[1] - self.padval]

        msk_t = None
        if msk is not None:
            msk = self.fe2plane(msk, border_value=aux_label)
            msk[msk == 255] = aux_label
            msk_t = cv2.warpPerspective(msk, T, dsize=msk.shape[:-1], borderValue=aux_label)[..., None]
            msk_t = self.plane2fe(msk_t, border_value=aux_label)
            msk_t[msk_t == 255] = aux_label
            msk_t = msk_t[self.padval:self.hw_padded[0] - self.padval, self.padval:self.hw_padded[1] - self.padval, ...]

        return img_t, msk_t


    def prepRot_sphereBased(self, rot=None, remap_sphere2fe=False, border_value=2):
        if rot is None:
            rot = [np.random.uniform(low=0, high=0.2) - 0.1,
                   np.random.uniform(low=0.1, high=0.2) * [-1, 1][np.random.randint(2)],
                   np.random.uniform(low=0, high=0.2) - 0.1]

        shell_maps = np.stack(self.fe2usphere_maps).squeeze() - self._c[::-1, None, None]

        T = np.linalg.norm(shell_maps / self.f[..., None, None], axis=0)
        P = np.arctan2(shell_maps[1], shell_maps[0])
        v3d = np.stack([np.sin(T) * np.cos(P),
                        np.sin(T) * np.sin(P),
                        np.cos(T)])

        v3d_rot = np.matmul(Rxyz(*rot), v3d.reshape(3, -1)).reshape(*v3d.shape)

        T_rot = np.arccos(v3d_rot[2])
        P_rot = np.arctan2(v3d_rot[1], v3d_rot[0])

        rot_map = self.f[:, None, None] * T_rot * np.stack([np.cos(P_rot), np.sin(P_rot)]) + self._c[::-1, None, None]
        rot_map = rot_map.astype(np.float32)
        if remap_sphere2fe:
            return [cv2.remap(rot_map[0], *self.shell2fe_maps, cv2.INTER_LINEAR, borderValue=border_value),
                    cv2.remap(rot_map[1], *self.shell2fe_maps, cv2.INTER_LINEAR, borderValue=border_value)]
        else:
            return rot_map

    def make_rot_collection(self, rot_func=None,  ranges=None, Nrots=(2*2)**3, aux_label=2):
        print('augs: creating img rotations grid...')
        if ranges is None:
            ranges = {'x': [0.1, 0.3], 'y': [0.3, 0.3 * np.pi], 'z': [0.1, 0.3]}
        if rot_func is None:
            rot_func = self.prepRot_sphereBased
        bag = []
        rot_arr = [np.linspace(ranges[c][0], ranges[c][1], round(Nrots**(1/3)) // 2) for c in ['x', 'y', 'z']]
        rot_arr = np.array([np.hstack([-arr[::-1], arr]) for arr in rot_arr])
        rot_arr = np.array(np.meshgrid(*rot_arr)).T.reshape(-1,3)
        for nrot in range(Nrots):
        #     # rot = [np.random.uniform(low=ranges['x'][0], high=ranges['x'][1]) * [-1, 1][np.random.randint(2)],
        #     #        np.random.uniform(low=ranges['y'][0], high=ranges['y'][1]) * [-1, 1][np.random.randint(2)],
        #     #        np.random.uniform(low=ranges['z'][0], high=ranges['z'][1]) * [-1, 1][np.random.randint(2)]]
        #     rot = []
            bag.append(rot_func(rot=rot_arr[nrot], border_value=aux_label))
        self.rot_bag = bag
    
    def rot_from_bag(self, img, msk=None, aux_label=2, p=1):
        if np.random.uniform() > p:
            return img, msk
        pick_rot = np.random.randint(len(self.rot_bag))
        img = self.transform(img, self.rot_bag[pick_rot], border_value=aux_label)[self.padval:-self.padval, self.padval:-self.padval, :]
        if msk is not None:
            msk = self.transform(msk, self.rot_bag[pick_rot], border_value=aux_label)[self.padval:-self.padval, self.padval:-self.padval, :]
        return img, msk


def test():
    fe = Fisheye(hw=[1, 1], padval=0, w=1, f=1)
    cam_height = 20
    print("old camera:")
    w, f = 1, 640 / np.pi
    p_bottom = 240
    hp = p_bottom / f
    p_ud = f * fe.undist_f(w, hp)
    Zmin = f * cam_height / p_ud
    Z50cm = f * (fe.dist_f(w, f * cam_height / 50 / f))
    assert fe.undist_f(1, 320 / f) > 1e10, "the undistorted coordinates of image border pixels should approach inf"
    assert np.pi * f / (2 * w) == 320, "error"
    print("p_bottom: {}\np_undistorted: {}\nz_closest (img short axis): {}\nz_50cm: {}".format(p_bottom, p_ud, Zmin, Z50cm))

    # print("new camera:")
    # w, f = 1, 260
    # Z_func = lambda x_: f * (fe.dist_f(w, f * cam_height / x_ / f))
    # plt.plot(np.arange(0, 100), -Z_func(np.arange(0, 100)))
    # plt.plot(Zmin, -p_bottom, marker='X')
    # plt.text(Zmin, -p_bottom, 'old cam min dist')
    # plt.xlabel('distance')
    # plt.ylabel('pixels from image center')
    # plt.show()
    # Zmin_from_old_cam = f * (fe.dist_f(w, f * cam_height / Zmin / f))
    # Z50cm = f * (fe.dist_f(w, f * cam_height / 50 / f))
    # print("z_min_from_old_cam: {}\nz_50cm: {}".format(Z_func(Zmin),))


if __name__ == '__main__':
    #TODO: convert to fixed-point before remaping, using INTER_LINEARcv2.convertMaps()
    test()
    with timer() as t:
        fe = Fisheye(hw=[800, 800],
                     padval=0,
                     w=0.9407,
                     f=261.3,
                     c=[240, 320])  #[255.23, 296.52])
        # img = plt.imread('/media/noam/Storage/semanticseg/datasets/annots_findgrass/rgo_annots_20210121_color/20200820_Ofek10b_color/img/frame-000000212959.png')
        # img = plt.imread('/media/noam/Storage/semanticseg/datasets/rgo_videos/multicam/20210325_082245_rgb_CaesareaMigdalPark/Images_col_MLRI_800x800/frame-000000194063.png')
        # img = plt.imread('/media/noam/Storage/semanticseg/datasets/rgo_videos/full/EP34_27042021/20210518_floor_tiles/Images/frame-000061938600.pgm')
        img = plt.imread('/media/noam/Storage/semanticseg/datasets/rgo_videos/full/EP34_27042021/20210518_floor_tiles/Images/frame-000061938856.pgm')
        img = np.dstack([img] * 3)
        # img = plt.imread('/media/noam/Storage/semanticseg/datasets/annots_findgrass/rgo_annots_20210121_color/20200820_Ofek10b_color/img/frame-000000199231.png')
        # img = np.hstack([img]*3)
        # img = cv2.resize(img, (473, 473))
        img_udist = fe.transform(img, fe.undist_maps, border_value=-1)
        plt.imshow(img)
        plt.show()
        plt.imshow(img_udist.astype(np.uint8))
        plt.show()
        plt.imshow(fe.transform(img_udist, fe.dist_maps, border_value=-1).astype(np.uint8))
        plt.show()
        # plt.imshow(
        #     fe.transform(fe.transform(img, fe.dist_maps, border_value=-1), fe.undist_maps).astype(np.uint8)[:480, :640,
        #     :])
        # plt.show()
        # plt.imshow(img)
        # plt.show()
        1==1

        # # test spherical fisheye against simple plane
        # fe = Fisheye(hw=[480, 640],
        #              padval=0,
        #              w=2 * np.arctan(0.5),
        #              f=261.3,
        #              c=[240, 320])
        # L = 1000
        # x, y = np.meshgrid(range(img.shape[1]), range(img.shape[0]))
        # r = (x ** 2 + y ** 2) ** 0.5
        #
        # r_ctr = ((x - fe.c[1]) ** 2 + (y - fe.c[0]) ** 2) ** 0.5
        # x_ctr, y_ctr = x - fe.c[1], y - fe.c[0]
        # theta = r_ctr / fe.f
        # phi = np.arctan2(y, x)
        # r_p = L * np.tan(r_ctr / fe.f)
        #
        # r_fe = fe.transform(np.dstack([r_ctr] * 3), fe.shell2fe_maps, border_value=-1)
        # r_camplane = fe.transform(np.dstack([r_fe] * 3), fe.undist_maps, border_value=-1)
        #
        # # x_fe = fe.transform(np.dstack([x_ctr] * 3), fe.usphere2fe_maps, border_value=-1)
        # # y_fe = fe.transform(np.dstack([y_ctr] * 3), fe.usphere2fe_maps, border_value=-1)
        # # r_fe = (x ** 2 + y ** 2) ** 0.5
        # # x_camplane = fe.transform(x_fe, fe.undist_maps, border_value=-1)
        # # y_camplane = fe.transform(y_fe, fe.undist_maps, border_value=-1)
        # # r_camplane = (x_camplane ** 2 + y_camplane ** 2) ** 0.5
        #
        # r_p2 = r_camplane / fe.f * L
        # y_test = img.shape[0] // 2
        # plt.scatter(x=r[y_test, :], y=r_p[y_test, :], c='b')
        # plt.scatter(x=r[y_test, :], y=r_p2[y_test, :, 0], s=2, c='r')
        # plt.show()

        # # test 3d rotations
        # img_lines = np.zeros((480, 640, 3))
        # for xx in range(0, img_lines.shape[1], 20):
        #     img_lines[20:-20, xx, :] = 255
        # for yy in range(0, img_lines.shape[0], 20):
        #     img_lines[yy, 20:-20, :] = 255
        # img_lines_t = fe.transform(img_lines, fe.dist_maps, border_value=2)[fe.padval:-fe.padval,fe.padval:-fe.padval]
        #
        # rotmap = fe.prepRot_sphereBased2(rot=[1, 0.1, 4 * np.pi /4], remap_sphere2fe=False, border_value=2)
        # img_rot = fe.transform(img_lines_t, rotmap, border_value=2)[fe.padval:-fe.padval,fe.padval:-fe.padval]
        # img_u = fe.transform(img_rot, fe.usphere2fe_maps, 2)[fe.padval:-fe.padval,fe.padval:-fe.padval]  #cv2.remap(img_rot, fe.usphere2fe_maps[0], fe.usphere2fe_maps[1], interpolation=cv2.INTER_LINEAR)
        # img_u = fe.transform(img_u, fe.undist_maps, 2)[fe.padval:-fe.padval,fe.padval:-fe.padval]   # cv2.remap(img_u, fe.undist_maps[0], fe.undist_maps[1], interpolation=cv2.INTER_LINEAR)
        # plt.imshow(cv2.equalizeHist(img_u.astype(np.uint8)[..., 0]), cmap='gray')
        # plt.plot(*fe.c[::-1] - fe.padval, 'x', c='r')
        # plt.show()


        # plt.imshow(img_lines)
        # plt.show()
        # plt.imshow(img_lines_t)
        # plt.show()
        #
        1==1

        # from train_predict import preprocessing
        #
        # img2, _ = preprocessing.random_spatial_saturation(img, img)
        # plt.imshow(img2)
        # plt.show()
    print(t.t)




    # ######## fix for wider fisheye rotations - under development #########
    #
    #
    # rot_map = fe.prepRot_sphereBased()
    # with timer() as t:
    #     fe.make_rot_collection()
    # print(t.t)
    # for _ in range(10):
    #     with timer() as t:
    #         a = fe.rot_from_bag(img, img)[0]
    #     print(t.t)
    #     plt.imshow(a)
    #     plt.show()
    #
    #

    # with timer() as t:
    #     img_rot = fe.rot_w_plane_proj(rot=[0, np.pi / 4, 0], img=img)[0]
    # print(t.t)
    # plt.imshow(img_rot)
    # plt.show()

    # img_rot = fe.rot_w_plane_proj(img, rot=[0, 0, 0], deblur=False)[0]
    # img_bck = img[:,::-1,:]
    # plt.imshow(np.where(img_rot,img_rot,img_bck))
    # plt.show()

    # plt.imshow(fe.rot_w_plane_proj(rot=[0.1, 1, 0.1], img=img)[0])
    # plt.show()

    # ###### double img rotate #######
    # x = np.random.uniform(np.pi/6, np.pi/3) * [1, -1][np.random.randint(2)]  #np.pi / 5
    # y = np.random.uniform(-np.pi/50, np.pi/50)
    # z = np.random.uniform(-np.pi/90, np.pi/90)
    #
    # x2 = np.clip(x + 0.8, a_min=-np.pi / 3, a_max=np.pi / 3)
    # rot_a = fe.rot_w_plane_proj(rot=[y, x, z], img=img)[0]
    # rot_a[rot_a == 0] = fe.rot_w_plane_proj(rot=[y, x2, z], img=img)[0][rot_a == 0]
    # plt.imshow(rot_a)
    # plt.show()

    # plt.imshow(fe.rot_w_plane_proj(fe.rot_w_plane_proj(img, rot=[0, np.pi / 8, 0])[0], rot=[0, np.pi / 8, 0])[0])
    # plt.show()
    # plt.imshow(img)
    # plt.show()
    # plt.imshow(fe.plane2fe(fe.fe2plane(img))[fe.padval:fe.hw_padded[0] - fe.padval, fe.padval:fe.hw_padded[1] - fe.padval, :])
    # plt.show()
    # plt.imshow(fe.fe2plane(img))
    # plt.show()
    # plt.imshow(fe.rot_w_plane_proj(img)[0])
    # plt.show()
    # plt.imshow(fe.rot_w_plane_proj(img)[0])
    # plt.show()
    # t0 = time.time()
    # fig, ax = plt.subplots(2, 3)
    # ax[0, 0].imshow(img)
    # ax[0, 1].imshow(fe.rot_w_plane_proj(img, rot=[0, 0, 0])[0] - img)
    # ax[0, 2].imshow(fe.fe2plane(img))
    # ax[1, 0].imshow(fe.rot_w_plane_proj(img, rot=[0, 0, 0])[0])
    # ax[1, 1].imshow(fe.rot_w_plane_proj(img, rot=[0, 0.5, 0])[0])
    # ax[1, 2].imshow(fe.rot_w_plane_proj(img, rot=[0, -0.5, 0])[0])
    # print(time.time() - t0)
    # plt.show()




