"use client";

import { ExternalLink, Github } from "lucide-react";

const projects = [
  {
    title: "E-Commerce Platform",
    description: "A full-featured e-commerce platform with payments, inventory management, and analytics dashboard.",
    tags: ["Next.js", "Stripe", "PostgreSQL"],
    github: "#",
    live: "#",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    title: "Task Management App",
    description: "Real-time collaborative task management application with team features and notifications.",
    tags: ["React", "Socket.io", "MongoDB"],
    github: "#",
    live: "#",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    title: "AI Content Generator",
    description: "An AI-powered content generation tool for marketing teams and content creators.",
    tags: ["Next.js", "OpenAI", "Vercel"],
    github: "#",
    live: "#",
    gradient: "from-orange-500 to-red-500",
  },
  {
    title: "Social Media Dashboard",
    description: "Analytics dashboard for managing and analyzing social media performance across platforms.",
    tags: ["React", "Chart.js", "API"],
    github: "#",
    live: "#",
    gradient: "from-green-500 to-emerald-500",
  },
  {
    title: "Real Estate Portal",
    description: "Property listing and search platform with virtual tours and mortgage calculator.",
    tags: ["Next.js", "Mapbox", "Prisma"],
    github: "#",
    live: "#",
    gradient: "from-indigo-500 to-purple-500",
  },
  {
    title: "Fitness Tracker",
    description: "Mobile-first fitness tracking app with workout plans, progress charts, and community features.",
    tags: ["React Native", "Firebase", "Charts"],
    github: "#",
    live: "#",
    gradient: "from-rose-500 to-orange-500",
  },
];

export default function Projects() {
  return (
    <section id="projects" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900/50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">Featured Projects</h2>
          <div className="w-20 h-1 bg-gradient-to-r from-blue-500 to-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-400 max-w-2xl mx-auto">
            A selection of projects I've worked on
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.title}
              className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden group hover:border-gray-700 transition-colors"
            >
              <div className={`h-48 bg-gradient-to-br ${project.gradient} opacity-80 flex items-center justify-center`}>
                <div className="text-6xl text-white/50">🚀</div>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-semibold text-white mb-2">{project.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-gray-800 text-gray-300 px-2 py-1 rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-4">
                  <a
                    href={project.github}
                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    <Github className="w-4 h-4" />
                    Code
                  </a>
                  <a
                    href={project.live}
                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Live Demo
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
