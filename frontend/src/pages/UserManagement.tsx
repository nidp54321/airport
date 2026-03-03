import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";
import NavigationPanel from "../components/NavigationPanel.tsx";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

interface User {
    id: number;
    username: string;
    full_name: string | null;
    email: string | null;
    role: string;
    is_active: boolean;
}

export default function UserManagement() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [showAddModal, setShowAddModal] = useState(false);
    const [newUser, setNewUser] = useState({
        username: "",
        password: "",
        email: "",
        full_name: "",
        role: "user"
    });
    const [showEditModal, setShowEditModal] = useState(false);
    const [editUser, setEditUser] = useState<User | null>(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/users/`);
            setUsers(response.data);
        } catch (err) {
            console.error("Error fetching users:", err);
            setError("Failed to load users");
        } finally {
            setLoading(false);
        }
    };

    const currentUser = JSON.parse(localStorage.getItem("user") || "null");

    const handleAddUser = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post(`${API}/users/`, newUser);
            setShowAddModal(false);
            setNewUser({
                username: "",
                password: "",
                email: "",
                full_name: "",
                role: "user"
            });
            fetchUsers();
        } catch (err) {
            console.error("Error adding user:", err);
            alert("Failed to add user");
        }
    };

    const handleEditClick = (user: User) => {
        setEditUser(user);
        setShowEditModal(true);
    };

    const handleUpdateUser = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!editUser) return;

        try {
            await axios.put(`${API}/users/${editUser.id}`, editUser);
            setShowEditModal(false);
            setEditUser(null);
            fetchUsers();
        } catch (err) {
            console.error("Error updating user:", err);
            alert("Failed to update user");
        }
    };

    const handleDeleteUser = async (userId: number) => {
        if (window.confirm("Are you sure you want to delete this user?")) {
            try {
                await axios.delete(`${API}/users/${userId}?username=${currentUser.username}`);
                fetchUsers();
            } catch (err) {
                console.error("Error deleting user:", err);
                alert("Failed to delete user");
            }
        }
    };

    return (
        <div className="dashboard-container">
            <NavigationPanel />
            <div className="dashboard-main">
                <div className="page-header">
                    <div>
                        <h1>User Management</h1>
                        <p>Manage system users and permissions</p>
                    </div>
                    <button className="btn-add-user" onClick={() => setShowAddModal(true)}>
                        ➕ Add User
                    </button>
                </div>

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
                                    <th>Actions</th>
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
                                            <td>
                                                <div className="action-icons">
                                                    <button
                                                        className="icon-btn edit-btn"
                                                        title="Edit user"
                                                        onClick={() => handleEditClick(user)}
                                                    >
                                                        ✏️
                                                    </button>

                                                    {currentUser?.role === "admin" &&
                                                        user.role !== "admin" &&
                                                        user.id !== currentUser.id && (
                                                            <button
                                                                className="icon-btn delete-btn"
                                                                title="Delete user"
                                                                onClick={() => handleDeleteUser(user.id)}
                                                            >
                                                                🗑️
                                                            </button>
                                                        )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={6} style={{ textAlign: "center", color: "#999" }}>
                                            No users found
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* Add User Modal */}
                {showAddModal && (
                    <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
                        <div className="modal" onClick={(e) => e.stopPropagation()}>
                            <div className="modal-header">
                                <h2>Add New User</h2>
                                <button className="modal-close" onClick={() => setShowAddModal(false)}>✕</button>
                            </div>
                            <form onSubmit={handleAddUser} className="modal-form">
                                <div className="form-group">
                                    <label htmlFor="username">Username *</label>
                                    <input
                                        type="text"
                                        id="username"
                                        required
                                        value={newUser.username}
                                        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                                        placeholder="Enter username"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="password">Password *</label>
                                    <input
                                        type="password"
                                        id="password"
                                        required
                                        value={newUser.password}
                                        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                        placeholder="Enter password"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="email">Email *</label>
                                    <input
                                        type="email"
                                        id="email"
                                        required
                                        value={newUser.email}
                                        onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                                        placeholder="Enter email"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="full_name">Full Name</label>
                                    <input
                                        type="text"
                                        id="full_name"
                                        value={newUser.full_name}
                                        onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                                        placeholder="Enter full name"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="role">Role *</label>
                                    <select
                                        id="role"
                                        required
                                        value={newUser.role}
                                        onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                                    >
                                        <option value="user">User</option>
                                        <option value="analyst">Analyst</option>
                                        <option value="manager">Manager</option>
                                        <option value="admin">Admin</option>
                                    </select>
                                </div>
                                <div className="modal-buttons">
                                    <button type="button" className="btn-cancel" onClick={() => setShowAddModal(false)}>
                                        Cancel
                                    </button>
                                    <button type="submit" className="btn-submit">
                                        Add User
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                {/* Edit User Modal */}
                {showEditModal && editUser && (
                    <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
                        <div className="modal" onClick={(e) => e.stopPropagation()}>
                            <div className="modal-header">
                                <h2>Edit User</h2>
                                <button className="modal-close" onClick={() => setShowEditModal(false)}>✕</button>
                            </div>

                            <form onSubmit={handleUpdateUser} className="modal-form">

                                <div className="form-group">
                                    <label>Username</label>
                                    <input
                                        type="text"
                                        value={editUser.username}
                                        disabled
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Full Name</label>
                                    <input
                                        type="text"
                                        value={editUser.full_name || ""}
                                        onChange={(e) =>
                                            setEditUser({ ...editUser, full_name: e.target.value })
                                        }
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Email</label>
                                    <input
                                        type="email"
                                        value={editUser.email || ""}
                                        onChange={(e) =>
                                            setEditUser({ ...editUser, email: e.target.value })
                                        }
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Role</label>
                                    <select
                                        value={editUser.role}
                                        disabled={editUser.role === "admin"} // Prevent changing admin role
                                        onChange={(e) =>
                                            setEditUser({ ...editUser, role: e.target.value })
                                        }
                                    >
                                        <option value="user">User</option>
                                        <option value="analyst">Analyst</option>
                                        <option value="manager">Manager</option>
                                        <option value="admin">Admin</option>
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label>Status</label>
                                    <select
                                        value={editUser.is_active ? "active" : "inactive"}
                                        onChange={(e) =>
                                            setEditUser({
                                                ...editUser,
                                                is_active: e.target.value === "active"
                                            })
                                        }
                                    >
                                        <option value="active">Active</option>
                                        <option value="inactive">Inactive</option>
                                    </select>
                                </div>

                                <div className="modal-buttons">
                                    <button
                                        type="button"
                                        className="btn-cancel"
                                        onClick={() => setShowEditModal(false)}
                                    >
                                        Cancel
                                    </button>
                                    <button type="submit" className="btn-submit">
                                        Update User
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

