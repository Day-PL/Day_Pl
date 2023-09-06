import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q, OuterRef, Subquery
from Day_Pl.models import Place, Plan, PlanPlace, UserPlanView
from django.utils import timezone

@login_required
def index(request):
    if request.method == 'PUT':
        user = request.user
        data = json.loads(request.body)
        
        target_id = ''
        target_table = ''

        if 'placeid' in data:
            target_id = data['placeid']
            target_table = Place

        elif 'planid' in data:
            target_id = data['planid']
            target_table = Plan

        target_obj = target_table.objects.get(pk=target_id)

        if target_obj.like_users.filter(pk=user.pk).exists():
            target_obj.like_users.remove(user)
            response = {
                'isliked': False,
            }
        else:
            target_obj.like_users.add(user)
            response = {
                'isliked': True,
            }

        return JsonResponse(response)
        
    return render(request, 'populars.html')

@login_required
def share_detail(request, plan_id):
    if request.method == 'PUT':
        user = request.user
        data = json.loads(request.body)
        
        target_id = ''
        target_table = ''

        if 'placeid' in data:
            target_id = data['placeid']
            target_table = Place

        elif 'planid' in data:
            target_id = data['planid']
            target_table = Plan

        target_obj = target_table.objects.get(pk=target_id)

        if target_obj.like_users.filter(pk=user.pk).exists():
            target_obj.like_users.remove(user)
            response = {
                'isliked': False,
            }
        else:
            target_obj.like_users.add(user)
            response = {
                'isliked': True,
            }

        return JsonResponse(response)
        
    return render(request, 'populars_detail.html', context = { 'plan_id': plan_id })

def get_plans(request, search_keyword):
    base_filter = Q(public = True)

    if search_keyword != 'none':
        search_query_filter = (
            Q(title__icontains = search_keyword) |
            Q(hashtag_area__icontains = search_keyword) |
            Q(hashtag_type__icontains = search_keyword) |
            Q(hashtag_pick__icontains = search_keyword) |
            Q(planplace__place__name__icontains = search_keyword) 
        )
        base_filter &= search_query_filter

    subquery = Plan.objects.filter(id=OuterRef('id'))\
                        .annotate(plan_like_users = Count('like_users'))\
                        .values('plan_like_users')[:1]
    
    plans = Plan.objects.filter(base_filter)\
                    .annotate(
                        # count = Count('like_users'),
                        count = Subquery(subquery),
                        nickname = F('user__profile__nickname'),)\
                    .order_by('-count')\
                    .values('id', 'title', 'count', 'nickname', 'hashtag_area', 'hashtag_type', 'hashtag_pick', 'uuid')\
                    .distinct()

    plans_list = list(plans)

    return JsonResponse(plans_list, safe=False)

def detail(request, plan_id):
    user = request.user
    plan = Plan.objects.get(uuid=plan_id)
    plan_places = PlanPlace.objects.filter(plan=plan)\
                                    .annotate(
                                        placeid = F('place__id'),
                                        place_name = F('place__name'),
                                        lat = F('place__lat'),
                                        lng = F('place__lng'),)\
                                    .order_by('order')\
                                    .values('placeid', 'place_name', 'expected_time_from_this', 'lat', 'lng', 'road_url')

    plan_places_list = list(plan_places)

    response = {
        'plan' : {
            'id' : plan.pk,
            'uuid' : plan.uuid,
            'name' : plan.title,
            'user' : plan.user.profile.nickname,
        },
        'plan_places' : plan_places_list,
    }

    control_user_plan_view(user, plan)

    return JsonResponse(response)

def control_user_plan_view(user, plan):
    user_plan_view, created = UserPlanView.objects.get_or_create(user=user, plan=plan)

    if not created:
        user_plan_view.view_at = timezone.now()
        user_plan_view.save()

    user_view_count = UserPlanView.objects.filter(user=user).count()
    if user_view_count > 50:
        oldest_record = UserPlanView.objects.filter(user=user).order_by('view_at').first()
        oldest_record.delete()