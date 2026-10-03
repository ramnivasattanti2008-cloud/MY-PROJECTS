"use client";

const skillCategories = [
  {
    name: "Frontend",
    skills: ["React", "Next.js", "TypeScript", "Tailwind CSS", "Vue.js", "Svelte"],
  },
  {
    name: "Backend",
    skills: ["Node.js", "Python", "PostgreSQL", "MongoDB", "GraphQL", "Redis"],
  },
  {
    name: "Tools & Cloud",
    skills: ["Git", "Docker", "AWS", "Vercel", "Figma", "CI/CD"],
  },
];

export default function Skills() {
  return (
    <section id="skills" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">Skills & Technologies</h2>
          <div className="w-20 h-1 bg-gradient-to-r from-blue-500 to-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Technologies I work with to bring ideas to life
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {skillCategories.map((category) => (
            <div
              key={category.name}
              className="bg-gray-900 border border-gray-800 rounded-xl p-6"
            >
              <h3 className="text-xl font-semibold text-white mb-6">{category.name}</h3>
              <div className="flex flex-wrap gap-2">
                {category.skills.map((skill) => (
                  <span
                    key={skill}
                    className="bg-gray-800 text-gray-300 px-4 py-2 rounded-lg text-sm hover:bg-blue-600 hover:text-white transition-colors cursor-default"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center p-6 bg-gray-900 border border-gray-800 rounded-xl">
            <div className="text-4xl font-bold text-white mb-2">50+</div>
            <div className="text-gray-400">Projects Completed</div>
          </div>
          <div className="text-center p-6 bg-gray-900 border border-gray-800 rounded-xl">
            <div className="text-4xl font-bold text-white mb-2">30+</div>
            <div className="text-gray-400">Happy Clients</div>
          </div>
          <div className="text-center p-6 bg-gray-900 border border-gray-800 rounded-xl">
            <div className="text-4xl font-bold text-white mb-2">5+</div>
            <div className="text-gray-400">Years Experience</div>
          </div>
          <div className="text-center p-6 bg-gray-900 border border-gray-800 rounded-xl">
            <div className="text-4xl font-bold text-white mb-2">100%</div>
            <div className="text-gray-400">Client Satisfaction</div>
          </div>
        </div>
      </div>
    </section>
  );
}
