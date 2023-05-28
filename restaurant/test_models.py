from django.test import TestCase
from restaurant.models import Menu


class MenuTest(TestCase):

    def setUp(self) -> None:
        self.item1 = Menu.objects.create(
            title = 'Osh',
            price = 12,
            menu_item_description = "Uzbek national food"
        )

    def test_create_menu_item(self) -> None:
        item2 = Menu.objects.create(
            title = 'Chef Burger',
            price = 9,
            menu_item_description = "Made by the chef"
        )
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(item2.title, 'Burger')
        self.assertEqual(item2.price,9)
        self.assertEqual(item2.menu_item_description, 'Made by the chef')

    def test_get_menu_item(self) -> None:
        item = Menu.objects.get(id = self.item1.id)
        self.assertEqual(item.title, 'Osh')
        self.assertEqual(item.price, 12)
        self.assertEqual(item.menu_item_description, "Uzbek national food")

    def test_delete_menu_item(self) -> None:
        item = Menu.objects.get(id = self.item1.id)
        item.delete()
        self.assertEqual(Menu.objects.count(), 0)