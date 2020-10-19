<h1> Installation </h1>
<ul>

<li>1. From the development folder create an .env file with your variables:<br/>
		<code> cp .env_template .env </code>
</li>
<li>2. Start the project:<br/>
		<code>docker-compose up -d —build</code>
</li>
<li>3. If you want to check the status of the running containers, run:<br/>
		<code>docker ps</code>
</li>
<li>4. Here are the instructions for the initial project setup as well as the database setup. Celery beat container is going to be restarting until you set up the database.<br/>
    Log in into uwsgi container:<br/>
        <code>docker-compose exec uwsgi bash</code><br/>
        In uwsgi container:<br/>
            <code>python manage.py collectstatic</code><br/>
            <code>python manage.py migrate</code><br/>
            <code>python manage.py createsuperuser</code><br/>
            <code>python manage.py shell</code><br/>
            In the python shell:<br/>
                <code>I) from users.models import Profile; from django.contrib.auth.models import User </code><br/>
                <code>II) Profile.objects.create(user=User.objects.create_superuser(username="root", password="root"), subdomain="root")</code>
</li></ul>
