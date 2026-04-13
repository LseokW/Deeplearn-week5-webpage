import { Link } from "react-router-dom";
import { BookOpen, LogOut, User } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, login, logout } = useAuth();

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-blue-600 text-lg">
          <BookOpen size={22} />
          DeepLearn Week5
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link to="/week5" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">
                강의 목차
              </Link>
              <Link to="/dashboard" className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-blue-600 transition-colors">
                <img
                  src={user.picture_url}
                  alt={user.name}
                  className="w-7 h-7 rounded-full"
                />
                <span className="hidden sm:inline">{user.name}</span>
              </Link>
              <button
                onClick={logout}
                className="flex items-center gap-1 text-sm text-gray-500 hover:text-red-500 transition-colors"
              >
                <LogOut size={16} />
                <span className="hidden sm:inline">로그아웃</span>
              </button>
            </>
          ) : (
            <button
              onClick={login}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Google로 시작하기
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
