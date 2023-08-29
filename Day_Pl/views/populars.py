import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count, F, Q
from Day_Pl.models import Place, Plan, PlanPlace, UserPlanView
from django.utils import timezone

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

def get_plans(request, seach_keyword):
    base_filter = Q(public = True)

    if seach_keyword != 'none':
        search_query_filter = (
            Q(title__icontains = seach_keyword) |
            Q(hashtag_area__icontains = seach_keyword) |
            Q(hashtag_type__icontains = seach_keyword) |
            Q(hashtag_pick__icontains = seach_keyword)
        )
        base_filter &= search_query_filter

    plans = Plan.objects.filter(base_filter)\
                    .annotate(
                        count = Count('like_users'),
                        nickname = F('user__profile__nickname'),)\
                    .order_by('-count')\
                    .values('title', 'count', 'nickname', 'hashtag_area', 'hashtag_type', 'hashtag_pick', 'uuid')
                    
    plans_list = list(plans)

    return JsonResponse(plans_list, safe=False)

def detail(request, plan_id):
    user = request.user
    plan = Plan.objects.get(uuid=plan_id)
    plan_places = PlanPlace.objects.filter(plan=plan)\
                                    .annotate(
                                        placeid = F('place__id'),
                                        place_name = F('place__name'),)\
                                    .order_by('order')\
                                    .values('placeid', 'place_name', 'expected_time_from_this')

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
        oldest_record = UserPlanView.objects.filter(user=user).order_by('created_at').first()
        oldest_record.delete()