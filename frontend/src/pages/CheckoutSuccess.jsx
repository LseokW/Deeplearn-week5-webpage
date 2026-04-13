import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import { CheckCircle } from "lucide-react";

export default function CheckoutSuccess() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center py-20 text-center gap-6">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
          <CheckCircle size={40} className="text-green-500" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">결제 완료!</h1>
          <p className="text-gray-500 mt-2">
            5주차 열람권 구매가 완료되었습니다.
            <br />
            이제 모든 섹션을 자유롭게 열람할 수 있습니다.
          </p>
        </div>
        <Link
          to="/week5"
          className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
        >
          강의 시작하기 →
        </Link>
      </div>
    </Layout>
  );
}
