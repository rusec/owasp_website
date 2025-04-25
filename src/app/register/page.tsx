"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Register() {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        username: "",
        email: "",
        password: "",
        phone_number: "",
    });
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const router = useRouter();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        // Validate form fields
        const { first_name, last_name, username, email, password, phone_number } = formData;
        if (!first_name || !last_name || !username || !email || !password || !phone_number) {
            setError("All fields are required.");
            return;
        }

        try {
            const response = await fetch("/api/user/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                setSuccess("User registered successfully!");
                setTimeout(() => router.push("/login"), 2000); // Redirect to login page after 2 seconds
            } else {
                const err = await response.json();
                setError(err.message || "Failed to register user.");
            }
        } catch (err) {
            setError("Server error. Please try again later.");
            console.error(err);
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">
            <main className="flex-1 flex items-center justify-center p-6">
                <div className="card w-full max-w-md shadow-xl bg-base-200 p-6 dark:bg-gray-800">
                    <h1 className="text-3xl font-bold text-center mb-6">Register</h1>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="form-control">
                            <label htmlFor="first_name" className="label">
                                <span className="label-text">First Name</span>
                            </label>
                            <input
                                id="first_name"
                                name="first_name"
                                type="text"
                                value={formData.first_name}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your first name"
                            />
                        </div>
                        <div className="form-control">
                            <label htmlFor="last_name" className="label">
                                <span className="label-text">Last Name</span>
                            </label>
                            <input
                                id="last_name"
                                name="last_name"
                                type="text"
                                value={formData.last_name}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your last name"
                            />
                        </div>
                        <div className="form-control">
                            <label htmlFor="username" className="label">
                                <span className="label-text">Username</span>
                            </label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                value={formData.username}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your username"
                            />
                        </div>
                        <div className="form-control">
                            <label htmlFor="email" className="label">
                                <span className="label-text">Email</span>
                            </label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your email"
                            />
                        </div>
                        <div className="form-control">
                            <label htmlFor="password" className="label">
                                <span className="label-text">Password</span>
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your password"
                            />
                        </div>
                        <div className="form-control">
                            <label htmlFor="phone_number" className="label">
                                <span className="label-text">Phone Number</span>
                            </label>
                            <input
                                id="phone_number"
                                name="phone_number"
                                type="text"
                                value={formData.phone_number}
                                onChange={handleChange}
                                className="input input-bordered w-full"
                                placeholder="Enter your phone number"
                            />
                        </div>
                        {error && <p className="text-error text-sm">{error}</p>}
                        {success && <p className="text-success text-sm">{success}</p>}
                        <button type="submit" className="btn btn-primary w-full">
                            Register
                        </button>
                    </form>
                    <div className="text-center mt-4">
                        <a className="link link-primary text-sm" href="/login">
                            Already have an account? Login here.
                        </a>
                    </div>
                </div>
            </main>
        </div>
    );
}
