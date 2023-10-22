from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta, time, datetime
from .forms import *
from .models import *

def home(request):
    current_time="11:00:00"
    target_time = TimeSlot.objects.get(start_time=current_time)
    statuss = Status.objects.filter(time_slot=target_time)

    # get plans that are relevant
    plan_objs = Plan.objects.all()
    plans = {}
    for plan in plan_objs:
        if str(plan.start_time) > current_time:
            plans[plan] = []

            for person in plan.person_set.all():
                plans[plan].append(person.name)

    context = {
        "statuss" : statuss,
        "plans" : plans
    }
    print(plans)
    print(context)
    return render(request, "home.html", context)

def create_plan(request):
    if request.method == 'POST':
        form = PlanCreateForm(request.POST)
        if form.is_valid():
            # Create a TimeSlot object from start and end times
            s_time = form.cleaned_data['start_time']
            e_time = form.cleaned_data['end_time']

            # Create the Plan object
            plan = Plan(
                start_time=s_time,
                end_time=e_time,
                location=form.cleaned_data['location']
            )
            plan.save()
            
            # for each person in the plan, update their status for the corresponding times to 'p'
            for person in form.cleaned_data['people']:
                person.plans.add(plan)
                overlapping_statuses = Status.objects.filter(
                    person=person,
                    time_slot__start_time__gte=s_time,
                    time_slot__end_time__lte=e_time
                )
    
                # Update the statuses of the overlapping Status objects to 'p'
                overlapping_statuses.update(status='p')

                eaten_statuses = Status.objects.filter(
                        person=person,
                        time_slot__end_time__gte=e_time,
                        time_slot__start_time__lte=datetime.strptime(str(e_time), '%H:%M:%S') + timedelta(hours=3)
                    )
                # Update the statuses of the eaten Status objects to 'e'
                eaten_statuses.update(status='e')
                for e in eaten_statuses:
                    e.save()
                
                person.save()
                for s in overlapping_statuses:
                    s.save()
            return redirect('/')
    else:
        form = PlanCreateForm()

    context = {
        "form" : form
    }
    return render(request, 'plans.html', context)

def profile(request, name):
    num_time_slots = TimeSlot.objects.all().count()
    sorted_times = TimeSlot.objects.all().order_by('start_time')
    start_time = sorted_times[0].start_time.hour
    half = sorted_times[0].start_time.minute != 0
    target_person = Person.objects.get(name=name)
    statuss = Status.objects.filter(person=target_person)
    initial_data = {}
    for obj in statuss:
        if obj.status == 'f':
            initial_data[str(obj.time_slot.start_time)[:-3]] = True
        else:
            initial_data[str(obj.time_slot.start_time)[:-3]] = False
    form = ProfileCreateForm(num_time_slots=num_time_slots, start_time=start_time, half=half, initial=initial_data)

    if request.method=='POST':
        form = ProfileCreateForm(request.POST, num_time_slots=num_time_slots, start_time=start_time, half=half, initial=initial_data)
        if form.is_valid():
            for time in form.cleaned_data.keys():
                if form.cleaned_data[time] != initial_data[time]:
                    if form.cleaned_data[time]:
                        new_status = 'f'
                    else:
                        new_status = 'b'
                    target_time_slot = TimeSlot.objects.get(start_time=f'{time}:00')
                    obj = statuss.get(time_slot=target_time_slot)
                    obj.status = new_status
                    obj.save()
    context = {
        "person" : target_person,
        "form" : form
    }
    return render(request, 'profile.html', context)