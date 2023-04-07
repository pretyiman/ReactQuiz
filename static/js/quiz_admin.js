$(document).ready(function() {
  // Get references to the subject and topic dropdown lists.
  var subjectSelect = $('#id_subject');
  var topicSelect = $('#id_topics');

  // When the page is loaded, filter the topics based on the selected subjects.
  filterTopics();

  // When the user selects a subject, update the available topics and questions.
  subjectSelect.change(function() {
    filterTopics();
    filterQuestions();
  });

  // When the user selects a topic, update the available questions.
  topicSelect.change(function() {
    filterQuestions();
  });

  // Helper function to get the selected subject IDs.
  function getSelectedSubjects() {
    var selectedSubjects = [];
    subjectSelect.find('option:selected').each(function() {
      selectedSubjects.push($(this).val());
    });
    return selectedSubjects;
  }

  // Helper function to get the selected topic IDs.
  function getSelectedTopics() {
    var selectedTopics = [];
    topicSelect.find('option:selected').each(function() {
      selectedTopics.push($(this).val());
    });
    return selectedTopics;
  }

  // Helper function to filter the available topics based on the selected subjects.
  function filterTopics() {
    var selectedSubjects = getSelectedSubjects();
    if (selectedSubjects.length > 0) {
      $.ajax({
        url: '/admin/filter-topics/',
        data: {subjects: selectedSubjects},
        success: function(data) {
          // Replace the existing topic options with the filtered options.
          topicSelect.empty().append(data);
          // Update the available questions based on the selected topics.
          filterQuestions();
        }
      });
    } else {
      // If no subjects are selected, show all available topics.
      $.ajax({
        url: '/admin/get-all-topics/',
        success: function(data) {
          // Replace the existing topic options with all available options.
          topicSelect.empty().append(data);
          // Update the available questions based on the selected topics.
          filterQuestions();
        }
      });
    }
  }

  // Helper function to filter the available questions based on the selected topics.
  function filterQuestions() {
    var selectedTopics = getSelectedTopics();
    if (selectedTopics.length > 0) {
      $.ajax({
        url: '/admin/filter-questions/',
        data: {topics: selectedTopics},
        success: function(data) {
          // Replace the existing question options with the filtered options.
          $('#id_questions').empty().append(data);
        }
      });
    } else {
      // If no topics are selected, show all available questions.
      $.ajax({
        url: '/admin/get-all-questions/',
        success: function(data) {
          // Replace the existing question options with all available options.
          $('#id_questions').empty().append(data);
        }
      });
    }
  }
});
