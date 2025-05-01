This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# 遥感影像随机森林匀色工具 (Random Forest Remote Sensing Image Color Normalization Tool)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 概述 (Overview)

本工具提供了一个图形用户界面 (GUI)，用于对两幅重叠的遥感影像进行色彩归一化（匀色）处理。它利用随机森林 (Random Forest) 回归算法，在影像的重叠区域学习色彩映射关系，并将学习到的模型应用于整个影像，生成色彩协调一致的结果图像。

This tool provides a Graphical User Interface (GUI) for performing color normalization (harmonization) between two overlapping remote sensing images. It utilizes the Random Forest regression algorithm to learn the color mapping relationship in the overlapping areas of the images and applies the learned models to the entire images to generate color-consistent output images.

## 主要功能 (Features)

*   **图形用户界面 (GUI):** 通过 Tkinter 构建，方便用户选择输入/输出文件和调整参数。
*   **随机森林模型:** 使用 Scikit-learn 的 `RandomForestRegressor` 对像素级色彩进行建模和预测。
*   **自动重叠区提取:** 自动计算并提取两幅输入影像的地理重叠区域。
*   **投影处理:** 能够检测输入影像的坐标参考系统 (CRS)，并在 CRS 不一致时自动对其中一幅进行重投影（目前基于 `projection.py` 中的实现）。
*   **分块处理:** 对完整的输入影像进行分块处理，以降低内存消耗，适用于较大的遥感影像。
*   **参数可调:** 用户可以调整随机森林模型的关键超参数（如树的数量、最大深度等）以及训练样本的数量。
*   **双向匀色:** 同时生成两个结果：将影像1匀色到影像2的色彩风格 (`LocalB_*.tif`)，以及将影像2匀色到影像1的色彩风格 (`LocalA_*.tif`)。
*   **进度显示与日志:** 在 GUI 中提供进度条和日志输出区域，方便用户监控处理过程。

## 环境要求 (Requirements)

*   **Python:** 3.8 或更高版本 (Python 3.8+ recommended)
*   **GDAL (`osgeo`):** 地理空间数据处理库。**注意：GDAL 的安装可能比较复杂，强烈建议使用 Conda 进行安装。** (Note: GDAL installation can be complex. Using Conda is highly recommended.)
*   **NumPy:** 科学计算库。
*   **Scikit-learn:** 机器学习库（用于随机森林）。
*   **Tkinter:** Python 标准 GUI 库（通常随 Python 安装）。

## 安装步骤 (Installation)

1.  **创建虚拟环境 (推荐):**
    *   **Using `venv`:**
        ```bash
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        venv\Scripts\activate    # Windows
        ```
    *   **Using Conda:**
        ```bash
        conda create -n rf_color_norm python=3.9 -y
        conda activate rf_color_norm
        ```

2.  **安装 GDAL:**
    *   **Using Conda (推荐):** 这是最简单可靠的方式。
        ```bash
        conda install -c conda-forge gdal
        ```
    *   **Using pip (可能需要预编译的 wheel 文件或系统库):**
        查阅 GDAL 官方文档或社区资源（如 Christoph Gohlke's Windows wheels）获取适合你操作系统的安装方法。直接 `pip install GDAL` 往往会失败。

3.  **安装其他 Python 库:**
    ```bash
    pip install numpy scikit-learn
    ```
    (Tkinter 通常是内置的)

4.  **获取代码:**
    将项目代码（`main.py`, `ui.py`, `io_utils.py`, `projection.py`, `process_image.py`, `process_overlap.py` 等）放在同一个目录下。

## 使用方法 (Usage)

1.  **打开终端或命令行。**
2.  **激活你的虚拟环境** (如果创建了)。
3.  **导航到项目代码所在的目录。**
4.  **运行主程序:**
    ```bash
    python main.py
    ```
5.  **图形界面将会弹出:**
    *   **选择输入图像:**
        *   点击 "参考图像 (Image 1)" 旁边的 "浏览" 按钮，选择第一幅 `.tif` 影像。
        *   点击 "待匀色图像 (Image 2)" 旁边的 "浏览" 按钮，选择第二幅 `.tif` 影像。
    *   **设置随机森林参数:**
        *   根据需要调整 "树的数量 (n_estimators)"、"最大深度 (max_depth)" 等参数。留空表示使用默认值或不限制。
        *   调整 "训练样本点数 (num_samples)" 来控制用于训练模型的数据量。
    *   **选择输出路径:**
        *   点击 "输出路径" 旁边的 "浏览" 按钮，选择一个用于存放结果文件的文件夹。
    *   **开始处理:**
        *   点击 "开始处理" 按钮。
6.  **监控进度:**
    *   程序将在下方的日志区域输出处理信息。
    *   进度条会显示大致的处理进度。
7.  **查看结果:**
    *   处理完成后，会在指定的输出路径下生成两个文件，例如：
        *   `LocalB_*.tif`: 影像1经过匀色，匹配影像2的色彩风格。
        *   `LocalA_*.tif`: 影像2经过匀色，匹配影像1的色彩风格。
    *   同时，日志区域会显示 "--- 处理成功完成 ---" 或相应的错误信息。

## 文件结构 (File Structure)

*   `main.py`: 主程序入口，负责启动 GUI，协调各个处理模块。
*   `ui.py`: 定义 Tkinter 图形用户界面的布局和组件。
*   `io_utils.py`: 包含读写栅格数据、获取地理信息、处理 NoData 值等辅助函数。
*   `projection.py`: 包含影像重投影相关的函数。
*   `process_image.py`: 核心影像处理逻辑，包括数据归一化、随机森林训练、分块应用模型、保存结果等。
*   `process_overlap.py`: 包含提取影像重叠区域的函数。

## 工作流程简述 (Workflow Outline)

1.  通过 GUI 获取用户输入的影像路径、输出路径和模型参数。
2.  加载参考影像 (Img1) 和待匀色影像 (Img2)。
3.  检查两幅影像的坐标参考系统 (CRS)。如果不同，将 Img1 重投影到 Img2 的 CRS。
4.  读取影像数据，处理 NoData 值。
5.  计算并提取 Img1 和 Img2 地理上的重叠区域。
6.  从重叠区域中采样指定数量的像素对。
7.  对采样像素进行归一化处理。
8.  基于采样像素训练两个随机森林模型：
    *   模型 A->B: 学习如何将 Img1 的像素值映射到 Img2 的像素值。
    *   模型 B->A: 学习如何将 Img2 的像素值映射到 Img1 的像素值。
9.  将模型 A->B 应用于完整的 Img1 (分块处理)，生成结果 `LocalB_*.tif`。
10. 将模型 B->A 应用于完整的 Img2 (分块处理)，生成结果 `LocalA_*.tif`。
11. 保存生成的匀色后影像。

## 注意事项 (Notes)

*   输入影像应为 GDAL 支持的栅格格式，推荐使用 GeoTIFF (`.tif`)。
*   输入影像需要有正确的地理参考信息（坐标系和仿射变换参数）才能正确提取重叠区。
*   处理时间和内存消耗取决于影像大小、选择的块大小以及随机森林参数（尤其是树的数量和样本点数）。
*   GDAL 的安装是关键，请确保其正确安装并能被 Python 环境找到。



