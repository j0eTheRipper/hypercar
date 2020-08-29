line = {
    'Change Oil': [],
    'Inflate Tires': [],
    'Diagnostic': [],
}
def waiting_time(ticket, priority):
    if priority == 1:
        return 2 * (ticket - 1)
    else:
        change_oil_time = 2 * line['Change Oil'][-1]
        if priority == 2:
            return 5 * (ticket - 1) + change_oil_time
        else:
            inflate_tires_time = 5 * (line['Inflate Tires'][-1]) + change_oil_time
            return 30 * (ticket - 1) + inflate_tires_time

