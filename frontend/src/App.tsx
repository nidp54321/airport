import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Dashboard from "./Dashboard";
import AllAssets from "./pages/AllAssets";
import Locations from "./pages/Locations";
import Maintenance from "./pages/Maintenance";
import Reports from "./pages/Reports";
import UserManagement from "./pages/UserManagement";
import {useState} from "react";

export default function App() {
    const [user, setUser] = useState(
        JSON.parse(localStorage.getItem("user") || "null")
    );
    return (
        <Routes>
            {/* Login Route */}
            <Route
                path="/"
                element={<Login setUser={setUser} />}
            />

            {/* Protected Routes */}
            {user && (
                <>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/assets" element={<AllAssets />} />
                    <Route path="/locations" element={<Locations />} />
                    <Route path="/maintenance" element={<Maintenance />} />
                    <Route path="/reports" element={<Reports />} />
                    <Route path="/users" element={<UserManagement />} />
                </>
            )}

            {/* Catch all */}
            <Route
                path="*"
                element={<Navigate to={user ? "/dashboard" : "/"} />}
            />
        </Routes>
    );
}