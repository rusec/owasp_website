"use client";
import { jwtDecode } from 'jwt-decode';
import React, { useEffect, useState } from 'react';

type EmployeeInfo = {
    'username': string;
    'email': string;
    'first_name': string;
    'last_name': string;
    'status': string;
    'privilege': string;
    'id': string;
    'avatar_url': string;
}

type BankInfo = {
    'users': number,
    'employees': number,
    'accounts': number,
    'transactions': number,
    'accounts_in_vault': number,
    'accounts_not_in_vault': number,
    'total_balance': number,
    'recent_transactions_count': number
}
const DashboardPage: React.FC = () => {
    const [user, setUser] = useState<EmployeeInfo | null>(null);
    const [loading, setLoading] = useState(false);
    const [bankInfo, setBankInfo] = useState<BankInfo | null>(null); // Adjust the type as needed
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        const cookies = document.cookie.split('; ');
        const authCookie = cookies.find((cookie) => cookie.startsWith('authorization='));
        if (authCookie) {
            const token = authCookie.split('=')[1];
            try {
                const decoded = jwtDecode<EmployeeInfo>(token);
                setUser(decoded);
            } catch (error) {
                console.error('Failed to decode token:', error);
                setError('Invalid token');
            }
        }
    }, []);

    useEffect(() => {
        if (user) {
            setLoading(true);
            async function fetchUserData() {
                const response = await fetch(`/api/employee/bank`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setBankInfo(data);
                setLoading(false);
            }
            fetchUserData().catch((error) => {
                console.error("Error fetching user data:", error);
                setError('Failed to fetch user data');
                setLoading(false);
            });
        }
    }, [user]);

    if (loading) {
        return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
    }
    if (error) {
        return <div className="flex items-center justify-center min-h-screen text-red-500">{error}</div>;
    }
    if (!user) {
        return <div className="flex items-center justify-center min-h-screen">Employee not found</div>;
    }

    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-800 dark:text-white">
            <header className="w-full px-6 py-4 flex justify-between items-center bg-blue-600 text-white shadow-md">
                <h1 className="text-2xl font-bold">Welcome, {user.username}!</h1>
            </header>
            <main className="p-6 min-h-screen">
                <h2 className="text-xl font-semibold mb-4">Employee Dashboard</h2>
                <div className="bg-white shadow-md rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-2">User Information</h3>
                    <p><strong>First Name:</strong> {user.first_name}</p>
                    <p><strong>Last Name:</strong> {user.last_name}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Status:</strong> {user.status}</p>
                    <p><strong>Privilege:</strong> {user.privilege}</p>
                </div>
                {bankInfo ? (
                    <div className="bg-gradient-to-r from-blue-500 to-indigo-600 shadow-lg rounded-lg p-6 mt-6 text-white">
                        <h3 className="text-lg font-semibold mb-4 border-b border-white pb-2">Bank Information</h3>
                        <ul className="grid grid-cols-2 gap-4">
                            <li className="flex justify-between">
                                <span className="font-medium">Total Users:</span>
                                <span>{bankInfo.users}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Total Employees:</span>
                                <span>{bankInfo.employees}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Total Accounts:</span>
                                <span>{bankInfo.accounts}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Total Transactions:</span>
                                <span>{bankInfo.transactions}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Accounts in Vault:</span>
                                <span>{bankInfo.accounts_in_vault}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Accounts Not in Vault:</span>
                                <span>{bankInfo.accounts_not_in_vault}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Total Balance:</span>
                                <span>${bankInfo.total_balance.toLocaleString()}</span>
                            </li>
                            <li className="flex justify-between">
                                <span className="font-medium">Recent Transactions:</span>
                                <span>{bankInfo.recent_transactions_count}</span>
                            </li>
                        </ul>
                    </div>
                ) : (
                    <div className="bg-gray-100 shadow-lg rounded-lg p-6 mt-6 text-gray-700">
                        <p className="text-center font-medium">Bank information is currently unavailable.</p>
                    </div>
                )}

            </main>
        </div>
    );




}
export default DashboardPage;