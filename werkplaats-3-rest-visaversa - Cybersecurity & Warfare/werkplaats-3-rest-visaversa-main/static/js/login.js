function handleLogin(event) {
    event.preventDefault();
    var form = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    }

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(data => {
                // document.getElementById("errorMessage") = data.message
                console.log(data.message)
                document.getElementById("error-message").innerHTML = data.message;
            });
        }
    })
}
