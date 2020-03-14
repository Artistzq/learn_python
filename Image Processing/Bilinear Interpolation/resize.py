import imageio
import numpy as np
from matplotlib import pyplot as plt


class Solution(object):

    def imresize(self, origin_image, origin_size: tuple, target_size: tuple, ret_gray: bool = True) -> np.ndarray:
        """
        把目标图片origin_image从origin_size转换到target_size大小，使用双线性插值法.

        Parameters
        ----------
        origin_image : 图像数组, list或np.ndarray子类
            需要被转换尺寸的原图。为灰度图或RGB彩色图
        origin_size : tuple
            源尺寸， 建议使用 origin_image.shape[:2]
        target_size : tuple
            目的尺寸
        ret_grey : bool, optional
            返回单通道（灰度图）还是三通道（彩色或灰色），默认单通道（灰度图），即ndim=2

        Returns
        -------
        np.ndarray
            转换后的图片.
        """
        assert origin_size == origin_image.shape[:2], "传入源图片和源尺寸不符"
        origin_image = np.asarray(
            origin_image, dtype=np.uint8)     # 转换为np.ndarray类型便于处理
        assert origin_image.ndim == 3 or origin_image.ndim == 2, "只接受三通道或单通道图片"
        # 如果是单通道图片（a, b），转为三通道处理(a, b, 1)
        if origin_image.ndim == 2:
            origin_image = np.expand_dims(origin_image, axis=-1)

        # 创建目标图片实体，尺寸为目标尺寸 + 通道数
        target_image = np.zeros(target_size + origin_image.shape[2:])
        # 缩放比例
        scale_x, scale_y = (
            (origin_size[0]-1)/(target_size[0]-1), (origin_size[1]-1)/(target_size[1]-1))
        for num in range(origin_image.shape[2]):
            # 对每个通道进行双线性差值
            channel = target_image[:, :, num]
            origin_channel = origin_image[:, :, num]
            for i in range(channel.shape[0]):
                for j in range(channel.shape[1]):
                    x, y = (i*scale_x, j*scale_y)
                    l_b = (int(x), int(y))          # 左下的点坐标， 如果在图像边界，需要防止数组越界
                    if l_b[1] == origin_size[1]-1 and l_b[0] != origin_size[0]-1:
                        l_b = (int(x), int(y)-1)
                    elif l_b[1] != origin_size[1]-1 and l_b[0] == origin_size[0]-1:
                        l_b = (int(x)-1, int(y))
                    elif l_b[1] == origin_size[1]-1 and l_b[0] == origin_size[0]-1:
                        l_b = (int(x)-1, int(y)-1)
                    r_t = (l_b[0]+1, l_b[1]+1)      # 右上的点坐标
                    l_t = (l_b[0], l_b[1]+1)        # 左上
                    r_b = (l_b[0]+1, l_b[1])        # 右下
                    a = l_t[0] - x
                    b = l_t[1] - y
                    # 双线性插值
                    channel[i, j] = (1-a)*(1-b)*origin_channel[l_t[0], l_t[1]] + a*(1-b)*origin_channel[r_t] + (
                        1-a)*b*origin_channel[l_b[0], l_b[1]] + a*b*origin_channel[r_b[0], r_b[1]]
        # 转换为无符号8位二进制整数
        target_image = target_image.astype(np.uint8)
        if ret_gray:
            return target_image[:, :, 0]  # 二维图，单通道，灰度图
        else:
            return target_image          # 三维图， 灰度图或者彩色图


if __name__ == "__main__":
    s = Solution()
    origin_image = imageio.imread("flowergray.jpg")
    origin_size = origin_image.shape[:2]
    target_size = (100, 100)
    target_img = s.imresize(origin_image, origin_size, target_size)

    plt.subplot(1, 2, 1)
    plt.imshow(origin_image, cmap="gray")
    plt.subplot(1, 2, 2)
    plt.imshow(target_img, cmap="gray")
    plt.show()
