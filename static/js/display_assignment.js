window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const assign_id = urlParams.get('assignment');

    fetch('http://localhost:5000/get_assignment_details/' + assign_id)
    .then(response => response.json())
    .then(data => {
        document.getElementById('course-name').innerText = data[0].CourseName;
        document.getElementById('module-name').innerText = data[0].ModuleName;
        document.getElementById('assignment-name').innerText = data[0].AssignmentName;
        document.getElementById('assignment-text').innerText = data[0].AssignmentText;
        
        let tasksContainer = document.getElementById('tasks-container');
        for(let i=0; i < data.length; i++) {
            let taskElement = document.createElement('div');
            taskElement.innerHTML = `
            <h4>Task: ${data[i].TaskText}</h4>
            <h5>Learning Objective: ${data[i].ObjectiveText}</h5>
            <h6>Question Criteria: ${data[i].QuestionCriteria}</h6>
            <p>Question: ${data[i].QuestionText}</p>
            <p>Suggested Evidence: ${data[i].EvidenceText}</p>
            <textarea placeholder="Enter your response here"></textarea>
            `;
            tasksContainer.appendChild(taskElement);
        }
    })
    .catch(error => console.error('Error:', error));
};
