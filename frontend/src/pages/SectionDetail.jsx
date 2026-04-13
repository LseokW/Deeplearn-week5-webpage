import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Layout from "../components/Layout";
import MarkdownRenderer from "../components/MarkdownRenderer";
import PaywallModal from "../components/PaywallModal";
import client from "../api/client";
import { ChevronLeft } from "lucide-react";

export default function SectionDetail() {
  const { sectionId } = useParams();
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [showPaywall, setShowPaywall] = useState(false);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    setLoading(true);
    client
      .get(`/api/content/week5/${sectionId}`)
      .then((res) => {
        setContent(res.data.data.content);
        setLoading(false);
      })
      .catch((err) => {
        if (err.response?.status === 403) {
          setShowPaywall(true);
          setLoading(false);
        } else {
          setNotFound(true);
          setLoading(false);
        }
      });
  }, [sectionId]);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </Layout>
    );
  }

  if (notFound) {
    return (
      <Layout>
        <div className="text-center py-20 text-gray-500">섹션을 찾을 수 없습니다.</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mb-6">
        <Link
          to="/week5"
          className="inline-flex items-center gap-1 text-sm text-blue-600 hover:underline"
        >
          <ChevronLeft size={16} />
          목차로 돌아가기
        </Link>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 sm:p-10">
        <MarkdownRenderer content={content} />
      </div>

      {showPaywall && (
        <PaywallModal onClose={() => setShowPaywall(false)} />
      )}
    </Layout>
  );
}
