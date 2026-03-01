//static/js/auth.js

async function loginUser(username, password) {
    const response = await fecthc("api/token/", {
        method: "POST",
        Headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    const data = await response.JSON();

    //guardar tokens
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    console.log("login exitoso");

}

function handleLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    loginUser(username, password);
}