import numpy as np
import rasterio

# 提取公共区域并处理 NaN
def extract_overlap(image1,transform1,bound1,image2,transform2,bound2):

    # 计算公共区域的边界
    print(f'bound1,bound2{bound1},{bound2}')
    print(f'transform1,{transform1}')
    print(f'transform2,{transform2}')



    intersection_left = max(bound1.left, bound2.left)
    intersection_right = min(bound1.right, bound2.right)
    intersection_top = min(bound1.top, bound2.top)
    intersection_bottom = max(bound1.bottom, bound2.bottom)
    print(f'left,right,top,bottom{intersection_left},{intersection_right},{intersection_top},{intersection_bottom}')

    if intersection_right <= intersection_left or intersection_top <= intersection_bottom:
        raise ValueError("没有交叉区域")

    # 获取行列索引
    rowcol1_top_left = rasterio.transform.rowcol(transform1, intersection_left, intersection_top)
    rowcol1_bottom_right = rasterio.transform.rowcol(transform1, intersection_right, intersection_bottom)
    rowcol2_top_left = rasterio.transform.rowcol(transform2, intersection_left, intersection_top)
    rowcol2_bottom_right = rasterio.transform.rowcol(transform2, intersection_right, intersection_bottom)

    # # 提取公共区域数据
    # window1 = Window(rowcol1_top_left[1], rowcol1_top_left[0],
    #                  rowcol1_bottom_right[1] - rowcol1_top_left[1],
    #                  rowcol1_bottom_right[0] - rowcol1_top_left[0])
    # window2 = Window(rowcol2_top_left[1], rowcol2_top_left[0],
    #                  rowcol2_bottom_right[1] - rowcol2_top_left[1],
    #                  rowcol2_bottom_right[0] - rowcol2_top_left[0])
    # 计算窗口大小
    height1 = rowcol1_bottom_right[0] - rowcol1_top_left[0]
    width1 = rowcol1_bottom_right[1] - rowcol1_top_left[1]
    height2 = rowcol2_bottom_right[0] - rowcol2_top_left[0]
    width2 = rowcol2_bottom_right[1] - rowcol2_top_left[1]

    # 计算公共区域宽度和高度_要保证两个图像长宽一致！
    height = min(height1, height2)
    width = min(width1, width2)

    # 提取公共区域（改了一下，不知道可不可以用）
    overlap1 = [band[rowcol1_top_left[0]:rowcol1_top_left[0] + height,
                rowcol1_top_left[1]:rowcol1_top_left[1] + width] for band in image1]

    overlap2 = [band[rowcol2_top_left[0]:rowcol2_top_left[0] + height,
                rowcol2_top_left[1]:rowcol2_top_left[1] + width] for band in image2]

    # 将数据转换为 MaskedArray 并处理 NaN
    # overlap1 = np.ma.masked_invalid(overlap1)
    # overlap2 = np.ma.masked_invalid(overlap2)

    overlap1 = np.ma.filled(overlap1, np.nan)
    overlap2 = np.ma.filled(overlap2, np.nan)

    print(f"Extracted overlap shapes: {overlap1[0].shape} and {overlap2[0].shape}")
    # 打印最终的 masked 数组形状和均值
    print(f"Overlap1 masked shape: {[data.shape for data in overlap1]}")
    for i, data in enumerate(overlap1):
        print(f"Overlap1 band {i + 1} mean: {np.nanmean(data)}")

    print(f"Overlap2 masked shape: {[data.shape for data in overlap2]}")
    for i, data in enumerate(overlap2):
        print(f"Overlap2 band {i + 1} mean: {np.nanmean(data)}")
    return overlap1, overlap2
