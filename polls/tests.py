#Base practica silenium
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
#Afergim import codi anunciat eac2
from django.contrib.auth.models import User
 
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
       # creem superusuari codi copiat anunciat eac2
        user = User.objects.create_user("isard", "isard@isarddvi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
        # cliquem link "Users"
        self.selenium.find_element(By.LINK_TEXT, "Users").click()
	# cliquem "Add user"
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()
        # introduim el nom del nostre nou usuari
        self.selenium.find_element(By.NAME, "username").send_keys("staff")

        # introduim el password 1
        self.selenium.find_element(By.NAME, "password1").send_keys("pirineus1234")

        # introduim el password 2
        self.selenium.find_element(By.NAME, "password2").send_keys("pirineus1234")
        # Guardem formulari
        #self.selenium.find_element(By.NAME, "_save").click()
        #Continuem editant
        self.selenium.find_element(By.NAME, "_continue").click()
        # esperem
        self.selenium.implicitly_wait(2)
        # cliquem staff status
        self.selenium.find_element(By.NAME, "is_staff").click()
        # guardar canvi
        self.selenium.find_element(By.NAME, "_save").click()
        #cliquem  logout
        self.selenium.find_element(By.XPATH, "//button[text()='Log out']").click()
        #cliquem  login again
        self.selenium.find_element(By.LINK_TEXT, "Log in again").click()
        #fem el login amb l'usuari staff
        # login staff
        self.selenium.find_element(By.NAME, "username").send_keys("staff")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus1234")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()
        # anar a la pagina change password 
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/password_change/'))
        #cliquem canvi de password i fegim old password mes dos vegades el nou
        self.selenium.find_element(By.NAME, "old_password").send_keys("pirineus1234")
        self.selenium.find_element(By.NAME, "new_password1").send_keys("pirineus12345")
        self.selenium.find_element(By.NAME, "new_password2").send_keys("pirineus12345")
        # cliquem  canvi de contrasenya
        self.selenium.find_element(By.XPATH, "//input[@value='Change my password']").click() 
