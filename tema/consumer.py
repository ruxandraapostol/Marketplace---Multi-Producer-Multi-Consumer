"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def run(self):
        # pentru fiecare cos din lista
        for current_cart in self.carts:

            # atribui un id
            cart_id = self.marketplace.new_cart()

            # pentru fiecare operatie din cosul curent
            for action in current_cart:

                # verific tipul actiunii
                if action["type"] == "add":

                    # pana am atins cantitatea dorita
                    j = 0
                    while j < action["quantity"]:

                        # incerc sa adaug produsul dorit in cos
                        if not self.marketplace.add_to_cart(cart_id, action["product"]):

                            # daca operatia nu are succes astept
                            sleep(self.retry_wait_time)
                        else:
                            # altfel trec mai departe
                            j += 1
                else:
                    # pana am atins cantitatea dorita
                    j = 0
                    while j < action["quantity"]:
                        # sterg produsul din cos
                        self.marketplace.remove_from_cart(cart_id, action["product"])

                        # trec mai departe
                        j += 1

            # afisez produsele din cos in urma tuturor operatiilor
            self.marketplace.place_order(self.kwargs["name"], cart_id)
