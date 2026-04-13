import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import SectionCard from "../components/SectionCard";
import PaywallModal from "../components/PaywallModal";
import client from "../api/client";
import { Lock } from "lucide-react";

export default function Week5Index() {
  const [sections, setSections] = useState([]);
  const [purchased, setPurchased] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showPaywall, setShowPaywall] = useState(false);

  useEffect(() => {
    client.get("/api/content/week5").then((res) => {
      setSections(res.data.data.sections);
      setPurchased(res.data.data.purchased);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Week 5 · 딥러닝 핵심 개념</h1>
        <p className="text-gray-500 mt-2">5개 섹션으로 구성된 딥러닝 집중 강의입니다.</p>

        {!purchased && (
          <div className="mt-4 flex items-center justify-between bg-amber-50 border border-amber-200 rounded-xl px-5 py-4">
            <div className="flex items-center gap-3">
              <Lock size={18} className="text-amber-500" />
              <p className="text-sm text-amber-700 font-medium">
                5주차 열람권을 구매하면 모든 섹션을 자유롭게 열람할 수 있습니다.
              </p>
            </div>
            <button
              onClick={() => setShowPaywall(true)}
              className="ml-4 bg-amber-500 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-amber-600 transition-colors whitespace-nowrap"
            >
              구매하기
            </button>
          </div>
        )}
      </div>

      <div className="space-y-4">
        {sections
          .sort((a, b) => a.order - b.order)
          .map((section) => (
            <div
              key={section.id}
              onClick={!purchased ? () => setShowPaywall(true) : undefined}
            >
              <SectionCard section={section} purchased={purchased} />
            </div>
          ))}
      </div>

      {showPaywall && <PaywallModal onClose={() => setShowPaywall(false)} />}
    </Layout>
  );
}
