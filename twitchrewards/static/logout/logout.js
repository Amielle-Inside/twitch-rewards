const parsedHash = new URLSearchParams(
    window.location.search
);

const code = parsedHash.get("code");
const data = { code: code };
fetch("/logout", { method: "POST" })
    .then((response) => {
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            window.location.href = `/?nocache=${(new Date()).getTime()}`;
        }
    });
