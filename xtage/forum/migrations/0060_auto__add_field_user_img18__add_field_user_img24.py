# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.img18'
        db.add_column(u'forum_user', 'img18',
                      self.gf('django.db.models.fields.files.ImageField')(default='upload_userface/noface_18.gif', max_length=100),
                      keep_default=False)

        # Adding field 'User.img24'
        db.add_column(u'forum_user', 'img24',
                      self.gf('django.db.models.fields.files.ImageField')(default='upload_userface/noface_24.gif', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.img18'
        db.delete_column(u'forum_user', 'img18')

        # Deleting field 'User.img24'
        db.delete_column(u'forum_user', 'img24')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.action': {
            'Meta': {'object_name': 'Action'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'canceled_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canceled_actions'", 'null': 'True', 'to': "orm['forum.User']"}),
            'canceled_ip': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'extra': ('forum.models.utils.PickledObjectField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'real_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proxied_actions'", 'null': 'True', 'to': "orm['forum.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['forum.User']"})
        },
        'forum.actionrepute': {
            'Meta': {'object_name': 'ActionRepute'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputes'", 'to': "orm['forum.Action']"}),
            'by_canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputes'", 'to': "orm['forum.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'forum.authkeyuserassociation': {
            'Meta': {'object_name': 'AuthKeyUserAssociation'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auth_keys'", 'to': "orm['forum.User']"})
        },
        'forum.award': {
            'Meta': {'unique_together': "(('user', 'badge', 'node'),)", 'object_name': 'Award'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'award'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            'awarded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'awards'", 'to': "orm['forum.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']", 'null': 'True'}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'awards'", 'null': 'True', 'to': "orm['forum.Action']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.badge': {
            'Meta': {'object_name': 'Badge'},
            'awarded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'awarded_to': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': "orm['forum.Award']", 'to': "orm['forum.User']"}),
            'cls': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'forum.flag': {
            'Meta': {'unique_together': "(('user', 'node'),)", 'object_name': 'Flag'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'flag'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            'flagged_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flags'", 'to': "orm['forum.Node']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flags'", 'to': "orm['forum.User']"})
        },
        'forum.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'value': ('forum.models.utils.PickledObjectField', [], {'null': 'True'})
        },
        'forum.markedtag': {
            'Meta': {'object_name': 'MarkedTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_selections'", 'to': "orm['forum.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_selections'", 'to': "orm['forum.User']"})
        },
        'forum.mysqlftsindex': {
            'Meta': {'object_name': 'MysqlFtsIndex', 'managed': 'False'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ftsindex'", 'unique': 'True', 'to': "orm['forum.Node']"}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'forum.node': {
            'Meta': {'object_name': 'Node'},
            'abs_parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_children'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'active_revision': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'active'", 'unique': 'True', 'null': 'True', 'to': "orm['forum.NodeRevision']"}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['forum.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'extra': ('forum.models.utils.PickledObjectField', [], {'null': 'True'}),
            'extra_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_ref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_activity_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']", 'null': 'True'}),
            'last_edited': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edited_node'", 'unique': 'True', 'null': 'True', 'to': "orm['forum.Action']"}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'node_type': ('django.db.models.fields.CharField', [], {'default': "'node'", 'max_length': '16'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state_string': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nodes'", 'symmetrical': 'False', 'to': "orm['forum.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'whitelist': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access_nodes'", 'symmetrical': 'False', 'to': "orm['forum.User']"})
        },
        'forum.noderevision': {
            'Meta': {'unique_together': "(('node', 'revision'),)", 'object_name': 'NodeRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'noderevisions'", 'to': "orm['forum.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['forum.Node']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'revised_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'revision': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'whitelist': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access_noderevisions'", 'symmetrical': 'False', 'to': "orm['forum.User']"})
        },
        'forum.nodestate': {
            'Meta': {'unique_together': "(('node', 'state_type'),)", 'object_name': 'NodeState'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'node_state'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': "orm['forum.Node']"}),
            'state_type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'forum.questionsubscription': {
            'Meta': {'object_name': 'QuestionSubscription'},
            'auto_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 30, 0, 0)'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['forum.User']", 'symmetrical': 'False', 'through': "orm['forum.Skillownership']", 'blank': 'True'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skillname': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.skillownership': {
            'Meta': {'unique_together': "(('skill', 'owner'),)", 'object_name': 'Skillownership'},
            'adore_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'adores': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'skilladorers'", 'blank': 'True', 'to': "orm['forum.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Skill']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'forum.subscriptionsettings': {
            'Meta': {'object_name': 'SubscriptionSettings'},
            'all_questions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_questions_watched_tags': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_joins': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'new_question': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'new_question_watched_tags': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1'}),
            'notify_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_answers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_comments_own_post': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_reply_to_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'questions_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_digest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subscribed_questions': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subscription_settings'", 'unique': 'True', 'to': "orm['forum.User']"})
        },
        'forum.tag': {
            'Meta': {'ordering': "('-used_count', 'name')", 'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tags'", 'to': "orm['forum.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'marked_tags'", 'symmetrical': 'False', 'through': "orm['forum.MarkedTag']", 'to': "orm['forum.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'used_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'forum.user': {
            'Meta': {'object_name': 'User', '_ormbases': [u'auth.User']},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bronze': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email_isvalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'default': "'upload_userface/noface.gif'", 'max_length': '100'}),
            'img128': ('django.db.models.fields.files.ImageField', [], {'default': "'upload_userface/noface_128.gif'", 'max_length': '100'}),
            'img18': ('django.db.models.fields.files.ImageField', [], {'default': "'upload_userface/noface_18.gif'", 'max_length': '100'}),
            'img24': ('django.db.models.fields.files.ImageField', [], {'default': "'upload_userface/noface_24.gif'", 'max_length': '100'}),
            'img32': ('django.db.models.fields.files.ImageField', [], {'default': "'upload_userface/noface_32.gif'", 'max_length': '100'}),
            'imgset': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'silver': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribers'", 'symmetrical': 'False', 'through': "orm['forum.QuestionSubscription']", 'to': "orm['forum.Node']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'forum.userproperty': {
            'Meta': {'unique_together': "(('user', 'key'),)", 'object_name': 'UserProperty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': "orm['forum.User']"}),
            'value': ('forum.models.utils.PickledObjectField', [], {'null': 'True'})
        },
        'forum.validationhash': {
            'Meta': {'unique_together': "(('user', 'type'),)", 'object_name': 'ValidationHash'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 31, 0, 0)'}),
            'hash_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.vote': {
            'Meta': {'unique_together': "(('user', 'node'),)", 'object_name': 'Vote'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'vote'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['forum.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['forum.User']"}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['forum']