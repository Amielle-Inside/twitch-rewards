const parsedHash = new URLSearchParams(
    window.location.search
);

const code = parsedHash.get("code");
console.log("DEBUG: code from URL:", code);
const data = { code: code };
console.log("DEBUG: POSTing to /token with:", data);
fetch("/token", { method: "POST", body: JSON.stringify(data), headers: { "Content-Type": "application/json" } })
    .then((response) => {
        console.log("DEBUG: Response status:", response.status, response.ok);
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            console.log("DEBUG: Redirecting to /");
            window.location.href = '/';
        }
    })
    .catch(err => {
        console.error("DEBUG: Fetch error:", err);
        alert('Erro de rede. Avisa no Discord!');
    });
