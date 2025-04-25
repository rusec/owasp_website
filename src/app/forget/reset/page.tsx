"use client";
import React, { Suspense } from "react";
import { useState } from "react";
import { useSearchParams } from "next/navigation";

export default function ResetPage() {
    return <Suspense>
        <Reset />
    </Suspense>
}
function Reset() {
    const searchParams = useSearchParams();
    const token = searchParams.get("token") || "";
    const email = searchParams.get("email") || "";
    // const userId = searchParams.get("userId") || "";

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleResetPassword = async () => {
        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }
        setLoading(true);
        const response = await fetch("/api/user/forget/reset" + `?token=${token}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ new_password: password, token, email }),
        })
        if (response.ok) {
            const data = await response.json();
            console.log("Password reset successful!", data.message);
            window.location.replace("/login");
        }
        else {
            setError("Error resetting password");
            setLoading(false);
        }

    };

    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">


            <main className="p-6 min-h-screen">
                <h1 className="text-2xl font-bold mb-4">Reset Password</h1>
                {error && <p className="text-red-500">{error}</p>}
                <input
                    type="password"
                    placeholder="New Password"
                    className="input input-bordered w-full mb-4"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    className="input input-bordered w-full mb-4"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button
                    className={`btn btn-primary ${loading ? "loading" : "w-full"}`}
                    onClick={handleResetPassword}
                    disabled={loading}
                >
                    {loading ? "Resetting..." : "Reset Password"}
                </button>
            </main>
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