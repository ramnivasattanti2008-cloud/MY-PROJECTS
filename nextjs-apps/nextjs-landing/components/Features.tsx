"use client";

const features = [
  {
    title: "Lightning Fast",
    description: "Built on Next.js 15 for optimal performance and speed.",
    icon: "⚡",
  },
  {
    title: "Beautiful Design",
    description: "Modern UI components with Tailwind CSS styling.",
    icon: "🎨",
  },
  {
    title: "Type Safe",
    description: "Full TypeScript support for better developer experience.",
    icon: "🔒",
  },
  {
    title: "Responsive",
    description: "Perfectly adapted for all screen sizes and devices.",
    icon: "📱",
  },
  {
    title: "SEO Optimized",
    description: "Built-in SEO best practices for better visibility.",
    icon: "🔍",
  },
  {
    title: "Easy to Customize",
    description: "Simple configuration and theming system.",
    icon: "🛠️",
  },
];

export default function Features() {
  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900/50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">Powerful Features</h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Everything you need to build and launch your product successfully.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition-colors"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
