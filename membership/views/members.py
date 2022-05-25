import json
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from membership.models.organization import Client
from membership.models.member_request import MemberRequest

User = get_user_model()


def member_list_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = user.id
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)
                context['this_user'] = this_user
            except User.DoesNotExist:
                return HttpResponse("That user does not exist.")
            try:
                member_list = Client.objects.get(owner=this_user)
            except Client.DoesNotExist:
                return HttpResponse(f"Could not find a friends list for {this_user.email}")

            # Must be friends to view a friends list
            if user != this_user:
                if not user in member_list.members.all():
                    return HttpResponse("You must be friends to view their friends list.")
            members = []  # [(friend1, True), (friend2, False), ...]
            # get the authenticated user's friend list
            auth_user_member_list = Client.objects.get(owner=user)
            for friend in member_list.members.all():
                members.append((friend, auth_user_member_list.is_mutual_friend(friend)))
            context['members'] = members
    else:
        return HttpResponse("You must be friends to view their friends list.")
    return render(request, "user/members.html", context)


def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        schema_name = request.POST.get("schema_name")
        # print(schema_name)
        client = Client.objects.get(schema_name=schema_name)
        print(client)
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = MemberRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                    friend_request = MemberRequest(sender=user, receiver=receiver)
                    content = f'{user} has been invite you for VNR services at {client.slug}'
                    friend_request.client = client
                    friend_request.message = content
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except MemberRequest.DoesNotExist:
                friend_request = MemberRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent."

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to sent a friend request"
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = MemberRequest.objects.get(receiver=friend_request_id)
            # confirm that is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    # Accepting the founded request
                    friend_request.accept()
                    payload['response'] = "Friend request accepted."

                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    else:
        payload['response'] = "You must be authenticated to accept a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = Client.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something went wrong: {str(e)}"
        else:
            payload['response'] = "There was an error. Unable to remove that friend."
    else:
        payload['response'] = "You must be authenticated to remove a friend."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = MemberRequest.objects.get(pk=friend_request_id)
            # confirm that is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    # Declining the founded request
                    friend_request.decline()
                    payload['response'] = "Friend request declined."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your friend request to decline."
        else:
            payload['response'] = "Unable to decline that friend request."
    else:
        payload['response'] = "You must be authenticated to decline a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")
