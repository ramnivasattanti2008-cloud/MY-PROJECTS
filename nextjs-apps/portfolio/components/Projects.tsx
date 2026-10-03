"use client";

import { motion } from "framer-motion";
import {
  Bot,
  Satellite,
  MessageSquare,
  Youtube,
  Mail,
  CloudSun,
  ArrowRight,
  Star,
  GitBranch,
  ExternalLink,
  Layers,
} from "lucide-react";

const projects = [
  {
    icon: Bot,
    title: "smriti-ai",
    tagline: "RAG Chatbot",
    description:
      "Intelligent chatbot using Retrieval-Augmented Generation with Gemini Pro and ChromaDB for context-aware conversations.",
    tech: ["Gemini Pro", "ChromaDB", "LangChain", "FastAPI"],
    stats: "Production Ready",
    color: "from-purple-500 to-violet-600",
    github: "https://github.com/ramnivasattanti2008-cloud/smriti-ai",
    demo: "https://smriti-ai.vercel.app",
  },
  {
    icon: Satellite,
    title: "VOJAS",
    tagline: "SIH 2026 Winner",
    description:
      "Satellite imagery analysis platform for MPLAD accountability. Features geospatial analysis, risk engine, and real-time anomaly detection across 60K+ projects.",
    tech: ["Next.js 15", "Prisma", "PostgreSQL", "MapLibre", "Framer Motion"],
    stats: "100+ Commits",
    color: "from-cyan-500 to-blue-600",
    github: "https://github.com/ramnivasattanti2008-cloud/vojas",
    demo: "https://vojas.app",
  },
  {
    icon: MessageSquare,
    title: "Sentiment Analyzer",
    tagline: "NLP Text Analysis",
    description:
      "Deep learning-powered sentiment analysis tool that classifies text emotions with high accuracy using transformer models.",
    tech: ["Python", "PyTorch", "BERT", "FastAPI", "React"],
    stats: "95% Accuracy",
    color: "from-emerald-500 to-teal-600",
    github: "https://github.com/ramnivasattanti2008-cloud/sentiment-analyzer",
    demo: "https://sentiment-demo.vercel.app",
  },
  {
    icon: Youtube,
    title: "YouTube Comment Analyzer",
    tagline: "YouTube API + AI",
    description:
      "AI-powered tool that analyzes YouTube video comments to extract insights, trends, and sentiment patterns.",
    tech: ["YouTube API", "OpenAI", "Next.js", "Tailwind"],
    stats: "Real-time",
    color: "from-red-500 to-orange-600",
    github: "https://github.com/ramnivasattanti2008-cloud/youtube-analyzer",
    demo: "https://yt-analyzer.vercel.app",
  },
  {
    icon: Mail,
    title: "AI Email Drafter",
    tagline: "Multi-format Composer",
    description:
      "Intelligent email drafting tool supporting 12 email types, 5 tones, and 9 languages with context-aware generation.",
    tech: ["GPT-4", "React", "Node.js", "OpenAI API"],
    stats: "45+ Variations",
    color: "from-amber-500 to-yellow-600",
    github: "https://github.com/ramnivasattanti2008-cloud/email-drafter",
    demo: "https://email-drafter.vercel.app",
  },
  {
    icon: CloudSun,
    title: "AI Weather Insights Bot",
    tagline: "Smart Weather Analysis",
    description:
      "ML-powered weather analysis bot providing contextual insights and predictions from weather data patterns.",
    tech: ["Python", "TensorFlow", "Weather API", "Streamlit"],
    stats: "Live Data",
    color: "from-sky-500 to-indigo-600",
    github: "https://github.com/ramnivasattanti2008-cloud/weather-bot",
    demo: "https://weather-insights.streamlit.app",
  },
];

const streamlitApps = [
  { name: "AI Chatbot", folder: "01-ai-chatbot", icon: Bot },
  { name: "SQL Generator", folder: "02-sql-generator", icon: Layers },
  { name: "Code Reviewer", folder: "03-code-reviewer", icon: MessageSquare },
  { name: "Study Buddy", folder: "04-study-buddy", icon: Star },
  { name: "Meeting Summarizer", folder: "05-meeting-summarizer", icon: Bot },
  { name: "Image Generator", folder: "06-image-generator", icon: Star },
];

export default function Projects() {
  return (
    <section id="projects" className="py-24 px-4 relative">
      {/* Background Decoration */}
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-600/10 rounded-full blur-[120px]" />

      <div className="max-w-6xl mx-auto relative">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-purple-400 text-sm font-medium tracking-wider uppercase">
            My Work
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-2 mb-4">
            Featured <span className="gradient-text">Projects</span>
          </h2>
          <div className="w-20 h-1 bg-gradient-to-r from-purple-500 to-cyan-500 mx-auto rounded-full" />
          <p className="text-gray-400 mt-4 max-w-2xl mx-auto">
            From production AI systems to experimental prototypes
          </p>
        </motion.div>

        {/* Projects Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project, index) => (
            <motion.div
              key={project.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -8 }}
              className="glass-card rounded-2xl p-6 group relative overflow-hidden"
            >
              {/* Gradient Accent */}
              <div
                className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${project.color} opacity-0 group-hover:opacity-100 transition-opacity`}
              />

              {/* Icon */}
              <div
                className={`w-14 h-14 rounded-xl bg-gradient-to-br ${project.color} p-[1px] mb-4`}
              >
                <div className="w-full h-full bg-[#030014] rounded-[10px] flex items-center justify-center">
                  <project.icon className="w-7 h-7 text-white" />
                </div>
              </div>

              {/* Badge */}
              <div className="flex items-center gap-2 mb-3">
                <span
                  className={`px-2 py-0.5 text-xs font-medium rounded-full bg-gradient-to-r ${project.color} text-white`}
                >
                  {project.tagline}
                </span>
                <span className="flex items-center gap-1 text-xs text-gray-500">
                  <GitBranch className="w-3 h-3" />
                  {project.stats}
                </span>
              </div>

              {/* Title */}
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-purple-300 transition-colors">
                {project.title}
              </h3>

              {/* Description */}
              <p className="text-gray-400 text-sm mb-4 line-clamp-3">
                {project.description}
              </p>

              {/* Tech Stack */}
              <div className="flex flex-wrap gap-2 mb-4">
                {project.tech.slice(0, 4).map((tech) => (
                  <span
                    key={tech}
                    className="px-2 py-1 text-xs bg-white/5 rounded-md text-gray-400"
                  >
                    {tech}
                  </span>
                ))}
              </div>

              {/* Links */}
              <div className="flex items-center gap-4 pt-4 border-t border-white/5">
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                >
                  <GitBranch className="w-4 h-4" />
                  Code
                </a>
                <a
                  href={project.demo}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  Demo
                </a>
                <ArrowRight className="w-4 h-4 text-purple-400 ml-auto opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Streamlit Apps Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-20"
        >
          <div className="flex items-center gap-3 mb-8">
            <Layers className="w-6 h-6 text-cyan-400" />
            <h3 className="text-2xl font-bold text-white">Streamlit AI Apps</h3>
            <span className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-xs text-cyan-400">
              Quick Prototypes
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {streamlitApps.map((app, index) => (
              <motion.a
                key={app.folder}
                href={`/projects/${app.folder}`}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.05, y: -4 }}
                className="glass-card rounded-xl p-4 text-center group cursor-pointer"
              >
                <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 flex items-center justify-center group-hover:from-cyan-500/30 group-hover:to-purple-500/30 transition-all">
                  <app.icon className="w-6 h-6 text-cyan-400" />
                </div>
                <h4 className="text-sm font-medium text-white group-hover:text-cyan-300 transition-colors">
                  {app.name}
                </h4>
              </motion.a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
