
$(document).ready(function() {
$('#id_subject').change(function() {
  var subjectId = $(this).val();
  $.ajax({
    url: '{% url 'get_topics' %}',
    data: {
      'subject_id': subjectId
    },
    dataType: 'json',
    success: function(data) {
      $('#id_topic').empty();
      $('#id_topic').append($('<option>').text('---------').attr('value', ''));
      $.each(data, function(i, item) {
        $('#id_topic').append($('<option>').text(item.topic).attr('value', item.id));
      });
    }
  });
});
});