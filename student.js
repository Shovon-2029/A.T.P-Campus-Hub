// This represents the data extracted by the AI from your uploaded file
const mockParsedData = [
    { time: "09:00 AM", mon: "Advanced AI", tue: "Neural Networks", wed: "Ethics in Tech" },
    { time: "11:00 AM", mon: "Cyber Security", tue: "Database Mgmt", wed: "UI/UX Design" },
    { time: "02:00 PM", mon: "Project Lab", tue: "Cloud Computing", wed: "Seminar" }
];

function automateScheduleUpdate(data) {
    const tableBody = document.getElementById('scheduleBody');
    
    // Clear the current static table
    tableBody.innerHTML = '';

    // Loop through the data and create new rows
    data.forEach(row => {
        const newRow = `
            <tr>
                <td>${row.time}</td>
                <td>${row.mon}</td>
                <td>${row.tue}</td>
                <td>${row.wed}</td>
            </tr>
        `;
        tableBody.innerHTML += newRow;
    });

    // Notify the user in the UI
    const heroText = document.querySelector('.welcome-hero p');
    heroText.innerHTML = "<strong>Schedule Synchronized!</strong> Your dashboard is up to date. ✅";
    heroText.style.color = "var(--primary)";
}

// Update your handleFileUpload to trigger the automation
function handleFileUpload(input) {
    if (input.files[0]) {
        appendMessage('user', `Uploaded: ${input.files[0].name}`);
        
        // Show AI "Processing" state
        appendMessage('ai', 'Scanning your document for dates and timings...');
        
        setTimeout(() => {
            // Trigger the automation
            automateScheduleUpdate(mockParsedData);
            
            appendMessage('ai', 'Automation complete! I have updated your main dashboard table with your new classes.');
        }, 2000);
    }
}
1027202675528-dq0u7ce0cpa851bm30op28dlvbmgk860.apps.googleusercontent.com
