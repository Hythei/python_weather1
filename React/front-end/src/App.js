import React, {useState, useEffect} from 'react'
import api from './api'

const App = () => {
    const [documents, setDocuments] = useState([])
    const [formData, setFormData] = useState({
        location: '',
        temperature: 0,
        match_prediction: false,
        date: '',
    })

    const fetchWeatherDocuments = async () => {
        const response = await api.get('/weather_information');
        setDocuments(response.data.weather_information)
    };

    useEffect(() => {
        fetchWeatherDocuments();
    }, []);

    const handleInputChange = (e) => {
        const prediction = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setFormData({
            ...formData,
            [e.target.name]: prediction
        });
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        const submissionData = {
            location: formData.location,
            temperature: parseFloat(formData.temperature),
            match_prediction: formData.match_prediction,
            date: new Date().toISOString(),
        }
        await api.post('/weather_information', submissionData);
        await fetchWeatherDocuments();
        setFormData({
            location: '',
            temperature: '',
            match_prediction: false,
            date: new Date().toLocaleString(),
        });
    };

    const deleteDocument = async (documentId) => {
        try {
            await api.delete(`/weather_information/${documentId}`);
            await fetchWeatherDocuments();
        } catch (error) {
            console.error('Error deleting document:', error);
        }
    }

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        Weather CRUD
                    </a>
                </div>
            </nav>
            <>
                <div className="container">
                    <h1 className="mt-4">Fetch from API</h1>
                    <form>
                        <div>
                            <label htmlFor="location">Location</label>
                            <input type="text" id="location" name="location" />
                            <button type="submit">Submit</button>
                        </div>
                    </form>
                    <div className="mt-4">
                        <h2>Weather information</h2>

                    </div>
                </div>
            </>
            <div className="container">
                <h1 className="mt-4">Add directly to collection</h1>
                <form onSubmit={handleFormSubmit}>
                    <div className="mb-3 mt-3">
                        <label htmlFor="location" className="form-label">Location</label>
                        <input type="text" className="form-control" id="location" name="location" value={formData.location} onChange={handleInputChange} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="temperature" className="form-label">Temperature</label>
                        <input type="number" className="form-control" id="temperature" name="temperature" value={formData.temperature} onChange={handleInputChange} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="match_prediction" className="form-label">Match prediction</label>
                        <input type="checkbox" className="form-check-input" id="match_prediction" name="match_prediction" checked={formData.match_prediction} onChange={handleInputChange} />
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>

                </form>
            </div>
            <div className="container mt-4">
                <table className="table table-striped table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>id</th>
                            <th>Location</th>
                            <th>Temperature</th>
                            <th>Match prediction</th>
                            <th>Date</th>
                            <th></th>
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
                                <td>
                                    <button
                                    onClick={ () => deleteDocument(document._id)}
                                    className="btn btn-primary">
                                    DEL
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
export default App;
