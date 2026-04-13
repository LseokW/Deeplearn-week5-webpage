# Transfer Learning (전이 학습)

## 개요

전이 학습은 대규모 데이터셋으로 사전 학습된 모델의 지식을 새로운 태스크에 활용하는 기법입니다.
수백만 장의 이미지로 학습된 특성 추출기를 그대로 재사용하여 적은 데이터로도 높은 성능을 달성할 수 있습니다.

---

## 1. 전이 학습 전략

### Feature Extraction (특성 추출)
- 사전 학습 모델의 가중치를 **고정(freeze)**
- 마지막 분류 레이어만 새로 학습

### Fine-tuning (미세 조정)
- 특성 추출 후, 일부 상위 레이어의 **동결을 해제**
- 낮은 학습률로 전체 네트워크를 재학습

---

## 2. MobileNetV2로 Feature Extraction

```python
import tensorflow as tf
from tensorflow import keras

# CIFAR-10 (32x32 → 96x96으로 리사이즈)
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

def preprocess(image, label):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, [96, 96])
    image = keras.applications.mobilenet_v2.preprocess_input(image)
    return image, label

train_ds = (tf.data.Dataset.from_tensor_slices((x_train, y_train))
            .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
            .shuffle(10000).batch(32).prefetch(tf.data.AUTOTUNE))
test_ds = (tf.data.Dataset.from_tensor_slices((x_test, y_test))
           .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
           .batch(32).prefetch(tf.data.AUTOTUNE))

# 사전 학습 모델 로드 (분류 헤드 제외)
base_model = keras.applications.MobileNetV2(
    input_shape=(96, 96, 3),
    include_top=False,        # 마지막 분류 레이어 제외
    weights='imagenet'        # ImageNet 사전 학습 가중치
)

# 가중치 동결 (Feature Extraction)
base_model.trainable = False

# 분류 헤드 추가
inputs = keras.Input(shape=(96, 96, 3))
x = base_model(inputs, training=False)
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs, outputs)
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print(f"전체 파라미터: {model.count_params():,}")
print(f"학습 가능 파라미터: {sum([tf.size(v).numpy() for v in model.trainable_variables]):,}")

# Phase 1: Feature Extraction
history_fe = model.fit(train_ds, epochs=10, validation_data=test_ds)
```

---

## 3. Fine-tuning

```python
# Phase 2: Fine-tuning (상위 레이어 동결 해제)
base_model.trainable = True

# 하위 100개 레이어는 계속 동결
for layer in base_model.layers[:100]:
    layer.trainable = False

# 낮은 학습률로 재컴파일 (중요!)
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),   # 10배 낮춤
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_ft = model.fit(train_ds, epochs=10, validation_data=test_ds)
```

---

## 4. 사전 학습 모델 비교

| 모델 | 파라미터 | Top-1 정확도 | 특징 |
|------|---------|-------------|------|
| MobileNetV2 | 3.4M | 71.8% | 경량, 모바일 최적화 |
| EfficientNetB0 | 5.3M | 77.1% | 효율적인 스케일링 |
| ResNet50 | 25.6M | 74.9% | 잔차 연결 |
| VGG16 | 138M | 71.3% | 단순하지만 무거움 |
| InceptionV3 | 23.9M | 77.9% | 다양한 커널 크기 |

---

## 5. 사전 학습 모델 선택 가이드

```python
# 데이터셋 크기에 따른 전략
def choose_strategy(dataset_size):
    if dataset_size < 1000:
        return "Feature Extraction만 사용 (동결 유지)"
    elif dataset_size < 10000:
        return "Feature Extraction → 상위 레이어만 Fine-tuning"
    else:
        return "전체 Fine-tuning 가능"

# 예시: 꽃 분류 (소규모 데이터셋)
flowers_ds = tf.keras.utils.get_file(
    'flower_photos',
    'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    untar=True
)
```
