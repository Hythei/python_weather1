import React, {useState, useEffect} from 'react'
import api from './api'

const App = () => {
    const [documents, setDocuments] = useState([])
//    const [formData, setFormData] = useState({
// }

    const fetchWeatherDocuments = async () => {
        const response = await api.get('/weather_information');
        setDocuments(response.data.weather_information)
    };

    useEffect(() => {
        fetchWeatherDocuments();
    }, []);

    return (
        <div className="container mt-4">
            <table className="table table-striped table-bordered table-hover">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>Location</th>
                        <th>Temperature</th>
                        <th>Match prediction</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {documents.map((document, index) => (
                        <tr key={index}>
                            <td>{document._id}</td>
                            <td>{document.location}</td>
                            <td>{document.temperature}</td>
                            <td>{document.match_prediction ? "Yes" : "No"}</td>
                            <td>{document.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
export default App;
