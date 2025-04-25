"use client";
import React from "react";
import { useState, useEffect } from "react";
import Message from "./Message";

type Message = {
    sender: string;
    sender_id: string;
    message: string;
};


export default function ChatRoom() {


    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const eventSource = new EventSource('/api/chat/', {
            'withCredentials': true,
        });

        eventSource.onmessage = (event) => {
            try {
                if (!event.data) return;

                console.log(typeof event.data, event.data);
                const parsedData = JSON.parse(event.data);

                setMessages(prevData => [...prevData, parsedData]);
            }
            catch (error) {
                console.error('Error parsing SSE data:', error);
            }

        };

        eventSource.onerror = (error) => {
            console.error('SSE error:', error);
        };

        return () => {
            eventSource.close();
        };
    }, []);

    const handleSendMessage = () => {
        if (newMessage.trim() === "") return;
        setLoading(true);
        fetch("/api/chat/publish", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: newMessage }),
        })
            .then((res) => res.json())
            .then((data) => {
                setMessages([...messages, data.message]);
                setNewMessage("");
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error sending message:", error);
                setLoading(false);
            });
    };

    return (
        <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-800 dark:text-white">
            <header className="w-full px-6 py-4 flex justify-between items-center bg-blue-600 text-white shadow-md">
                <div className="flex items-center gap-2">
                    <span className="text-lg font-bold">Chat Room</span>
                </div>
            </header>

            <div className="card w-full shadow-xl bg-base-200 p-6 dark:bg-gray-800">
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <div className="overflow-y-auto h-96 border border-gray-300 rounded-lg p-4 mb-4">
                        {messages.map((msg, index) => (
                            <Message
                                key={index}
                                message={msg}
                            />
                        ))}
                    </div>
                )}
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        className="input input-bordered w-full"
                        placeholder="Type your message..."
                    />
                    <button
                        onClick={handleSendMessage}
                        className="btn btn-primary"
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );

}
