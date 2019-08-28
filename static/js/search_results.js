function sendAlert(alertMsg) {
  alert('Your selections have been added to your Destination List!');
}

function handleOrderSubmit(evt) {
  evt.preventDefault();

  const userId = $(evt.target).data('userId');

  const dlist = [];
  $.each($(':checkbox[name=destination]:checked'), function(){
    dlist.push($(this).val());
  });
  
  const formInputs = {
    'destination': dlist
  };
  
  $.post(`/${userId}/map`, formInputs, sendAlert);
}

$('#destinations').on('submit', handleOrderSubmit);