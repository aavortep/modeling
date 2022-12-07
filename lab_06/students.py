from random import random
from numpy import random as numpy_random

TIME_DELTA = 0.01
FINISH_PROCESS_REQUEST = 1
CURRENT_REQUEST = 0
DONT_HAVE_FREE_TEACHER = -1
FIRST_QUEUE_PROB = 0.8


class Time:
    def get_time(self):
        return 0


class TimeDistribution(Time):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_time(self):
        return self.a + (self.b - self.a) * random()


class TimeConstant(Time):
    def __init__(self, t):
        self.t = t

    def get_time(self):
        return self.t


class TimeProcessor:
    def __init__(self, time_distribution):
        self.time_distribution = time_distribution
        self.remaining_time = 0

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= TIME_DELTA

        if self.remaining_time <= 1e-5:
            self.remaining_time = self.time_distribution.get_time()
            return Request()

        return None


class Teacher:
    def __init__(self, storage, recipient, time_distribution):
        self.time_distribution = time_distribution
        self.requests_storage = storage
        self.recipient = recipient
        self.remaining_time = 0
        self.is_busy = False
        self.processing_request = None
        self.max_queue_len = 0
        self.work_time = 0

    def update_time(self):
        self.remaining_time -= TIME_DELTA
        if len(self.requests_storage) > self.max_queue_len:
            self.max_queue_len = len(self.requests_storage)

        if self.is_busy and self.remaining_time <= 1e-5:
            self.recipient.append(self.processing_request)
            self.is_busy = False
            self.processing_request = None

        if not self.is_busy and len(self.requests_storage) != 0:
            self.processing_request = self.requests_storage.pop(0)
            self.remaining_time = self.time_distribution.get_time()
            self.work_time += self.remaining_time
            self.is_busy = True


class Request:
    request_id = 0

    def __init__(self):
        global CURRENT_REQUEST
        self.request_id = CURRENT_REQUEST
        CURRENT_REQUEST += 1


class Defense:
    def __init__(self, requests_storage, time_distribution):
        self.requests_storage = requests_storage
        self.time_distribution = time_distribution
        self.is_busy = False
        self.processing_request = None
        self.remaining_time = 0
        self.max_queue_len = 0

    def update_time(self):
        if self.remaining_time != 0:
            self.remaining_time -= TIME_DELTA

        if len(self.requests_storage) > self.max_queue_len:
            self.max_queue_len = len(self.requests_storage)

        if self.is_busy and self.remaining_time <= 1e-5:
            self.is_busy = False
            self.processing_request = None
            return FINISH_PROCESS_REQUEST

        if not self.is_busy and len(self.requests_storage) != 0:
            self.processing_request = self.requests_storage.pop(0)
            self.remaining_time = self.time_distribution.get_time()
            self.is_busy = True


def find_free_teacher(teachers):
    for i in range(len(teachers)):
        if not teachers[i].is_busy:
            return i
    return DONT_HAVE_FREE_TEACHER


def iteration(students, storage_1, storage_2, teachers, defense, request_info, is_new=True):
    if is_new:
        request = students.update_time()
        if request:
            request_info['generated_count'] += 1
            if numpy_random.random_sample() <= FIRST_QUEUE_PROB:
                storage_1.append(request)
                request_info['first_teacher'] += 1
            else:
                storage_2.append(request)
                request_info['second_teacher'] += 1

    for teacher in teachers:
        teacher.update_time()

    result = defense.update_time()
    if result == FINISH_PROCESS_REQUEST:
        request_info['processed_count'] += 1


def modeling(students, storage_1, storage_2, teachers, defense, requests_count):
    statistics_info = {'generated_count': 0, 'first_teacher': 0, 'second_teacher': 0, 'processed_count': 0}

    while statistics_info['generated_count'] < requests_count:
        iteration(students, storage_1, storage_2, teachers, defense, statistics_info)

    while statistics_info['processed_count'] < requests_count:
        iteration(students, storage_1, storage_2, teachers, defense, statistics_info, False)

    return statistics_info


if __name__ == '__main__':
    requests_count = int(input("Введите количество студентов: "))
    if requests_count <= 0:
        print("Неверное количество студентов")
        exit(1)

    students = TimeProcessor(TimeDistribution(1, 3))

    storage_1 = []
    storage_2 = []
    storage_3 = []

    defense = Defense(storage_3, TimeConstant(5))

    teachers = [Teacher(storage_1, storage_3, TimeDistribution(2, 6)),
                Teacher(storage_2, storage_3, TimeDistribution(15, 25))]

    result = modeling(students, storage_1, storage_2, teachers, defense, requests_count)

    print('Общее количество запросов: ', result['generated_count'])
    print('Проверено первым преподавателем: ', result['first_teacher'])
    print('Проверено вторым преподавателем: ', result['second_teacher'])
    print('Макс. очередь у 1-го преподавателя: ', teachers[0].max_queue_len)
    print('Макс. очередь у 2-го преподавателя: ', teachers[1].max_queue_len)
    print('Макс. очередь на защиту: ', defense.max_queue_len)
    print('Общее время проверки студентов 1-м преподавателем (в минутах): ', round(teachers[0].work_time, 4))
    print('Общее время проверки студентов 2-м преподавателем (в минутах): ', round(teachers[1].work_time, 4))
