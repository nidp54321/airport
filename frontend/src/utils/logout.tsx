import {useNavigate} from "react-router-dom";

export function useLogout() {
    const navigate = useNavigate();

    return () => {
        localStorage.removeItem("user"); // clear login
        navigate("/"); // redirect to login
    };
}