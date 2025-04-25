"use client";
import React, { useEffect, useState } from "react";
import ChatRoom from "./components/ChatRoom";
import { jwtDecode } from "jwt-decode";

type UserInfo = {
    'username': string;
    'email': string;
    'first_name': string;
    'last_name': string;
    'status': string;
    'privilege': string;
    'id': string;
    'avatar_url': string;
}

export default function Employee() {

    const [user, setUser] = useState<UserInfo | null>(null);

    useEffect(() => {
        // Get the authorization cookie
        const cookies = document.cookie.split("; ");
        const authCookie = cookies.find(cookie => cookie.startsWith("authorization="));
        if (authCookie) {
            const token = authCookie.split("=")[1];
            try {
                // Decode the JWT
                const decoded = jwtDecode<UserInfo>(token);
                setUser(decoded);
            } catch (error) {
                console.error("Failed to decode token:", error);
            }
        }
    }, []);



    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">

            {/* Employee Section */}
            <main className="p-6 min-h-screen">
                <h1 className="text-2xl font-bold mb-4">Welcome, {user ? user["username"] : "Guest"}!</h1>
                <ChatRoom />

            </main>
        </div>
    );

}