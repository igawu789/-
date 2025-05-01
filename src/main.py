import tkinter as tk
from tkinter import messagebox
import threading # 导入线程模块
from osgeo import gdal
import numpy as np
import os # 导入 os 模块


# 已经定义或从其他模块导入
from io_utils import get_geo, get_nodata, get_optimal_block_size
from projection import reproject_to_utm50
from process_image import fuse_images
from process_overlap import extract_overlap
from ui import ImageNormalizationUI # 导入你的 UI 类

# --- 1. 定义核心处理函数 ---
def run_color_normalization(params, ui_instance):
    """
    执行遥感影像匀色的核心处理流程。

    Args:
        params (dict): 从 UI 获取的参数字典。
        ui_instance (ImageNormalizationUI): UI 实例，用于更新进度和日志。
    """
    raster1 = None # 初始化为 None，确保 finally 块能处理未成功打开的情况
    raster2 = None
    reprojected_path1_temp = None # 临时存储重投影文件路径

    try:
        print("--- 开始处理 ---")
        ui_instance.set_progress(0) # 重置进度条

        # --- 2. 从字典中提取参数 ---
        path1 = params["image1_path"]
        path2 = params["image2_path"]
        output_dir = params["output_path"]
        # 提取随机森林参数 (这些需要传递给 fuse_images 或相关处理步骤)
        rf_params = {k: v for k, v in params.items() if k not in ["image1_path", "image2_path", "output_path"]}
        print("随机森林及采样参数:", rf_params)

        # --- 3. 执行你的 GDAL 和 Numpy 处理流程 ---
        print(f"正在打开参考图像: {path1}")
        print(f"正在打开待匀色图像: {path2}")
        raster1 = gdal.Open(path1)
        raster2 = gdal.Open(path2)
        if raster1 is None:
            raise ValueError(f"无法打开图像: {path1}")
        if raster2 is None:
             raise ValueError(f"无法打开图像: {path2}")

        ui_instance.set_progress(5)

        transform1, bound1, crs1 = get_geo(path1)
        transform2, bound2, crs2 = get_geo(path2)
        print("投影信息（CRS1）:", crs1)
        print("投影信息（CRS2）:", crs2)

        # 判断并处理投影不一致
        if crs1 != crs2:
            print(f"投影不同，正在将 {os.path.basename(path1)} 重投影到 {crs2}...")
            # 创建一个临时文件名用于存储重投影结果
            reprojected_path1_temp = os.path.join(output_dir, f"temp_reprojected_{os.path.basename(path1)}")
            print(f"临时重投影文件: {reprojected_path1_temp}")

            # 确保你的 projection.reproject_to_utm50 函数存在且可用
            reproject_to_utm50(path1, reprojected_path1_temp, crs2) # 调用重投影函数
            # ********** 占位符：你需要调用实际的重投影函数 **********
            print("警告: 重投影函数 'projection.reproject_to_utm50' 未实现或未调用！")
            # *****************************************************

            raster1 = None # 关闭原始文件
            path1 = reprojected_path1_temp # 更新 path1 为重投影后的路径
            raster1 = gdal.Open(path1) # 重新打开重投影后的文件
            if raster1 is None:
                raise ValueError(f"无法打开重投影后的图像: {path1}")
            transform1, bound1, crs1 = get_geo(path1) # 重新获取地理信息
            print("重投影后投影信息（CRS1）:", crs1)
        else:
            print("图像投影一致，无需重投影。")

        ui_instance.set_progress(15)

        # 读取数据并处理 NoData
        # 注意：get_nodata 需要正确处理并返回 numpy 数组
        print("读取图像数据并处理 NoData 值...")
        # 假设 get_nodata 返回 (nodata_value, numpy_array)
        no_data1, raster1_new_array = get_nodata(raster1)
        no_data2, raster2_new_array = get_nodata(raster2)

        # 确保返回的是 numpy 数组
        if not isinstance(raster1_new_array, np.ndarray):
            raster1_new_array = np.array(raster1_new_array)
        if not isinstance(raster2_new_array, np.ndarray):
             raster2_new_array = np.array(raster2_new_array)

        print("图像1处理后形状:", raster1_new_array.shape, "数据类型:", raster1_new_array.dtype)
        print("图像2处理后形状:", raster2_new_array.shape, "数据类型:", raster2_new_array.dtype)

        ui_instance.set_progress(25)

        # 提取重叠区域
        print("提取重叠区域...")
        # 确保 extract_overlap 使用的是处理后的 numpy 数组和正确的地理信息
        overlap1, overlap2 = extract_overlap(raster1_new_array, transform1, bound1,
                                             raster2_new_array, transform2, bound2)

        # 检查重叠区结果
        if overlap1 is None or overlap2 is None or overlap1.size == 0 or overlap2.size == 0:
            raise ValueError("未能成功提取重叠区域或重叠区域为空。")
        print(f"提取到重叠区域1形状: {overlap1.shape}")
        print(f"提取到重叠区域2形状: {overlap2.shape}")

        ui_instance.set_progress(40)

        # --- 4. 调用你的核心匀色/融合函数 ---
        print("开始执行匀色/融合...")
        block_size = get_optimal_block_size() # 获取块大小
        print(f"使用块大小: {block_size}")

        # ********** 重要: 修改 fuse_images 函数签名 **********
        # 你需要修改 fuse_images 函数，使其能够接收并使用 rf_params 字典中的参数
        # 例如: def fuse_images(..., rf_params, ui_callback=None):
        # 在 fuse_images 内部:
        #   n_estimators = rf_params['n_estimators']
        #   # ... 获取其他参数 ...
        #   # 在循环或耗时操作中调用 ui_callback(percentage) 更新进度
        # **************************************************
        fuse_images(
            overlap1=overlap1,
            overlap2=overlap2,
            image1=raster1_new_array,
            image2=raster2_new_array,
            path1 = path1,
            path2 = path2,
            output_dir=output_dir,
            block_size=block_size,
            rf_params=rf_params,        # <--- 传递随机森林参数
            ui_callback=ui_instance.set_progress # <--- 传递进度更新回调函数
        )


        ui_instance.set_progress(100)
        print("--- 处理成功完成 ---")
        messagebox.showinfo("成功", "影像匀色处理完成！")

    except Exception as e:
        error_message = f"处理过程中发生错误: {e}"
        print(f"错误: {error_message}")
        import traceback
        traceback.print_exc() # 打印详细的错误堆栈信息到控制台/日志
        messagebox.showerror("错误", error_message)
        ui_instance.set_progress(0) # 出错时重置进度条


    finally:

        # --- 5. 清理资源 ---

        print("关闭 GDAL 数据集...")

        # Correct way to close GDAL datasets: remove references

        if raster1 is not None:
            raster1 = None

            print("已释放 raster1 引用.")

        if raster2 is not None:
            raster2 = None

            print("已释放 raster2 引用.")

        # 可选：删除临时的重投影文件

        if reprojected_path1_temp and os.path.exists(reprojected_path1_temp):

            try:

                os.remove(reprojected_path1_temp)

                print(f"已删除临时文件: {reprojected_path1_temp}")

            except OSError as e:

                print(f"删除临时文件失败: {e}")

        # 重新启用提交按钮

        if ui_instance:
            # 确保在主线程中更新UI元素

            # Using after(0, ...) is a good practice for thread safety with Tkinter UI updates

            ui_instance.master.after(0, lambda: ui_instance.button_submit.config(state=tk.NORMAL))

            print("提交按钮已重新启用.")  # Added for clarity

        print("--- 清理完成 ---")


# --- 主函数 ---
def main():
    # 启用 GDAL 异常处理
    gdal.UseExceptions()

    root = tk.Tk()
    app = ImageNormalizationUI(root) # 创建 UI 实例

    # --- 包装函数，由提交按钮触发 ---
    def on_submit_wrapper():
        params = app.submit() # 调用 UI 的 submit 方法获取参数字典
        if params:
            # 参数校验通过
            print("UI 参数获取成功，准备开始处理...")
            # 禁用按钮防止重复点击
            app.button_submit.config(state=tk.DISABLED)
            # 创建并启动处理线程
            processing_thread = threading.Thread(
                target=run_color_normalization, # 线程执行的函数
                args=(params, app),            # 传递参数字典和 UI 实例
                daemon=True                    # 设置为守护线程，主程序退出时线程也退出
            )
            processing_thread.start()
        else:
            # 参数校验失败 (ui.submit 内部会显示错误消息)
            print("UI 参数校验失败，请检查输入。")

    # --- 将包装函数绑定到 UI 的提交按钮 ---
    app.button_submit.config(command=on_submit_wrapper)

    # --- 启动 Tkinter 事件循环 ---
    root.mainloop()


if __name__ == "__main__":
    # --- 运行主函数 ---
    main()