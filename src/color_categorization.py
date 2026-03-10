def categoriza_cor(cor):
    cores_base = {
        'Branco': ['White', 'Pearl White', 'Taffeta White', 'Platinum White', 'White Orchid Pearl'],
        'Preto': ['Black', 'Crystal Black', 'Crystal Black Pearl'],
        'Cinza': ['Gray', 'Modern Steel', 'Meteorite Gray', 'Urban Titanium', 'Polished Metal Metallic', 'Charcoal'],
        'Prata': ['Silver', 'Lunar Silver', 'Alabaster Silver', 'Cool Mist Metallic'],
        'Azul': ['Blue', 'Aegean Blue', 'Cosmic Blue', 'Dyno Blue'],
        'Vermelho': ['Red', 'Rallye Red', 'Crimson Pearl', 'Burgundy', 'Burgundy Night Pearl', 'Molten Lava Pearl'],
        'Marrom': ['Brown', 'Kona Coffee Metallic'],
        'Outras': ['Green', 'Orange', 'Yellow', 'Purple', 'Gold', 'Bronze', 'Teal', 'Pewter', 'Platinum', 
                  'Frozen Grey', 'Maroon', 'Beige', 'Pear', 'Burgandy']
    }
    
    for base, variantes in cores_base.items():
        if any(variante in cor for variante in variantes):
            return base
    return 'Outras'

def categoriza_cor_interna(cor):
    cores_base = {
        'Black': ['Black', 'Blk', 'Dark', 'Charcoal', 'Nonjackassstaff', 'Nonjackass', 'Blk Clth'],
        'Gray': ['Gray', 'Grey', 'Stone'],
        'Beige': ['Beige', 'Tan', 'Ivory', 'Cream', 'Champagne', 'Off-White'],
        'Brown': ['Brown'],
        'White': ['White'],
        'Red': ['Red'],
        'Silver': ['Silver'],
        'Desconhecido': ['Desconhecido']
    }
    
    for base, variantes in cores_base.items():
        if any(variante.lower() in cor.lower() for variante in variantes):
            return base
    return 'Desconhecido'


