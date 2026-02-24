import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const API = "http://127.0.0.1:8000";

interface Maintenance {
    id: number;
    maintenance_id: string;
    asset_id: number;
    maintenance_type: string;
    status: string;
    scheduled_date: string;
}

export default function Maintenance() {
    const navigate = useNavigate();
    const [maintenance, setMaintenance] = useState<Maintenance[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchMaintenance();
    }, []);

    const fetchMaintenance = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/maintenance/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMaintenance(response.data);
        } catch (err) {
            console.error("Error fetching maintenance:", err);
            setError("Failed to load maintenance records");
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        navigate("/");
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString();
    };

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <div className="dashboard-sidebar">
                <h3>Airport Assets</h3>

                <p onClick={() => navigate("/dashboard")}>Dashboard</p>
                <p onClick={() => navigate("/assets")}>All Assets</p>
                <p onClick={() => navigate("/locations")}>Locations</p>
                <p><strong>Maintenance</strong></p>
                <p onClick={() => navigate("/reports")}>Reports</p>
                <p onClick={() => navigate("/users")}>User Management</p>

                <button className="dashboard-logout-btn" onClick={logout}>
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="dashboard-main">
                <h1>Maintenance</h1>
                <p>Track and manage asset maintenance schedules</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading maintenance records...</p>
                ) : error ? (
                    <p style={{ textAlign: "center", color: "red" }}>{error}</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Maintenance ID</th>
                                    <th>Asset ID</th>
                                    <th>Type</th>
                                    <th>Scheduled Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {maintenance.length > 0 ? (
                                    maintenance.map((m) => (
                                        <tr key={m.id}>
                                            <td>{m.maintenance_id}</td>
                                            <td>{m.asset_id}</td>
                                            <td>{m.maintenance_type}</td>
                                            <td>{formatDate(m.scheduled_date)}</td>
                                            <td className="status-active">{m.status}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} style={{ textAlign: "center", color: "#999" }}>
                                            No maintenance records found
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

