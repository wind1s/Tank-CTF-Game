class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def buy(self):
        print()
        print(f'Thank you for buying {self.title} for ${self.price*2}!')
        print('Your product will arrive shortly!')
        print('(We already have all your personal information)')
        # TODO: Query the database we bought from facebook

    def print_description(self):
        print()
        print(f'{self.title} - Now only ${self.price}!!')


class VideoGame(Product):
    def __init__(self, title, price, developer, platform):
        super().__init__(title, price)
        self.developer = developer
        self.platform = platform

    def print_description(self):
        super().print_description()
        print(f'Developed by {self.developer} for {self.platform}')


class PC_Game(VideoGame):
    def __init__(self, title, price, developer, platform, requirements):
        super().__init__(title, price, developer, platform)
        self.requirements = requirements

    def print_description(self):
        super().print_description()
        print(f'Requirements {self.requirements}')


game = PC_Game("BF4", "79", "Dice", "Xbox", "Intel neon 6400")
game.print_description()
