import React, { useState } from 'react';
import axios from 'axios';

function AddReminder() {
    const [medicationName, setMedicationName] = useState('');
    const [dosage, setDosage] = useState('');
    const [time, setTime] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post(
                'http://localhost:5000/reminders',
                { medication_name: medicationName, dosage, time },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Reminder added');
        } catch (error) {
            alert('Error adding reminder');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={medicationName}
                onChange={(e) => setMedicationName(e.target.value)}
                placeholder="Medication Name"
            />
            <input
                type="text"
                value={dosage}
                onChange={(e) => setDosage(e.target.value)}
                placeholder="Dosage"
            />
            <input
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
            />
            <button type="submit">Add Reminder</button>
        </form>
    );
}

export default AddReminder;
