# MNIST CNN 실습

## 개요

합성곱 신경망(CNN)을 구현하여 MNIST 손글씨 숫자를 분류합니다.
Conv2D, MaxPooling2D, Flatten, Dense 레이어의 역할을 이해하고
완전한 분류 파이프라인을 구축합니다.

![CNN 결과](05_mnist_cnn_result.png)

---

## 1. CNN 구조 이해

```
입력 (28×28×1)
    ↓
Conv2D(32, 3×3) → (26×26×32)
    ↓
MaxPooling2D(2×2) → (13×13×32)
    ↓
Conv2D(64, 3×3) → (11×11×64)
    ↓
MaxPooling2D(2×2) → (5×5×64)
    ↓
Flatten → (1600,)
    ↓
Dense(128) → (128,)
    ↓
Dropout(0.5)
    ↓
Dense(10, softmax) → (10,)
```

---

## 2. 전체 구현

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# 1. 데이터 로드 및 전처리
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# CNN은 (H, W, C) 형태 필요
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

print(f"훈련 데이터: {x_train.shape}")  # (60000, 28, 28, 1)
print(f"테스트 데이터: {x_test.shape}")  # (10000, 28, 28, 1)

# 2. 모델 구성
model = keras.Sequential([
    # 첫 번째 합성곱 블록
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),

    # 두 번째 합성곱 블록
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),

    # 세 번째 합성곱 블록
    keras.layers.Conv2D(64, (3, 3), activation='relu'),

    # 분류 헤드
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='softmax')
], name="mnist_cnn")

model.summary()
```

---

## 3. 학습

```python
# 3. 컴파일
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 콜백 설정
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_accuracy', patience=3, restore_best_weights=True
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=2, min_lr=1e-7
    )
]

# 4. 학습
history = model.fit(
    x_train, y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.1,
    callbacks=callbacks,
    verbose=1
)

# 5. 평가
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n테스트 정확도: {test_acc:.4f} ({test_acc*100:.2f}%)")
```

---

## 4. 결과 시각화

```python
# 학습 곡선
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(history.history['accuracy'], label='훈련')
ax1.plot(history.history['val_accuracy'], label='검증')
ax1.set_title('정확도')
ax1.set_xlabel('Epoch')
ax1.legend()

ax2.plot(history.history['loss'], label='훈련')
ax2.plot(history.history['val_loss'], label='검증')
ax2.set_title('손실')
ax2.set_xlabel('Epoch')
ax2.legend()

plt.tight_layout()
plt.savefig('mnist_cnn_training.png', dpi=150)
plt.show()

# 예측 시각화
predictions = model.predict(x_test[:25])
pred_labels = np.argmax(predictions, axis=1)

fig, axes = plt.subplots(5, 5, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i].reshape(28, 28), cmap='gray')
    color = 'green' if pred_labels[i] == y_test[i] else 'red'
    ax.set_title(f"예측: {pred_labels[i]}", color=color)
    ax.axis('off')

plt.suptitle(f"MNIST CNN 예측 결과 (정확도: {test_acc*100:.1f}%)")
plt.tight_layout()
plt.savefig('mnist_predictions.png', dpi=150)
plt.show()
```

---

## 5. Conv2D 필터 시각화

```python
# 첫 번째 합성곱 레이어의 필터 시각화
first_conv = model.layers[0]
filters, biases = first_conv.get_weights()

fig, axes = plt.subplots(4, 8, figsize=(12, 6))
for i, ax in enumerate(axes.flat):
    if i < filters.shape[-1]:
        ax.imshow(filters[:, :, 0, i], cmap='viridis')
    ax.axis('off')

plt.suptitle("Conv2D 첫 번째 레이어 필터 (32개)")
plt.tight_layout()
plt.show()
```

---

## 기대 성능

| 모델 | 테스트 정확도 |
|------|-------------|
| MLP (Dense only) | ~98% |
| CNN (위 구조) | ~99.2% |
| 고급 CNN + Augmentation | ~99.7% |
