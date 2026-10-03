"use client";

import { motion } from "framer-motion";
import {
  Code2,
  Brain,
  Database,
  Cloud,
  Palette,
  GitBranch,
  Terminal,
  Layers,
} from "lucide-react";

const skillCategories = [
  {
    icon: Code2,
    title: "Languages",
    skills: [
      { name: "Python", level: 95 },
      { name: "TypeScript", level: 85 },
      { name: "JavaScript", level: 90 },
      { name: "SQL", level: 80 },
      { name: "Java", level: 75 },
    ],
  },
  {
    icon: Brain,
    title: "AI/ML",
    skills: [
      { name: "TensorFlow/PyTorch", level: 85 },
      { name: "LangChain", level: 90 },
      { name: "OpenAI/Gemini API", level: 95 },
      { name: "ChromaDB/Pinecone", level: 85 },
      { name: "Scikit-learn", level: 80 },
    ],
  },
  {
    icon: Layers,
    title: "Frameworks",
    skills: [
      { name: "React/Next.js", level: 90 },
      { name: "FastAPI", level: 85 },
      { name: "Node.js", level: 80 },
      { name: "Tailwind CSS", level: 95 },
      { name: "Framer Motion", level: 85 },
    ],
  },
  {
    icon: Database,
    title: "Data & Storage",
    skills: [
      { name: "PostgreSQL", level: 80 },
      { name: "MongoDB", level: 75 },
      { name: "Prisma ORM", level: 85 },
      { name: "Redis", level: 70 },
      { name: "Firebase", level: 80 },
    ],
  },
  {
    icon: Cloud,
    title: "Cloud & DevOps",
    skills: [
      { name: "AWS", level: 75 },
      { name: "Vercel", level: 90 },
      { name: "Docker", level: 80 },
      { name: "GitHub Actions", level: 85 },
      { name: "CI/CD", level: 80 },
    ],
  },
  {
    icon: GitBranch,
    title: "Tools & More",
    skills: [
      { name: "Git", level: 90 },
      { name: "Postman", level: 85 },
      { name: "VS Code", level: 95 },
      { name: "Figma", level: 70 },
      { name: "Streamlit", level: 90 },
    ],
  },
];

const tools = [
  "ChatGPT",
  "GitHub Copilot",
  "Cursor AI",
  "Vercel AI SDK",
  "OpenCV",
  "Leaflet/MapLibre",
  "Chart.js",
  "Shadcn/UI",
];

export default function Skills() {
  return (
    <section id="skills" className="py-24 px-4 relative">
      {/* Background Decoration */}
      <div className="absolute top-1/2 left-0 w-72 h-72 bg-purple-600/10 rounded-full blur-[100px] -translate-y-1/2" />

      <div className="max-w-6xl mx-auto relative">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-cyan-400 text-sm font-medium tracking-wider uppercase">
            My Expertise
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-2 mb-4">
            Technical <span className="gradient-text">Skills</span>
          </h2>
          <div className="w-20 h-1 bg-gradient-to-r from-cyan-500 to-purple-500 mx-auto rounded-full" />
          <p className="text-gray-400 mt-4 max-w-2xl mx-auto">
            A comprehensive toolkit for building production-ready AI applications
          </p>
        </motion.div>

        {/* Skills Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {skillCategories.map((category, categoryIndex) => (
            <motion.div
              key={category.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: categoryIndex * 0.1 }}
              className="glass-card rounded-2xl p-6"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/20 to-cyan-500/20 flex items-center justify-center">
                  <category.icon className="w-6 h-6 text-purple-400" />
                </div>
                <h3 className="text-xl font-semibold text-white">{category.title}</h3>
              </div>

              <div className="space-y-4">
                {category.skills.map((skill, skillIndex) => (
                  <div key={skill.name}>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm text-gray-300">{skill.name}</span>
                      <span className="text-xs text-purple-400">{skill.level}%</span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${skill.level}%` }}
                        viewport={{ once: true }}
                        transition={{
                          duration: 1,
                          delay: categoryIndex * 0.1 + skillIndex * 0.1,
                          ease: "easeOut",
                        }}
                        className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full relative"
                      >
                        <div className="absolute inset-0 bg-white/20 animate-pulse" />
                      </motion.div>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* AI & Development Tools */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="glass-card rounded-2xl p-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <Terminal className="w-6 h-6 text-cyan-400" />
            <h3 className="text-xl font-semibold text-white">AI & Development Tools</h3>
          </div>
          <div className="flex flex-wrap gap-3">
            {tools.map((tool, index) => (
              <motion.span
                key={tool}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.05, y: -2 }}
                className="px-4 py-2 bg-gradient-to-r from-purple-500/10 to-cyan-500/10 border border-purple-500/20 rounded-full text-sm text-gray-300 hover:border-purple-500/50 hover:text-white transition-all cursor-default"
              >
                {tool}
              </motion.span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
