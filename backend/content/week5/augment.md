# Data Augmentation (데이터 증강)

## 개요

데이터 증강은 기존 훈련 데이터를 다양하게 변형하여 데이터셋의 크기와 다양성을 늘리는 기법입니다.
별도의 데이터 수집 없이 모델의 일반화 성능을 크게 향상시킬 수 있습니다.

![데이터 증강 예시](03_augmentation_examples.png)

---

## 1. Keras 증강 레이어

TensorFlow 2.x부터 증강을 모델 레이어로 직접 추가할 수 있습니다.

```python
import tensorflow as tf
from tensorflow import keras

data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),          # 좌우 반전
    keras.layers.RandomRotation(0.1),               # ±10% 회전
    keras.layers.RandomZoom(0.1),                   # ±10% 확대/축소
    keras.layers.RandomTranslation(0.1, 0.1),       # 이동
    keras.layers.RandomContrast(0.1),               # 대비 조정
])
```

---

## 2. 이미지 분류 모델에 증강 적용

```python
import tensorflow as tf
from tensorflow import keras

# CIFAR-10 데이터
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 증강 레이어 정의
data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomRotation(0.1),
    keras.layers.RandomZoom(0.1),
], name="data_augmentation")

# 모델 구성 (증강 포함)
inputs = keras.Input(shape=(32, 32, 3))
x = data_augmentation(inputs, training=True)   # 학습 시에만 증강
x = keras.layers.Conv2D(32, 3, activation='relu', padding='same')(x)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.Conv2D(64, 3, activation='relu', padding='same')(x)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.Flatten()(x)
x = keras.layers.Dense(128, activation='relu')(x)
x = keras.layers.Dropout(0.3)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs, outputs)
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(x_train, y_train, epochs=30,
                    validation_data=(x_test, y_test),
                    batch_size=64)
```

---

## 3. 증강 효과 시각화

```python
import matplotlib.pyplot as plt
import numpy as np

# 단일 이미지에 증강 반복 적용
sample_image = x_train[0:1]  # (1, 32, 32, 3)

plt.figure(figsize=(12, 4))
plt.subplot(1, 9, 1)
plt.imshow(sample_image[0])
plt.title("원본")
plt.axis('off')

for i in range(8):
    augmented = data_augmentation(sample_image, training=True)
    plt.subplot(1, 9, i + 2)
    plt.imshow(augmented[0].numpy())
    plt.title(f"증강 {i+1}")
    plt.axis('off')

plt.tight_layout()
plt.savefig('augmentation_examples.png', dpi=150)
plt.show()
```

---

## 4. 증강 기법 비교

| 기법 | 설명 | 적합한 도메인 |
|------|------|---------------|
| RandomFlip | 좌우/상하 반전 | 자연 이미지 |
| RandomRotation | 임의 회전 | 자연 이미지, 의료 이미지 |
| RandomZoom | 확대/축소 | 대부분 |
| RandomTranslation | 이동 | 대부분 |
| RandomBrightness | 밝기 조정 | 실외 이미지 |
| CutMix | 이미지 잘라 섞기 | 고급 분류 |
| MixUp | 이미지 블렌딩 | 고급 분류 |

---

## 5. tf.data 파이프라인과 증강

```python
import tensorflow as tf

BATCH_SIZE = 64
AUTOTUNE = tf.data.AUTOTUNE

def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.1)
    image = tf.image.random_contrast(image, 0.9, 1.1)
    return image, label

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_ds = (
    train_ds
    .shuffle(10000)
    .map(augment, num_parallel_calls=AUTOTUNE)   # 병렬 증강
    .batch(BATCH_SIZE)
    .prefetch(AUTOTUNE)                           # 다음 배치 미리 준비
)

val_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test))
val_ds = val_ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)

model.fit(train_ds, validation_data=val_ds, epochs=30)
```
