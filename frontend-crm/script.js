async function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    try {
        const response = await fetch("http://localhost:3000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (data.token) {
            // Si el token existe, lo guardamos y saltamos al dashboard
            localStorage.setItem("token", data.token);
            window.location.href = "dashboard.html"; 
        } else {
            // Si el servidor responde pero con un error (clave mal, etc)
            alert("Error: " + data.error);
        }

    } catch (error) {
        // Si el servidor ni siquiera responde
        alert("No se pudo conectar con el servidor. ¿Está encendido?");
    }
} // <--- Esta llave cierra la función completa y es la que faltaba