"use client";

import Link from "next/link";
import {
  LayoutDashboard,
  Users,
  ShoppingBag,
  BarChart3,
  Settings,
  FileText,
  Bell,
  HelpCircle,
} from "lucide-react";

const navItems = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard, active: true },
  { name: "Users", href: "/", icon: Users, active: false },
  { name: "Products", href: "/", icon: ShoppingBag, active: false },
  { name: "Analytics", href: "/", icon: BarChart3, active: false },
  { name: "Reports", href: "/", icon: FileText, active: false },
  { name: "Notifications", href: "/", icon: Bell, active: false },
];

const bottomItems = [
  { name: "Settings", href: "/", icon: Settings },
  { name: "Help", href: "/", icon: HelpCircle },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-gray-800">
        <Link href="/" className="text-xl font-bold text-white">
          Dash<span className="text-blue-500">board</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
              item.active
                ? "bg-blue-600 text-white"
                : "text-gray-400 hover:bg-gray-800 hover:text-white"
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.name}</span>
          </Link>
        ))}
      </nav>

      {/* Bottom Items */}
      <div className="px-4 py-4 border-t border-gray-800 space-y-1">
        {bottomItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition-colors"
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.name}</span>
          </Link>
        ))}
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
            JD
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-white">John Doe</div>
            <div className="text-xs text-gray-400">Admin</div>
          </div>
        </div>
      </div>
    </aside>
  );
}
