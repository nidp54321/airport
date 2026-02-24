import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "./styles.css";

const API = "http://127.0.0.1:8000";

interface Asset {
    id: number;
    asset_id: string;
    asset_name: string;
    category: string;
    status: string;
}

interface Maintenance {
    id: number;
    maintenance_id: string;
    status: string;
}

interface Stats {
    total_assets: number;
    active_users: number;
    pending_maintenance: number;
    system_health: string;
}

export default function Dashboard() {
    const navigate = useNavigate();
    const [stats, setStats] = useState<Stats>({
        total_assets: 0,
        active_users: 0,
        pending_maintenance: 0,
        system_health: "0%"
    });
    const [loading, setLoading] = useState(true);
    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchDashboardStats();
    }, []);

    const fetchDashboardStats = async () => {
        try {
            setLoading(true);
            const [assetsRes, maintenanceRes] = await Promise.all([
                axios.get(`${API}/assets/`, {
                    headers: { Authorization: `Bearer ${token}` }
                }),
                axios.get(`${API}/maintenance/`, {
                    headers: { Authorization: `Bearer ${token}` }
                })
            ]);

            const assets = assetsRes.data;
            const maintenance = maintenanceRes.data;

            const pendingMaintenance = maintenance.filter(
                (m: Maintenance) => m.status === "scheduled" || m.status === "in_progress"
            ).length;

            setStats({
                total_assets: assets.length,
                active_users: 42, // Placeholder
                pending_maintenance: pendingMaintenance,
                system_health: "98%"
            });
        } catch (error) {
            console.error("Error fetching dashboard stats:", error);
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

                <p onClick={() => navigate("/dashboard")} style={{ cursor: "pointer" }}><strong>Dashboard</strong></p>
                <p onClick={() => navigate("/assets")} style={{ cursor: "pointer" }}>All Assets</p>
                <p onClick={() => navigate("/locations")} style={{ cursor: "pointer" }}>Locations</p>
                <p onClick={() => navigate("/maintenance")} style={{ cursor: "pointer" }}>Maintenance</p>
                <p onClick={() => navigate("/reports")} style={{ cursor: "pointer" }}>Reports</p>
                <p onClick={() => navigate("/users")} style={{ cursor: "pointer" }}>User Management</p>

                <button className="dashboard-logout-btn" onClick={logout}>
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="dashboard-main">
                <h1>Dashboard</h1>
                <p>Welcome to Airport Assets Management System</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading dashboard data...</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Value</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Total Assets</td>
                                    <td>{stats.total_assets}</td>
                                    <td className="status-active">Operational</td>
                                </tr>
                                <tr>
                                    <td>Active Users</td>
                                    <td>{stats.active_users}</td>
                                    <td className="status-active">Active</td>
                                </tr>
                                <tr>
                                    <td>Pending Maintenance</td>
                                    <td>{stats.pending_maintenance}</td>
                                    <td className="status-active">Scheduled</td>
                                </tr>
                                <tr>
                                    <td>System Health</td>
                                    <td>{stats.system_health}</td>
                                    <td className="status-active">Excellent</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}