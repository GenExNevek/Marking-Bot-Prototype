window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    
    var course = urlParams.get('course');
    var module = urlParams.get('module');
    var assignment = urlParams.get('assignment');
    
    fetch('http://localhost:5000/display_assignment?course=' + course + '&module=' + module + '&assignment=' + assignment)
        .then(response => response.json())
        .then(data => {
            document.getElementById('course-title').textContent = data.CourseTitle;
            document.getElementById('module-title').textContent = data.ModuleTitle;
            document.getElementById('assignment-title').textContent = data.AssignmentTitle;
            document.getElementById('assignment-description').textContent = data.AssignmentDescription;

            var taskDetailsDiv = document.getElementById('task-details');
            data.TaskDetails.forEach(function(task) {
                var taskDiv = document.createElement('div');
                taskDiv.innerHTML = '<h3>Task Description: ' + task.TaskDescription + '</h3>';
                task.Questions.forEach(function(question) {
                    taskDiv.innerHTML += '<p>Learning Objective: ' + question.LearningObjectiveDescription + '</p>' +
                                         '<p>Question Criteria: ' + question.QuestionCriteria + '</p>' +
                                         '<p>Question Description: ' + question.QuestionDescription + '</p>' +
                                         '<p>Suggested Evidence: ' + question.SuggestedEvidenceDescription + '</p>';
                });
                taskDetailsDiv.appendChild(taskDiv);
            });
        });
};