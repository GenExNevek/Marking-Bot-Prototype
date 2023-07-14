window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    
    var course = urlParams.get('course');
    var module = urlParams.get('module');
    var assignment = urlParams.get('assignment');
    
    fetch('http://localhost:5000/display_assignment?course=' + course + '&module=' + module + '&assignment=' + assignment)
        .then(response => response.json())
        .then(data => {
            document.getElementById('course-name').textContent = data.CourseName;
            document.getElementById('module-name').textContent = data.ModuleName;
            document.getElementById('assignment-name').textContent = data.AssignmentName;
            document.getElementById('assignment-text').textContent = data.AssignmentText;

            var tasksDiv = document.getElementById('tasks');
            data.Tasks.forEach(task => {
                var taskDiv = document.createElement('div');
                taskDiv.textContent = 'Task: ' + task[1];
                tasksDiv.appendChild(taskDiv);

                task[2].forEach(objective => {
                    var objectiveDiv = document.createElement('div');
                    objectiveDiv.textContent = 'Learning Objective: ' + objective[1];
                    taskDiv.appendChild(objectiveDiv);

                    objective[2].forEach(question => {
                        var questionDiv = document.createElement('div');
                        questionDiv.textContent = 'Question: ' + question[1];
                        objectiveDiv.appendChild(questionDiv);

                        var evidenceDiv = document.createElement('div');
                        evidenceDiv.textContent = 'Suggested Evidence: ' + question[2];
                        objectiveDiv.appendChild(evidenceDiv);
                    });
                });
            });
        });
};
