"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
type Message = {
    sender: string;
    sender_id: string;
    message: string;
};
type User = {
    'username': string;
    'email': string;
    'first_name': string;
    'last_name': string;
    'status': string;
    'privilege': string;
    'id': string;
    'avatar_url': string;

}

export default function Message({ message, isSender = false }: { message: Message, isSender?: boolean }) {
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        setLoading(true);
        fetch(`/api/employee/${message.sender_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((res) => res.json())
            .then((data) => {
                setUser(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error sending message:", error);
            });

    }, [message]);

    if (loading && !user) {
        return (
            <div className="flex items-center justify-start mb-4">
                <div className="bg-gray-200 text-gray-700 p-2 rounded-lg max-w-xs break-words animate-pulse">
                    Loading...
                </div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="flex items-center justify-start mb-4">
                <div className="bg-red-200 text-red-700 p-2 rounded-lg max-w-xs break-words">
                    User not found
                </div>
            </div>
        );
    }

    return (
        <div className={`p-1`}>
            <div className={`${isSender ? "bg-green-500" : "bg-blue-500"} text-white p-2 rounded-lg flex w-fit`}>
                <div className="flex items-center gap-2 mr-2">
                    <Image
                        src={user["avatar_url"]}
                        alt="Profile Image"
                        width={20}
                        height={20}
                        className="rounded-full"
                    />
                    <span className="text-sm font-semibold">{user["username"]}</span>
                </div>

                <div className={`text-white p-1 rounded-lg max-w-xs break-words flex items-center`}>
                    <div dangerouslySetInnerHTML={{ __html: message.message }} />
                </div>
            </div>

        </div>
    );
}