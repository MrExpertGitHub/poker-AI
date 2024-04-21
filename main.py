import random


def deal(players, hands, deck, community):
    for player in range(players):
        hands.append([])
        for j in range(2):
            card_id: int = random.randint(0, 51 - 2 * player - j)
            hands[player].append(deck[card_id])
            deck.pop(card_id)
    for player in range(5):
        card_id = random.randint(0, 51 - player - players * 2)
        community.append(deck[card_id])
        deck.pop(card_id)


def result(players, combination, pot, hands, community, money):
    suits_c = [0, 0, 0, 0]
    numbers_c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    numbers_cf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    flush_suit = 0
    first_flush = True
    
    for hand in range(5):
        suits_c[community[hand][0]] += 1
        numbers_c[community[hand][1] - 2] += 1
    for hand in range(players):
        combination.append([""])
        if pot[hand + 1][1]:
            length = 0
            suits = suits_c[:]
            numbers = numbers_c[:]
            if pot[hand + 1] != "fold":
                for j in range(2):
                    suits[hands[hand][j][0]] += 1
                    numbers[hands[hand][j][1] - 2] += 1
                for j in range(14):
                    if numbers[12 - j] > 0:
                        length += 1
                        if length == 5:
                            combination[hand] = ["straight", 14 - j]
                            break
                    else:
                        length = 0
                for j in range(4):
                    if suits[j] >= 5:
                        combination[hand] = ["flush"]
                        flush_suit = j
                        break
                if combination[hand] == ["flush"]:
                    if first_flush:
                        for j in range(5):
                            if community[j][0] == flush_suit:
                                numbers_cf[community[j][1] - 2] += 1
                        first_flush = False
                    numbersf = numbers_cf[:]
                    for j in range(2):
                        if hands[hand][j][0] == flush_suit:
                            numbersf[hands[hand][j][1] - 2] += 1
                    length = 0
                    for j in range(14):
                        if numbersf[12 - j] > 0:
                            if len(combination[hand]) != 6:
                                combination[hand].append(14 - j)
                            length += 1
                            if length == 5:
                                combination[hand] = ["straight flush", 14 - j]
                                break
                        else:
                            length = 0
                if combination[hand][0] != "straight flush":
                    for j in range(13):
                        if numbers[j] == 4:
                            combination[hand] = ["poker", j + 2]
                            for k in range(13):
                                if numbers[12 - k] == 1:
                                    combination[hand].append(14 - k)
                                    break
                    if combination[hand][0] != "poker":
                        for j in range(13):
                            if numbers[12 - j] == 3:
                                combination[hand] = ["drill", 14 - j]
                                for k in range(13):
                                    if numbers[12 - k] >= 2 and combination[hand][1] != 14 - k:
                                        combination[hand][0] = "full house"
                                        combination[hand].append(14 - k)
                                        break
                                break
                        if (combination[hand][0] != "flush" and combination[hand][0] != "straight" and
                                combination[hand][0] != "full house"):
                            if combination[hand][0] == "drill":
                                for j in range(13):
                                    if len(combination[hand]) != 4:
                                        if numbers[12 - j] > 0 and 14 - j != combination[hand][1]:
                                            combination[hand].append(14 - j)
                            if combination[hand][0] != "drill":
                                for j in range(13):
                                    if numbers[12 - j] == 2:
                                        if combination[hand][0] == "":
                                            combination[hand][0] = "pair"
                                            combination[hand].append(14 - j)
                                        else:
                                            combination[hand][0] = "double pair"
                                            combination[hand].append(12 - j)
                                            break
                                if combination[hand][0] == "double pair":
                                    for j in range(13):
                                        if (numbers[12 - j] > 0 and 14 - j != combination[hand][1] and
                                                14 - j != combination[hand][2]):
                                            combination[hand].append(14 - j)
                                            break
                                elif combination[hand][0] == "pair":
                                    for j in range(13):
                                        if numbers[12 - j] > 0 and 14 - j != combination[hand][1]:
                                            if len(combination[hand]) == 5:
                                                break
                                            combination[hand].append(14 - j)
                                else:
                                    for j in range(13):
                                        if numbers[12 - j] > 0:
                                            if len(combination[hand]) == 6:
                                                break
                                            combination[hand].append(14 - j)

            if combination[hand][0] == "":
                combination[hand][0] = 0
            elif combination[hand][0] == "pair":
                combination[hand][0] = 1
            elif combination[hand][0] == "double pair":
                combination[hand][0] = 2
            elif combination[hand][0] == "drill":
                combination[hand][0] = 3
            elif combination[hand][0] == "straight":
                combination[hand][0] = 4
            elif combination[hand][0] == "flush":
                combination[hand][0] = 5
            elif combination[hand][0] == "full house":
                combination[hand][0] = 6
            elif combination[hand][0] == "poker":
                combination[hand][0] = 7
            else:
                combination[hand][0] = 8
            combination[hand].append(hand + 1)
        else:
            combination[hand] = [0]
    combination.sort(reverse=True)
    for hand in range(players):
        combination[hand].append(hand + 1)
    for hand in range(players - 1):
        if combination[hand][:len(combination[hand + 1]) - 2] == combination[hand - 1][:len(combination[hand]) - 2]:
            combination[hand][-1] = combination[hand - 1][-1]
    print(hands[1:players])
    wnumber = 0
    for hand in range(players):
        if combination[hand][-1] == 1:
            wnumber += 1
        else:
            break
    for hand in range(wnumber):
        money[combination[hand][-2] - 1] += pot[0] / wnumber


def bet(which, players: int, raised, pot, money, player_place):
    not_raised: int = 0
    while not_raised < players:
        player_id: int = 2
        if pot[player_id % players + 1][1]:
            if player_id % players == player_place:

                match player_id % players + 1:
                    case 1:
                        print("You are the small blind!")
                    case 2:
                        print("You are the big blind!")
                    case _:
                        print(f"You are the player {player_id % players + 1}!")

                print(f"Your bet is currently {pot[player_id % players + 1][0]}!")
                print(f"Your bet must be raised up to {raised}!")

                a: int = int(input("Raise:\n"))

                if a + pot[player_id % players + 1][0] < raised:
                    pot[player_id % players + 1][1] = False
            else:
                a = ai(player_id % players + 1, which)
            if pot[player_id % players + 1][1]:
                pot[player_id % players + 1][1] = False
                print(player_id % players + 1, "folded")
            else:
                pot[0] += int(a)
                raised += int(a) - raised + pot[player_id % players + 1][0]
                pot[player_id % players + 1][0] += int(a)
                money[player_id % players] -= int(a)
        player_id += 1


def ai(player, which):
    #     if != 1:
    #         print(community[:1+which])
    #     print(hands[player-1])
    #     print(pot)
    return 50


def main():
    # The first player is the small blind
    # The second player is the big blind

    players = int(input("How much player are playing?\n"))
    
    money = []
    for i in range(players):
        money.append(1000)

    while True:
        # 0th game state
        raised = 100
        pot = [150]
        for i in range(players):
            pot.append([0, True])
        order: list[str] = ["bot" for i in range(players)]
        player_place: int = random.randint(0, players - 1)

        deck = \
            [[0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13],
             [0, 14], 
             [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13],
             [1, 14], 
             [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [2, 11], [2, 12], [2, 13],
             [2, 14], 
             [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13],
             [3, 14]]

        hands = []
        community = []

        combination = []
        deal(players, hands, deck, community)
        print("In your hand:", str(hands[0]).strip(), sep='\n')
        pot[1][0] = 50
        money[0] -= 50
        pot[2][0] = 100
        money[1] -= 100

        # 1st game state
        bet(1, players, raised, pot, money, player_place)
        print(community[:3])

        # 2nd game state
        bet(2, players, raised, pot, money, player_place)
        print(community[3])

        # 3rd game state
        bet(3, players, raised, pot, money, player_place)
        print(community[4])

        # 4th game state
        bet(4, players, raised, pot, money, player_place)
        result(players, combination, pot, hands, community, money)

        print(money)
        input("Next:")


if __name__ == '__main__':
    main()
