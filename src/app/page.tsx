"use client";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white text-gray-800 dark:bg-gray-900 dark:text-white font-sans">

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center text-center px-6 py-20 sm:py-32 gap-6">
        <h1 className="text-3xl sm:text-5xl font-bold tracking-tight">
          Welcome to Bank
        </h1>
        <p className="max-w-xl text-lg text-gray-600 dark:text-gray-300">
          WE ARE VERY SECURE OHHH YESSSS
        </p>
        <div className="flex gap-4 mt-6 flex-wrap justify-center">
          <a
            href="login"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-full shadow transition"
          >
            Login
          </a>
          <a
            href="about"
            className="border border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-gray-800 font-semibold py-3 px-6 rounded-full transition"
          >
            Learn More
          </a>
        </div>
      </main>

      {/* bottom of the page */}
      <footer className="w-full py-6 flex flex-wrap justify-center gap-6 text-sm bg-gray-100 dark:bg-gray-800 dark:text-gray-300">
        <a href="https://nextjs.org" target="_blank" rel="noopener noreferrer" className="hover:underline">
          Powered by Next.js
        </a>
        <a href="#" className="hover:underline">
          Privacy Policy
        </a>
        <a href="#" className="hover:underline">
          Terms of Service
        </a>
        <a href="#" className="hover:underline">
          Help Center
        </a>
      </footer>
    </div>
  );
}
