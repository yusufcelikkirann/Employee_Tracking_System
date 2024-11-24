Employee Tracking System - Setup & Usage Guide
Prerequisites
Docker Desktop installed and running in the background.
Docker Compose installed on your machine.
Terminal or Command Prompt access.
Step-by-Step Instructions
1. Run Docker Compose
In your terminal, navigate to the project directory and run the following command to build and start the services:

bash
Kodu kopyala
docker-compose up --build
This will start all the necessary containers, including the application service, database, and any other dependencies defined in the docker-compose.yml file.

2. Access the Docker Container
Once the Docker containers are up and running, access the terminal of the running web container (employee_tracking_system-web-1) by using the following command:

bash
Kodu kopyala
docker exec -it employee_tracking_system-web-1 /bin/bash
This will open a shell session inside the web container.

3. Run Migrations
Inside the container, navigate to the project directory (if necessary) and apply the database migrations:

bash
Kodu kopyala
python manage.py migrate
This will ensure the database is up-to-date with the latest schema changes.

4. Create a Superuser
To create a superuser for the Django Admin panel, run the following command:

bash
Kodu kopyala
python manage.py createsuperuser
You will be prompted to enter a username, email, and password for the superuser account.

5. Login to the Admin Panel
After successfully creating the superuser, you can access the Django Admin panel by visiting the following URL in your browser:

bash
Kodu kopyala
http://localhost:8000/admin/
Log in using the superuser credentials you just created.

6. Change User Permissions
Once logged in to the Django Admin panel:

Navigate to the Users section.
Find the user you want to modify.
Edit the user and change their role/permissions to Admin (by checking the “Staff status” and “Superuser status” options).
7. Normal Login
Once the user has been granted admin permissions, they will have full access to the admin panel and other features of the application. You can also perform a normal login by navigating to the login page.

8. Access Swagger UI
To access the Swagger UI for API documentation, go to the following URL:

bash
Kodu kopyala
http://localhost:8000/swagger/
This will display the API endpoints and their respective details.

Troubleshooting
Docker Not Running: Make sure Docker Desktop is running in the background.
Permission Issues: Ensure that your user has the necessary permissions to run Docker and Docker Compose commands.
Conclusion
This guide walks you through the process of setting up, running migrations, creating a superuser, and accessing the admin panel and Swagger UI. By following these steps, you should be able to use the Employee Tracking System with full administrative privileges.

***************************************************************************************************************************************************************************************************************************************************

Employee Tracking System - Kurulum ve Kullanım Rehberi
Önkoşullar
Docker Desktop bilgisayarınızda yüklü ve arka planda çalışıyor olmalı.
Docker Compose bilgisayarınızda yüklü olmalı.
Terminal veya Komut Satırı erişiminiz olmalı.
Adım Adım Talimatlar
1. Docker Compose Çalıştırma
Terminalinize projenizin bulunduğu dizine gidin ve aşağıdaki komutu çalıştırarak servisleri başlatın:

bash
Kodu kopyala
docker-compose up --build
Bu komut, gerekli tüm konteynerleri (uygulama servisi, veritabanı ve diğer bağımlılıklar) oluşturup çalıştıracaktır.

2. Docker Konteynerine Erişim
Docker konteynerleri çalışmaya başladıktan sonra, aşağıdaki komut ile employee_tracking_system-web-1 konteynerinin terminaline erişebilirsiniz:

bash
Kodu kopyala
docker exec -it employee_tracking_system-web-1 /bin/bash
Bu komut, web konteyneri içinde bir kabuk oturumu açacaktır.

3. Veritabanı Migrasyonlarını Çalıştırma
Konteyner içinde, proje dizinine gitmeniz gerekebilir, ardından veritabanı migrasyonlarını çalıştırmak için aşağıdaki komutu kullanın:

bash
Kodu kopyala
python manage.py migrate
Bu komut, veritabanınızı en son şema değişiklikleriyle güncelleyecektir.

4. Superuser (Yönetici Kullanıcı) Oluşturma
Django admin paneline giriş yapabilmek için bir süper kullanıcı (superuser) oluşturmanız gerekir. Aşağıdaki komutu çalıştırarak süper kullanıcı oluşturabilirsiniz:

bash
Kodu kopyala
python manage.py createsuperuser
Komut, kullanıcı adı, e-posta ve şifre girmenizi isteyecektir. Bu bilgileri girerek süper kullanıcıyı oluşturun.

5. Admin Paneline Giriş Yapma
Süper kullanıcıyı başarıyla oluşturduktan sonra, aşağıdaki URL'yi kullanarak Django admin paneline giriş yapabilirsiniz:

bash
Kodu kopyala
http://localhost:8000/admin/
Burada, daha önce oluşturduğunuz süper kullanıcı bilgilerini kullanarak giriş yapın.

6. Kullanıcı Yetkilerini Değiştirme
Admin paneline giriş yaptıktan sonra:

Kullanıcılar bölümüne gidin.
Yetkilerini değiştirmek istediğiniz kullanıcıyı bulun.
Kullanıcının detaylarını düzenleyin ve “Staff status” ve “Superuser status” seçeneklerini işaretleyerek kullanıcının admin yetkilerini aktif edin.
7. Normal Giriş Yapma
Admin yetkilerini verdiğiniz kullanıcı, artık admin paneline ve diğer uygulama özelliklerine tam erişime sahip olacaktır. Ayrıca normal bir giriş işlemi için giriş sayfasını ziyaret edebilirsiniz.

8. Swagger UI'ye Erişim
API dokümantasyonu için Swagger UI'yi görmek amacıyla aşağıdaki URL'yi ziyaret edebilirsiniz:

bash
Kodu kopyala
http://localhost:8000/swagger/
Bu sayfa, API uç noktalarını ve ilgili detayları gösterir.

Sorun Giderme
Docker Çalışmıyor: Docker Desktop'un arka planda çalıştığından emin olun.
İzin Sorunları: Docker ve Docker Compose komutlarını çalıştırmak için gerekli izinlere sahip olduğunuzdan emin olun.
Sonuç
Bu rehber, projenin kurulumundan, veritabanı migrasyonlarının yapılmasına, süper kullanıcı oluşturulmasına ve admin paneline erişime kadar tüm adımları kapsar. Adımları takip ederek Employee Tracking System'i tam yönetici ayrıcalıklarıyla kullanabilirsiniz.
