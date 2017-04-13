from django.conf.urls import url, include
from question_app.views import *
urlpatterns = [
    url(r'^testers$', testers, name='testers'),
    url(r'^tester/(?P<interview_id>\d+)$', tester, name='tester'),
    url(r'^votes/done/$', votes, name="dones"),
    url(r'^votes/done/(?P<question_id>\d+)$', vote, name="done"),
    url(r'^votes/result$', voteField, name='result'),
    url(r'^votes/(?P<question_id>\d+)$', voteField, name='votes'),
    url(r'^questions$', detail, name='question'),
    url(r'^results$', resultsInterview, name='results'),
    url(r'^', testers),
    url(r'^', index, name='/'),

]