"use client";
import { useState } from "react";

export default function Login() {
    const [email, setEmail] = useState("");
    // const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!email) {
            setError(" Email fields are required");
            return;
        }

        const response = await fetch("/api/employee/forget", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email }),
        });

        if (response.ok && response.status === 200) {
            console.log("successful");
            // Dont do this, this is only because of the demo
            window.location.replace(response.url);

            // add
        } else if (response.status === 302) {
        } else {
            setError("Invalid email or password");

        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">


            {/* Forgot Password Form */}
            <main className="flex-1 flex items-center justify-center p-6">
                <div className="card w-full max-w-sm shadow-xl bg-base-200 p-6 dark:bg-gray-800">
                    <div className="flex flex-col items-center mb-6">
                        <h1 className="text-3xl font-bold mt-4">Forgot Password?</h1>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="form-control">
                            <label htmlFor="email" className="label">
                                <span className="label-text">Email</span>
                            </label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="input input-bordered w-full"
                                placeholder="Enter your email"
                            />
                        </div>

                        {error && <p className="text-error text-sm">{error}</p>}

                        <button type="submit" className="btn btn-primary w-full">
                            Set New Password
                        </button>
                    </form>
                </div>
            </main>

            {/* Footer */}
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
