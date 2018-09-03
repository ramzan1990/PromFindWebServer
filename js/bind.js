function bind(){
  $('#tButton').on('click', function (e) {
    history.back();
  });

  $('#submitButton').on('click', function (e) {  
    var $btn = $(this).button('loading');
    maxRows = $('#maxRows').val();
    e.preventDefault();
    sendReq();    
  });
}

function displayTable(response) {
    $("#rTable").empty();
    if(response.rows.length > 0){  
    trHTML = '<tr class="asbol"><td><b>Query</b></td><td><b>First digit and explanation</b></td><td><b>Second digit and expanation  </b></td><td><b>Third digit and explanation</b></td></tr>'
    $.each(response.rows, function (i, item) {
      trHTML += '<tr><td>' + item.i1 + '</td><td>' + item.i2 + '</td><td>' + item.i3 + '</td><td>' + item.i4 + '</td></tr>';              
    });
    
    $('#rTable').append(trHTML); 
    $('.table1').show();  
    $('.qhDiv').hide();  
    $('#tButton').show();  
}