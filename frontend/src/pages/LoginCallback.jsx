import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginCallback() {
  const { checkAuth } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    checkAuth().then(() => navigate("/week5"));
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-gray-500">로그인 처리 중...</p>
    </div>
  );
}
