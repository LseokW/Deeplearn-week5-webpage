import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login, user } = useAuth();

  useEffect(() => {
    if (!user) login();
  }, [user]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-gray-500">Google 로그인 페이지로 이동 중...</p>
    </div>
  );
}
