// place any jQuery/helper plugins in here, instead of separate, slower script files.
function start_update_main() {
  var status_url = $(this).data('status_url');

  // create a progress bar
  var dots = 1;
  var progressTitle = document.getElementById('progress-title');
  updateProgressTitle(status_url, dots, progressTitle);

}

function updateProgressTitle(status_url, dots, progressTitle) {
  dots++;
  if (dots > 3) {
    dots = 1;
  }
  progressTitle.innerHTML = 'processing images ';
  for (var i = 0; i < dots; i++) {
    progressTitle.innerHTML += '.';
  }
  // send GET request to status URL
  $.getJSON(status_url, function(data) {
      // update UI
      if (data['task_status'] != 'PENDING' && data['task_status'] != 'PROGRESS') {
          if ('results' in data) {
              // show result
              var url = window.location.protocol + '//' + window.location.host + data['results']['archive_path'];
              var a = document.createElement("a");
              a.target = '_BLANK';
              document.body.appendChild(a);
              a.style = "display: none";
              a.href = url;
              a.download = 'results.zip';
              a.click();
              document.body.removeChild(a);
          }
          else {
              // something unexpected happened
              progressTitle.innerHTML = 'An error occured';
          }
      }
      else {
          // rerun in 2 seconds
          setTimeout(function() {
              update_progress(status_url, dots, progressTitle);
          }, 2000);
      }
  });
}

$(function() {
  $('#start-progress-check').click(start_update_main);
});