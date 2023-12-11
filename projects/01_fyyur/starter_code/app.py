#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime, date, timedelta

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='shows', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  start_time = db.Column(db.DateTime(timezone=True))
  artists = db.relationship('Artist', backref='artists', lazy=True)
  venues = db.relationship('Venue', backref='venues', lazy=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):

  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#---------
# Convert checkbox value to True/False
# @aram value
#---------
def convert_checkbox(value):
  
  if value == 'y':
    return True
  else:
    return False

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  query_venues = Show.query.join(Venue).with_entities(Venue.city, Venue.state, Venue.id, Venue.name).group_by(Venue.id).order_by(Venue.state)

  areas = []
  city_state = ''

  venues = {}
  
  for city, state, id, name in query_venues:

    city_state = (city, state)

    if city_state not in venues:
      venues[city_state] = []

    venues[city_state].append({
      'id': id,
      'name': name,
    })

  for city, state in list(venues):

    areas.append({
      'city': city,
      'state': state,
      'venues': venues[(city, state)]
    })
  
  # finally:
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term', '')

  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  venues = venues.order_by(Venue.name)

  response = {
    'count': venues.count(),
    'data': []
  }

  for venue in venues:
    response['data'].append({
      'id': venue.id,
      'name': venue.name
    })

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = []
  genres = []
  genresList = []
  past_show_list = []
  upcoming_show_list = []

  venue = Venue.query.filter(Venue.id == venue_id).one_or_none()

  present_day = date.today()

  if venue is None:
    abort(404)

  if venue.genres != None:
    genres = venue.genres
    genres = genres.replace('{', '')
    genres = genres.replace('}', '')
    genresList = genres.split(',')

  if venue.shows != None:
    for show in venue.shows:
      show_id = show.artists.id

      start_time = show.start_time.date()

      show_artist_name = show.artists.name
      show_artist_image = show.artists.image_link

      if present_day < start_time:
        upcoming_show_list.append({
          'artist_id': show_id,
          'start_time': start_time,
          'artist_name': show_artist_name,
          'artist_image_link': show_artist_image
        })
      else:
        past_show_list.append({
          'artist_id': show_id,
          'start_time': start_time,
          'artist_name': show_artist_name,
          'artist_image_link': show_artist_image
        })
  
  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': genresList,
    'city': venue.city,
    'state': venue.state,
    'address': venue.address,
    'phone': venue.phone,
    'image_link': venue.image_link,
    'website': venue.website_link,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'upcoming_shows_count': len(upcoming_show_list),
    'upcoming_shows': upcoming_show_list,
    'past_shows_count': len(past_show_list),
    'past_shows': past_show_list
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  data = {}
  try:
    data = request.form
    name = data['name']
    city = data['city']
    state = data['state']
    address = data['address']
    phone = data['phone']
    genres = request.form.getlist('genres')
    facebook_link = data['facebook_link']
    image_link = data['image_link']
    website_link = data['website_link']
    seeking_talent = data['seeking_talent']
    seeking_description = data['seeking_description']

    venue = Venue(
      name = name,
      city = city,
      state = state,
      address = address,
      phone = phone,
      genres = genres,
      facebook_link = facebook_link,
      image_link = image_link,
      website_link = website_link,
      seeking_talent = convert_checkbox(seeking_talent),
      seeking_description = seeking_description
    )

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + name + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
    flash(data)
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html')
  else: abort(500)
  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.all()
  data = []

  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')

  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  artists = artists.order_by(Artist.name)

  response = {
    'count': artists.count(),
    'data': []
  }

  for artist in artists:
    response['data'].append({
      'id': artist.id,
      'name': artist.name
    })

  # return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  data = []
  genres = []
  genresList = []
  venuesList = []
  past_shows_list = []
  upcoming_shows_list = []

  artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
  shows = Show.query.filter(Show.artist_id == artist_id)

  present_day = date.today()

  if artist is None:
    abort(404)

  if artist.genres != None:
    genres = artist.genres
    genres = genres.replace('{', '')
    genres = genres.replace('}', '')
    genresList = genres.split(',')

  if shows != None:

    for show in shows:

      venue = Venue.query.get(show.venue_id)

      show_id = show.id
      start_time = show.start_time.date()
      venue_artist_name = venue.name
      venue_artist_image = venue.image_link

      if present_day < start_time:
        upcoming_shows_list.append({
          'venue_id': show_id,
          'start_time': start_time,
          'venue_name': venue_artist_name,
          'venue_image_link': venue_artist_image
        })
      else:
        past_shows_list.append({
          'venue_id': show_id,
          'start_time': start_time,
          'venue_name': venue_artist_name,
          'venue_image_link': venue_artist_image
        })

  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': genresList,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'image_link': artist.image_link,
    'website': artist.website_link,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    "upcoming_shows_count": len(upcoming_shows_list),
    "upcoming_shows": upcoming_shows_list,
    "past_shows_count": len(past_shows_list),
    'past_shows': past_shows_list,
  }


  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  error = False
  data = {}
  artist = {}
  genres = []
  seeking_venue = 'seeking_venue'

  try:

    artist = Artist.query.get(artist_id)
    data = request.form

    genres = data.getlist('genres')

    if seeking_venue in data :
      artist.seeking_venue = convert_checkbox(data['seeking_venue'])

    artist.name = data['name']
    artist.genres = genres
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.image_link = data['image_link']
    artist.website_link = data['website_link']
    artist.facebook_link = data['facebook_link']
    artist.seeking_description = data['seeking_description']

    db.session.commit()

    flash(f'Great success! That {artist.name} as edited!')
    flash(data)
    # flash(artist)
  except:
    flash('An error occured. The following data was trying to send')
    flash(data['name'])
    flash(artist.name)
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  error = False
  data = {}
  venue = {}
  seeking_talent = 'seeking_talent'

  try:

    venue = Venue.query.get(venue_id)
    data = request.form

    if seeking_talent in data :
      venue.seeking_talent = convert_checkbox(data['seeking_talent'])

    venue.name = data['name']
    venue.genres = data['genres']
    venue.city = data['city']
    venue.state = data['state']
    venue.phone = data['phone']
    venue.image_link = data['image_link']
    venue.website_link = data['website_link']
    venue.facebook_link = data['facebook_link']
    venue.seeking_description = data['seeking_description']

    db.session.commit()

    flash(f'Great success! That {venue.name} as edited!')
    flash(data)
    # flash(artist)
  except:
    flash('An error occured. The following data was trying to send')
    flash(data['name'])
    flash(venue.name)
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
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  data = {}

  try:
    data = request.form
    name = data['name']
    city = data['city']
    state = data['state']
    phone = data['phone']

    genres = request.form.getlist('genres')

    image_link = data['image_link']
    facebook_link = data['facebook_link']

    seeking_venue = convert_checkbox(data['seeking_venue'])

    seeking_description = data['seeking_description']

    artist = Artist(
      name = name,
      city = city,
      state = state,
      phone = phone,
      genres = genres,
      image_link = image_link,
      facebook_link = facebook_link,
      seeking_venue = seeking_venue,
      seeking_description = seeking_description,

    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html')
  else: abort(500)


  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = Show.query.all()

  data = []

  for show in shows:

    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)

    data.append({
      'venue_id': venue.id,
      'venue_name': venue.name,
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': show.start_time
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  data = {}
  error = False

  try:
    data = request.form
    artist_id = data['artist_id']
    venue_id = data['venue_id']
    start_time = data['start_time']

    show = Show(
      artist_id = artist_id,
      venue_id = venue_id,
      start_time = start_time
    )

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Show ' + data['name'] + ' could not be listed.')
    flash(data)
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html')
  else:
    abort(500)
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

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
