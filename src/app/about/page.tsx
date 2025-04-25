"use client";

export default function About() {
  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">


      {/* Main Content */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-6">
        <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
          <h1 className="text-3xl font-bold text-center sm:text-left">
            About Our Bank
          </h1>
          <p className="text-lg text-center sm:text-left max-w-2xl">
            Welcome to our bank! We are committed to providing exceptional financial services to our customers.
            With a focus on innovation, security, and customer satisfaction, we strive to help you achieve your financial goals.
          </p>
          <p className="text-lg text-center sm:text-left max-w-2xl">
            Our mission is to empower individuals and businesses with the tools and resources they need to succeed.
            From savings accounts to loans, we offer a wide range of products tailored to meet your needs.
          </p>

          <div className="flex gap-4 items-center flex-col sm:flex-row">
            <a
              className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
              href="/contact"
            >
              Contact Us
            </a>
            <a
              className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 w-full sm:w-auto md:w-[158px]"
              href="/services"
            >
              Our Services
            </a>
          </div>
        </main>
      </div>

      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="/privacy-policy"
        >
          Privacy Policy
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="/terms-of-service"
        >
          Terms of Service
        </a>
      </footer>
    </div>
  );
}
