from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.shortcuts import get_object_or_404

from taggit.models import Tag

from .models import Post, Contact, Services, FAQ, Laws, ServiceCategory
from .forms import EmailForm, SearchForm, PostForm


def home_view(request):
    services = Services.objects.all()
    laws = Laws.objects.all()
    context = {
        'services': services,
        'laws': laws
    }
    if request.method == 'POST':
        service_name = request.POST.get('services')
        service = get_object_or_404(Services, name=service_name)

        # Perform validation on the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name:
            messages.error(request, 'Please enter your name.')
        elif not phone:
            messages.error(request, 'Please enter your phone number.')
        elif not message:
            messages.error(request, 'Please enter a message.')
        else:
            contact = Contact(
                name=name,
                services=service,
                phone=phone,
                message=message
            )
            contact.save()
            messages.success(request, 'Success')
            return HttpResponseRedirect('/')

    return render(request, 'home.html', context=context)


def about_us(request):
    laws = Laws.objects.all()
    context = {
        'laws': laws
    }
    return render(request, 'about_us.html', context=context)


def services(request):
    laws = Laws.objects.all()
    context = {
        'laws': laws
    }
    return render(request, 'services.html', context=context)


def post_list(request, tag_slug=None):
    laws = Laws.objects.all()
    posts_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
        'tag': tag,
        'laws': laws
    }
    return render(request, 'list.html', context=context)


@login_required(login_url='admin/')
def post_add(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'post_add.html', context)


def post_detail(request, post_slug):
    laws = Laws.objects.all()
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post_slug)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]
    context = {
        'post': post,
        'similar_pots': similar_posts,
        'laws': laws,
    }
    return render(request, 'list_detail.html', context=context)


def post_share(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{cd['name']} recommends to read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'shukrullo.coder@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'post_share.html', context=context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'post/search.html', context=context)


def contact_us(request):
    laws = Laws.objects.all()
    services = Services.objects.all()
    context = {
        'services': services,
        'laws': laws
    }
    if request.method == 'POST':
        service_name = request.POST.get('services')
        service = get_object_or_404(Services, name=service_name)

        # Perform validation on the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name:
            messages.error(request, 'Please enter your name.')
        elif not phone:
            messages.error(request, 'Please enter your phone number.')
        elif not message:
            messages.error(request, 'Please enter a message.')
        else:
            contact = Contact(
                name=name,
                services=service,
                phone=phone,
                message=message
            )
            contact.save()
            messages.success(request, 'Success')
            return HttpResponseRedirect('/contact/')

    return render(request, 'contact_us.html', context=context)


def services_view(request, service_slug):
    laws = Laws.objects.all()
    services = Services.objects.all()
    service = get_object_or_404(Services,
                                slug=service_slug)
    if request.method == 'POST':
        service_name = request.POST.get('services')
        service = get_object_or_404(Services, name=service_name)

        # Perform validation on the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name:
            messages.error(request, 'Please enter your name.')
        elif not phone:
            messages.error(request, 'Please enter your phone number.')
        elif not message:
            messages.error(request, 'Please enter a message.')
        else:
            contact = Contact(
                name=name,
                services=service,
                phone=phone,
                message=message
            )
            contact.save()
            messages.success(request, 'Success')
            return HttpResponseRedirect(f'/services/{service_slug}/')
    context = {
        'service': service,
        'services': services,
        'laws': laws,
    }
    return render(request, 'service_detail.html', context=context)


def faqs_view(request):
    faqs = FAQ.objects.all()
    laws = Laws.objects.all()
    context = {
        'faqs': faqs,
        'laws': laws,
    }
    return render(request, 'faqs.html', context=context)


def laws_view(request, law_slug):
    law = Laws.objects.get(slug=law_slug)
    context = {
        'law': law
    }
    return render(request, 'laws.html', context=context)
