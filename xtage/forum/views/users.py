# -*- coding: utf-8 -*-
from forum.models import User
from forum.models.skill import Skillownership, Skill
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from forum.http_responses import HttpResponseUnauthorized
from django.utils.translation import ugettext as _
from django.utils.http import urlquote_plus
from django.utils.html import strip_tags
from django.utils.encoding import smart_unicode, smart_str
from django.core.urlresolvers import reverse, NoReverseMatch
from forum.forms import *
from forum.utils.html import sanitize_html
from forum.modules import decorate, ReturnImediatelyException
from datetime import datetime, date
from forum.actions import EditProfileAction, FavoriteAction, BonusRepAction, SuspendAction, ReportAction
from forum.modules import ui
from forum.utils import pagination
from forum.views.readers import QuestionListPaginatorContext, AnswerPaginatorContext
from forum.settings import ONLINE_USERS
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from PIL import Image

import os
import json 
import time
import datetime
import decorators
import cgi

class UserReputationSort(pagination.SimpleSort):
    def apply(self, objects):
        return objects.order_by('-is_active', self.order_by)

class UserListPaginatorContext(pagination.PaginatorContext):
    def __init__(self, pagesizes=(20, 40, 60), default_pagesize=40):
        super (UserListPaginatorContext, self).__init__('USERS_LIST', sort_methods=(
            (_('reputation'), UserReputationSort(_('reputation'), '-reputation', _("sorted by reputation"))),
            (_('newest'), pagination.SimpleSort(_('recent'), '-date_joined', _("newest members"))),
            (_('last'), pagination.SimpleSort(_('oldest'), 'date_joined', _("oldest members"))),
            (_('name'), pagination.SimpleSort(_('by username'), 'username', _("sorted by username"))),
        ), pagesizes=pagesizes, default_pagesize=default_pagesize)

class SubscriptionListPaginatorContext(pagination.PaginatorContext):
    def __init__(self):
        super (SubscriptionListPaginatorContext, self).__init__('SUBSCRIPTION_LIST', pagesizes=(5, 10, 20), default_pagesize=20)

class UserSkillListPaginatorContext(pagination.PaginatorContext):
    def __init__(self):
        super (UserSkillListPaginatorContext, self).__init__('USER_SKILL_LIST', sort_methods=(
            (_('hottest'), pagination.SimpleSort(_('hottest'), '-adore_num', )),
        ), pagesizes=(3, 4, 5), default_pagesize=5)

class SkillListPaginatorContext(pagination.PaginatorContext):
    def __init__(self):
        super (SkillListPaginatorContext, self).__init__('SKILL_LIST', sort_methods=(
            (_('name'), pagination.SimpleSort(_('name'), 'skillname', _("sorted alphabetically"))),
            (_('hottest'), pagination.SimpleSort(_('hottest'), '-popularity', _("sorted by popularity"))),
            (_('newest'), pagination.SimpleSort(_('recent update'), '-last_update_at', _("latest created"))),
        ), default_sort=_('hottest'), pagesizes=(30, 60, 120), default_pagesize=20)

class UserAnswersPaginatorContext(pagination.PaginatorContext):
    def __init__(self):
        super (UserAnswersPaginatorContext, self).__init__('USER_ANSWER_LIST', sort_methods=(
            (_('oldest'), pagination.SimpleSort(_('oldest answers'), 'added_at', _("oldest answers will be shown first"))),
            (_('newest'), pagination.SimpleSort(_('newest answers'), '-added_at', _("newest answers will be shown first"))),
            (_('votes'), pagination.SimpleSort(_('popular answers'), '-score', _("most voted answers will be shown first"))),
        ), default_sort=_('votes'), pagesizes=(5, 10, 20), default_pagesize=20, prefix=_('answers'))

USERS_PAGE_SIZE = 35# refactor - move to some constants file

@decorators.render('users/users.html', 'Users', _('Users'), weight=200)
def users(request):
    suser = request.REQUEST.get('q', "")
    users = User.objects.all()
    if suser != "":
        users = User.objects.filter((Q(username__icontains = suser) | Q(first_name__icontains = suser) | Q(last_name__icontains = suser)))

    return pagination.paginated(request, ('users', UserListPaginatorContext()), {
        "users" : users,
        "suser" : suser,
        "users_page" : True,
    })

@decorators.render('skills/skills.html', 'Talent Profile', _('Talent Profile'), weight=200)
def skills(request):
    skill_owners = {}
    sskill = request.REQUEST.get('q', "")
    skills = Skill.objects.all()

    if request.method == "GET":
        sskill = request.GET.get("q", "").strip()

    if sskill:
        skills = skills.filter(skillname__icontains=sskill)

    for skill in skills:
        #print "leo ===> skillname: %r" % skill.skillname
        skill_owners[skill.skillname] = {}
        if User.objects.filter(skill__skillname=skill.skillname).count():
            skill_owners[skill.skillname]["user_order"] = list(User.objects.filter(skill__skillname=skill.skillname).order_by('-skillownership__adore_num'))
            for owner in User.objects.filter(skill__skillname=skill.skillname):
                skill_owners[skill.skillname][owner] = str(Skillownership.objects.get(skill=skill, owner=owner).adores.all().count())
                #print "leo ===> adore_num:", Skillownership.objects.get(skill=skill, owner=owner).adores.all().count()

    return pagination.paginated(request, ('skills', SkillListPaginatorContext()), {
        "skills" : skills,
        "sskill" : sskill,
        "skill_owners": skill_owners,
        "skills_page": True,
    })

@decorators.render('users/online_users.html', 'online_users', _('Online Users'), weight=200, tabbed=False)
def online_users(request):
    suser = request.REQUEST.get('q', "")

    sort = ""
    if request.GET.get("sort", None):
        try:
            sort = int(request.GET["sort"])
        except ValueError:
            logging.error('Found invalid sort "%s", loading %s, refered by %s' % (
                request.GET.get("sort", ''), request.path, request.META.get('HTTP_REFERER', 'UNKNOWN')
            ))
            raise Http404()

    page = 0
    if request.GET.get("page", None):
        try:
            page = int(request.GET["page"])
        except ValueError:
            logging.error('Found invalid page "%s", loading %s, refered by %s' % (
                request.GET.get("page", ''), request.path, request.META.get('HTTP_REFERER', 'UNKNOWN')
            ))
            raise Http404()

    pagesize = 10
    if request.GET.get("pagesize", None):
        try:
            pagesize = int(request.GET["pagesize"])
        except ValueError:
            logging.error('Found invalid pagesize "%s", loading %s, refered by %s' % (
                request.GET.get("pagesize", ''), request.path, request.META.get('HTTP_REFERER', 'UNKNOWN')
            ))
            raise Http404()


    users = None
    if sort == "reputation":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.reputation)
    elif sort == "newest" :
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.newest)
    elif sort == "last":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.last)
    elif sort == "name":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.name)
    elif sort == "oldest":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.oldest)
    elif sort == "newest":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.newest)
    elif sort == "votes":
        users = sorted(ONLINE_USERS.sets.keys(), key=lambda user: user.votes)
    else:
        users = sorted(ONLINE_USERS.iteritems(), key=lambda x: x[1])

    return render_to_response('users/online_users.html', {
        "users" : users,
        "suser" : suser,
        "sort" : sort,
        "page" : page,
        "pageSize" : pagesize,
    })


def edit_user(request, id, slug):
    error = ""
    user = get_object_or_404(User, id=id)
    if not (request.user.is_superuser or request.user == user):
        return HttpResponseUnauthorized(request)
    if request.method == "POST":
        if request.POST.get("for_userpic", None ):
            form = EditUserForm(user)
            f = request.FILES['avatar_file']
            avatar_data = request.POST.get("avatar_data", None)
            if avatar_data:
                # avatar_data is used for cropper and rotate the raw img file
                avatar_data = json.loads(avatar_data)
	        x = avatar_data['x']
	        y = avatar_data['y']
	        height = avatar_data['height']
	        width  = avatar_data['width']
	        rotate = -avatar_data['rotate']
            if not request.user.can_upload_files():
                raise UploadPermissionNotAuthorized()
            if f.size > float(settings.ALLOW_MAX_FILE_SIZE)*1000000.0:
                error = "img file exceed limitation " + settings.ALLOW_MAX_FILE_SIZE + "M"
            try:
                storage = FileSystemStorage(str(settings.UPFACE_FOLDER), str(settings.UPFACE_ALIAS))
                newtime = str(int(time.time()))
                newfilesuff = os.path.splitext(f.name)[1].lower()
                newfilesuff = '.gif'
                newfilename = user.username + "_" + newtime + newfilesuff

		oldfilename = user.img.url
                if user.imgset and storage.exists(oldfilename):
                    storage.delete(oldfilename)
                # newfilename = storage.save(newfilename, f)
                user.img = newfilename

                if avatar_data:
                    img = Image.open(f)
                    box = (x, y, x+width, y + height)
                    img = img.crop(box)
                    if rotate != 0:
                        img = img.rotate(rotate)
                    box = (x, y, x+width, y + height)
                    #img = img.crop(box)

                    imgdir = os.path.join((settings.UPFACE_FOLDER), newfilename)
                    img.save(imgdir, 'gif')
                    f = imgdir

                # for thumbnail
                sizefactor = 1.5

                oldfilename = user.img18.url
                if user.imgset and storage.exists(oldfilename):
                    storage.delete(oldfilename)
                img18name = user.username + "_18_" + newtime + ".gif"
                img18dir = os.path.join(str(settings.UPFACE_FOLDER), img18name)
                img18 = Image.open(f)
                size = 18*sizefactor 
                img18.thumbnail((size, size), Image.ANTIALIAS)
                img18.save(img18dir, "GIF")
                user.img18 = img18name

                oldfilename = user.img24.url
                if user.imgset and storage.exists(oldfilename):
                    storage.delete(oldfilename)
                img24name = user.username + "_24_" + newtime + ".gif"
                img24dir = os.path.join(str(settings.UPFACE_FOLDER), img24name)
                img24 = Image.open(f)
                size = 24*sizefactor
                img24.thumbnail((size, size), Image.ANTIALIAS)
                img24.save(img24dir, "GIF")
                user.img24 = img24name

                oldfilename = user.img32.url
                if user.imgset and storage.exists(oldfilename):
                    storage.delete(oldfilename)  
                img32name = user.username + "_32_" + newtime + ".gif"
                img32dir  = os.path.join(str(settings.UPFACE_FOLDER), img32name)
                img32 = Image.open(f)
                size = 32*sizefactor
                img32.thumbnail((size, size), Image.ANTIALIAS) 
                img32.save(img32dir, 'GIF')
                user.img32 = img32name

                oldfilename = user.img128.url
                if user.imgset and storage.exists(oldfilename):
                    storage.delete(oldfilename)
                img128name = user.username + "_128_" + newtime + ".gif"
                img128dir = os.path.join(str(settings.UPFACE_FOLDER), img128name)
                img128 = Image.open(f) 
                size = 128*sizefactor
                img128.thumbnail((size, size), Image.ANTIALIAS)
                img128.save(img128dir, "GIF")
                user.img128 = img128name

                user.imgset = True
                user.save()
                result = {}
                return_url = settings.UPFACE_ALIAS+'/'+ img128name
                result['result'] = return_url
            except KeyError:
                raise FileTypeNotAllow()
            return HttpResponse(json.dumps(result), content_type='application/json')
          

        else:   
            # update user info
            form = EditUserForm(user, request.POST)
            if form.is_valid():
                new_email = sanitize_html(form.cleaned_data['email'])
    
                if new_email != user.email:
                    user.email = new_email
                    user.email_isvalid = False
    
                    try:
                        hash = ValidationHash.objects.get(user=request.user, type='email')
                        hash.delete()
                    except:
                        pass
    
                if settings.EDITABLE_SCREEN_NAME:
                    user.username = sanitize_html(form.cleaned_data['username'])
                user.real_name = sanitize_html(form.cleaned_data['realname'])
                user.website = sanitize_html(form.cleaned_data['website'])
                user.location = sanitize_html(form.cleaned_data['city'])
                user.date_of_birth = form.cleaned_data['birthday']
                if user.date_of_birth == "None":
                    user.date_of_birth = datetime(1900, 1, 1, 0, 0)
                user.about = sanitize_html(form.cleaned_data['about'])
                # print "Leo debug => ", smart_str(sanitize_html(form.cleaned_data['about']))
                user.save()
                EditProfileAction(user=user, ip=request.META['REMOTE_ADDR']).save()
    
                messages.info(request, _("Profile updated."))
                return HttpResponseRedirect(user.get_profile_url())
    else:
        form = EditUserForm(user)
    return render_to_response('users/edit.html', {
    'user': user,
    'form' : form,
    'gravatar_faq_url' : reverse('faq') + '#gravatar',
    }, context_instance=RequestContext(request))


@decorate.withfn(decorators.command)
def user_powers(request, id, action, status):
    if not request.user.is_superuser:
        raise decorators.CommandException(_("Only superusers are allowed to alter other users permissions."))

    if (action == 'remove' and 'status' == 'super') and not request.user.is_siteowner():
        raise decorators.CommandException(_("Only the site owner can remove the super user status from other user."))

    user = get_object_or_404(User, id=id)
    new_state = action == 'grant'

    if status == 'super':
        user.is_superuser = new_state
    elif status == 'staff':
        user.is_staff = new_state
    else:
        raise Http404()

    user.save()
    return decorators.RefreshPageCommand()


@decorate.withfn(decorators.command)
def award_points(request, id):
    if not request.POST:
        return render_to_response('users/karma_bonus.html')

    if not request.user.is_superuser:
        raise decorators.CommandException(_("Only superusers are allowed to award reputation points"))

    try:
        points = int(request.POST['points'])
    except:
        raise decorators.CommandException(_("Invalid number of points to award."))

    awarding_user = get_object_or_404(User, id=request.user.pk)

    if points > awarding_user.reputation:
        raise decorators.CommandException(_("Invalid number of points to award."))

    user = get_object_or_404(User, id=id)

    extra = dict(message=request.POST.get('message', ''), awarding_user=request.user.id, value=points)

    BonusRepAction(user=request.user, extra=extra).save(data=dict(value=points, affected=user))

    return {'commands': {
            'update_profile_karma': [user.reputation]
        }}
    

@decorate.withfn(decorators.command)
def suspend(request, id):
    user = get_object_or_404(User, id=id)

    if not request.user.is_superuser:
        raise decorators.CommandException(_("Only superusers can suspend other users"))

    if not request.POST.get('bantype', None):
        if user.is_suspended():
            suspension = user.suspension
            suspension.cancel(user=request.user, ip=request.META['REMOTE_ADDR'])
            return decorators.RefreshPageCommand()
        else:
            return render_to_response('users/suspend_user.html')

    data = {
        'bantype': request.POST.get('bantype', 'Indefinitely').strip(),
        'publicmsg': request.POST.get('publicmsg', _('Bad behaviour')),
        'privatemsg': request.POST.get('privatemsg', None) or request.POST.get('publicmsg', ''),
        'suspended': user
    }

    if data['bantype'] == 'forxdays':
        try:
            data['forxdays'] = int(request.POST['forxdays'])
        except:
            raise decorators.CommandException(_('Invalid numeric argument for the number of days.'))

    SuspendAction(user=request.user, ip=request.META['REMOTE_ADDR']).save(data=data)

    return decorators.RefreshPageCommand()

@decorate.withfn(decorators.command)
def report_user(request, id):
    user = get_object_or_404(User, id=id)

    if not request.POST.get('publicmsg', None):
        return render_to_response('users/report_user.html')

    data = {
        'publicmsg': request.POST.get('publicmsg', _('N/A')),
        'reported': user
    }

    ReportAction(user=request.user, ip=request.META['REMOTE_ADDR']).save(data=data)


    return decorators.RefreshPageCommand()



def user_view(template, tab_name, tab_title, tab_description, private=False, tabbed=True, render_to=None, weight=500):
    def decorator(fn):
        def params(request, id=None, slug=None):
            # Get the user object by id if the id parameter has been passed
            if id is not None:
                user = get_object_or_404(User, id=id)
            # ...or by slug if the slug has been given
            elif slug is not None:
                try:
                    user = User.objects.get(username__iexact=slug)
                except User.DoesNotExist:
                    raise Http404

            if private and not (user == request.user or request.user.is_superuser):
                raise ReturnImediatelyException(HttpResponseUnauthorized(request))

            if render_to and (not render_to(user)):
                raise ReturnImediatelyException(HttpResponseRedirect(user.get_profile_url()))

            return [request, user], { 'slug' : slug, }

        decorated = decorate.params.withfn(params)(fn)

        def result(context_or_response, request, user, **kwargs):
            rev_page_title = smart_unicode(user.username) + " - " + tab_description

            # Check whether the return type of the decorated function is a context or Http Response
            if isinstance(context_or_response, HttpResponse):
                response = context_or_response

                # If it is a response -- show it
                return response
            else:
                # ...if it is a context move forward, update it and render it to response
                context = context_or_response

            context.update({
                "tab": "users",
                "active_tab" : tab_name,
                "tab_description" : tab_description,
                "page_title" : rev_page_title,
                "can_view_private": (user == request.user) or request.user.is_superuser
            })
            return render_to_response(template, context, context_instance=RequestContext(request))

        decorated = decorate.result.withfn(result, needs_params=True)(decorated)

        if tabbed:
            def url_getter(vu):
                try:
                    return reverse(fn.__name__, kwargs={'id': vu.id, 'slug': slugify(smart_unicode(vu.username))})
                except NoReverseMatch:
                    try:
                        return reverse(fn.__name__, kwargs={'id': vu.id})
                    except NoReverseMatch:
                        return reverse(fn.__name__, kwargs={'slug': slugify(smart_unicode(vu.username))})

            ui.register(ui.PROFILE_TABS, ui.ProfileTab(
                tab_name, tab_title, tab_description,url_getter, private, render_to, weight
            ))

        return decorated
    return decorator


@user_view('users/stats.html', 'stats', _('overview'), _('user overview'))
def user_profile(request, user, **kwargs):
    involved_group_questions = Question.objects.filter_state(deleted=False).filter(public=False).filter(whitelist__in=[user.id]).order_by('-added_at')
    public_questions = Question.objects.filter_state(deleted=False).filter(author=user).filter(public=True).order_by('-added_at')
    private_questions = Question.objects.filter_state(deleted=False).filter(author=user).filter(public=False).filter(whitelist=None).order_by('-added_at')
    created_group_questions = Question.objects.filter_state(deleted=False).filter(author=user).filter(public=False).exclude(whitelist=None).order_by('-added_at')
    if request.user == user:
        answers = Answer.objects.filter_state(deleted=False).filter(author=user).order_by('-added_at')
    else:
        answers = Answer.objects.filter_state(deleted=False).filter(author=user).filter(public=True).order_by('-added_at')

    # Check whether the passed slug matches the one for the user object
    slug = kwargs['slug']
    if slug != slugify(smart_unicode(user.username)):
        return HttpResponseRedirect(user.get_absolute_url())

    up_votes = user.vote_up_count
    down_votes = user.vote_down_count
    votes_today = user.get_vote_count_today()
    votes_total = user.can_vote_count_today()

    #Leo: get user skillownership object 
    user_skills = Skillownership.objects.filter(owner=user).order_by('-adore_num')
    view_page = "user_profile_page"
    user_tags = Tag.objects.filter(Q(nodes__author=user) | Q(nodes__children__author=user)) \
        .annotate(user_tag_usage_count=Count('name')).order_by('-user_tag_usage_count')

    awards = [(Badge.objects.get(id=b['id']), b['count']) for b in
              Badge.objects.filter(awards__user=user).values('id').annotate(count=Count('cls')).order_by('-count')]

    return pagination.paginated(request, (
    ('group_questions', QuestionListPaginatorContext('USER_GROUP_QUESTION_LIST', _('group_questions'), default_pagesize=15)),
    ('public_questions', QuestionListPaginatorContext('USER_QUESTION_LIST', _('public_questions'), default_pagesize=15)),
    ('private_questions', QuestionListPaginatorContext('USER_PRIVATE_QUESTION_LIST', _('private_questions'), default_pagesize=15)),
    ('answers', UserAnswersPaginatorContext()),
    ('user_skills', UserSkillListPaginatorContext())), {
    "view_user" : user,
    "group_questions" : (involved_group_questions|created_group_questions).distinct(),
    "public_questions" : public_questions,
    "private_questions" : private_questions,
    "answers" : answers,
    "up_votes" : up_votes,
    "down_votes" : down_votes,
    "total_votes": up_votes + down_votes,
    "votes_today_left": votes_total-votes_today,
    "votes_total_per_day": votes_total,
    "user_tags" : user_tags[:50],
    "awards": awards,
    "total_awards" : len(awards),
    "user_skills" : user_skills,
    "view_page" : view_page,
    })
    
@user_view('users/recent.html', 'recent', _('recent activity'), _('recent user activity'))
def user_recent(request, user, **kwargs):
    activities = user.actions.exclude(
            action_type__in=("voteup", "votedown", "voteupcomment", "flag", "newpage", "editpage")).order_by(
            '-action_date')[:USERS_PAGE_SIZE]

    return {"view_user" : user, "activities" : activities}


@user_view('users/reputation.html', 'reputation', _('reputation history'), _('graph of user karma'))
def user_reputation(request, user, **kwargs):
    rep = list(user.reputes.order_by('date'))
    values = [r.value for r in rep]
    redux = lambda x, y: x+y

    graph_data = json.dumps([
    (time.mktime(rep[i].date.timetuple()) * 1000, reduce(redux, values[:i+1], 0))
    for i in range(len(values))
    ])

    rep = user.reputes.filter(action__canceled=False).order_by('-date')[0:20]

    return {"view_user": user, "reputation": rep, "graph_data": graph_data}

@user_view('users/votes.html', 'votes', _('votes'), _('user vote record'), True)
def user_votes(request, user, **kwargs):
    votes = user.votes.exclude(node__state_string__contains="(deleted").filter(
            node__node_type__in=("question", "answer")).order_by('-voted_at')[:USERS_PAGE_SIZE]

    return {"view_user" : user, "votes" : votes}

@user_view('users/questions.html', 'favorites', _('favorites'), _('questions that user selected as his/her favorite'))
def user_favorites(request, user, **kwargs):
    favorites = FavoriteAction.objects.filter(canceled=False, user=user)

    return {"favorites" : favorites, "view_user" : user}

@user_view('users/subscriptions.html', 'subscriptions', _('subscription'), _('subscriptions'), True, tabbed=False)
def user_subscriptions(request, user, **kwargs):
    return _user_subscriptions(request, user, **kwargs)

def _user_subscriptions(request, user, **kwargs):
    enabled = True

    tab = request.GET.get('tab', "settings")

    # Manage tab
    if tab == 'manage':
        manage_open = True

        auto = request.GET.get('auto', 'True')
        if auto == 'True':
            show_auto = True
            subscriptions = QuestionSubscription.objects.filter(user=user).order_by('-last_view')
        else:
            show_auto = False
            subscriptions = QuestionSubscription.objects.filter(user=user, auto_subscription=False).order_by('-last_view')

        return pagination.paginated(request, ('subscriptions', SubscriptionListPaginatorContext()), {
            'subscriptions':subscriptions,
            'view_user':user,
            "auto":show_auto,
            'manage_open':manage_open,
        })
    # Settings Tab and everything else
    else:
        manage_open = False
        if request.method == 'POST':
            manage_open = False
            form = SubscriptionSettingsForm(data=request.POST, instance=user.subscription_settings)

            if form.is_valid():
                form.save()
                message = _('New subscription settings are now saved')

                user.subscription_settings.enable_notifications = enabled
                user.subscription_settings.save()

                messages.info(request, message)
        else:
            form = SubscriptionSettingsForm(instance=user.subscription_settings)

        return {
            'view_user':user,
            'notificatons_on': enabled,
            'form':form,
            'manage_open':manage_open,
        }

@user_view('users/preferences.html', 'preferences', _('preferences'), _('preferences'), True, tabbed=False)
def user_preferences(request, user, **kwargs):
    if request.POST:
        form = UserPreferencesForm(request.POST)

        if form.is_valid():
            user.prop.preferences = form.cleaned_data
            messages.info(request, _('New preferences saved'))

    else:
        preferences = user.prop.preferences

        if preferences:
            form = UserPreferencesForm(initial=preferences)
        else:
            form = UserPreferencesForm()
            
    return {'view_user': user, 'form': form}


def add_skill(request, id):
    user = get_object_or_404(User, id=id)
    if not (request.user.is_superuser or request.user == user):
        return HttpResponseUnauthorized(request)
    if request.method == "POST":
        new_skill = request.POST.get("skill")
        #print "new skill ==>",new_skill,"end"
        new_skill_remove_blank = new_skill.replace(" ",'')
        #print Skillownership.objects.filter(skill__skillname = new_skill_remove_blank.lower())
        #print Skillownership.objects.filter(skill__skillname = new_skill_remove_blank.lower()).filter(owner__id = user.id)
        if Skillownership.objects.filter(skill__skillname = new_skill_remove_blank.lower()).filter(owner__id = user.id):
            #print user.username," already add",new_skill_remove_blank
            messages.info(request, _("You have already added this skill."))
            return HttpResponseRedirect("users/%s/" % id)
        elif new_skill == "":
            messages.info(request, _("Skill can not be empty."))
            return HttpResponseRedirect("users/%s/" % id)
        else:
            try:
                skill = Skill.objects.get(skillname = new_skill.lower())
            except:
                skill = Skill.objects.create(skillname = new_skill.lower())

            m1 = Skillownership.objects.create(skill = skill, owner = user, time= datetime.date.today())
            m1.save()
            skill.popularity += 1
            skill.last_update_at = datetime.datetime.now()
            skill.save()
            msg1 = "You added "
            msg2 = " into your skill list."
            msg = msg1.decode('utf-8')+new_skill+msg2.decode('utf-8')
            #print "add msg->",msg
            messages.info(request, _(cgi.escape(msg)))
    return HttpResponseRedirect("users/%s/" % id)

def remove_skill(request, id):
    user = get_object_or_404(User, id=id)
    # if not (request.user.is_superuser or request.user == user):
    #     return HttpResponseUnauthorized(request)
    if request.method == "POST":
        relationship_2_remove = request.POST.get("skill")
        view_user_id = request.POST.get("view_user_id")
        view_user = get_object_or_404(User, id = view_user_id)
        s1 = Skillownership.objects.get(id = relationship_2_remove)
        s1_name = s1.skill.skillname
        s1.skill.popularity -= 1
        s1.skill.save()
        #print "type==>",type(s1_name)
        #print s1_name
        s1.delete()
        msg1 = "You deleted "
        msg2 = " from skill list."
        msg = msg1.decode('utf-8')+s1_name+msg2.decode('utf-8')
        #print "msg==>",msg
        messages.info(request, _(cgi.escape(msg)))
    return HttpResponseRedirect(view_user.get_profile_url())

def ajax_skill_search(request):
    skill_list = Skill.objects.all()
    skill_name_list = []
    for skill in skill_list:
        skill_name_list.append(skill.skillname)
    return HttpResponse(json.dumps(skill_name_list), content_type='application/json')
														
