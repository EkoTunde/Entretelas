from costs.models import Cost


def load_moc_data_to_DB(name, price):
    Cost.objects.create(
        name=name,
        price=price,
    )


DATA = [
    ('Aplique', 130.00),
    ('Bellón', 380.00),
    ('Cierre', 4000),
    ('Cinta Plástica (baño)', 10.00),
    ('Cinta Plástica (cortina)', 25.00),
    ('Cordón', 15.00),
    ('Elástico', 20.00),
    ('Frizelina', 130.00),
    ('Guata', 150.00),
    ('Luz/hilo', 130.00),
    ('Belcro', 60.00),
    ('Varillas', 500),
]


def load_all():
    for name, price in DATA:
        load_moc_data_to_DB(name, price)
