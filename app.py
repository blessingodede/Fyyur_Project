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
from sqlalchemy import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)
    
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'
db.create_all()

class Artist(db.Model):
    __tablename__ = 'artist'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    

db.create_all()      
    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tableName__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Show {self.id} {self.artist_id} {self.venue_id} {self.start_time}>'

db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    find_venues = set()
    find_areas = Venue.query.all()
   

    for find_area in find_areas:
        find_venues.add((find_area.city, find_area.state))
    
    data = []
    
    for find_venue in find_venues:
        data.append({
            "city": find_venue[0],
            "state": find_venue[1],
            "venues": []
    })
  
    for find_area in find_areas:
        time = datetime.now()
        shows = [show for show in find_area.shows if show.start_time > time]
    for range_data in range(0, len(data)):
        if  find_area.city == data[range_data]['city'] and find_area.state == data[range_data]['state']:
            data[range_data]['venues'].append({
            "id": find_area.id,
            "name": find_area.name,
            "upcoming_shows": len(shows)
        })
    return render_template('pages/venues.html', areas=data);
            

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    data = []
    response = {}
    
    search_term = request.form.get('search_term')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    
    for venue in venues:
        new_venue = {}
        new_venue['id'] = venue.id
        new_venue['name'] = venue.name
        data.append(new_venue)
    
    response['count'] = len(data)
    response['data'] = data
    
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    venue_query = Venue.query.get(venue_id)
    
    if venue_query is None:
        return render_template('errors/404.html')
    
    past = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(
        Show.start_time<datetime.now()).all()


    upcoming = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(
        Show.start_time>datetime.now()).all()
    
    past_shows = []
    upcoming_shows = []

    

    for replace_upcoming in upcoming:
        upcoming_shows.append({
            'artist_id': replace_upcoming.artist.id,
            'artist_name': replace_upcoming.artist.name,
            'image_link': replace_upcoming.artist.image_link,
            'start_time': str(replace_upcoming.start_time)
        })
        
    for replace_past in past:
        past_shows.append({
            'artist_id': replace_past.artist.id,
            'artist_name': replace_past.artist.name,
            'image_link': replace_past.artist.image_link,
            'start_time': str(replace_past.start_time) 
        })

    
    if venue_query is None:
        return render_template('errors/404.html')

    data = {
        "id": venue_query.id,
        "name": venue_query.name,
        "genres": [venue_query.genres],
        "address": venue_query.address,
        "city": venue_query.city,
        "state": venue_query.state,
        "phone": venue_query.phone,
        "website_link": venue_query.website_link,
        "facebook_link": venue_query.facebook_link,
        "seeking_talent": venue_query.seeking_talent,
        "seeking_description": venue_query.seeking_description,
        "image_link": venue_query.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
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
    skeeK_talent = json.loads(request.form['seeking_talent'].lower())
    try:
        insert_venue = Venue(
            name = request.form['name'],
            city = request.form['city'],
            state = request.form['state'],
            address = request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website_link=request.form['website_link'],
            seeking_talent=skeeK_talent,
            seeking_description=request.form['seeking_description']
        
        )
        db.session.add(insert_venue)
        db.session.commit()
        
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
    except:
       
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()
        
    finally:
        db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.filter(Venue.id==venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    data = []
    response ={}
    
    search_term = request.form.get('search_term')
    
    artist_query = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    
    for search_artist in artist_query:
        new_artist = {}
        new_artist['id'] = search_artist.id
        new_artist['name'] = search_artist.name
        data.append(new_artist)
    
    response['count'] = len(data)
    response['data'] = data
    
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    
    artist_query = Artist.query.get(artist_id)
    
    if artist_query is None:
        flash("This artist does not available.")
        return render_template('errors/404.html')
    upcoming = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()
     
    past = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).all()
    
    upcoming_shows = []
    past_shows = []
    
    
    for replace_upcoming in upcoming:
        upcoming_shows.append(
            {
                "venue_id": replace_upcoming.venue_id,
                "venue_name": replace_upcoming.venue.name,
                "venue_image_link": replace_upcoming.venue.image_link,
                "start_time": str(replace_incoming.start_time) 
            }
        )
 
        
    for replace_past in past:
        past_shows.append(
            {
                "venue_id":  replace_past.venue_id,
                "venue_name":  replace_past.venue.name,
                "venue_image_link":  replace_past.venue.image_link,
                "start_time":  str(replace_past.start_time) 
            }
        )

    data = {
        "id": artist_query.id,
        "name": artist_query.name,
        "city": artist_query.city,
        "state": artist_query.state,
        "genres": (artist_query.genres).split(","),
        "phone": artist_query.phone,
        "website": artist_query.website_link,
        "facebook_link": artist_query.facebook_link,
        "seeking_venue": artist_query.seeking_venue,
        "seeking_description": artist_query.seeking_description,
        "image_link": artist_query.image_link,
        "upcoming_shows_count": len(upcoming_shows),
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "past_shows": past_shows,
    }
    
    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter(Artist.id==artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>
    
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description


    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
   
    artist_record = Artist.query.get(artist_id)
    #form = ArtistForm(request.form)
    seek_venue = True if 'seeking_venue' in request.form else False
    try:
        artist_record.name = request.form['name']
        artist_record.city = request.form['city']
        artist_record.state = request.form['state']
        artist_record.phone = request.form['phone'],
        artist_record.genres = request.form.getlist("genres")
        artist_record.facebook_link = request.form['facebook_link']
        artist_record.website_link = request.form['website_link']
        artist_record.seeking_venue = seek_venue
        artist_record.seeking_description = request.form['seeking_description']
    
        
        db.session.commit()
        
        flash("Artist: " + request.form['name'] + " has been successfully updated")
        
    except:
        flash("An error occured. Artist " + request.form['name'] + " could not be upcated")
        db.session.rollback()
  # artist record with ID <artist_id> using the new attributes
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))
 

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    
  # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
 
    venue_record = Venue.query.get(venue_id)
    seek_talent = True if 'seeking_talent' in request.form else False
    
    try:
    
        venue_record.name = request.form['name']
        venue_record.city = request.form['city']
        venue_record.state = request.form['state']
        venue_record.address = request.form['address']
        venue_record.phone = request.form['phone']
        venue_record.genres = request.form.getlist("genres")
        venue_record.facebook_link = request.form['facebook_link']
        venue_record.image_link = request.form['image_link']
        venue_record.website_link = request.form['website_link']
        venue_record.seeking_talent = seek_talent
        venue_record.seeking_description = request.form['seeking_description']
        
        db.session.commit()
        
        flash("Venue: " + request.form['name'] + " has been successfully updated!")
    
    except:
        flash("An error occured Venue " + request.form['name'] + " could not be updated!")
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
    skeeK_venue = json.loads(request.form['seeking_venue'].lower())
    try:
        insert_artist = Artist(
            name = request.form['name'],
            city = request.form['city'],
            state = request.form['state'],
            phone = request.form['phone'],
            genres = request.form.getlist('genres'),
            image_link = request.form['image_link'],
            facebook_link = request.form['facebook_link'],
            seeking_venue = skeeK_venue,
            website_link = request.form['website_link'],
            seeking_description = request.form['seeking_description']
        )
        db.session.add(insert_artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed!')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')
    


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    query_show = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()
    
    data = []
    
    for venue_result in query_show:
        data.append({
            "venue_id":   venue_result.venue_id,
            "venue_name":   venue_result.venue.name,
            "artist_id":  venue_result.artist_id,
            "artist_name":  venue_result.artist.name,
            "image_link":  venue_result.artist.image_link,
            "start_time": str( venue_result.start_time)
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
    try:
        insert_show = Show(
            artist_id = request.form['artist_id'],
            venue_id = request.form['venue_id'],
            start_time = request.form['start_time']
        )
        
        db.session.add(insert_show)
        db.session.commit()
        
        flash('Show was successfully listed!')
        
    except:
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
 
    finally:
        db.session.close()
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
