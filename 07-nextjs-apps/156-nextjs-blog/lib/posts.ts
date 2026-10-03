import fs from "fs";
import path from "path";
import matter from "gray-matter";

export interface Post {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  category: string;
  coverImage?: string;
  readingTime: string;
}

const postsDirectory = path.join(process.cwd(), "content/posts");

export function getAllPosts(): Post[] {
  if (!fs.existsSync(postsDirectory)) {
    return getSamplePosts();
  }

  const fileNames = fs.readdirSync(postsDirectory);
  const posts = fileNames.map((fileName) => {
    const slug = fileName.replace(/\.mdx$/, "");
    const fullPath = path.join(postsDirectory, fileName);
    const fileContents = fs.readFileSync(fullPath, "utf8");
    const { data, content } = matter(fileContents);

    return {
      slug,
      title: data.title || "Untitled",
      date: data.date || new Date().toISOString(),
      excerpt: data.excerpt || content.slice(0, 150) + "...",
      category: data.category || "General",
      coverImage: data.coverImage,
      readingTime: data.readingTime || "5 min read",
    };
  });

  return posts.sort((a, b) => (a.date > b.date ? -1 : 1));
}

export function getAllCategories(): string[] {
  const posts = getAllPosts();
  const categories = new Set(posts.map((post) => post.category));
  return ["All", ...Array.from(categories)];
}

export function getPostBySlug(slug: string): Post | undefined {
  const posts = getAllPosts();
  return posts.find((post) => post.slug === slug);
}

function getSamplePosts(): Post[] {
  return [
    {
      slug: "getting-started-nextjs-15",
      title: "Getting Started with Next.js 15",
      date: "2024-01-15",
      excerpt: "Learn how to build modern web applications with Next.js 15 and its powerful features.",
      category: "Tutorial",
      readingTime: "8 min read",
    },
    {
      slug: "tailwind-css-dark-mode",
      title: "Implementing Dark Mode with Tailwind CSS",
      date: "2024-01-10",
      excerpt: "A comprehensive guide to implementing dark mode in your web applications using Tailwind CSS.",
      category: "Tutorial",
      readingTime: "6 min read",
    },
    {
      slug: "typescript-best-practices",
      title: "TypeScript Best Practices for 2024",
      date: "2024-01-05",
      excerpt: "Essential TypeScript patterns and best practices for building robust applications.",
      category: "Development",
      readingTime: "10 min read",
    },
    {
      slug: "web-performance-tips",
      title: "10 Tips to Improve Web Performance",
      date: "2024-01-01",
      excerpt: "Practical tips and techniques to make your websites faster and more efficient.",
      category: "Performance",
      readingTime: "7 min read",
    },
    {
      slug: "react-server-components",
      title: "Understanding React Server Components",
      date: "2023-12-28",
      excerpt: "Deep dive into React Server Components and how they change the way we build React apps.",
      category: "React",
      readingTime: "12 min read",
    },
    {
      slug: "design-systems-guide",
      title: "Building a Design System from Scratch",
      date: "2023-12-20",
      excerpt: "A complete guide to creating and maintaining a scalable design system.",
      category: "Design",
      readingTime: "9 min read",
    },
  ];
}
