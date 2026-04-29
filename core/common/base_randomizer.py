import hashlib
import random
import time
import uuid

from faker import Faker


class BaseRandomizer:
    faker = Faker('ru-RU')
    random = random

    def random_string(self, string_length=10, ru=False, with_spaces=True):
        if not ru:
            return self.faker.pystr(string_length, string_length)

        s = self.faker.sentence(nb_words=string_length // 5, variable_nb_words=False)

        if not with_spaces:
            s = s.replace(' ', 'х')

        return s[:string_length]

    @staticmethod
    def uid():
        return str(uuid.uuid4())

    @staticmethod
    def choice(array):
        return random.choice(array)

    @staticmethod
    def randint(star=0, end=100):
        return random.randint(star, end)

    def md5(self):
        some_string = str(time.time())
        md5_obj = hashlib.md5(some_string.encode())
        return md5_obj.hexdigest()

    def email(self):
        return self.faker.ascii_free_email()

    @staticmethod
    def uniq_test_email():
        return f'autotest_{uuid.uuid4()}@icl-services.ru'

    def phone(self, mask=None):
        """
        Random phone generator. Will be return phone in random format or in format according to specified mask.
        :param mask: string in format like '+7(9xx)-xxx-xx-xx' where X will be replaced to random digit
        :return: random phone as string
        """
        if mask:
            return ''.join([(c, str(self.random.randint(0, 9)))[c == 'x'] for c in mask])
        return self.faker.phone_number()

    @staticmethod
    def few_random_elements(elements, count):
        return random.sample(population=elements, k=count)

    def name(self):
        while True:
            name = self.faker.name()
            if len(name.split(' ')) == 3:
                return name
