from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin_page), # render the sign page
    url(r'^logout$', views.logout), # log the user out
    url(r'^register$', views.register_page), # render the register page
    url(r'^dashboard$', views.dashboard), # render the dashboard page for the user or admin
    url(r'^new$', views.new_user_page), # render the new user form page
    url(r'^edit_profile/(?P<id>\d+)$', views.edit_profile_page), # render the edit profile page form
    url(r'^show/(?P<id>\d+)$', views.show), # show the user inforamtion and messages
    url(r'^(?P<id>\d+)/destroy$', views.destroy), # show the user inforamtion and messages

    # Registration and Login urls
    url(r'^register_me$', views.register_me), # create a new account for a user
    url(r'^login$', views.login), # create a login the user

    # Update information
    url(r'^update_personal$', views.update_personal), # update the user person info (first and last name, email)
    url(r'^update_password$', views.update_password), # update the user password
    url(r'^update_description$', views.update_description), # update the user description

    # Messages urls
    url(r'^send_message$', views.send_message), # send message to another user
    url(r'^post_comment$', views.post_comment), # post message to a message

]