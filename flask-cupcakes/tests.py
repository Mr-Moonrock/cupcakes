from unittest import TestCase
from flask import Flask
from app import app
from models import db, Cupcake


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SmokingPot420@localhost/cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app = Flask(__name__)
client = app.test_client()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        with app.app_context():
            db.create_all()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_cupcakes(self):
        resp = client.get("/api/cupcakes")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data, {"cupcakes": [{"id": self.cupcake.id, **CUPCAKE_DATA}]})

    def test_get_cupcake(self):
        url = f"/api/cupcakes/{self.cupcake.id}"
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data, {"cupcake": {"id": self.cupcake.id, **CUPCAKE_DATA}})

    def test_create_cupcake(self):
        resp = client.post("/api/cupcakes", json=CUPCAKE_DATA_2)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIsInstance(data['cupcake']['id'], int)
        del data['cupcake']['id']
        self.assertEqual(data, {"cupcake": CUPCAKE_DATA_2})
        self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        url = f"/api/cupcakes/{self.cupcake.id}"
        updated_data = {
            "flavor": "TestFlavor2",
            "size": "TestSize2",
            "rating": 7,
            "image": "http://test.com/cupcake2.jpg"
        }
        resp = client.patch(url, json=updated_data)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data, {"cupcake": {'id': self.cupcake.id, **updated_data}})


    def test_delete_cupcake(self):
        url = f"/api/cupcakes/{self.cupcake.id}"
        resp = client.delete(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data, {'message': 'Deleted'})
        self.assertIsNone(Cupcake.query.get(self.cupcake.id))


if __name__ == '__main__':
    import unittest
    unittest.main()