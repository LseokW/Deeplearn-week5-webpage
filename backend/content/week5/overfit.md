# Overfitting vs Underfitting

## 개요

모델 학습에서 가장 중요한 두 가지 문제:

- **과적합(Overfitting)**: 훈련 데이터에는 잘 맞지만 새로운 데이터에는 성능이 나쁨
- **과소적합(Underfitting)**: 훈련 데이터조차 제대로 학습하지 못함

![Overfitting vs Underfitting 비교](02_overfitting_underfitting.png)

---

## 1. 편향-분산 트레이드오프 (Bias-Variance Tradeoff)

| 문제 | 편향(Bias) | 분산(Variance) |
|------|-----------|----------------|
| 과소적합 | 높음 | 낮음 |
| 적절한 모델 | 낮음 | 낮음 |
| 과적합 | 낮음 | 높음 |

$$\text{오차} = \text{편향}^2 + \text{분산} + \text{불가피한 노이즈}$$

---

## 2. 과적합 진단

```python
import matplotlib.pyplot as plt

def plot_learning_curves(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # 손실 곡선
    ax1.plot(history.history['loss'], label='훈련 손실')
    ax1.plot(history.history['val_loss'], label='검증 손실')
    ax1.set_title('학습/검증 손실')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()

    # 정확도 곡선
    ax2.plot(history.history['accuracy'], label='훈련 정확도')
    ax2.plot(history.history['val_accuracy'], label='검증 정확도')
    ax2.set_title('학습/검증 정확도')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('learning_curves.png', dpi=150)
    plt.show()
```

**과적합 징후:**
- 훈련 손실은 계속 감소하지만 검증 손실은 증가
- 훈련 정확도 >> 검증 정확도

---

## 3. 해결 방법

### 과적합 해결

```python
from tensorflow import keras

# 방법 1: 더 많은 데이터 수집/증강
# 방법 2: 모델 단순화
model_simple = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 방법 3: Early Stopping
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,          # 5 epoch 동안 개선 없으면 중단
    restore_best_weights=True
)

# 방법 4: Dropout + L2
model_reg = keras.Sequential([
    keras.layers.Dense(256, activation='relu',
                       kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='softmax')
])

history = model_reg.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=0
)

print(f"학습 중단 epoch: {early_stop.stopped_epoch}")
```

### 과소적합 해결

```python
# 모델 복잡도 증가
model_complex = keras.Sequential([
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 학습률 조정
model_complex.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 더 많은 epoch으로 학습
history = model_complex.fit(x_train, y_train, epochs=50)
```

---

## 4. 모델 복잡도 선택 가이드

```python
# 검증 곡선으로 최적 복잡도 찾기
import numpy as np

layer_sizes = [32, 64, 128, 256, 512]
val_accuracies = []

for size in layer_sizes:
    model = keras.Sequential([
        keras.layers.Dense(size, activation='relu'),
        keras.layers.Dense(size // 2, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=10,
                        validation_split=0.2, verbose=0)
    val_accuracies.append(max(history.history['val_accuracy']))

best_size = layer_sizes[np.argmax(val_accuracies)]
print(f"최적 레이어 크기: {best_size}, 검증 정확도: {max(val_accuracies):.4f}")
```
