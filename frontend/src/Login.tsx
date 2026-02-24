import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles.css";

const API = "http://127.0.0.1:8000";

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const login = async () => {
        try {
            const formData = new URLSearchParams();
            formData.append("username", username);
            formData.append("password", password);

            const res = await axios.post(`${API}/auth/token`, formData);

            localStorage.setItem("token", res.data.access_token);

            navigate("/dashboard"); // 🔥 redirect after login
        } catch (err: any) {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Login</h2>

                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={login}>Login</button>

                {error && <p className="login-error">{error}</p>}
            </div>
        </div>
    );
}