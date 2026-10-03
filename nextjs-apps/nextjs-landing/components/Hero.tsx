"use client";

export default function Hero() {
  return (
    <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
          Build Something <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
            Amazing
          </span>
        </h1>
        <p className="text-xl text-gray-400 max-w-3xl mx-auto mb-10">
          The modern platform for building and launching your next big idea.
          Fast, reliable, and beautifully designed.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105">
            Start Free Trial
          </button>
          <button className="border border-gray-700 hover:border-gray-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors">
            View Demo
          </button>
        </div>
        <div className="mt-16">
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4 shadow-2xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <pre className="text-left text-sm text-gray-300 font-mono">
              <code>{`$ npm install launchpad
✓ Ready in 2.3s
✓ Building for production...
✓ Deployed to cloud`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
