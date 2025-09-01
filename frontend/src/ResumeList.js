import React, { useState, useEffect } from 'react';
import { getResumes, createResume, improveResume } from './api';

const ResumeList = () => {
  const [resumes, setResumes] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [improvedContent, setImprovedContent] = useState('');

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const data = await getResumes();
      setResumes(data);
    } catch (error) {
      console.error('Error loading resumes:', error);
    }
  };

  const handleCreateResume = async (e) => {
    e.preventDefault();
    try {
      await createResume({ title: newTitle, content: newContent });
      setNewTitle('');
      setNewContent('');
      setShowForm(false);
      loadResumes();
    } catch (error) {
      console.error('Error creating resume:', error);
    }
  };

  const handleImprove = async (resumeId) => {
    try {
      const result = await improveResume(resumeId);
      setImprovedContent(result.improved_content);
    } catch (error) {
      console.error('Error improving resume:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>My Resumes</h2>

      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : 'Create New Resume'}
      </button>

      {showForm && (
        <form onSubmit={handleCreateResume}>
          <input
            placeholder="Title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            required
          />
          <textarea
            placeholder="Content"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            required
          />
          <button type="submit">Create</button>
        </form>
      )}

      {improvedContent && (
        <div>
          <h3>Improved Content:</h3>
          <p>{improvedContent}</p>
        </div>
      )}

      <div>
        {resumes.map((resume) => (
          <div key={resume.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
            <h3>{resume.title}</h3>
            <p>{resume.content}</p>
            <button onClick={() => handleImprove(resume.id)}>Improve</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResumeList;