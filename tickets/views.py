from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from collections import deque

links = {
    'change_oil': ('/get_ticket/change_oil', 'Change Oil', deque()),
    'inflate_tires': ('/get_ticket/inflate_tires', 'Inflate Tires', deque()),
    'diagnostic': ('/get_ticket/diagnostic', 'Diagnostic', deque()),
}


def welcome(request):
    return HttpResponse('<h2>Welcome to the Hypercar service!</h2>')


def operator_menu(request):
    line = {
        'Change oil queue': len(links['change_oil'][2]),
        'Inflate tires queue': len(links['inflate_tires'][2]),
        'Get diagnostic queue': len(links['diagnostic'][2]),
    }
    return render(request, 'tickets/operator_menu.html', {'line': line})


def user_menu(request):
    return render(request, 'tickets/customer_menu.html', {'menu': links})


class GetTicket(View):
    def check_in(self, service):
        service_line = links[f'{service}'][2]
        service_line.append(len(service_line) + 1)
        priority = 1 if service == 'change_oil' else 2 if service == 'inflate_tires' else 3

        return service_line[-1], priority

    def waiting_time(self, ticket, priority):
        if priority == 1:
            return 2 * (ticket - 1)
        else:
            change_oil_line = links['change_oil'][2]
            change_oil_time = 2 * change_oil_line[-1] if len(change_oil_line) != 0 else 0
            if priority == 2:
                return 5 * (ticket - 1) + change_oil_time
            else:
                inflate_tires_line = links['inflate_tires'][2]
                if len(inflate_tires_line) != 0:
                    inflate_tires_time = 5 * inflate_tires_line[-1] + change_oil_time
                else:
                    inflate_tires_time = change_oil_time

                return 30 * (ticket - 1) + inflate_tires_time

    def get(self, request, service, *args, **kwargs):
        ticket, priority = self.check_in(service)
        time = self.waiting_time(ticket, priority)

        return render(request, 'tickets/get_ticket.html', {'time': time, 'ticket': ticket})
