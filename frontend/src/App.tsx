import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Login from "./Login";
import Dashboard from "./Dashboard";
import AllAssets from "./pages/AllAssets";
import Locations from "./pages/Locations";
import Maintenance from "./pages/Maintenance";
import Reports from "./pages/Reports";
import UserManagement from "./pages/UserManagement";

export default function App() {
    const token = localStorage.getItem("token");

    return (
        <Routes>
            <Route
                path="/"
                element={token ? <Navigate to="/dashboard" /> : <Login />}
            />
            <Route
                path="/dashboard"
                element={token ? <Dashboard /> : <Navigate to="/" />}
            />
            <Route
                path="/assets"
                element={token ? <AllAssets /> : <Navigate to="/" />}
            />
            <Route
                path="/locations"
                element={token ? <Locations /> : <Navigate to="/" />}
            />
            <Route
                path="/maintenance"
                element={token ? <Maintenance /> : <Navigate to="/" />}
            />
            <Route
                path="/reports"
                element={token ? <Reports /> : <Navigate to="/" />}
            />
            <Route
                path="/users"
                element={token ? <UserManagement /> : <Navigate to="/" />}
            />
        </Routes>
    );
}