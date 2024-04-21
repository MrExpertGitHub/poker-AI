from typing import Self

numbers: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits: list[str] = ["C", "D", "H", "P"]


class Card:
    def __init__(self, card_id: str | int) -> None:
        """
        :param card_id: The representation of the card with a string:
        The first character is the suit and the others are the numbers
        """
        # Club, Diamond, Heart, Pike
        card_id = str(card_id)
        suit: int | str = card_id[0]
        number: int | str = card_id[1:]
        self.suit: int
        try:
            if not (0 < int(suit) < 5):
                raise Exception("The suit have to be greater than 0 and less than 5")
            else:
                self.suit = int(suit)
        except ValueError:
            match suit:
                case "C" | "c":
                    self.suit = 1
                case "D" | "d":
                    self.suit = 2
                case "H" | "h":
                    self.suit = 3
                case "P" | "p":
                    self.suit = 4
                case _:
                    raise ValueError("Invalid suit!")

        self.number: int
        try:
            if not (1 < int(number) < 15):
                raise Exception("The number have to be greater than 1 and less than 1")
            else:
                self.number = int(number)
        except ValueError:
            match number:
                case "J" | "j":
                    self.number = 11
                case "Q" | "q":
                    self.number = 12
                case "K" | "k":
                    self.number = 13
                case "A" | "a":
                    self.number = 14
                case _:
                    raise ValueError("Invalid number!")

        self.id: tuple[int, int] = (self.suit, self.number)

    def __str__(self) -> str:
        suit: str
        match self.id[0]:
            case 1:
                suit = "C"
            case 2:
                suit = "D"
            case 3:
                suit = "H"
            case _:
                suit = "P"

        number: str
        match self.id[1]:
            case 11:
                number = "J"
            case 12:
                number = "Q"
            case 13:
                number = "K"
            case 14:
                number = "A"
            case _:
                number = str(self.id[1])
        return str(suit + number)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Self) -> bool:
        """
        returns with True if two card are identical, otherwise returns with False
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

    def is_pair(self, other: Self) -> bool:
        """
        returns with True if a pair can be made out of the given cards
        """
        return self.number == other.number

    def __lt__(self, other: Self):
        return int(str(self.number + self.suit)) < int(str(other.number + other.suit))


class FullHand:
    def __init__(self, cards: tuple[Card, Card, Card, Card, Card]) -> None:
        self.cards: tuple[Card, Card, Card, Card, Card] = cards
        self.string: str = str([c for c in self.cards])

    def get_high_card(self):
        high_card: Card = self.cards[0]
        for card in self.cards:
            if high_card < card:
                high_card = card
        return high_card

    def get_pairs(self) -> list[list[Card]] | list[None]:
        pairs: list[str] | list[None] = []
        for number in numbers:
            if self.string.count(number) == 2:
                pairs.append(number)

        return pairs

    def get_three_of_a_kind(self) -> str | None:
        for number in numbers:
            if self.string.count(number) == 3:
                return number

    def get_full_house(self) -> str | None:
        """
        If there is it returns with a full house
        :return: {three of a kind}-{pair}
        """
        if bool(self.get_three_of_a_kind()) and bool(self.get_pairs()):
            return str(self.get_three_of_a_kind()) + "-" + str(self.get_pairs()[0])

    def get_four_of_a_kind(self) -> str | None:
        for number in numbers:
            if self.string.count(number) == 4:
                return number

    def get_flush(self) -> str | None:
        for suit in suits:
            if self.string.count(suit) == 5:
                return suit


if __name__ == '__main__':
    h: FullHand = FullHand((Card("110"), Card("210"), Card("112"), Card("212"), Card("312")))
    print(h.get_full_house())
