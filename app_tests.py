from app import app
from unittest import TestCase
from models import User, db, connect_db, Post, Tag, Post_Tag
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


class Tester(TestCase):
        
    def setUp(self):
        db.drop_all()
        db.create_all()

        recs = [User(first_name= 'Yaron', last_name='Ilan', image_url='www.cnn.com'),
                User(first_name='Danny', last_name='Smith', image_url='www.google.com'),
                User(first_name= 'John', last_name='Dow', image_url='www.nbc.com'), 
                Post(title="A title", content="The content", created_at='2022-06-20', user_id=1),
                Tag(name='Funny'),
                Tag(name='Sad'),
                Tag(name='Factual'),
                Tag(name='Geedy')]
        db.session.add_all(recs)
        db.session.commit()

        self.user1= recs[0].id
        self.user2= recs[1].id
        self.user3= recs[2].id
        self.post1= recs[3].id
        
        recs = [Post_Tag(post_id=1, tag_id=1),
                Post_Tag(post_id=1, tag_id=2),
                Post_Tag(post_id=1, tag_id=3),
                Post_Tag(post_id=1, tag_id=4)]
                
                

        db.session.add_all(recs)
        db.session.commit()

       

    def test_a_show_all_users(self):
        with app.test_client() as client:
            resp = client.get("/") 
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yaron", html)
            self.assertIn("Danny", html)
            self.assertIn("John", html)

    def test_b_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user1}/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yaron", html)
            self.assertIn("Edit", html)
            self.assertIn("Delete", html)

    def test_c_insert(self):
        with app.test_client() as client:
            usr = {"f_name": "Steve", "l_name": "Jobs", "image_url": "www.apple.com"}
            resp = client.post("/users/new/", data=usr, follow_redirects=True)
            # db.session.commit()
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Steve Jobs", html)

    def test_d_delete_user(self):
        with app.test_client() as client:  
            resp=client.post(f'/users/{self.user1}/delete/', data={}, follow_redirects=True)
            html=resp.get_data(as_text=True)
            self.assertNotIn('Yaron Ilan', html)
            self.assertIn('Danny Smith', html)

    def test_e_update_user(self):
        with app.test_client() as client:  
            usr = User.query.get(self.user1)  
            req_user = {'f_name': 'Yaronile',
                        'l_name': 'Ilanchook',
                        'image_url': usr.image_url}
            resp = client.post(f'/users/{self.user1}/save_edits/', data=req_user, follow_redirects=True)
            resp = client.get("/") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Yaronile", html)

    def test_f_show_new_post_form(self):
        with app.test_client() as client:  
            resp=client.get('/users/2/posts/new/')
            html=resp.get_data(as_text=True)
            self.assertIn("Danny", html)
        
    def test_g_add_new_post(self):
        with app.test_client() as client:            
            new_post={'title': 'A test title',
                        'content': 'The test post content'}
            resp=client.post('/users/2/posts/new/', data=new_post) 
            html=resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Danny Smith", html)
            self.assertIn('A test title', html)
            
    def test_h_show_post_details(self):
        with app.test_client() as client:
            resp=client.get(f'/posts/{self.post1}/')
            html=resp.get_data(as_text=True)
            self.assertIn('A title', html)
            self.assertIn('The content', html)
            self.assertIn('Funny', html)
            self.assertIn('Sad', html)
            self.assertIn('Factual', html)
            self.assertIn('Geedy', html)
            

    def test_i_show_edit_post_form(self):
        with app.test_client() as client:  
            resp=client.get(f'/posts/{self.post1}/edit/')
            html=resp.get_data(as_text=True)
            self.assertIn('Edit post', html)
            self.assertIn('A title', html)
            self.assertIn('Funny', html)
            self.assertIn('Sad', html)
            self.assertIn('Factual', html)
            self.assertIn('Geedy', html)
    
    def test_j_delete_post(self):
        with app.test_client() as client:  
            resp=client.post(f'/posts/{self.post1}/delete/', data={})
            html=resp.get_data(as_text=True)
            self.assertNotIn('A title', html)

    def test_k_show_tag_list(self):
        with app.test_client() as client:  
            resp=client.get('/tags/')
            html=resp.get_data(as_text=True)
            self.assertIn('Funny', html)
            self.assertIn('Sad', html)
            self.assertIn('Factual', html)
            self.assertIn('Geedy', html)

    def test_l_show_tag(self):
         with app.test_client() as client:  
            resp=client.get('/tags/1/')
            html=resp.get_data(as_text=True)
            self.assertIn('Funny', html)
            self.assertNotIn('Sad', html)
            self.assertNotIn('Factual', html)
            self.assertNotIn('Geedy', html)

    def test_m_show_add_tag_form(self):
        with app.test_client() as client:  
            resp=client.get('/tags/new/')
            html=resp.get_data(as_text=True)
            self.assertIn('Add a tag', html)
            self.assertIn('Name', html)
            self.assertIn('this.select()', html)

    def test_n_add_new_tag(self):        
        with app.test_client() as client:  
            new_tag={'name':'A test tag name'}
            resp=client.post('/tags/new/', data=new_tag)
            html=resp.get_data(as_text=True)
            self.assertIn('A test tag name', html)
            self.assertIn('Tags', html)

    def test_o_show_edit_tag_form(self):
        with app.test_client() as client:  
            resp=client.get('/tags/1/edit/')
            html=resp.get_data(as_text=True)
            self.assertIn('Edit a tag', html)
            self.assertIn('Funny', html)

    def test_p_save_tag_updates(self):
        with app.test_client() as client:  
            a_tag={'name':'An updated tag name'}
            resp=client.post('/tags/1/edit/', data=a_tag)
            html=resp.get_data(as_text=True)
            self.assertIn('An updated tag name', html)
            self.assertIn('Tags', html)

    def test_q_delete_tag(self):
        with app.test_client() as client: 
            resp=client.post('/tags/1/delete/', follow_redirects=True)
            html=resp.get_data(as_text=True)
            self.assertNotIn('An updated tag name', html)
            self.assertIn('Tags', html)
            self.assertIn('Sad', html)
            self.assertIn('Factual', html)
            self.assertIn('Geedy', html)


 








    