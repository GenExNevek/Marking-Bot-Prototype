// Create User
document.getElementById('create-user-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    fetch('http://localhost:5000/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'username': username
        })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('user_id', data.user_id);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function handleDropdowns(assignmentRedirectUrl) {
    // Display the 'Course' dropdown
    document.getElementById('course-dropdown').hidden = false;
    // Hide the 'Module' and 'Assignment' dropdowns until they are needed
    document.getElementById('module-dropdown').hidden = true;
    document.getElementById('assignment-dropdown').hidden = true;

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
        // Create a new button element
        var btn = document.createElement("button");
        
        // Set the button's text
        btn.innerHTML = "Proceed";
        
        // Set the button's onclick event to navigate to the next page
        btn.onclick = function () {
            const user_id = localStorage.getItem('user_id');
            window.location.href = `${assignmentRedirectUrl}?user_id=${user_id}`; // use the redirect URL passed to the function
        };
        
        // Append the button to the body (or wherever you want to add it)
        document.body.appendChild(btn);
    });
}

document.getElementById('submit-assignment-btn').addEventListener('click', function() {
    handleDropdowns("submit_assignment.html");
});

document.getElementById('edit-assignment-btn').addEventListener('click', function() {
    handleDropdowns("edit_assignment.html");
});

document.getElementById('review-feedback-btn').addEventListener('click', function() {
    handleDropdowns("review_assignment.html");
});