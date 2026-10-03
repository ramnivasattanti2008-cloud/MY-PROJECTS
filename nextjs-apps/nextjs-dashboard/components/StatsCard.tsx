"use client";

import { ReactNode } from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string;
  change: string;
  changeType: "positive" | "negative";
  icon: ReactNode;
}

export default function StatsCard({
  title,
  value,
  change,
  changeType,
  icon,
}: StatsCardProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-blue-500/20 rounded-lg text-blue-500">
          {icon}
        </div>
        <div
          className={`flex items-center gap-1 text-sm font-medium ${
            changeType === "positive" ? "text-green-500" : "text-red-500"
          }`}
        >
          {changeType === "positive" ? (
            <TrendingUp className="w-4 h-4" />
          ) : (
            <TrendingDown className="w-4 h-4" />
          )}
          {change}
        </div>
      </div>
      <div className="text-2xl font-bold text-white mb-1">{value}</div>
      <div className="text-gray-400 text-sm">{title}</div>
    </div>
  );
}
