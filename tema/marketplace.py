"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # numarul producatorilor necesar obtinerii id-ului
        self.producers_number = -1

        # lista care retine cate produse are adaugate producatorul cu id-ul i
        self.producers_items = []

        # mutex pentru a modifica variabilele referitoare la producatori
        self.producers_number_lock = Lock()

        # lista cu toate produsele din stoc
        self.available_products = []

        # lista cu tupluri de forma (produs, id-ul producatorului)
        self.available_products_origin = []

        # mutex pentru variabilele referitoare la produsele din stoc
        self.available_products_lock = Lock()

        # numarul cosurilor necesar pentru obtinerea id-ului
        self.carts_number = -1

        # lista cu listele produselor din fiecare cos
        self.carts = []

        # mutex pentru modificarea variabilelor referitoare la cosuri
        self.carts_number_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # ma asigur ca nu atribui acelasi numar mai multor producatori
        with self.producers_number_lock:
            # actualizez numarul de producatori
            self.producers_number += 1

            # pe pozitia corespunzatoare noului producator din
            # lista cu numarul de produse al fiecaruia adaug 0
            self.producers_items.append(0)

        # returnez numarul atribuit noului producator
        return self.producers_number

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # verific daca producatorul nu are deja in Marketplace numarul maxim de produse
        if self.producers_items[int(producer_id)] < self.queue_size_per_producer:
            # adaug produsul in stoc
            self.available_products.append(product)
            # actualizez numarul de produse din stoc al producatorului
            self.producers_items[producer_id] += 1
            # adaug produsul si id-ul producatorului in lista pentru provenienta fiecarui produs
            self.available_products_origin.append((product, producer_id))
            return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        #  ma asigur ca nu atribui acelasi numar mai multor cosuri
        with self.carts_number_lock:
            # actualizez numarul de producatori
            self.carts_number += 1

            # pe pozitia corespunzatoare noului cos din lista cu
            # listele produselor din fiecare cos adaug []
            self.carts.append([])

        # returnez numarul atribuit noului cosurilor
        return self.carts_number

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # ma asigur ca doi cumaparatori nu isi pun simultan acelasi produs in cos
        # prin mutexul destinat
        with self.available_products_lock:
            # daca produsul dorit se afla in lista produselor din stoc
            if product in self.available_products:
                # adaug produsul in lista cu produse corespunzatoare cosului
                self.carts[cart_id].append(product)

                # sterg produsul dorit din lista produselor aflate in stoc
                self.available_products.remove(product)
                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # sterg produsul din lista produselor din cosul curent
        self.carts[cart_id].remove(product)

        # agaug produsul in lista produselor din stoc
        self.available_products.append(product)

    def place_order(self, consumer_id, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        # transform lista cu tupluri (produs, origine) intr-un dictionar
        # pentru a usura cautarea unui element
        dictionary = dict(self.available_products_origin)

        # pentru fiecare produs din lista cosului dorit
        for prod in self.carts[cart_id]:

            # ma asigur ca doi consumatori nu vor sa cumpere acelasi produs
            # desi ei au produse diferite in cos
            with self.producers_number_lock:

                # daca gasesc produsul curent in dictionar
                if prod in dictionary:

                    # actualizez numarul de produse pe care producatorul
                    # acestuia il are in stoc
                    self.producers_items[dictionary[prod]] -= 1

                    # afisez produsul
                    print(consumer_id, "bought", prod)

        # returnez lista cu produsele din cos
        return self.carts[cart_id]
