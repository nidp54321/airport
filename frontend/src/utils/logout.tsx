import { useNavigate } from "react-router-dom";

export function useLogout() {
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("user"); // clear login
        navigate("/"); // redirect to login
    };

    return logout;
}