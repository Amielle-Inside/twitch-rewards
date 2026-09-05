function handleSubmitActiveTrophies(e) {
    e.preventDefault();
    const checked_trophies = [...document.querySelectorAll('.active-trophy-option:checked')];
    const checked_trophies_ids = checked_trophies.map((trophy_element) => parseInt(trophy_element.getAttribute("data-trophy-id")));
    if (checked_trophies_ids.length > 3) {
        alert('So pode ter 3 de uma vez. Tira uns ai');
        return;
    }

    const data = {
        'trophies_ids': checked_trophies_ids
    }
    fetch("/users/active-trophies", { method: "POST", body: JSON.stringify(data), headers: { "Content-Type": "application/json" } })
        .then((response) => {
            if (!response.ok) {
                alert('Algo deu errado. Avisa no Discord!');
            }
            else {
                alert('Foi! Se você mudou durante a live, espera 5 minutinhos pra aparecer la');
            }
        });
}

document.getElementById('submit-active-trophies').addEventListener("click", handleSubmitActiveTrophies);
