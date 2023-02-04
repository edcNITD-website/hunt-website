from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from game.models import *
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
import json
import uuid
# Create your views here.

def get_gamers_list()->list:
    gamers_list = []
    for gamer in Gamer.objects.all():
        gamers_list.append(gamer.user)
    return gamers_list

def get_clubmember_list()->list:
    member_list = []
    for member in ClubMember.objects.all():
        member_list.append(member.user)
    return member_list

def get_successfull_scans(request):
    gamer = Gamer.objects.get(user=request.user)
    scans_list = SuccessfullScan.objects.all().filter(gamer=gamer)
    return scans_list

def prepare_context(request):
    context = {}
    is_game_user = request.user in get_gamers_list()
    is_club_member = request.user in get_clubmember_list()
    context['is_game_user'] = is_game_user
    context['is_club_member'] = is_club_member
    return context

def get_total_points(gamer):
    scans_list = SuccessfullScan.objects.all().filter(gamer=gamer)
    qr_points = 0
    for scan in scans_list:
        qr_points+=scan.points_given
    total_points = gamer.points + qr_points
    print(gamer.points,qr_points)
    return total_points

def get_key(gamer):
    print(gamer['get_total_points'])
    return int(gamer['get_total_points'])

def order_by_points():
    gamers = Gamer.objects.all().order_by('-points','user__first_name')
    # print(gamers)
    gamers_list = []
    for gamer in gamers:
        if gamer.user in get_clubmember_list():
            # user is a club member
            continue
        new_gamer = {}
        social_account = SocialAccount.objects.get(user=gamer.user)
        new_gamer['profile_img'] = social_account.extra_data.get('picture')
        new_gamer['user'] = gamer.user
        new_gamer['phone'] = gamer.phone
        new_gamer['college'] = gamer.college
        new_gamer['referral_code'] = gamer.referral_code
        new_gamer['points'] = gamer.points
        new_gamer['get_total_points'] = gamer.get_total_points
        new_gamer['share_code'] = gamer.share_code
        gamers_list.append(new_gamer)
    print(gamers_list)
    gamers_list.sort(key=get_key,reverse=True)
    print(gamers_list)
    return gamers_list

def get_rank(request):
    gamers = order_by_points()
    rank = 1
    for gamer in gamers:
        if gamer['user'] == request.user:
            break;
        rank = rank + 1
    return rank

def leaderboard(request):
    context = {}
    context = prepare_context(request)
    ordered = order_by_points()
    # for gamer in ordered:
    #     print(gamer.get('user__first_name'),gamer.get('points'))
    context['gamers'] = ordered
    return render(request,'game/leaderboard.html',context)

@login_required
def profile(request):
    # check if user has a gameUser account or a moderator account
    context = {}
    context = prepare_context(request)
    # print(context)
    if not context['is_game_user']:
        # tell to register as a game user and then start playing
        messages.info(request,"Please register as a gamer before starting to play")
        return redirect('/game/register')
    else:
        context['gamer'] = Gamer.objects.get(user=request.user)
        social_account = SocialAccount.objects.get(user=request.user)
        gamers = Gamer.objects.all().order_by('points','user__first_name')
        context['profile_img'] = social_account.extra_data.get('picture')
        context['gamers_count'] = len(order_by_points())
        context['rank'] = get_rank(request)
        context['scans'] = get_successfull_scans(request)
        # print(Gamer.objects.get(user=request.user).user)
    return render(request,'game/profile.html',context)

@login_required
def register(request):
    context = {}
    if request.method == 'POST':
        if 'save-btn' in request.POST:
            # got some data in POST, create the gamer, save and redirect to profile page with a message
            new_gamer = Gamer()
            new_gamer.user = request.user
            new_gamer.college = request.POST.get('college')
            new_gamer.phone = request.POST.get('phone')
            # print("college: "+ new_gamer.college)
            # if ref code in valid ref code points+ 10 for both parties
            # check if ref-code is not empty
            if request.POST.get('ref-code')!='':
                # we got a referral code, lets check if its valid
                share_code = request.POST.get('ref-code')
                share_code = str(share_code).upper()
                gamers = Gamer.objects.all().filter(share_code =share_code)
                if gamers.count() == 0:
                    messages.info(request,"The share code you enterred is not correct, please enter correctly or try register without the share code.")
                    return redirect('/game/register')
                else:
                    share_gamer = gamers.first()
                    share_gamer.points += 10
                    share_gamer.save()
                    new_gamer.points = 10
                    messages.info(request,"The share code you enterred is correct")
            # print('ref-code:',request.POST.get('ref-code')=='')
            new_gamer.save()
            messages.success(request,'You have completed registration now you can start playing and get prizes!')
            return redirect('/game/profile')
    return render(request,'game/register.html',context)

@login_required
def scanner(request):
    context = {}
    context = prepare_context(request)
    if request.method == 'POST':
        qr_code = request.POST.get('qr-code')
        if qr_code:
            try:
                qr_scan = QRScan.objects.get(code = qr_code)
            except QRScan.DoesNotExist:
                qr_scan = None
            if qr_scan is not None:
                # check if user is club member if yes text if scan exists and reply saying so
                if context['is_club_member']:
                    messages.success(request,"QR works, you can learn more about the qr in manage QR panel.")
                    return redirect('/game/profile')
                # check if user has scanned it once already if yes show message and dont allow more scans
                successfull_scans = get_successfull_scans(request)
                for s_scan in successfull_scans:
                    if s_scan.qr_code_id == qr_scan.id:
                        # trying to scan again
                        messages.info(request,'You have already scanned this QR.')
                        return redirect('/game/profile')
                if qr_scan.count == 0:
                    # scanned for the first time give max points and save
                    successfull_scan = SuccessfullScan()
                    successfull_scan.gamer = Gamer.objects.get(user=request.user)
                    successfull_scan.qr_code_id = qr_scan.id
                    successfull_scan.points_given = qr_scan.points_max
                    successfull_scan.save()
                    qr_scan.count = qr_scan.count + 1
                    qr_scan.save()
                    messages.success(request,"Congrats you succesfully scanned the QR. The QR was scanned for the first time, so you get "+str(successfull_scan.points_given) +" points!")
                    return redirect('/game/profile')
                elif qr_scan.count < 5:
                    # scanned for the first  5time give mid points and save
                    successfull_scan = SuccessfullScan()
                    successfull_scan.gamer = Gamer.objects.get(user=request.user)
                    successfull_scan.qr_code_id = qr_scan.id
                    successfull_scan.points_given = qr_scan.points_mid
                    successfull_scan.save()
                    qr_scan.count = qr_scan.count + 1
                    qr_scan.save()
                    messages.success(request,"Congrats you succesfully scanned the QR. The QR was scanned for the "+str(qr_scan.count)+" time(s), so you get "+str(successfull_scan.points_given) +" points!")
                    return redirect('/game/profile')
                else:
                    # scan is now common give min points and save
                    successfull_scan = SuccessfullScan()
                    successfull_scan.gamer = Gamer.objects.get(user=request.user)
                    successfull_scan.qr_code_id = qr_scan.id
                    successfull_scan.points_given = qr_scan.points_min
                    successfull_scan.save()
                    qr_scan.count = qr_scan.count + 1
                    qr_scan.save()
                    messages.success(request,"Congrats you succesfully scanned the QR. The QR was scanned for the "+str(qr_scan.count)+" time(s), so you get "+str(successfull_scan.points_given) +" points!")
                    return redirect('/game/profile')
    return render(request,'game/scanner.html',context)

@login_required
def manage_qr(request):
    context = {}
    context = prepare_context(request)
    if not context['is_club_member']:
        # tell to register as a game user and then start playing
        messages.info(request,"Restricted to club members only.")
        return redirect('/game/profile')
    else:
        context['gamer'] = Gamer.objects.get(user=request.user)
        social_account = SocialAccount.objects.get(user=request.user)
        context['profile_img'] = social_account.extra_data.get('picture')
        context['qr_scans'] = QRScan.objects.all()
        # print(context)
        # print(Gamer.objects.get(user=request.user).user)
    return render(request,'game/manage_qr.html',context)

@login_required
def add_qr(request):
    context = {}
    context = prepare_context(request)
    if not context['is_club_member']:
        # tell to register as a game user and then start playing
        messages.info(request,"Restricted to club members only.")
        return redirect('/game/profile')
    else:
        if request.method == 'POST':
            if 'save-btn' in request.POST:
                location = request.POST.get('location')
                qr_scan = QRScan()
                qr_scan.location = location
                qr_scan.sponsor = request.POST.get('sponsor')
                qr_scan.code = 'QR_'+uuid.uuid4().hex[:9].upper()
                qr_scan.save()
                messages.success(request,"Succesfully added QR,Sponsored by "+qr_scan.sponsor+" QR_VAL="+str(qr_scan.code))
                return redirect('/game/manage_qr')
        # print(Gamer.objects.get(user=request.user).user)
    return render(request,'game/add_qr.html',context)

def detail_qr(request, qr_id):
    context = {}
    context = prepare_context(request)
    if not context['is_club_member']:
        # tell to register as a game user and then start playing
        messages.info(request,"Restricted to club members only.")
        return redirect('/game/profile')
    else:
        qr_scan = QRScan.objects.get(id=qr_id)
        context['scan'] = qr_scan
    return render(request,'game/qr_detail.html',context)

@login_required
def delete_qr(request, qr_id):
    context = {}
    context = prepare_context(request)
    if not context['is_club_member']:
        # tell to register as a game user and then start playing
        messages.info(request,"Restricted to club members only.")
        return redirect('/game/profile')
    else:
        qr_scan = QRScan.objects.get(id=qr_id)
        code = qr_scan.code
        qr_scan.delete()
        messages.success(request,"Succesfully deleted QR, QR_VAL="+str(code))
        return redirect('/game/manage_qr')

def edit_qr(request, qr_id):
    context = {}
    context = prepare_context(request)
    if not context['is_club_member']:
        # tell to register as a game user and then start playing
        messages.info(request,"Restricted to club members only.")
        return redirect('/game/profile')
    else:
        qr_scan = QRScan.objects.get(id=qr_id)
        context['scan'] = qr_scan
        if request.method == 'POST':
            if 'save-btn' in request.POST:
                qr_scan.location = request.POST.get('location')
                qr_scan.sponsor = request.POST.get('sponsor')
                qr_scan.save()
                messages.success(request,"Succesfully edited QR, QR_VAL="+str(qr_scan.code))
                return redirect('/game/manage_qr')
        return render(request,'game/edit_qr.html',context)