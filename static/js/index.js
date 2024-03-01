document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.getElementById('searchForm');
  searchForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission

      // Get the selected engine value
      const selectedEngine = document.querySelector('input[name="engine"]:checked').value;
      // Get the query value
      const queryValue = document.getElementById('input').value;

      // Update the form's action attribute to include both the query and the selected engine as query parameters
      this.action = `/search?engine=${selectedEngine}&query=${encodeURIComponent(queryValue)}`;

      // Submit the form programmatically
      this.submit();
  });
});
