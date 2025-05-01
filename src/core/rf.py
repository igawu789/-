from sklearn.ensemble import RandomForestRegressor
from tqdm import tqdm
import numpy as np

# 这应该就算得到了一个函数
def train_random_forest(X, y, rf_params): # <-- NEW (accepts params)
    # Inside train_random_forest:
    # model = RandomForestRegressor(...) <-- OLD
    model = RandomForestRegressor(
        n_estimators=rf_params.get('n_estimators', 10), # Use .get for defaults
        max_depth=rf_params.get('max_depth', None),
        min_samples_split=rf_params.get('min_samples_split', 2),
        min_samples_leaf=rf_params.get('min_samples_leaf', 1),
        max_features=rf_params.get('max_features', 'sqrt'),
        random_state=rf_params.get('random_state', None),
        n_jobs=rf_params.get('n_jobs', -1),
        # ... other RF params if needed
    )
    for i in tqdm(range(1, model.n_estimators + 1), desc="Training RandomForest"):
        model.n_estimators = i  # 逐步增加树的数量
        model.fit(X, y)  # 继续训练
    # ... rest of training ...
    return model


# 这个是用上面得到的函数进行预测。所以输入的数据应当是，原始图像对吧
# 预测函数，带进度条
def predict_with_rf(rf, input_data, description="Predicting with RandomForest"):
    input_data = input_data.reshape(-1, 1)

    # 使用 tqdm 显示进度条
    with tqdm(total=len(input_data), desc=description, unit="samples") as pbar:
        predictions = rf.predict(input_data)
        # 打印预测结果的形状和部分内容进行检查
        print(f"Predictions shape: {predictions.shape}")
        print(f"Some of the predictions: {predictions[:5]}")  # 打印前五个预测结果
        pbar.update(len(predictions))

    return np.array(predictions)
