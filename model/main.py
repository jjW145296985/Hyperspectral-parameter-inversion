from water import water_extract_NDWI
from contours import draw_contours, river_end
from buildshp import raster2shp, raster2vector
from water_quality import water_quality_test


if __name__ == '__main__':

    # 读取原始影像进行水体提取
    water_extract_NDWI('GF1_PMS1_E119.3_N30.5_20250606_L1A13908417001-MSS1.tiff')
    # 读取3波段影像3bd.tif和水体二值图影像NDWI_mask.jpg
    # 提取所有水体轮廓NDWI_water.jpg，进行滤波NDWI_river.jpg，几何约束NDWI_end.jpg，最终获取河流二值图NDWI_river_end.jpg
    draw_contours('3bd.tif', 'NDWI_mask.jpg', 'NDWI_water.jpg', 'NDWI_river.jpg', 'NDWI_end.jpg', 'NDWI_river_end.jpg')    # 绘制轮廓
    # 二值图转shp文件
    raster2shp('NDWI_river_end.jpg', 'NDWI.shp')

    # 进行水质反演
    water_quality_test("chuli.tif")

