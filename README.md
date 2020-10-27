![Image of Yaktocat](economy/static/game_economy.PNG)

<h1> Installation </h1>
<ul>

<li>1. From the development folder create an .env file:<br/>
		<code> cp .env_template .env </code> <br/>
		    Populate the .env file with your sensitive variables. This file is included in the .gitignore and your variables will not be accessible to anyone else.
	  
</li>
<li>2. Build and start the project:<br/>
		<code>docker-compose up -d —build</code>
</li>
<li>3. If you want to check the status of the running containers, run:<br/>
		<code>docker ps</code> <br/>
		Celery beat container is going to keep restarting until you set up the database as it is shown in the next bulletpoint.
</li>
<li>4. Here are the instructions for the initial project setup as well as the database setup.<br/>
  Log in into uwsgi container:<br/>
        <code>docker-compose exec uwsgi bash</code><br/>
        In uwsgi container:<br/>
            <code>python manage.py collectstatic</code><br/>
            <code>python manage.py migrate</code><br/>
            <code>python manage.py shell</code><br/>
            In the python shell (you can substitute 'root' to any other name/password you like):<br/>
                              <code> from users.models import Profile; from django.contrib.auth.models import User </code><br/>
                              <code> Profile.objects.create(user=User.objects.create_superuser(username="root", password="root"), subdomain="root")</code>
</li></ul>
