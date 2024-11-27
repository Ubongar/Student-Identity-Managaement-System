document.addEventListener("DOMContentLoaded", function() {
    // Example of simple client-side validation
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const inputs = form.querySelectorAll("input, select");
        let valid = true;
        inputs.forEach(function(input) {
            if (input.value === "") {
                valid = false;
                alert("Please fill in all fields.");
            }
        });

        if (!valid) {
            event.preventDefault();  // Prevent form submission if not valid
        }
    });
});
