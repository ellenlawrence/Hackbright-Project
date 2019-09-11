console.log('hi');

function updateProfPic(evt) {
    $('#prof-modal').css('display', 'flex')
}

$('#hover-text-container').on('click', updateProfPic);

function closeModal(evt) {
    $('#prof-modal').css('display', 'none')
}

$('#prof-modal').on('click', closeModal);

$('#modal-content').on('click', (evt) => {
    evt.stopPropagation();
});

