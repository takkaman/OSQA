var currentSideBar = 'div#title_side_bar';
function changeSideBar(enabled_bar) {
    if (enabled_bar != currentSideBar) {
        $(currentSideBar).hide();
        currentSideBar = enabled_bar;
        $(currentSideBar).fadeIn('slow');
    }

}

$(function () {
    $('div#editor_side_bar').hide();
    $('div#tags_side_bar').hide();

    $('#id_title').focus(function(){changeSideBar('div#title_side_bar')});
    $('#editor').focus(function(){changeSideBar('div#editor_side_bar')});
    $('#id_tags').focus(function(){changeSideBar('div#tags_side_bar')});
});


$(function () {

    var past_num_words = 0;
    var results_cache = {};
    var $input = $('#id_title');

    tinymce.init({
        selector: "textarea",
        toolbar: "undo redo bold italic left right strikethrough link unlink numlist bullist blockquote fullscreen preview image imageupload ",
        width: 740,     
        height: 400,
        plugins: [
            "advlist autolink lists link  charmap print preview anchor",
            "searchreplace visualblocks code fullscreen",
            "insertdatetime media table contextmenu paste imageupload",
        ],
        relative_urls: false,
        imageupload_url: '/upload/',

        init_instance_callback: function (editor) {
            editor.on('keyup', check_update_recommends);
            editor.on('Change', check_update_recommends);
            editor.on('focus', reload_recommends);
            editor.on('blur', reload_recommends);
        }
    });

    function reload_recommends(e) {
        var relatedUsersDiv = $('#related-skills-users');
        var user_template = $('#user-template').html();
        var recmd_user_template = $('#recmd-user-template').html();
        var body = tinyMCE.activeEditor.getContent();
        var title = $input.val();
        var q = title + ' ' + body;

        if (results_cache[q] && results_cache[q] != '') {
            relatedUsersDiv.html(results_cache[q]);
            return false;
        }

        $.post(related_users_url, {content:q}, function(data) {
            if (data) {
                // var c = $input.val() + ' ' + real_editor.value
                // if (c != q) {
                //     return;
                // }

                if(data.length == 0) {
                    relatedUsersDiv.html('<div align="center">No related experts on this have been found.</div>');
                    return;
                }

                var html = '';
                for (var skill in data) {
                    var users = '';
                    for (var i = 0; i < (data[skill]).length; i++) {
                        var item = user_template.replace(new RegExp('%USERID%', 'g'), data[skill][i].username)
                                       .replace(new RegExp('%DECORATED_NAME%', 'g'), data[skill][i].decorated_name)
                                       .replace(new RegExp('%SCORE%', 'g'), data[skill][i].score)
                                       .replace(new RegExp('%PROFILE%', 'g'), escape(data[skill][i].profile_url))
                                       .replace(new RegExp('%IMG%', 'g'), escape(data[skill][i].img))
                                       .replace(new RegExp('%BADGE%', 'g'), escape(data[skill][i].badge));
                        users += item;
                    }
                    var line = recmd_user_template.replace(new RegExp('%SKILL%', 'g'), skill)
                                                  .replace(new RegExp('%USERS%', 'g'), users);
                    html += line;
                }
                results_cache[q] = html;
                relatedUsersDiv.html(html);
            } else {
                relatedUsersDiv.html('<div align="center">No related experts on this have been found.</div>');
            }

        }, 'json');

        return false;
    }

    function check_update_recommends(e) {
        var body = tinyMCE.activeEditor.getContent();
        var title = $input.val();
        var q = title + ' ' + body;
        num_words = q.split(/[^\w-_]+/).length;
        if (num_words !== past_num_words) {
            past_num_words = num_words;
            reload_recommends();
        }
    };

    $input.keyup(check_update_recommends);
    $input.focus(reload_recommends);
});


$(function() {
    var $input = $('#id_title');
    var $box = $('#ask-related-questions');
    var template = $('#question-summary-template').html();
    var $editor = $('#editor');

    var results_cache = {};

    function reload_suggestions_box(e) {
        var relatedQuestionsDiv = $('#ask-related-questions');
        var q = $input.val().replace(/^\s+|\s+$/g,"");

        if(q.length == 0) {
            close_suggestions_box();
            relatedQuestionsDiv.html('');
            return false;
        } else if(relatedQuestionsDiv[0].style.height == 0 || relatedQuestionsDiv[0].style.height == '0px') {
            relatedQuestionsDiv.animate({'height':'150'}, 350);
        }

        if (results_cache[q] && results_cache[q] != '') {
            relatedQuestionsDiv.html(results_cache[q]);
            return false;
        }

        $.post(related_questions_url, {title: q}, function(data) {
            if (data) {
                var c = $input.val().replace(/^\s+|\s+$/g,"");

                if (c != q) {
                    return;
                }

                if(data.length == 0) {
                    relatedQuestionsDiv.html('<br /><br /><div align="center">No questions like this have been found.</div>');
                    return;
                }

                var html = '';
                for (var i = 0; i < data.length; i++) {
                    var item = template.replace(new RegExp('%URL%', 'g'), data[i].url)
                                       .replace(new RegExp('%SCORE%', 'g'), data[i].score)
                                       .replace(new RegExp('%TITLE%', 'g'), data[i].title)
                                       .replace(new RegExp('%SUMMARY%', 'g'), data[i].summary);

                    html += item;

                }

                results_cache[q] = html;

                relatedQuestionsDiv.html(html);
            }
        }, 'json');

        return false;
    }

    function close_suggestions_box() {
        $('#ask-related-questions').animate({'height':'0'},350, function() {
            $('#ask-related-questions').html('');
        });
    }

    $input.keyup(reload_suggestions_box);
    $input.focus(reload_suggestions_box);

    $editor.change(function() {
        if ($editor.html().length > 10) {
            close_suggestions_box();
        }
    });

    // for chrome
    $input.keydown(focus_on_question);
    function focus_on_question(e) {
        var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;

        if(e.keyCode == 9 && is_chrome) {
            $('#editor')[0].focus();
        }
    }
});


