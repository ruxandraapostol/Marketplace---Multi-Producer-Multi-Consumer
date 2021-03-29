"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def run(self):
        # asociez un id producatorului
        producer_id = self.marketplace.register_producer()

        # cat timp programul nu s-a terminat
        while self.kwargs['daemon'] is True:

            # pentru fiecare produs din lista
            for current_product in self.products:

                # pana am atins cantitatea dorita
                i = 0
                while i < current_product[1]:

                    # incerc sa adaug produsul in stoc
                    if not self.marketplace.publish(producer_id, current_product[0]):
                        # in caz negativ doar astept timpul necesar producatorului
                        sleep(self.republish_wait_time)
                    else:
                        # in caz afirmativ astept timpul necesar produsului
                        sleep(current_product[2])

                        # trec la urmatorul produs
                        i += 1
