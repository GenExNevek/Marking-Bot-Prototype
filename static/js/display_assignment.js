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
        });
};