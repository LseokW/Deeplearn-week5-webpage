import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">
        {children}
      </main>
      <footer className="border-t border-gray-200 bg-white py-6 text-center text-sm text-gray-400">
        © 2026 DeepLearn Week5 · 딥러닝 핵심 개념 학습 플랫폼
      </footer>
    </div>
  );
}
