# Website Amber

**[See in action](https://www.amberdevuyst.be/)**

## Deployment

  Hosted using [Heroku](https://www.heroku.com/)
  
  Domain name on [GoDaddy](https://www.godaddy.com/)
  
  DNS using [Cloudflare](https://www.cloudflare.com/)
  
  
## Technology

Built mainly on the [Django](https://www.djangoproject.com/) framework. Also using a basic Heroku dyno paired with the [Heroku postgres add-on](https://elements.heroku.com/addons/heroku-postgresql)

See [requirements.txt](requirements.txt) for all the technologies used.

## Usage

By surfing to the [admin page](https://amberdevuyst.be/admin/), the admin can add timeslots associated with dates.
The admin can also customize dates, timeslots & patients which will then be rendered and displayed on the [appointment page](https://amberdevuyst.be/appointment).

Normal users can make appointments, after which they will receive a custom email. The admin can also see and edit that appointment.
