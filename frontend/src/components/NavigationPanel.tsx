import { useNavigate, useLocation } from "react-router-dom";
import "../styles.css";

export default function NavigationPanel() {
    const navigate = useNavigate();
    const location = useLocation();

    const logout = () => {
        localStorage.removeItem("user"); // since we removed token
        navigate("/");
    };

    const isActive = (path: string) => location.pathname === path;

    return (
        <div className="dashboard-sidebar">
            <h3>Airport Assets</h3>

            <p
                onClick={() => navigate("/dashboard")}
                style={{ fontWeight: isActive("/dashboard") ? "bold" : "normal", cursor: "pointer" }}
            >
                Dashboard
            </p>

            <p
                onClick={() => navigate("/assets")}
                style={{ fontWeight: isActive("/assets") ? "bold" : "normal", cursor: "pointer" }}
            >
                All Assets
            </p>

            <p
                onClick={() => navigate("/locations")}
                style={{ fontWeight: isActive("/locations") ? "bold" : "normal", cursor: "pointer" }}
            >
                Locations
            </p>

            <p
                onClick={() => navigate("/maintenance")}
                style={{ fontWeight: isActive("/maintenance") ? "bold" : "normal", cursor: "pointer" }}
            >
                Maintenance
            </p>

            <p
                onClick={() => navigate("/reports")}
                style={{ fontWeight: isActive("/reports") ? "bold" : "normal", cursor: "pointer" }}
            >
                Reports
            </p>

            <p
                onClick={() => navigate("/users")}
                style={{ fontWeight: isActive("/users") ? "bold" : "normal", cursor: "pointer" }}
            >
                User Management
            </p>

            <button className="dashboard-logout-btn" onClick={logout}>
                Logout
            </button>
        </div>
    );
}