from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from collections import deque

links = {
    'change_oil': ('/get_ticket/change_oil', 'Change Oil', deque()),
    'inflate_tires': ('/get_ticket/inflate_tires', 'Inflate Tires', deque()),
    'diagnostic': ('/get_ticket/diagnostic', 'Diagnostic', deque()),
}

served_clients = deque()  # Stack for the clients that are served


def welcome(request):
    return HttpResponse('<h2>Welcome to the Hypercar service!</h2>')


def user_menu(request):
    return render(request, 'tickets/customer_menu.html', {'menu': links})


class Processing(View):
    line = {
        'Change oil queue': links['change_oil'][2],
        'Inflate tires queue': links['inflate_tires'][2],
        'Get diagnostic queue': links['diagnostic'][2],
    }

    def next_queue(self):
        """Returns the next ticket to be served"""
        for queue in self.line.values():
            if len(queue) != 0:
                return queue

    def get(self, request):
        return render(request, 'tickets/operator_menu.html', {'line': self.line})

    def post(self, request):
        queue = self.next_queue()  # the queue

        if queue is not None:
            served_clients.append(queue.popleft())

        return redirect('/processing')


class GetTicket(View):
    def get_ticket(self):
        ticket = 1
        for i in links.values():
            ticket += len(i[2])
        print(ticket)
        return ticket

    def check_in(self, service):
        """Generates a ticket for the customer."""
        service_line = links[f'{service}'][2]
        service_line.append(self.get_ticket())
        priority = 1 if service == 'change_oil' else 2 if service == 'inflate_tires' else 3

        return service_line[-1], priority

    def waiting_time(self, ticket, priority):
        """Calculates the waiting time for the customer."""
        def get_ticket_index(service):
            """Gets the ticket index"""
            return links[service][2].index(ticket)

        if priority == 1:
            return 2 * get_ticket_index('change_oil')
        else:
            change_oil_line = links['change_oil'][2]
            change_oil_time = 2 * len(change_oil_line)
            if priority == 2:
                return 5 * get_ticket_index('inflate_tires') + change_oil_time
            else:
                inflate_tires_line = links['inflate_tires'][2]
                inflate_tires_time = 5 * len(inflate_tires_line) + change_oil_time

                return 30 * get_ticket_index('diagnostic') + inflate_tires_time

    def get(self, request, service):
        ticket, priority = self.check_in(service)
        time = self.waiting_time(ticket, priority)
        print(ticket)
        return render(request, 'tickets/get_ticket.html', {'time': time, 'ticket': ticket})


class NextTicket(View):
    def get(self, request):
        if served_clients:
            return HttpResponse(f'<div>Next ticket #{served_clients.pop()}</div>')
        else:
            return HttpResponse(f'<div>Waiting for the next client</div>')
