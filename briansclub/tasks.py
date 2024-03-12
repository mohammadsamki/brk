from background_task import background
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from.models import Ticket, AdminReply

@background(schedule=120)
def send_auto_reply():
    tickets = Ticket.objects.filter(status='open')
    for ticket in tickets:
        if now() - ticket.created_at > timedelta(minutes=2):
            ticket.status = 'closed'
            ticket.save()
            subject = 'Your ticket has been closed'
            message = render_to_string('auto_reply.txt', {'ticket': ticket})
            send_mail(subject, message, 'noreply@example.com', [ticket.user.email])
            admin_reply = AdminReply.objects.create(ticket=ticket, user=None, message='This is an auto-reply from the system. The ticket has been closed due to inactivity.')