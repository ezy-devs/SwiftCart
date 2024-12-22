function msgModal() {
    const modal = document.getElementById('msg-modal');
    modal.style.display = 'none';
    modal.style.transition = 'opacity 5s';
    modal.style.opacity = '0';
}

setInterval(msgModal, 5000);