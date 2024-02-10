from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.decorators import login_required
from accounts.models import UserLibraryAccount
from transactions.models import Transaction
from transactions.constants import BORROWED, RETURN
from decimal import Decimal
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def confirmation_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@login_required
def post_details(request, id):
    post = models.Post.objects.get(id=id)
    user = request.user
    user_account = UserLibraryAccount.objects.filter(user=user).first()
    borrowers_list = []
    return_list = []

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = user
            new_comment.save()
            messages.success(request, 'Comment is added successfully!')
            return redirect('details_post', id=post.id)
        
        if 'borrow' in request.POST:
            if user_account.balance < post.price:
                messages.error(request, 'You do not have enough balance to borrow this post.')
                return redirect('details_post', id=post.id)
            user_account.balance -= Decimal(str(post.price))
            user_account.save()

            Transaction.objects.create(
                account=user_account,
                amount=post.price,
                balance_after_transaction=user_account.balance,
                transaction_type=BORROWED
            )
            
            post.borrowers.add(user)
            borrowers_list.append(post)
            print(borrowers_list)
            messages.success(request, 'Book is borrowed successfully!')
            confirmation_email(user, post.price, 'Borrow Book Message','borrow_email.html')
            
        elif 'return' in request.POST:
            user_account.balance += Decimal(str(post.price))
            user_account.save()
            Transaction.objects.create(
                account=user_account,
                amount=post.price,
                balance_after_transaction=user_account.balance,
                transaction_type=RETURN
            )
            post.borrowers.remove(user)
            return_list.append(user)
            messages.success(request, 'Book is returned successfully!')
            confirmation_email(user, post.price, 'Return Book Message','return_email.html')

        return redirect('details_post', id=post.id)
      
    comments = models.Comment.objects.filter(post=post)
    comment_form = forms.CommentForm()

    return render(request, 'post_details.html', {'post': post, 'comments': comments, 'comment_form': comment_form})