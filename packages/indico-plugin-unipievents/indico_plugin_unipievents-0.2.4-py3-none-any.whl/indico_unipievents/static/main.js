const WPSYNC_CONFIG = {
    TEXT: 'Synchronize now',
    INPROGRESS_TEXT: 'Synchronization in progress ...'
}

function disableSyncButton() {
    let el = document.getElementById('wp-sync-button');
    el.innerHTML = WPSYNC_CONFIG.INPROGRESS_TEXT;
    el.onclick = undefined;
}

function enableSyncButton() {
    let el = document.getElementById('wp-sync-button');
    el.innerHTML = WPSYNC_CONFIG.TEXT;
    el.onclick = onWordpressSync;
}

async function onWordpressSync(event) {
    disableSyncButton();
    
    try {
	    const response = await fetch('./update');
	    const data = await response.json();
    } catch (error) {
	    console.error("Failed to request the update");
    }

    enableSyncButton();
}

window.addEventListener('DOMContentLoaded', enableSyncButton);

