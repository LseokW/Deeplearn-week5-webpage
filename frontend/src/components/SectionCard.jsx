import { Link } from "react-router-dom";
import { Lock, ChevronRight } from "lucide-react";

export default function SectionCard({ section, purchased }) {
  const locked = !purchased;

  const inner = (
    <div
      className={`group flex items-center justify-between p-5 rounded-xl border transition-all ${
        locked
          ? "bg-gray-50 border-gray-200 opacity-70"
          : "bg-white border-blue-100 hover:border-blue-300 hover:shadow-md cursor-pointer"
      }`}
    >
      <div className="flex items-center gap-4">
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
            locked ? "bg-gray-200 text-gray-400" : "bg-blue-100 text-blue-600"
          }`}
        >
          {section.order}
        </div>
        <div>
          <h3 className={`font-semibold text-base ${locked ? "text-gray-400" : "text-gray-800"}`}>
            {section.title}
          </h3>
          <p className="text-sm text-gray-500 mt-0.5">{section.description}</p>
          <div className="flex flex-wrap gap-1.5 mt-2">
            {section.keywords.map((kw) => (
              <span key={kw} className="bg-gray-100 text-gray-500 text-xs px-2 py-0.5 rounded-full">
                {kw}
              </span>
            ))}
          </div>
        </div>
      </div>
      <div className="ml-4 flex-shrink-0">
        {locked ? (
          <Lock size={18} className="text-gray-400" />
        ) : (
          <ChevronRight size={18} className="text-blue-400 group-hover:translate-x-1 transition-transform" />
        )}
      </div>
    </div>
  );

  if (locked) return inner;
  return <Link to={`/week5/${section.id}`}>{inner}</Link>;
}
