from django.shortcuts import render




def home_page(request):
    return render(request, 'index.html')




def pricing_page(request):
    return render(request, 'packages.html')





def about_page(request):
    return render(request, 'about.html')



def contact_page(request):
    return render(request, 'contact.html')






