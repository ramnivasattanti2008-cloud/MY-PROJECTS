"use client";

import { Download, Mail, MapPin, Calendar } from "lucide-react";

export default function About() {
  return (
    <section id="about" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900/50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">About Me</h2>
          <div className="w-20 h-1 bg-gradient-to-r from-blue-500 to-purple-600 mx-auto"></div>
        </div>
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="bg-gray-800 rounded-xl p-8 border border-gray-700">
              <div className="w-full h-80 bg-gradient-to-br from-blue-500/20 to-purple-600/20 rounded-lg flex items-center justify-center mb-6">
                <div className="text-8xl">👨‍💻</div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-2 text-gray-400">
                  <MapPin className="w-4 h-4" />
                  <span>San Francisco, CA</span>
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <Calendar className="w-4 h-4" />
                  <span>5+ Years Experience</span>
                </div>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white mb-4">
              Passionate about building exceptional digital products
            </h3>
            <p className="text-gray-400 mb-6 leading-relaxed">
              I'm a full-stack developer with a passion for creating beautiful,
              functional, and user-centered digital experiences. With over 5 years
              of experience in the industry, I've had the privilege of working with
              startups and established companies alike.
            </p>
            <p className="text-gray-400 mb-8 leading-relaxed">
              When I'm not coding, you'll find me exploring new technologies,
              contributing to open-source projects, or sharing knowledge through
              blog posts and mentoring.
            </p>
            <div className="flex flex-wrap gap-4">
              <a
                href="#"
                className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                <Download className="w-4 h-4" />
                Download CV
              </a>
              <a
                href="#contact"
                className="inline-flex items-center gap-2 border border-gray-700 hover:border-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                <Mail className="w-4 h-4" />
                Contact Me
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
