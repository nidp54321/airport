import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const API = "http://127.0.0.1:8000";

interface User {
    id: number;
    username: string;
    full_name: string | null;
    email: string | null;
    role: string;
    is_active: boolean;
}

export default function UserManagement() {
    const navigate = useNavigate();
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/users/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUsers(response.data);
        } catch (err) {
            console.error("Error fetching users:", err);
            setError("Failed to load users");
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        navigate("/");
    };

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <div className="dashboard-sidebar">
                <h3>Airport Assets</h3>

                <p onClick={() => navigate("/dashboard")}>Dashboard</p>
                <p onClick={() => navigate("/assets")}>All Assets</p>
                <p onClick={() => navigate("/locations")}>Locations</p>
                <p onClick={() => navigate("/maintenance")}>Maintenance</p>
                <p onClick={() => navigate("/reports")}>Reports</p>
                <p><strong>User Management</strong></p>

                <button className="dashboard-logout-btn" onClick={logout}>
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="dashboard-main">
                <h1>User Management</h1>
                <p>Manage system users and permissions</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading users...</p>
                ) : error ? (
                    <p style={{ textAlign: "center", color: "red" }}>{error}</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Username</th>
                                    <th>Full Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.length > 0 ? (
                                    users.map((user) => (
                                        <tr key={user.id}>
                                            <td>{user.username}</td>
                                            <td>{user.full_name || "N/A"}</td>
                                            <td>{user.email || "N/A"}</td>
                                            <td>{user.role}</td>
                                            <td className={user.is_active ? "status-active" : "status-inactive"}>
                                                {user.is_active ? "Active" : "Inactive"}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} style={{ textAlign: "center", color: "#999" }}>
                                            No users found
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

