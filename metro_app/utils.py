import random


def get_weight(weights):
    assert abs(sum(weights) - 1) < 0.0001
    x = random.random()
    s = 0
    for index, weight in enumerate(weights):
        s += weight
        if x - s < 0:
            return index


def randomize():
    location_id = get_weight([0.15, 0.1, 0.35, 0.3, 0.1]) + 2
    if location_id == 2:
        event_id = get_weight([0.74, 0.15, 0, 0.05, 0.05, 0.01]) + 1
        faction_id = get_weight([0.3, 0.3, 0.3, 0.1]) + 1
    elif location_id == 3:
        event_id = get_weight([0.5, 0.11, 0.03, 0.25, 0.09, 0.02]) + 1
        faction_id = get_weight([0.05, 0.05, 0.05, 0.85]) + 1
    elif location_id == 4:
        event_id = get_weight([0.6, 0.15, 0, 0.16, 0.07, 0.02]) + 1
        faction_id = get_weight([0.3, 0.3, 0.3, 0.1]) + 1
    elif location_id == 5:
        event_id = get_weight([0.3, 0.15, 0.05, 0.33, 0.13, 0.04]) + 1
        faction_id = get_weight([0.03, 0.03, 0.03, 0.91]) + 1
    else:
        event_id = get_weight([0.25, 0.05, 0.1, 0.32, 0.03, 0.25]) + 1
        faction_id = get_weight([0.3, 0.3, 0.3, 0.1]) + 1
    if event_id == 1:
        bullets_found = get_weight([0.55, 0.25, 0.1, 0.05, 0.04, 0.01])
        enemies_quant = 0
        enemy_id = 0
        hp_lost = 0
    elif event_id == 2:
        bullets_found = get_weight([0, 0.1, 0.3, 0.3, 0.2, 0.05, 0.01, 0.01, 0.01, 0.01, 0.01]) + 3
        enemies_quant = 0
        enemy_id = 0
        hp_lost = 0
    elif event_id == 3:
        bullets_found = get_weight([0, 0.1, 0.3, 0.3, 0.2, 0.05, 0.01, 0.01, 0.01, 0.01, 0.01]) + 5
        enemies_quant = 0
        enemy_id = 0
        hp_lost = 0
    elif event_id == 4:
        bullets_found = 0
        enemies_quant = get_weight([0.3, 0.4, 0.2, 0.1]) + 1
        enemy_id = 1
        hp_lost = 0
        for enemy in range(enemies_quant):
            hp_lost += get_weight([0.7, 0.3])
    elif event_id == 5:
        bullets_found = 0
        enemies_quant = get_weight([0.3, 0.4, 0.2, 0.1]) + 1
        enemy_id = 2
        hp_lost = 0
        for enemy in range(enemies_quant):
            hp_lost += get_weight([0.6, 0.3, 0.1])
    else:
        bullets_found = 0
        enemies_quant = get_weight([0.3, 0.4, 0.2, 0.1]) + 1
        enemy_id = 3
        hp_lost = 0
        for enemy in range(enemies_quant):
            hp_lost += get_weight([0.5, 0.3, 0.1, 0.1])

    return {'location_id': location_id, 'event_id': event_id, 'faction_id': faction_id,
            'bullets_found': bullets_found, 'enemy_id': enemy_id, 'enemies': enemies_quant, 'hp_lost': hp_lost}
