import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const API = "http://127.0.0.1:8000";

interface Asset {
    id: number;
    asset_id: string;
    asset_name: string;
    category: string;
    location_id: number;
    status: string;
}

export default function AllAssets() {
    const navigate = useNavigate();
    const [assets, setAssets] = useState<Asset[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchAssets();
    }, []);

    const fetchAssets = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/assets/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setAssets(response.data);
        } catch (err) {
            console.error("Error fetching assets:", err);
            setError("Failed to load assets");
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
                <p onClick={() => navigate("/assets")}><strong>All Assets</strong></p>
                <p onClick={() => navigate("/locations")}>Locations</p>
                <p onClick={() => navigate("/maintenance")}>Maintenance</p>
                <p onClick={() => navigate("/reports")}>Reports</p>
                <p onClick={() => navigate("/users")}>User Management</p>

                <button className="dashboard-logout-btn" onClick={logout}>
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="dashboard-main">
                <h1>All Assets</h1>
                <p>View and manage all airport assets</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading assets...</p>
                ) : error ? (
                    <p style={{ textAlign: "center", color: "red" }}>{error}</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Asset ID</th>
                                    <th>Asset Name</th>
                                    <th>Category</th>
                                    <th>Location ID</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {assets.length > 0 ? (
                                    assets.map((asset) => (
                                        <tr key={asset.id}>
                                            <td>{asset.asset_id}</td>
                                            <td>{asset.asset_name}</td>
                                            <td>{asset.category}</td>
                                            <td>{asset.location_id}</td>
                                            <td className="status-active">{asset.status}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} style={{ textAlign: "center", color: "#999" }}>
                                            No assets found
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

