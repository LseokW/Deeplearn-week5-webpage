# Regularization (규제)

## 개요

규제(Regularization)는 딥러닝 모델의 **과적합(Overfitting)**을 방지하는 핵심 기법입니다.
모델이 훈련 데이터에 너무 맞춰지면 새로운 데이터에 대한 예측이 나빠집니다.
규제를 통해 모델의 복잡도를 제한하고 일반화 성능을 높입니다.

---

## 1. L1 / L2 정규화

### L2 정규화 (Weight Decay)

손실 함수에 가중치의 제곱합을 추가합니다.

$$L_{total} = L_{original} + \lambda \sum w_i^2$$

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu',
                       kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dense(64, activation='relu',
                       kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dense(10, activation='softmax')
])
```

### L1 정규화

손실 함수에 가중치의 절댓값 합을 추가합니다. 희소(sparse) 가중치를 유도합니다.

```python
keras.layers.Dense(128, activation='relu',
                   kernel_regularizer=keras.regularizers.l1(0.001))
```

| 구분 | L1 | L2 |
|------|----|----|
| 수식 | λ Σ\|w\| | λ Σw² |
| 효과 | 가중치를 0으로 만듦 (희소성) | 가중치를 작게 만듦 |
| 사용 | 특성 선택 | 일반적인 정규화 |

---

## 2. Dropout

학습 시 무작위로 뉴런을 비활성화하여 과적합을 방지합니다.
앙상블 학습과 유사한 효과를 냅니다.

```python
model = keras.Sequential([
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.5),   # 50% 뉴런을 랜덤하게 끔
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(10, activation='softmax')
])
```

> **주의**: Dropout은 학습 시에만 적용되고, 추론(inference) 시에는 자동으로 비활성화됩니다.

---

## 3. Batch Normalization

미니배치 단위로 입력을 정규화하여 학습을 안정화하고 속도를 높입니다.

```python
model = keras.Sequential([
    keras.layers.Dense(256),
    keras.layers.BatchNormalization(),   # 정규화
    keras.layers.Activation('relu'),     # 활성화 함수는 BN 뒤에
    keras.layers.Dense(128),
    keras.layers.BatchNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Dense(10, activation='softmax')
])
```

**Batch Normalization의 장점:**
- 학습률을 더 높게 설정 가능
- 가중치 초기화에 덜 민감
- Dropout 없이도 정규화 효과

---

## 실습 코드

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# 데이터 준비
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# 규제 없는 모델 (과적합 위험)
model_no_reg = keras.Sequential([
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 규제 적용 모델
model_reg = keras.Sequential([
    keras.layers.Dense(512, activation='relu',
                       kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.4),
    keras.layers.Dense(512, activation='relu',
                       kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.4),
    keras.layers.Dense(10, activation='softmax')
])

model_reg.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model_reg.fit(
    x_train, y_train,
    epochs=20, batch_size=128,
    validation_split=0.2,
    verbose=1
)
```

결과 이미지:

![Regularization 비교](01_regularization_plot.png)
