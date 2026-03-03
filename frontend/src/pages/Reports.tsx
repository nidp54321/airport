import { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";
import NavigationPanel from "../components/NavigationPanel.tsx";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

interface Report {
    id: number;
    report_id: string;
    report_name: string;
    report_type: string;
    generated_date: string;
}

export default function Reports() {
    const [reports, setReports] = useState<Report[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await axios.get(`${API}/reports/`);
            setReports(response.data);
        } catch (err) {
            console.error("Error fetching reports:", err);
            setError("Failed to load reports");
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString();
    };

    return (
        <div className="dashboard-container">
            <NavigationPanel />
            <div className="dashboard-main">
                <h1>Reports</h1>
                <p>View analytics and system reports</p>

                {loading ? (
                    <p style={{ textAlign: "center", color: "#999" }}>Loading reports...</p>
                ) : error ? (
                    <p style={{ textAlign: "center", color: "red" }}>{error}</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Report ID</th>
                                    <th>Report Name</th>
                                    <th>Type</th>
                                    <th>Generated Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {reports.length > 0 ? (
                                    reports.map((report) => (
                                        <tr key={report.id}>
                                            <td>{report.report_id}</td>
                                            <td>{report.report_name}</td>
                                            <td>{report.report_type}</td>
                                            <td>{formatDate(report.generated_date)}</td>
                                            <td className="status-active">Available</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} style={{ textAlign: "center", color: "#999" }}>
                                            No reports found
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

