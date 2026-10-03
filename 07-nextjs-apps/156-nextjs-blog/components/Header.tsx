"use client";

import Link from "next/link";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-950/80 backdrop-blur-md border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-white">
            Dev<span className="text-blue-500">Blog</span>
          </Link>
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-400 hover:text-white transition-colors">
              Home
            </Link>
            <Link href="/" className="text-gray-400 hover:text-white transition-colors">
              Articles
            </Link>
            <Link href="/" className="text-gray-400 hover:text-white transition-colors">
              About
            </Link>
            <Link href="/" className="text-gray-400 hover:text-white transition-colors">
              Contact
            </Link>
          </nav>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors text-sm">
            Subscribe
          </button>
        </div>
      </div>
    </header>
  );
}
