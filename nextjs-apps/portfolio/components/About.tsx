"use client";

import { motion } from "framer-motion";
import { GraduationCap, Award, MapPin, Sparkles, Brain, Globe } from "lucide-react";

const highlights = [
  {
    icon: GraduationCap,
    title: "B.Tech CSBS",
    description: "Jain (Deemed-to-be University), Bengaluru",
  },
  {
    icon: Award,
    title: "9.3 CGPA",
    description: "Consistent academic excellence",
  },
  {
    icon: MapPin,
    title: "Bengaluru, India",
    description: "Silicon Valley of India",
  },
];

const interests = [
  {
    icon: Brain,
    title: "AI & Machine Learning",
    description: "Building intelligent systems",
  },
  {
    icon: Globe,
    title: "Geospatial Analysis",
    description: "Satellite imagery & Earth observation",
  },
  {
    icon: Sparkles,
    title: "Innovation",
    description: "SIH 2026 National Winner",
  },
];

export default function About() {
  return (
    <section id="about" className="py-24 px-4 relative">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-purple-400 text-sm font-medium tracking-wider uppercase">
            Get to Know Me
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-2 mb-4">
            About <span className="gradient-text">Me</span>
          </h2>
          <div className="w-20 h-1 bg-gradient-to-r from-purple-500 to-cyan-500 mx-auto rounded-full" />
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Image/Visual */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="relative w-full aspect-square max-w-md mx-auto">
              {/* Gradient Background Circle */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 to-cyan-600/20 rounded-full blur-3xl" />

              {/* Avatar Placeholder */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="relative w-full h-full rounded-full bg-gradient-to-br from-purple-500/30 to-cyan-500/30 border-2 border-purple-500/30 flex items-center justify-center overflow-hidden"
              >
                <div className="text-center">
                  <span className="text-7xl font-bold gradient-text">AR</span>
                  <div className="mt-4 flex items-center justify-center gap-2">
                    <span className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-gray-400">Open to Work</span>
                  </div>
                </div>
              </motion.div>

              {/* Decorative Elements */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="absolute inset-4 border-2 border-dashed border-purple-500/20 rounded-full"
              />
            </div>

            {/* Floating Stats */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="absolute -bottom-4 -right-4 sm:right-10 bg-gradient-to-r from-purple-600 to-cyan-600 px-6 py-3 rounded-2xl shadow-xl"
            >
              <div className="text-3xl font-bold">100+</div>
              <div className="text-sm text-white/80">Git Commits</div>
            </motion.div>
          </motion.div>

          {/* Right Column - Content */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <div className="space-y-4 text-gray-300 text-lg leading-relaxed">
              <p>
                I&apos;m <span className="text-white font-semibold">Attanti Ramnivas</span>, an
                AI/ML enthusiast and B.Tech Computer Science & Business Systems student
                at Jain University, Bengaluru.
              </p>
              <p>
                With a passion for building intelligent systems, I specialize in
                developing AI-powered applications ranging from RAG chatbots to
                geospatial analysis platforms. My work combines cutting-edge
                machine learning with practical real-world solutions.
              </p>
              <p>
                I&apos;m proud to have won <span className="text-purple-400 font-semibold">SIH 2026</span>{" "}
                and developed production systems serving <span className="text-cyan-400 font-semibold">
                  60,000+ projects</span> with satellite imagery analysis and risk assessment.
              </p>
            </div>

            {/* Highlight Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
              {highlights.map((item, index) => (
                <motion.div
                  key={item.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="glass-card rounded-2xl p-4 text-center"
                >
                  <item.icon className="w-6 h-6 text-purple-400 mx-auto mb-2" />
                  <h3 className="font-semibold text-white">{item.title}</h3>
                  <p className="text-sm text-gray-400 mt-1">{item.description}</p>
                </motion.div>
              ))}
            </div>

            {/* Interests */}
            <div className="mt-8">
              <h3 className="text-lg font-semibold text-white mb-4">What I&apos;m Passionate About</h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {interests.map((item, index) => (
                  <motion.div
                    key={item.title}
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center gap-3 p-3 bg-white/5 rounded-xl"
                  >
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500/20 to-cyan-500/20 flex items-center justify-center">
                      <item.icon className="w-5 h-5 text-purple-400" />
                    </div>
                    <div>
                      <h4 className="font-medium text-white text-sm">{item.title}</h4>
                      <p className="text-xs text-gray-400">{item.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
