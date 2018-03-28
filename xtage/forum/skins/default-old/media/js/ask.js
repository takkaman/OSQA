$(document).ready(function() {
  var tagsInput = $('input#id_tags');
  var tagsLinks = $('[class^=tag-link]');
  var tagsLinksTexts = {};
  var invites = $('input#id_invites');

  $(tagsLinks).each(function() {
    tagsLinksTexts[$(this).text()] = this;
  });

  var updateTags = function() {
    var tags = $(tagsInput).val().split(/\s+/);
    $(tagsLinks).show();
    for (var i = 0; i < tags.length; ++i) {
      if (tags[i] == "") continue;
      if ($.inArray(tags[i], tagsLinksTexts.keys)) {
        $(tagsLinksTexts[tags[i]]).hide();
      }
    }
  };

  var hash = window.location.hash.substring(1);
  var url_parts = hash.replace(/\/\s*$/,'').split('/');
  if (url_parts.length > 2 && url_parts[1]=='tags') {
    var predefTags = url_parts.slice(2)
    tagsInput.val(tagsInput.val() + ' ' + predefTags.join(' '));
    updateTags();
  }
  if (url_parts.length > 2 && url_parts[1]=='tags' && url_parts[2]=='Innoday_2016') {
    $('div#main-bar').html("<h2>Your Idea <img src=\"http://xtage/upfiles/innoday-tiny.jpg\" alt=\"Post your idea\" vertical-align=\"middle\"></h2>");//.attr({'text-align':'center'});
  }

  if (url_parts.length > 2 && url_parts[1]=='tags' && url_parts[2]=='inno_panel_discuss') {
    invites.val(invites.val() + 'helenbao yhu wygu jjliu jinxu');
  }

  tagsLinks.each(function() {
    var tagValue = $(this).text();
    this.onclick = function() {
      tagsInput.val(tagsInput.val() + ' ' + tagValue);
      updateTags();
    };
  });

  tagsInput.on('keyup change', function() {
      updateTags();
  });
});
