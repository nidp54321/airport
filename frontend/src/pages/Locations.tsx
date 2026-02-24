import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const API = "http://127.0.0.1:8000";

interface Location {
    id: number;
    name: string;
    location_type: string;
    capacity: number | null;
    is_active: boolean;
}

export default function Locations() {
    const navigate = useNavigate();
    const [locations, setLocations] = useState<Location[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchLocations();
    }, []);

    const fetchLocations = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/locations/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setLocations(response.data);
        } catch (err) {
            console.error("Error fetching locations:", err);
            setError("Failed to load locations");
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
                <p><strong>Locations</strong></p>
                <p onClick={() => navigate("/maintenance")}>Maintenance</p>
                <p onClick={() => navigate("/reports")}>Reports</p>
                <p onClick={() => navigate("/users")}>User Management</p>

                <button className="dashboard-logout-btn" onClick={logout}>
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="dashboard-main">
                <h1>Locations</h1>
                <p>Manage airport locations and terminals</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading locations...</p>
                ) : error ? (
                    <p style={{ textAlign: "center", color: "red" }}>{error}</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Location Name</th>
                                    <th>Type</th>
                                    <th>Capacity</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {locations.length > 0 ? (
                                    locations.map((location) => (
                                        <tr key={location.id}>
                                            <td>{location.name}</td>
                                            <td>{location.location_type}</td>
                                            <td>{location.capacity || "N/A"}</td>
                                            <td className={location.is_active ? "status-active" : "status-inactive"}>
                                                {location.is_active ? "Active" : "Inactive"}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={4} style={{ textAlign: "center", color: "#999" }}>
                                            No locations found
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

