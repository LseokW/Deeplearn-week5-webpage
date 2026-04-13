import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";
import client from "../api/client";
import { User, ShoppingBag } from "lucide-react";

export default function Dashboard() {
  const { user } = useAuth();
  const [purchaseStatus, setPurchaseStatus] = useState(null);

  useEffect(() => {
    client.get("/api/payment/status").then((res) => {
      setPurchaseStatus(res.data.data);
    });
  }, []);

  if (!user) return null;

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">내 대시보드</h1>

      {/* 프로필 */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 mb-6 flex items-center gap-5">
        <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-200 flex-shrink-0">
          {user.picture_url ? (
            <img src={user.picture_url} alt={user.name} className="w-full h-full object-cover" />
          ) : (
            <User size={32} className="m-2 text-gray-400" />
          )}
        </div>
        <div>
          <p className="font-semibold text-gray-900 text-lg">{user.name}</p>
          <p className="text-gray-500 text-sm">{user.email}</p>
        </div>
      </div>

      {/* 구매 내역 */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <ShoppingBag size={18} className="text-blue-500" />
          구매 내역
        </h2>

        {purchaseStatus?.purchased ? (
          <div className="flex items-center justify-between bg-green-50 border border-green-100 rounded-xl px-4 py-3">
            <div>
              <p className="font-medium text-green-800">5주차 열람권</p>
              <p className="text-xs text-green-600 mt-0.5">
                구매일: {new Date(purchaseStatus.purchased_at).toLocaleDateString("ko-KR")}
              </p>
            </div>
            <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">활성</span>
          </div>
        ) : (
          <p className="text-gray-400 text-sm py-4 text-center">구매 내역이 없습니다.</p>
        )}
      </div>
    </Layout>
  );
}
