import numpy as np

# 归一化数据
def normalize(data, block_size=1024):
    """ 使用 2%-98% 分位数归一化，分块处理减少内存占用 """
    q2 = np.nanpercentile(data, 2)  # 计算 2% 分位数
    q98 = np.nanpercentile(data, 98)  # 计算 98% 分位数
    print(f"2% 分位数: {q2}, 98% 分位数: {q98}")

    if q98 == q2:
        print("Warning: 98% 和 2% 分位数相同，归一化可能失败")
        return np.zeros_like(data), q2, q98  # 避免除 0

    # 预分配内存
    normalized_data = np.zeros_like(data, dtype=np.float32)

    # 分块归一化
    for i in range(0, data.shape[0], block_size):
        for j in range(0, data.shape[1], block_size):
            block = data[i:i + block_size, j:j + block_size]
            normalized_data[i:i + block_size, j:j + block_size] = np.clip((block - q2) / (q98 - q2), 0, 1)

    return normalized_data, q2, q98

def normalize_noq2(data, q98, q2, block_size=1024):
    """ 使用已知 q2 和 q98 进行归一化，分块处理减少内存占用 """
    if q98 == q2:
        print("Warning: 98% 和 2% 分位数相同，归一化可能失败")
        return np.zeros_like(data)  # 避免除 0

    # 预分配内存
    normalized_data = np.zeros_like(data, dtype=np.float32)

    # 分块归一化
    for i in range(0, data.shape[0], block_size):
        for j in range(0, data.shape[1], block_size):
            block = data[i:i + block_size, j:j + block_size]
            normalized_data[i:i + block_size, j:j + block_size] = np.clip((block - q2) / (q98 - q2), 0, 1)

    return normalized_data




# 反归一化数据
def denormalize(data, min_val, max_val):
    if np.isnan(min_val) or np.isnan(max_val):
        print("Error: min_val 或 max_val 计算错误")
        return np.full_like(data, np.nan)

    result = data * (max_val - min_val) + min_val
    result_int = np.round(result).astype(np.int32)

    # 添加调试信息
    # print(f"反归一化：min_val={min_val}, max_val={max_val}")
    # print(f"输入数据范围: {np.min(data)} ~ {np.max(data)}")
    # print(f"反归一化后数据范围: {np.min(result_int)} ~ {np.max(result_int)}")

    return result_int


# 将数据展开并归一化,要同时删去两个图像的对应nan索引，因此要放在一个函数
def flatten_and_normalize(overlap1, overlap2):
    # 展平图像并记录 NaN 位置
    overlap1_flat = overlap1.flatten()
    overlap2_flat = overlap2.flatten()

    # 找到 overlap1 中的 NaN 值的索引
    nan_mask = np.isnan(overlap1_flat)

    # 删除 overlap1 和 overlap2 中对应的 NaN 值
    overlap1_cleaned = overlap1_flat[~nan_mask]
    overlap2_cleaned = overlap2_flat[~nan_mask]

    print(f"Shape of overlap1_cleaned after NaN removal: {overlap1_cleaned.shape}")
    print(f"Shape of overlap2_cleaned after NaN removal: {overlap2_cleaned.shape}")
    # 删除2
    nan_mask = np.isnan(overlap2_cleaned)
    overlap1_cleaned = overlap1_cleaned[~nan_mask]
    overlap2_cleaned = overlap2_cleaned[~nan_mask]

    overlap1_cleaned = overlap1_cleaned.reshape(-1, 1)
    overlap2_cleaned = overlap2_cleaned.reshape(-1, 1)
    print(f"Shape of overlap1_cleaned after NaN removal: {overlap1_cleaned.shape}")
    print(f"Shape of overlap2_cleaned after NaN removal: {overlap2_cleaned.shape}")

    nan_mask = np.isnan(overlap1_cleaned)
    valid_indices = ~nan_mask

    print("1有效像素数:", np.sum(overlap1_cleaned))

    # 提取有效数据
    valid_data = overlap1_cleaned[valid_indices].reshape(-1, 1)
    if valid_data.size == 0:
        print("1所有数据均为 NaN，返回全 NaN 影像")
        return np.full_like(overlap1, np.nan)

    print("1有效数据均值:", np.mean(valid_data))

    # 归一化（使用 clip 限制范围）
    # normalized_data = np.clip((valid_data - src_min) / (src_max - src_min), 0, 1)
    norm_overlap1, min_val1, max_val1  = normalize(valid_data)

    print("norm_overlap1归一化后数据均值:", np.nanmean(norm_overlap1))

    # 确保归一化后数据无 NaN
    if np.isnan(norm_overlap1).any():
        print("Error: norm_overlap1归一化数据包含 NaN")
        return np.full_like(overlap1, np.nan)



    nan_mask = np.isnan(overlap2_cleaned)
    valid_indices = ~nan_mask

    print("2有效像素数:", np.sum(valid_indices))

    # 提取有效数据
    valid_data = overlap2_cleaned[valid_indices].reshape(-1, 1)
    if valid_data.size == 0:
        print("2所有数据均为 NaN，返回全 NaN 影像")
        return np.full_like(overlap2, np.nan)

    print("2有效数据均值:", np.mean(valid_data))

    # 归一化（使用 clip 限制范围）
    # normalized_data = np.clip((valid_data - src_min) / (src_max - src_min), 0, 1)
    norm_overlap2, min_val2, max_val2 = normalize(valid_data)

    print("norm_overlap2归一化后数据均值:", np.nanmean(norm_overlap2))

    # 确保归一化后数据无 NaN
    if np.isnan(norm_overlap2).any():
        print("Error: norm_overlap2归一化数据包含 NaN")
        return np.full_like(overlap2, np.nan)

    return norm_overlap1, norm_overlap2, min_val1, max_val1, min_val2, max_val2
