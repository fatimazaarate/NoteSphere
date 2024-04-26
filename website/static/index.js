// Function to dismiss alert messages
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('close')) {
    var alertDiv = event.target.closest('.alert');
    alertDiv.remove();
  }
});
