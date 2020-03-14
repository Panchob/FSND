#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import db, Artist, Venue, Show
from sqlalchemy import func, cast

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)


migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  locations = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  data = []

  for location in locations:
    result = {
      "city": location.city,
      "state": location.state,
      "venues": []
    }

    venues=Venue.query.filter_by(city=location.city, state=location.state)
    for venue in venues:
      result['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id and Show.start_time > datetime.now()).count()
      })
    data.append(result)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  response={}
  search_term= "%" + request.form.get('search_term') + "%"
  venue_search = Venue.query.filter(Venue.name.ilike(search_term)).all()
  data = []

  for venue in venue_search:
    venue_info = {}
    venue_info['id'] = venue.id
    venue_info['name'] = venue.name
    data.append(venue_info)
  
  response['count'] = len(data)
  response['data'] = data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.get(venue_id)
  shows = db.session.query(Artist, Show.start_time).join(Show).filter(Show.venue_id == venue_id)
  past_shows_count = 0
  upcoming_shows_count = 0
  upcoming_shows = []
  past_shows = []

  for artist, start_time in shows:
    show_info = {
      'artist_id': artist.id,
      'artist_name':artist.name,
      'artist_image_link':artist.image_link,
      'start_time': str(start_time)
    }

    if start_time < datetime.now():
      past_shows.append(show_info)
      past_shows_count += 1
    else:
      upcoming_shows.append(show_info)
      upcoming_shows_count += 1
    
  setattr(venue, 'upcoming_shows', upcoming_shows)
  setattr(venue, 'past_shows', past_shows)
  setattr(venue, 'upcoming_shows_count', upcoming_shows_count)
  setattr(venue, 'past_shows_count', past_shows_count)

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    try:
      venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data,
      image_link=form.image_link.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data
      )

      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      print(sys.exc_info())
      print(e)
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('A form error occured. Venue ' + request.form['name'] + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted')
  except:
   db.session.rollback()
  finally:
   db.session.close()
      
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  response={}
  search_term= "%" + request.form.get('search_term') + "%"
  artist_search = Artist.query.filter(Artist.name.ilike(search_term)).all()
  data = []

  for artist in artist_search:
    artist_info = {}
    artist_info['id'] = artist.id
    artist_info['name'] = artist.name
    data.append(artist_info)
  
  response['count'] = len(data)
  response['data'] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get(artist_id)
  shows = db.session.query(Venue, Show.start_time).join(Show).filter(Show.artist_id == artist_id)
  past_shows_count = 0
  upcoming_shows_count = 0
  upcoming_shows = []
  past_shows = []

  for venue, start_time in shows:
    show_info = {
      'venue_id': venue.id,
      'venue_name':venue.name,
      'venue_image_link':venue.image_link,
      'start_time': str(start_time)
    }

    if start_time < datetime.now():
      past_shows.append(show_info)
      past_shows_count += 1
    else:
      upcoming_shows.append(show_info)
      upcoming_shows_count += 1
    
  setattr(artist, 'upcoming_shows', upcoming_shows)
  setattr(artist, 'past_shows', past_shows)
  setattr(artist, 'upcoming_shows_count', upcoming_shows_count)
  setattr(artist, 'past_shows_count', past_shows_count)

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form=ArtistForm()
  artist = Artist.query.get(artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  form=ArtistForm()
  artist = Artist.query.get(artist_id)

  try:
    artist.name = form.name.data
    artist.city = form.city.data,
    artist.state = form.state.data,
    artist.phone = form.phone.data,
    artist.website = form.website.data,
    artist.facebook_link = form.facebook_link.data,
    artist.seeking_venue = form.seeking_venue.data,
    artist.seeking_description = form.seeking_description.data,
    artist.image_link = form.image_link.data

    db.session.add(artist)
    db.commit()
    flash('Artist updated')
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form=VenueForm()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form=VenueForm()
  venue = Venue.query.get(venue_id)

  try:
    venue.name = form.name.data
    venue.city = form.city.data,
    venue.state = form.state.data,
    venue.address = form.address.data,
    venue.phone = form.phone.data,
    venue.website = form.website.data,
    venue.facebook_link = form.facebook_link.data,
    venue.seeking_talent = form.seeking_venue.data,
    venue.seeking_description = form.seeking_description.data,
    venue.image_link = form.image_link.data

    db.session.add(venue)
    db.commit()
    flash('Venue updated')
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  data = {}
  if form.validate():
    try:
      artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
      image_link=form.image_link.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception:
      db.session.rollback
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('A form error occured. This show could not be listed.')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=db.session.query(Show.venue_id.label('venue_id'),
                        Venue.name.label('venue_name'), Show.artist_id, 
                        Show.artist_id.label('artist_id'),
                        Artist.name.label('artist_name'), 
                        Artist.image_link.label('artist_image_link'), 
                        cast(Show.start_time, db.String).label('start_time')).join(Venue).join(Artist).all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  data = {}
  if form.validate():
    try:
      show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )

      db.session.add(show)
      db.session.commit()
      flash('A new show was successfully listed!')
    except Exception:
      db.session.rollback
      print(sys.exc_info())
      flash('An error occurred. This show could not be listed.')
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('A form error occured. This show could not be listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
