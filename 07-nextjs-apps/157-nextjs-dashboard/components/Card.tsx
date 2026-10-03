"use client";

import { ReactNode } from "react";

interface CardProps {
  title: string;
  children: ReactNode;
  action?: ReactNode;
}

export default function Card({ title, children, action }: CardProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {action}
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}
