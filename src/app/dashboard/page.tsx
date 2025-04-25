"use client";
import React, { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';

type UserInfo = {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    phone: string;
    address: string;
    city: string;
    state: string;
    zip: string;
    country: string;
    status: string;
    account_number: string;
    created_at: string;
    updated_at: string;
};
type AccountInfo = {
    account_number: string;
    account_type: string;
    user_id: string;
    account_status: string;
    balance: string;
    created_at: string;
    updated_at: string;
};
type Transaction = {
    id: number,
    account_number: string,
    transaction_type: 'deposit' | 'withdrawal',
    amount: number,
    timestamp: string,

};

const DashboardPage: React.FC = () => {
    const [user, setUser] = useState<UserInfo | null>(null);
    const [accountInfo, setAccountInfo] = useState<AccountInfo | null>(null);
    const [transactions, setTransactions] = useState<Transaction[]>([]); // Adjust the type as needed
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const cookies = document.cookie.split('; ');
        const authCookie = cookies.find((cookie) => cookie.startsWith('authorization='));
        if (authCookie) {
            const token = authCookie.split('=')[1];
            try {
                const decoded = jwtDecode<UserInfo>(token);
                setUser(decoded);
            } catch (error) {
                console.error('Failed to decode token:', error);
                setError('Invalid token');
            }
        }
    }, []);

    useEffect(() => {
        if (user) {
            async function fetchUserAccountInfo() {
                setLoading(true);
                setError(null);
                if (!user) {
                    setLoading(false);
                    return;
                }
                try {
                    const response = await fetch(`/api/account/${user.account_number}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
                    if (response.ok) {
                        const data = await response.json();
                        setAccountInfo(data);
                    } else {
                        setError('Failed to fetch account information');
                    }
                } catch (err) {
                    console.error('Error fetching user account info:', err);
                    setError('An error occurred while fetching account information');
                } finally {
                    setLoading(false);
                }
            }
            async function fetchUserTransactions() {
                setLoading(true);
                setError(null);
                if (!user) {
                    setLoading(false);
                    return;
                }
                try {
                    const response = await fetch(`/api/account/transactions`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
                    if (response.ok) {
                        const data = await response.json();
                        setTransactions(data);
                    } else {
                        setError('Failed to fetch transaction information');
                    }
                } catch (err) {
                    console.error('Error fetching user transaction info:', err);
                    setError('An error occurred while fetching transaction information');
                } finally {
                    setLoading(false);
                }
            }

            fetchUserAccountInfo().then(() => {
                fetchUserTransactions();
            });
        }
    }, [user]);

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
            <p className="text-gray-600">Welcome {user?.first_name} {user?.last_name} !</p>
            {loading && (
                <div className="flex justify-center items-center mt-6">
                    <span className="loading loading-spinner loading-lg"></span>
                </div>
            )}
            {error && (
                <div className="alert alert-error shadow-lg mt-6">
                    <div>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="stroke-current flex-shrink-0 h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M18.364 5.636l-12.728 12.728M5.636 5.636l12.728 12.728"
                            />
                        </svg>
                        <span>{error}</span>
                    </div>
                </div>
            )}
            {user && (
                <div className="card bg-base-100 shadow-xl mt-6">
                    <div className="card-body">
                        <h3 className="card-title">User Information</h3>
                        <p>
                            <strong>Name:</strong> {user.first_name} {user.last_name}
                        </p>
                        <p>
                            <strong>Email:</strong> {user.email}
                        </p>
                        <p>
                            <strong>Phone:</strong> {user.phone}
                        </p>
                        <p>
                            <strong>Address:</strong> {user.address}, {user.city}, {user.state}, {user.zip}, {user.country}
                        </p>
                    </div>
                </div>
            )}
            {accountInfo && (
                <div className="card bg-base-100 shadow-xl mt-6">
                    <div className="card-body">
                        <h3 className="card-title">Account Information</h3>
                        <p>
                            <strong>Account Number:</strong> {accountInfo.account_number}
                        </p>
                        <p>
                            <strong>Account Type:</strong> {accountInfo.account_type}
                        </p>
                        <p>
                            <strong>Status:</strong> {accountInfo.account_status}
                        </p>
                        <p>
                            <strong>Balance:</strong> ${accountInfo.balance}
                        </p>
                    </div>
                </div>
            )}
            {transactions.length > 0 && (
                <div className="card bg-base-100 shadow-xl mt-6">
                    <div className="card-body">
                        <h3 className="card-title">Recent Transactions</h3>
                        <table className="table w-full">
                            <thead>
                                <tr>
                                    <th>Transaction ID</th>
                                    <th>Type</th>
                                    <th>Amount</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                {transactions.map((transaction) => (
                                    <tr key={transaction.id}>
                                        <td>{transaction.id}</td>
                                        <td>{transaction.transaction_type}</td>
                                        <td>${transaction.amount}</td>
                                        <td>{new Date(transaction.timestamp).toLocaleDateString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}



            {!loading && !error && transactions.length === 0 && (
                <div className="alert alert-info shadow-lg mt-6">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="stroke-current flex-shrink-0 h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                    <span>No transactions found.</span>
                </div>
            )}
        </div>
    );
};

export default DashboardPage;