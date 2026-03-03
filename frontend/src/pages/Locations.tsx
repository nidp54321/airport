import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";
import NavigationPanel from "../components/NavigationPanel.tsx";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

interface Location {
    id: number;
    name: string;
    location_type: string;
    capacity: number | null;
    is_active: boolean;
}

export default function Locations() {
    const [locations, setLocations] = useState<Location[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchLocations();
    }, []);

    const fetchLocations = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/locations/`);
            setLocations(response.data);
        } catch (err) {
            console.error("Error fetching locations:", err);
            setError("Failed to load locations");
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="dashboard-container">
            <NavigationPanel />
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
