import random
import string

liste_taches = [
    'Préparation et Planification',
    'Approvisionnement et Achat',
    'Travaux de Gros Œuvre',
    'Travaux de Second Œuvre',
    'Finitions et Réceptions'
]


def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


if __name__ == '__main__':
    password_generate = generate_random_password()

