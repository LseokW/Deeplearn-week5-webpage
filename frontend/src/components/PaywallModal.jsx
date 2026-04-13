import { X, Lock, CreditCard } from "lucide-react";
import { useState } from "react";
import client from "../api/client";

export default function PaywallModal({ onClose }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handlePurchase() {
    setLoading(true);
    setError("");
    try {
      const res = await client.post("/api/payment/checkout");
      window.location.href = res.data.data.checkout_url;
    } catch (err) {
      setError(
        err.response?.data?.detail?.message ||
          "결제 페이지 연결에 실패했습니다. 잠시 후 다시 시도해주세요."
      );
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X size={20} />
        </button>

        <div className="flex flex-col items-center text-center gap-4">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
            <Lock size={28} className="text-blue-600" />
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900">5주차 열람권</h2>
            <p className="text-gray-500 mt-2 text-sm leading-relaxed">
              이 콘텐츠는 유료 콘텐츠입니다.
              <br />
              5주차 전체 5개 섹션을 무제한 열람하세요.
            </p>
          </div>

          <div className="w-full bg-blue-50 rounded-xl p-4 text-left">
            <p className="text-xs text-blue-700 font-semibold mb-2">포함된 섹션</p>
            {[
              "Regularization (규제)",
              "Overfitting vs Underfitting",
              "Data Augmentation (데이터 증강)",
              "Transfer Learning (전이 학습)",
              "MNIST CNN 실습",
            ].map((s) => (
              <p key={s} className="text-sm text-blue-800 flex items-center gap-1.5 py-0.5">
                <span className="text-blue-400">✓</span> {s}
              </p>
            ))}
          </div>

          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}

          <button
            onClick={handlePurchase}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-60"
          >
            <CreditCard size={18} />
            {loading ? "연결 중..." : "polar.sh로 결제하기"}
          </button>

          <p className="text-xs text-gray-400">
            polar.sh의 안전한 결제 시스템을 이용합니다.
          </p>
        </div>
      </div>
    </div>
  );
}
