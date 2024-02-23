import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [message, setMessage] = useState('');
  const [commonSkills, setCommonSkills] = useState([]);
  
  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resumeFile) {
      console.error('No resume file selected');
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post('http://localhost:8000/preprocess', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setMessage(response.data.message);
      setCommonSkills(response.data.common_skills); // New line to set common skills
      
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Job Matcher</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <textarea placeholder="Enter job description" value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} />
        <button type="submit">Evaluate</button>
      </form>
      {message && <p>{message}</p>}
      {commonSkills.length > 0 && (
        <div>
          <h2>Common Skills</h2>
          <ul>
            {commonSkills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
