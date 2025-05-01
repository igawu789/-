# ui.py
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import sys
import os  # 导入 os 模块用于路径检查

class ImageNormalizationUI:
    def __init__(self, master):
        self.master = master
        self.master.title("随机森林遥感影像匀色")
        self.master.geometry("500x750") # 调整窗口大小以容纳更多参数

        # --- 输入图像 ---
        input_frame = tk.Frame(master, pady=5)
        input_frame.pack(fill=tk.X)
        tk.Label(input_frame, text="输入图像设置", font=("Arial", 10, "bold")).pack()

        # 输入图像1 (参考图像)
        frame1 = tk.Frame(input_frame)
        frame1.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame1, text="参考图像 (Image 1):", width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_image1 = tk.Entry(frame1)
        self.entry_image1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.button_image1 = tk.Button(frame1, text="浏览", command=self.select_image1)
        self.button_image1.pack(side=tk.RIGHT)

        # 输入图像2 (待匀色图像)
        frame2 = tk.Frame(input_frame)
        frame2.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame2, text="待匀色图像 (Image 2):", width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_image2 = tk.Entry(frame2)
        self.entry_image2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.button_image2 = tk.Button(frame2, text="浏览", command=self.select_image2)
        self.button_image2.pack(side=tk.RIGHT)

        # --- 随机森林参数 ---
        rf_frame = tk.LabelFrame(master, text="随机森林参数设置", padx=10, pady=10)
        rf_frame.pack(fill=tk.X, padx=10, pady=5)

        # n_estimators
        row1 = tk.Frame(rf_frame)
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="树的数量 (n_estimators):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_n_estimators = tk.Entry(row1, width=10)
        self.entry_n_estimators.insert(0, "100")  # 默认值
        self.entry_n_estimators.pack(side=tk.LEFT, padx=5)

        # max_depth
        row2 = tk.Frame(rf_frame)
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="最大深度 (max_depth, 留空不限制):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_max_depth = tk.Entry(row2, width=10)
        self.entry_max_depth.insert(0, "")  # 默认不限制
        self.entry_max_depth.pack(side=tk.LEFT, padx=5)

        # min_samples_split
        row3 = tk.Frame(rf_frame)
        row3.pack(fill=tk.X, pady=2)
        tk.Label(row3, text="最小分裂样本数 (min_samples_split):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_min_samples_split = tk.Entry(row3, width=10)
        self.entry_min_samples_split.insert(0, "2")  # 默认值
        self.entry_min_samples_split.pack(side=tk.LEFT, padx=5)

        # min_samples_leaf
        row4 = tk.Frame(rf_frame)
        row4.pack(fill=tk.X, pady=2)
        tk.Label(row4, text="最小叶节点样本数 (min_samples_leaf):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_min_samples_leaf = tk.Entry(row4, width=10)
        self.entry_min_samples_leaf.insert(0, "1")  # 默认值
        self.entry_min_samples_leaf.pack(side=tk.LEFT, padx=5)

        # max_features
        row5 = tk.Frame(rf_frame)
        row5.pack(fill=tk.X, pady=2)
        tk.Label(row5, text="最大特征数 (max_features, 'sqrt', 'log2', <1 比例):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_max_features = tk.Entry(row5, width=10)
        self.entry_max_features.insert(0, "sqrt")  # 默认值
        self.entry_max_features.pack(side=tk.LEFT, padx=5)

        # random_state
        row6 = tk.Frame(rf_frame)
        row6.pack(fill=tk.X, pady=2)
        tk.Label(row6, text="随机种子 (random_state, 留空不固定):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_random_state = tk.Entry(row6, width=10)
        self.entry_random_state.insert(0, "42")  # 默认值，方便复现
        self.entry_random_state.pack(side=tk.LEFT, padx=5)

        # n_jobs
        row7 = tk.Frame(rf_frame)
        row7.pack(fill=tk.X, pady=2)
        tk.Label(row7, text="并行任务数 (n_jobs, -1 使用所有核心):", width=25, anchor='w').pack(side=tk.LEFT)
        self.entry_n_jobs = tk.Entry(row7, width=10)
        self.entry_n_jobs.insert(0, "-1")  # 默认值
        self.entry_n_jobs.pack(side=tk.LEFT, padx=5)


        # --- 训练样本采样设置 ---
        sampling_frame = tk.LabelFrame(master, text="训练样本采样设置", padx=10, pady=10)
        sampling_frame.pack(fill=tk.X, padx=10, pady=5)

        # num_samples
        s_row1 = tk.Frame(sampling_frame)
        s_row1.pack(fill=tk.X, pady=2)
        tk.Label(s_row1, text="训练样本点数:", width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_num_samples = tk.Entry(s_row1, width=10)
        self.entry_num_samples.insert(0, "50000")  # 默认值
        self.entry_num_samples.pack(side=tk.LEFT, padx=5)

        # sampling_method (使用 Combobox 更佳，但为简单起见保留 Entry)
        s_row2 = tk.Frame(sampling_frame)
        s_row2.pack(fill=tk.X, pady=2)
        tk.Label(s_row2, text="采样方法:", width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_sampling_method = tk.Entry(s_row2, width=10)
        self.entry_sampling_method.insert(0, "random") # 默认值
        self.entry_sampling_method.pack(side=tk.LEFT, padx=5)
        # 可以考虑使用 ttk.Combobox 提供选项:
        # self.combo_sampling_method = ttk.Combobox(s_row2, values=["random", "stratified"], width=8)
        # self.combo_sampling_method.set("random")
        # self.combo_sampling_method.pack(side=tk.LEFT, padx=5)


        # --- 输出路径 ---
        output_frame = tk.Frame(master, pady=5)
        output_frame.pack(fill=tk.X)
        tk.Label(output_frame, text="输出设置", font=("Arial", 10, "bold")).pack()

        frame_out = tk.Frame(output_frame)
        frame_out.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(frame_out, text="输出路径:", width=20, anchor='w').pack(side=tk.LEFT)
        self.entry_output = tk.Entry(frame_out)
        self.entry_output.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.button_output = tk.Button(frame_out, text="浏览", command=self.select_output)
        self.button_output.pack(side=tk.RIGHT)

        # --- 提交按钮 ---
        self.button_submit = tk.Button(self.master, text="开始处理", command=self.submit, height=2)
        self.button_submit.pack(pady=10)

        # --- 进度条 ---
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=480, mode="determinate")
        self.progress.pack(pady=5, padx=10)

        # --- 日志输出区 ---
        self.log_text = tk.Text(self.master, height=10, width=70)
        self.log_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # 重定向 print 输出
        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")


    def select_image1(self):
        # 选择TIF文件，同时允许所有文件类型
        file_path = filedialog.askopenfilename(
            title="选择参考图像 (Image 1)",
            filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")]
        )
        if file_path: # 确保用户选择了文件
            self.entry_image1.delete(0, tk.END)
            self.entry_image1.insert(0, file_path)

    def select_image2(self):
         # 选择TIF文件，同时允许所有文件类型
        file_path = filedialog.askopenfilename(
            title="选择待匀色图像 (Image 2)",
            filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")]
        )
        if file_path: # 确保用户选择了文件
            self.entry_image2.delete(0, tk.END)
            self.entry_image2.insert(0, file_path)

    def select_output(self):
        output_path = filedialog.askdirectory(title="选择输出文件夹")
        if output_path: # 确保用户选择了文件夹
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, output_path)

    def submit(self):
        # 获取并校验用户输入
        image1_path = self.entry_image1.get()
        image2_path = self.entry_image2.get()
        output_path = self.entry_output.get()

        # 校验路径
        if not image1_path or not os.path.isfile(image1_path):
            messagebox.showerror("错误", "请选择有效的参考图像文件！")
            return None
        if not image2_path or not os.path.isfile(image2_path):
            messagebox.showerror("错误", "请选择有效的待匀色图像文件！")
            return None
        if not output_path or not os.path.isdir(output_path):
            messagebox.showerror("错误", "请选择有效的输出路径！")
            return None

        try:
            # 获取并校验随机森林参数
            n_estimators_str = self.entry_n_estimators.get()
            n_estimators = int(n_estimators_str)
            if n_estimators <= 0:
                raise ValueError("树的数量必须是正整数")

            max_depth_str = self.entry_max_depth.get()
            max_depth = int(max_depth_str) if max_depth_str else None
            if max_depth is not None and max_depth <= 0:
                raise ValueError("最大深度必须是正整数或留空")

            min_samples_split_str = self.entry_min_samples_split.get()
            min_samples_split = int(min_samples_split_str)
            if min_samples_split < 2:
                raise ValueError("最小分裂样本数必须 >= 2")

            min_samples_leaf_str = self.entry_min_samples_leaf.get()
            min_samples_leaf = int(min_samples_leaf_str)
            if min_samples_leaf <= 0:
                 raise ValueError("最小叶节点样本数必须是正整数")

            max_features_str = self.entry_max_features.get().lower() # 转小写方便比较
            max_features = None
            if max_features_str in ['sqrt', 'log2']:
                max_features = max_features_str
            else:
                try:
                    max_features_val = float(max_features_str)
                    if 0 < max_features_val <= 1:
                        max_features = max_features_val # 比例
                    elif max_features_val > 1 and max_features_val == int(max_features_val):
                         max_features = int(max_features_val) # 整数
                    else:
                        raise ValueError("无效的最大特征数值")
                except ValueError:
                     raise ValueError("最大特征数必须是 'sqrt', 'log2', 0到1的小数或正整数")

            random_state_str = self.entry_random_state.get()
            random_state = int(random_state_str) if random_state_str else None

            n_jobs_str = self.entry_n_jobs.get()
            n_jobs = int(n_jobs_str)

            # 获取并校验采样参数
            num_samples_str = self.entry_num_samples.get()
            num_samples = int(num_samples_str)
            if num_samples <= 0:
                 raise ValueError("训练样本点数必须是正整数")

            sampling_method = self.entry_sampling_method.get().strip().lower()
            # 这里可以添加对 sampling_method 的具体值校验，例如：
            # if sampling_method not in ["random", "stratified"]:
            #     raise ValueError("采样方法无效，当前支持 'random', 'stratified'")

            # 如果一切正常，打印参数并准备返回 (实际应用中，这里会调用处理函数)
            print("--- 参数校验通过 ---")
            print(f"参考图像: {image1_path}")
            print(f"待匀色图像: {image2_path}")
            print(f"输出路径: {output_path}")
            print(f"n_estimators: {n_estimators}")
            print(f"max_depth: {max_depth}")
            print(f"min_samples_split: {min_samples_split}")
            print(f"min_samples_leaf: {min_samples_leaf}")
            print(f"max_features: {max_features}")
            print(f"random_state: {random_state}")
            print(f"n_jobs: {n_jobs}")
            print(f"num_samples: {num_samples}")
            print(f"sampling_method: {sampling_method}")
            print("---------------------")

            # 返回所有收集到的参数，用于后续处理
            # 注意：这里不再调用 self.master.quit()，以便UI可以持续显示日志和进度
            # 处理逻辑应该在调用此UI的代码中进行
            return {
                "image1_path": image1_path,
                "image2_path": image2_path,
                "output_path": output_path,
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "min_samples_leaf": min_samples_leaf,
                "max_features": max_features,
                "random_state": random_state,
                "n_jobs": n_jobs,
                "num_samples": num_samples,
                "sampling_method": sampling_method
            }

        except ValueError as e:
            messagebox.showerror("参数错误", f"输入参数无效: {e}")
            return None
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {e}")
            return None

    def set_progress(self, value):
        # 设置进度条
        self.progress["value"] = value
        self.master.update_idletasks() # 使用 update_idletasks 避免界面卡顿

    def log(self, message):
        # 方便外部调用写入日志
        print(message)


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag # 可以用来区分 stdout 和 stderr

    def write(self, str):
        # 确保在主线程更新UI
        self.widget.after(0, self._write_callback, str)

    def _write_callback(self, str):
        self.widget.configure(state="normal") # 允许编辑
        self.widget.insert(tk.END, str, (self.tag,)) # 可以为不同来源设置不同tag样式
        self.widget.see(tk.END) # 自动滚动到底部
        self.widget.configure(state="disabled") # 禁止编辑

    def flush(self):
        # 在Tkinter上下文中，flush通常不需要特殊操作
        pass

