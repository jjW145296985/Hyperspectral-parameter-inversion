import numpy as np
from osgeo import gdal
import cv2

def extract_and_save_rgb(input_tif_path, output_image_path):
    """
    提取GF-1的蓝、绿、红波段，并保存为OpenCV可读的RGB图像
    :param input_tif_path: 输入GF-1的TIF文件路径
    :param output_image_path: 输出图像路径（支持.jpg或.png）
    """
    # 1. 读取GF-1数据
    ds = gdal.Open(input_tif_path)
    if ds is None:
        raise ValueError("无法打开文件，请检查路径！")

    # 获取波段数据（假设波段顺序为B、G、R、NIR）
    b = ds.GetRasterBand(1).ReadAsArray()  # 蓝波段
    g = ds.GetRasterBand(2).ReadAsArray()  # 绿波段
    r = ds.GetRasterBand(3).ReadAsArray()  # 红波段

    # 2. 将数据归一化到0-255（假设原始数据是反射率或DN值）
    # 如果数据是浮点型反射率（如0-1），直接乘以255
    # if b.dtype == np.float32 or b.dtype == np.float64:
    #     b = (b * 255).clip(0, 255).astype(np.uint8)
    #     g = (g * 255).clip(0, 255).astype(np.uint8)
    #     r = (r * 255).clip(0, 255).astype(np.uint8)
    # # 如果是整型DN值，线性拉伸到0-255
    # else:
    #     b = cv2.normalize(b, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #     g = cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #     r = cv2.normalize(r, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # # 3. 合并为3波段RGB图像（OpenCV顺序为BGR！）
    # rgb = cv2.merge([b, g, r])
    #
    # # 4. 保存为OpenCV可读格式（JPG或PNG）
    # 保存为带地理信息的GeoTIFF（替换cv2.imwrite）
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(output_image_path, ds.RasterXSize, ds.RasterYSize, 3, gdal.GDT_Byte)
    for i, band in enumerate([b, g, r], 1):
        out_ds.GetRasterBand(i).WriteArray(band)
    out_ds.SetProjection(ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.FlushCache()
    out_ds = None  # 确保文件写入磁盘
    print(f"RGB图像已保存至：{output_image_path}")

    # # 可选：返回RGB数组供后续处理
    # return rgb

# 示例调用
if __name__ == "__main__":
    input_tif = "GF1_PMS1_E119.3_N30.5_20250606_L1A13908417001-MSS1.tiff"  # 替换为你的GF-1文件路径
    output_image = "3bd.tif"  # 输出图像路径
    rgb_array = extract_and_save_rgb(input_tif, output_image)