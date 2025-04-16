"use client"
import Image from "next/image";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // checks if emails and password is filled out
    if (!email || !password) {
      setError("Both fields are required");
      return;
    }

    try {
      // Mock API call for login
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        // Redirect or handle successful login here
        console.log("Login successful");
      } else {
        setError("Invalid email or password");
      }
    } catch (err) {
      setError("Something went wrong, please try again");
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-3xl font-semibold">Login</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full sm:w-[400px]">
          <div className="flex flex-col">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="border p-2 rounded-md focus:outline-none"
              placeholder="Enter your email"
            />
          </div>
          <div className="flex flex-col">
            <label htmlFor="password" className="text-sm font-medium">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="border p-2 rounded-md focus:outline-none"
              placeholder="Enter your password"
            />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button type="submit" className="bg-blue-500 text-white rounded-full h-12 mt-4">Login</button>
        </form>
        <div className="flex gap-4 items-center flex-col sm:flex-row mt-6">
          <a
            className="text-sm text-blue-500 hover:underline"
            href=" "
          >
            Don't have an account? Sign up here.
          </a>
        </div>
      </main>
    </div>
  );
}
