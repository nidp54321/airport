import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import NavigationPanel from "./components/NavigationPanel";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

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
    const user = localStorage.getItem("user");

    const [stats, setStats] = useState<Stats>({
        total_assets: 0,
        active_users: 0,
        pending_maintenance: 0,
        system_health: "0%"
    });

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) {
            navigate("/");
            return;
        }

        fetchDashboardStats();
    }, []);

    const fetchDashboardStats = async () => {
        try {
            setLoading(true);

            const [assetsRes, maintenanceRes, usersRes] = await Promise.all([
                axios.get(`${API}/assets/`),
                axios.get(`${API}/maintenance/`),
                axios.get(`${API}/users/`)
            ]);

            const assets = assetsRes.data;
            const maintenance = maintenanceRes.data;
            const users = usersRes.data;

            const pendingMaintenance = maintenance.filter(
                (m: Maintenance) =>
                    m.status === "scheduled" || m.status === "in_progress"
            ).length;

            setStats({
                total_assets: assets.length,
                active_users: users.length,
                pending_maintenance: pendingMaintenance,
                system_health: "98%"
            });

        } catch (error) {
            console.error("Error fetching dashboard stats:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <NavigationPanel />

            <div className="dashboard-main">
                <h1>Dashboard</h1>
                <p>Welcome to Airport Assets Management System</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>
                        Loading dashboard data...
                    </p>
                ) : (
                    <>
                        <div className="quick-actions">
                            <button
                                className="quick-action-btn"
                                onClick={() => navigate("/users")}
                                title="Go to User Management"
                            >
                                👥 Manage Users
                            </button>

                            <button
                                className="quick-action-btn primary"
                                onClick={() => navigate("/users")}
                                title="Add New User"
                            >
                                ➕ Add User
                            </button>
                        </div>

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
                                    <td className="status-active">
                                        Operational
                                    </td>
                                </tr>
                                <tr>
                                    <td>Active Users</td>
                                    <td>{stats.active_users}</td>
                                    <td className="status-active">
                                        Active
                                    </td>
                                </tr>
                                <tr>
                                    <td>Pending Maintenance</td>
                                    <td>{stats.pending_maintenance}</td>
                                    <td className="status-active">
                                        Scheduled
                                    </td>
                                </tr>
                                <tr>
                                    <td>System Health</td>
                                    <td>{stats.system_health}</td>
                                    <td className="status-active">
                                        Excellent
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}