from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message, User
from django.views import View
from django.db.models import Q 
from .utils import get_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ChatList(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(Q(user_id=user_id) & ~Q(title=None)).order_by("-created")
        return render(request, "main/chat_list.html", {"chats": chats, "user_id": user_id})

@method_decorator(csrf_exempt, name='dispatch')
class ChatDetail(View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        messages = Message.objects.filter(chat=chat)
        return render(request, "main/chat_detail.html", {"messages": messages, "chat": chat})
    
    def post(self, request, chat_id):
        content = request.POST.get("content")
        chat = get_object_or_404(Chat, id=chat_id)
        Message.objects.create(role=Message.USER, content=content, chat=chat)
        if not chat.title:
            chat.title = content
            chat.save()
        chat_messages = Message.objects.filter(chat=chat)
        messages = []
        for chat_message in chat_messages:
            messages.append({"role": chat_message.role, "content": chat_message.content})
        # Messages List
        response = get_response(messages)
        Message.objects.create(role=Message.ASSISTANT, content=response, chat=chat)
        return redirect('message_list', chat.id)


def add_new_chat(request, user_id):
    chat = Chat.objects.create(
        user_id=user_id
    )
    return redirect('message_list', chat.id)


def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user_id = chat.user.id
    Message.objects.filter(chat=chat).delete()
    chat.delete()
    return redirect("chat_list", user_id)
