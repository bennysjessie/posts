// Keep track of form changes
let formChanged = false;

// Function to set the formChanged flag
function setFormChanged() {
  formChanged = true;
}

// Function to reset the formChanged flag
function resetFormChanged() {
  formChanged = false;
}

// Function to prompt warning on page leave
function warnOnPageLeave(event) {
  if (formChanged) {
    event.preventDefault();
    event.returnValue = "You have unsaved changes. Are you sure you want to leave?";
  }
}
