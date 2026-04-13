import { Link } from "react-router-dom";
import { BookOpen, Lock, Zap, Award } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/Layout";

const SECTIONS = [
  { id: "reg", title: "Regularization (규제)", desc: "L1/L2, Dropout, Batch Normalization" },
  { id: "overfit", title: "Overfitting vs Underfitting", desc: "과적합/과소적합 진단 및 해결" },
  { id: "augment", title: "Data Augmentation", desc: "RandomFlip, RandomRotation, RandomZoom" },
  { id: "transfer", title: "Transfer Learning", desc: "MobileNetV2, Feature Extraction, Fine-tuning" },
  { id: "cnn", title: "MNIST CNN 실습", desc: "Conv2D, MaxPooling2D, 완전한 CNN 파이프라인" },
];

export default function Landing() {
  const { user, login } = useAuth();

  return (
    <Layout>
      {/* Hero */}
      <section className="text-center py-16">
        <span className="inline-block bg-blue-100 text-blue-700 text-xs font-semibold px-3 py-1 rounded-full mb-4">
          Week 5 · 딥러닝 핵심 개념
        </span>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight">
          딥러닝을 제대로 배우는<br />
          <span className="text-blue-600">가장 빠른 방법</span>
        </h1>
        <p className="mt-4 text-lg text-gray-500 max-w-xl mx-auto">
          Regularization부터 Transfer Learning까지,<br />
          실습 코드와 함께 딥러닝 핵심 개념을 완벽하게 이해하세요.
        </p>
        <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
          {user ? (
            <Link
              to="/week5"
              className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
            >
              강의 보러가기 →
            </Link>
          ) : (
            <button
              onClick={login}
              className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
            >
              Google로 시작하기
            </button>
          )}
        </div>
      </section>

      {/* 특장점 */}
      <section className="grid sm:grid-cols-3 gap-6 my-12">
        {[
          { icon: <BookOpen className="text-blue-500" />, title: "구조화된 강의", desc: "개념 설명 + 코드 예시 + 결과 이미지로 구성된 완성도 높은 학습 자료" },
          { icon: <Zap className="text-yellow-500" />, title: "즉시 실습 가능", desc: "복사해서 바로 실행 가능한 Python/TensorFlow 코드 제공" },
          { icon: <Award className="text-green-500" />, title: "5개 핵심 주제", desc: "딥러닝 입문자가 반드시 알아야 할 5가지 핵심 개념 완전 정복" },
        ].map((item) => (
          <div key={item.title} className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <div className="mb-3">{item.icon}</div>
            <h3 className="font-semibold text-gray-800 mb-1">{item.title}</h3>
            <p className="text-sm text-gray-500">{item.desc}</p>
          </div>
        ))}
      </section>

      {/* 목차 미리보기 */}
      <section className="my-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">5주차 커리큘럼</h2>
        <p className="text-gray-500 mb-6">구매 후 모든 섹션을 무제한 열람할 수 있습니다.</p>
        <div className="space-y-3">
          {SECTIONS.map((s, i) => (
            <div key={s.id} className="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
              <div className="w-9 h-9 bg-blue-50 text-blue-600 font-bold rounded-full flex items-center justify-center text-sm flex-shrink-0">
                {i + 1}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-800">{s.title}</p>
                <p className="text-xs text-gray-400 mt-0.5">{s.desc}</p>
              </div>
              <Lock size={16} className="text-gray-300 flex-shrink-0" />
            </div>
          ))}
        </div>
      </section>
    </Layout>
  );
}
