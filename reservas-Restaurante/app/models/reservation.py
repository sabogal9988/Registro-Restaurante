class Reservation:
    def __init__(self, id, user_id, table_id, reservation_time, status):
        self.id = id
        self.user_id = user_id
        self.table_id = table_id
        self.reservation_time = reservation_time
        self.status = status