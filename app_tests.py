from app import app
from unittest import TestCase
from models import User, db, connect_db




app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

class Tester(TestCase):

    

    @classmethod
    def setUpClass(self):
        connect_db(app)
        db.drop_all()
        db.create_all()
        
        
    def setUp(self):
        recs = [User(first_name= 'Yaron', last_name='Ilan', image_url='www.cnn.com'),
            User(first_name='Danny', last_name='Smith', image_url='www.google.com'),
            User(first_name= 'John', last_name='Dow', image_url='www.nbc.com')]

        db.session.add_all(recs)
        db.session.commit()


    def test_insert(self):
        with app.test_client() as client:
            usr = {"f_name": "Steve", "l_name": "Jobs", "image_url": "www.apple.com"}
            resp = client.post("/users/new/", data=usr, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<a href=""/users/4/"">Steve Jobs</a>", html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get("/users/2/") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Danny", html)

    def test_show_all_users(self):
        with app.test_client() as client:
            usr = {"f_name": "Yaron", "l_name": "Ilan", "image_url": "www.cnn.com"}
            resp = client.post("/users/new/", data=usr, follow_redirects=True)
            resp = client.get("/") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yaron", html)
            self.assertIn("Danny", html)
            self.assertIn("Steve", html)
            self.assertIn("John", html)

    def test_update_user(self):
        with app.test_client() as client:  
            usr = User.query.get(1)  
            req_user = {'f_name': 'Yaronile',
                        'l_name': 'Ilanchook',
                        'image_url': usr.image_url}
            resp = client.post('/users/1/save_edits/', data=req_user, follow_redirects=True)
            resp = client.get("/") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yaronile", html)

    