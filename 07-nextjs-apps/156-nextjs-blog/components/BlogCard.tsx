"use client";

import Link from "next/link";
import { Post } from "@/lib/posts";

interface BlogCardProps {
  post: Post;
}

export default function BlogCard({ post }: BlogCardProps) {
  const formattedDate = new Date(post.date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <article className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-gray-700 transition-colors group">
      <div className="bg-gray-800 h-48 flex items-center justify-center">
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 w-full h-full flex items-center justify-center">
          <span className="text-4xl text-white/50">{post.category[0]}</span>
        </div>
      </div>
      <div className="p-6">
        <div className="flex items-center gap-4 mb-4">
          <span className="bg-blue-500/20 text-blue-400 text-xs font-medium px-2 py-1 rounded">
            {post.category}
          </span>
          <span className="text-gray-500 text-sm">{post.readingTime}</span>
        </div>
        <Link href={`/blog/${post.slug}`}>
          <h2 className="text-xl font-semibold text-white mb-2 group-hover:text-blue-400 transition-colors">
            {post.title}
          </h2>
        </Link>
        <p className="text-gray-400 mb-4 line-clamp-2">{post.excerpt}</p>
        <div className="flex items-center justify-between">
          <span className="text-gray-500 text-sm">{formattedDate}</span>
          <Link
            href={`/blog/${post.slug}`}
            className="text-blue-400 hover:text-blue-300 text-sm font-medium transition-colors"
          >
            Read more
          </Link>
        </div>
      </div>
    </article>
  );
}
