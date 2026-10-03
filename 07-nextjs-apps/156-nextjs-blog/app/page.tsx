import BlogList from "@/components/BlogList";
import CategoryFilter from "@/components/CategoryFilter";
import { getAllPosts, getAllCategories } from "@/lib/posts";

export default function Home() {
  const posts = getAllPosts();
  const categories = getAllCategories();

  return (
    <main className="min-h-screen pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Latest Articles
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Insights, tutorials, and thoughts on web development, design, and technology.
          </p>
        </div>
        <CategoryFilter categories={categories} />
        <BlogList posts={posts} />
      </div>
    </main>
  );
}
