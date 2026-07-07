from django.shortcuts import render, redirect, reverse


def account(request):
	if request.user.is_subscribe:
		return redirect('allProjects')
	else:
		return redirect(reverse('index') + '#pricingSection')

