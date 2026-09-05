function handleRedeemButton(e) {
    const button = document.getElementById("redeem");
    const trophy_id = button.getAttribute("data-trophy-id");

    fetch(`/trophies/api/${trophy_id}/redeem`, { method: "POST" })
        .then((response) => {
            if (!response.ok) {
                alert('Algo deu errado. Avisa no Discord!');
            }
            else {
                alert('Foi! Agora voce pode ver o trofeu no seu perfil e usar na live :)');
                window.location.reload();
            }
        });
}

document.getElementById('redeem').addEventListener("click", handleRedeemButton);
