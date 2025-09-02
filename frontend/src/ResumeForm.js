import React, { useState } from 'react';
import { createResume } from './api';

const ResumeForm = ({ onResumeCreated, onCancel }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createResume({ title, content });
      setTitle('');
      setContent('');
      setError('');
      onResumeCreated();
    } catch (error) {
      setError('Failed to create resume');
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '20px', margin: '10px 0' }}>
      <h3>Create New Resume</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            placeholder="Resume Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div>
          <textarea
            placeholder="Resume Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            style={{ width: '100%', height: '100px', padding: '8px', margin: '5px 0' }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div>
          <button type="submit" style={{ marginRight: '10px' }}>
            Create Resume
          </button>
          <button type="button" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ResumeForm;