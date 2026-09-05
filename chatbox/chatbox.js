const customDataCache = new Map();
const server = "UPDATE WITH SERVER URL"

async function getCustomDataFromServer(displayName) {
  const response = await fetch(`${server}/users/${displayName}`, {
    method: "GET",
	});

  if (response.status != 200) {
    return null;
  }

  return await response.json();
}

function getDisplayName(rawPayload) {
  const re = /display-name=(\w*)/;
  return displayName = re.exec(rawPayload)[1];
}

async function getUserData(displayName) {
  if (customDataCache.has(displayName)) {
  	return customDataCache.get(displayName);
  }

  const customData = await getCustomDataFromServer(displayName);
  customDataCache.set(displayName, customData);
  return customData;
}

async function getCustomDisplayName(displayName) {
	const userData = await getUserData(displayName);
  if (!userData) {
    return displayName;
  }

  return `${userData.display_name}(${userData.pronouns})`
}

function updateName(twitchName, customName) {
  const messagesFromUser = document.querySelectorAll(`#log div[data-from="${twitchName}"]`);
  for (const message of messagesFromUser) {
    message.querySelector('.meta .name').textContent = customName;
	}
}

document.addEventListener('onEventReceived', async (obj) => {
  const twitchDisplayName = getDisplayName(obj.detail.payload.raw);
  const customDisplayName = await getCustomDisplayName(twitchDisplayName);

  if (customDisplayName) {
	  updateName(twitchDisplayName, customDisplayName);
  }
});

function cleanupHiddenMessages() {
  var messages = document.querySelectorAll('#log > div');
  for (const message of messages) {
    if (window.window.getComputedStyle(message).opacity == "0") {
      message.remove();
    }
	}
}

setInterval(cleanupHiddenMessages, 10000);