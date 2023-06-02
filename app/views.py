import asyncio
from typing import Tuple, Union

import aiohttp
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render

from .forms import AddURLForm
from .models import URL


def home(request):
    if request.user.is_authenticated:
        form = AddURLForm(request.POST or None, instance=URL(user=request.user))
        if form.is_valid():
            form.save()
            messages.success(request, "URL added.")
            return redirect(".")
    else:
        form = None
    return render(request, "base.html", dict(form=form))


@login_required
def toggle(request):
    pause = request.POST.get("pause")
    if pause:
        request.user.url_set.filter(id=pause).update(paused=True)
    else:
        resume = request.POST.get("resume")
        request.user.url_set.filter(id=resume).update(paused=False)
    return redirect("home")


async def check_url(session, url) -> Tuple[int, int]:
    try:
        async with session.head(url.url) as resp:
            return url.id, resp.status
    except OSError:
        return url.id, 0


async def check(request) -> Union[HttpResponseForbidden, JsonResponse]:
    # request.user is lazy and accessing it will result in DB query
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        return HttpResponseForbidden()
    async with aiohttp.ClientSession() as session:
        jobs = []
        async for url in request.user.url_set.filter(paused=False):
            jobs.append(check_url(session, url))
        return JsonResponse({"result": dict(await asyncio.gather(*jobs))})
