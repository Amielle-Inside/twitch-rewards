function updateSelectedOption(pronouns_id) {
    let selector = document.querySelector(`#pronouns-selector [value="${pronouns_id}"]`);
    if (!selector) {
        selector = document.querySelector('#pronouns-selector [value="0"]');
    }
    selector.checked = true;
}

function handlePronounsChange(e) {
    const data = { pronouns: e.target.value };
    fetch("/users/set-pronouns", { method: "POST", body: JSON.stringify(data), headers: { "Content-Type": "application/json" } })
        .then((response) => {
            if (!response.ok) {
                alert('Algo deu errado. Avisa no Discord!');
            }
            else {
                alert('Foi! Se você mudou durante a live, pede pra Ada atualizar o chat :)');
            }
        });
}

fetch("/users")
    .then((response) => {
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            response.json().then((r) => updateSelectedOption(r.pronouns_id));
        }
    });

document.getElementById('pronouns-selector').addEventListener("change", handlePronounsChange);
