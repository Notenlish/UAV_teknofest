const serverUrl = `wss://${window.location.host}/offer`; // or use `http://` for HTTP without SSL

const peerConnection = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
});

const videoElement = document.createElement('video');
document.body.appendChild(videoElement);
videoElement.autoplay = true;

async function start() {
    // Create an offer
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    // Send the offer to the server
    const response = await fetch(serverUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            sdp: peerConnection.localDescription.sdp,
            type: peerConnection.localDescription.type
        })
    });

    const { sdp, type } = await response.json();
    await peerConnection.setRemoteDescription(new RTCSessionDescription({ sdp, type }));

    // Handle incoming video stream
    peerConnection.ontrack = (event) => {
        if (event.track.kind === 'video') {
            videoElement.srcObject = event.streams[0];
        }
    };
}

start().catch(console.error);