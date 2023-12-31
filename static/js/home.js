function handleDropdowns(assignmentRedirectUrl) {
    //------------------------------------------------------------------
    // GET COURSE
    //------------------------------------------------------------------

    fetch('http://localhost:5000/get_courses')
    .then(response => response.json())
    .then(data => {
        let dropdown = document.getElementById('course-dropdown');
        dropdown.length = 0;

        let defaultOption = document.createElement('option');
        defaultOption.text = 'Choose Course';
        dropdown.add(defaultOption);
        dropdown.selectedIndex = 0;

        let option;
        for (let i = 0; i < data.length; i++) {
            option = document.createElement('option');
            option.text = data[i].CourseTitle;
            option.value = data[i].CourseID;
            dropdown.add(option);
        }
    }).catch(error => console.error('Error:', error));

    //------------------------------------------------------------------
    // GET MODULES
    //------------------------------------------------------------------

    document.getElementById('course-dropdown').addEventListener('change', function() {
        // Display the 'Module' dropdown when a course is selected
        document.getElementById('module-dropdown').hidden = false;

        fetch('http://localhost:5000/get_modules/' + this.value)
        .then(response => response.json())
        .then(data => {
            let dropdown = document.getElementById('module-dropdown');
            dropdown.length = 0;

            let defaultOption = document.createElement('option');
            defaultOption.text = 'Choose Module';
            dropdown.add(defaultOption);
            dropdown.selectedIndex = 0;

            let option;
            for (let i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.text = data[i].ModuleTitle;
                option.value = data[i].ModuleNo;
                dropdown.add(option);
            }
        });
    });

    //------------------------------------------------------------------
    // GET ASSIGNMENTS
    //------------------------------------------------------------------

    document.getElementById('module-dropdown').addEventListener('change', function() {
        // Display the 'Assignment' dropdown when a module is selected
        document.getElementById('assignment-dropdown').hidden = false;

        fetch('http://localhost:5000/get_assignments/' + this.value)
        .then(response => response.json())
        .then(data => {
            let dropdown = document.getElementById('assignment-dropdown');
            dropdown.length = 0;

            let defaultOption = document.createElement('option');
            defaultOption.text = 'Choose Assignment';
            dropdown.add(defaultOption);
            dropdown.selectedIndex = 0;

            let option;
            for (let i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.text = data[i].AssignmentTitle;
                option.value = data[i].AssignmentID;
                dropdown.add(option);
            }
        });
    });

    //------------------------------------------------------------------
    // NAVIGATE TO ASSIGNMENT
    //------------------------------------------------------------------

    document.getElementById('assignment-dropdown').addEventListener('change', function() {
        var course = document.getElementById('course-dropdown').value;
        var module = document.getElementById('module-dropdown').value;
        var assignment = document.getElementById('assignment-dropdown').value;
        
        if (course && module && assignment) {
            // Create a new button element
            var btn = document.createElement("button");

            // Set the button's text
            btn.innerHTML = "Proceed";

            // Set the button's onclick event to navigate to the next page
            btn.onclick = function () {
                console.log(course, module, assignment);
                window.location.href = assignmentRedirectUrl + '?course=' + encodeURIComponent(course) + '&module=' + encodeURIComponent(module) + '&assignment=' + encodeURIComponent(assignment); // use the redirect URL passed to the function
        };

        // Append the button to the body (or wherever you want to add it)
        document.body.appendChild(btn);
    }
    });

    // Display the 'Course' dropdown at the end of the function
    document.getElementById('course-dropdown').hidden = false;
}

document.getElementById('submit-assignment-btn').addEventListener('click', function() {
    handleDropdowns("display_assignment.html");
});

document.getElementById('edit-assignment-btn').addEventListener('click', function() {
    handleDropdowns("display_assignment.html");
});

document.getElementById('review-feedback-btn').addEventListener('click', function() {
    handleDropdowns("review_assignment.html");
});

//------------------------------------------------------------------
// ASSIGN USER
//------------------------------------------------------------------

document.getElementById('assign-user-btn').addEventListener('click', function() {
    const username = document.getElementById('username-input').value;
    fetch('http://localhost:5000/assign_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // User was successfully assigned, allow them to proceed
            alert('User was successfully assigned');
            document.getElementById('submit-assignment-btn').hidden = false;
            document.getElementById('edit-assignment-btn').hidden = false;
            document.getElementById('review-feedback-btn').hidden = false;
        } else {
            // Show error message
            alert(data.message);
        }
    });
});

//------------------------------------------------------------------
// CREATE USER
//------------------------------------------------------------------

document.getElementById('create-user-btn').addEventListener('click', function() {
    const username = document.getElementById('username-input').value;
    fetch('http://localhost:5000/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // User was successfully created, allow them to proceed
            alert('User was successfully created');
            document.getElementById('submit-assignment-btn').hidden = false;
            document.getElementById('edit-assignment-btn').hidden = false;
            document.getElementById('review-feedback-btn').hidden = false;
        } else {
            // Show error message
            alert(data.message);
        }
    });
});